from typing import Literal
import sqlite3
from datetime import datetime, timedelta

import humanize

database = sqlite3.connect("bandwidth.db")

# setup the table
database.cursor().execute(
    "CREATE TABLE IF NOT EXISTS bandwidth (timestamp DATETIME, bytes INTEGER, direction TEXT, category TEXT, detail TEXT)"
)
database.commit()

# logs bandwidth that gets used
def log(
    bytes: int | float,  # how many bytes were used?
    direction: Literal["inbound"] | Literal["outbound"],  # inbound = download, outbound = upload
    category: str | None = None,  # very general description of the type of usage (i.e. "download_attachment")
    detail: str | None = None,  # specific description of the usage (i.e. "HTTP GET http://url.com")
) -> None:
    cursor = database.cursor()

    cursor.execute(
        "INSERT INTO bandwidth (timestamp, bytes, direction, category, detail) VALUES (?, ?, ?, ?, ?)",
        (datetime.now(), bytes, direction, category, detail),
    )

    database.commit()


# returns information about bandwidth after the given date
def summary(after: datetime) -> dict[str, dict[str, int | float]]:
    cursor = database.cursor()

    query = """
          SELECT COALESCE(category, '(uncategorized)') AS category,
                 SUM(CASE direction WHEN 'inbound' THEN bytes END) AS inbound_bytes,
                 SUM(CASE direction WHEN 'outbound' THEN bytes END) AS outbound_bytes,
                 COUNT(*) AS usages
            FROM bandwidth
           WHERE timestamp > ?
        GROUP BY category
        ORDER BY usages DESC
    """

    cursor.execute(query, (after,))

    return {
        category: {"inbound_bytes": inbound_bytes or 0, "outbound_bytes": outbound_bytes or 0, "usages": usages or 0}
        for category, inbound_bytes, outbound_bytes, usages in cursor.fetchall()
    }


# Pretty print bandwidth information after a certain data (humans should manually invoke this function!)
def print_summary(after: datetime) -> None:
    print(f"Bandwidth Summary (Starting {after.strftime('%A %b %d %H:%M')})")
    for category, info in summary(after).items():
        print(f"* Within the {category!r} category")
        print(f"    Recorded Usages: {info['usages']}")
        print(f"       Inbound Data: {humanize.naturalsize(info['inbound_bytes'], binary=True)}")
        print(f"      Outbound Data: {humanize.naturalsize(info['outbound_bytes'], binary=True)}")
        print()


# prints the summary from the last week
def print_weekly_summary():
    print_summary(datetime.now() - timedelta(days=7))


__all__ = ["database", "log", "summary", "print_summary", "print_weekly_summary"]


if __name__ == "__main__":
    print_weekly_summary()

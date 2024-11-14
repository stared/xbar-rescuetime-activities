#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# <xbar.title>RescueTime Activities</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Piotr Migdał</xbar.author>
# <xbar.author.github>stared</xbar.author.github>
# <xbar.desc>List your RescueTime activities in the status bar</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
#
# You need RescueTime account and API key.
# Generate the key at https://www.rescuetime.com/anapi/manage
# Put the API key in ~/Library/RescueTime.com/api.key

import datetime
import os

import json
import urllib
from urllib.request import urlopen

MAPPING_COLOR = {
    2: "#27ae60",  # Dark green - very productive
    1: "#2ecc71",  # Light green - productive
    0: "#3498db",  # Blue - neutral
    -1: "#e67e22",  # Orange - distracting
    -2: "#e74c3c",  # Red - very distracting
}

TOP_ACTIVITIES = 15


def get(url: str, params: dict) -> dict:
    """Simple function to mimic the signature of requests.get.
    The later is not always available."""
    params = urllib.parse.urlencode(params)
    result = urlopen(url + "?" + params).read()
    return json.loads(result)


def format_time(seconds: int) -> str:
    """Format seconds into hours and minutes, e.g. '2h 13min'"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"


def main() -> None:
    """Main function to execute the script logic."""

    API_KEY = os.path.expanduser("~/Library/RescueTime.com/api.key")

    if not os.path.exists(API_KEY):
        print("X")
        print("---")
        print("Missing API Key")
        print(
            "Generate an API key in RescueTime | href=https://www.rescuetime.com/anapi/manage"
        )
        print("and put it in ~/Library/RescueTime.com/api.key")
        exit()

    with open(API_KEY) as fp:
        key = fp.read().strip()

    date = datetime.date.today().strftime("%Y-%m-%d")
    params = {
        "format": "json",
        "key": key,
        "resolution_time": "day",
        "restrict_begin": date,
        "restrict_end": date,
        "restrict_kind": "activity",
    }
    result = get("https://www.rescuetime.com/anapi/data", params)

    pulse = get(
        "https://www.rescuetime.com/anapi/current_productivity_pulse.json",
        params={"key": key},
    )

    # Calculate total productive time
    productive_seconds = sum(
        seconds
        for _, seconds, _, _, _, productivity in result["rows"]
        if productivity > 0
    )

    # Print header with total productive time
    print(f"{format_time(productive_seconds)} | color={pulse['color']}")
    print("---")
    print("Rescue Time | href=https://www.rescuetime.com/dashboard?src=bitbar")

    # Calculate totals for each productivity category
    categories = [
        ("Productive", lambda p: p > 0, 2),
        ("Neutral", lambda p: p == 0, 0),
        ("Distracting", lambda p: p < 0, -2),
    ]

    totals = {}
    for name, condition, p_value in categories:
        total_seconds = sum(
            seconds for _, seconds, _, _, _, p in result["rows"] if condition(p)
        )
        totals[name] = total_seconds
        print(
            f"{name}: {format_time(totals[name])} | "
            f"font='Menlo' size=12 color={MAPPING_COLOR[p_value]}"
        )
    print("---")
    print("Activities")

    # Print top activities
    for _, seconds, _, activity, _, productivity in result["rows"][:TOP_ACTIVITIES]:
        print(
            f"{format_time(seconds):>5} {activity} | font='Menlo' size=12 trim=false color={MAPPING_COLOR[productivity]}"
        )


if __name__ == "__main__":
    main()

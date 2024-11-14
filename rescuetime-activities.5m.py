#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# <xbar.title>RescueTime Activities</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>Piotr Migdał</xbar.author>
# <xbar.author.github>stared</xbar.author.github>
# <xbar.desc>List your RescueTime activities in the status bar</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
#
# You need a RescueTime account and API key.
# Generate the key at https://www.rescuetime.com/anapi/manage
# Put the API key in ~/Library/RescueTime.com/api.key

import os
import json
import datetime
import urllib.parse
import urllib.request

# Constants
API_KEY_PATH = os.path.expanduser("~/Library/RescueTime.com/api.key")

MAPPING_COLOR = {
    2: "#27ae60",  # Dark green - very productive
    1: "#2ecc71",  # Light green - productive
    0: "#3498db",  # Blue - neutral
    -1: "#e67e22",  # Orange - distracting
    -2: "#e74c3c",  # Red - very distracting
}
TOP_ACTIVITIES = 15


def load_api_key(api_key_path: str) -> str:
    """Load the API key from the specified file path."""
    if not os.path.exists(api_key_path):
        print("X")
        print("---")
        print("Missing API Key")
        print(
            "Generate an API key in RescueTime | href=https://www.rescuetime.com/anapi/manage"
        )
        print(f"and put it in {api_key_path}")
        exit()
    with open(api_key_path) as fp:
        return fp.read().strip()


def fetch_data(url: str, params: dict) -> dict:
    """Fetch data from the given URL with parameters."""
    query_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_params}"
    try:
        with urllib.request.urlopen(full_url) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}


def rescuetime_activity_data(params: str) -> list[dict]:
    """See RescueTime API docs for details, https://www.rescuetime.com/rtx/developers.

    Note: User data, particularly activity logs, is synced to the RescueTime servers on a set interval depending on the user's plan subscription. Premium/Organization (paid) plan users' activities are synced every 3 minutes, Lite (free) plan users' activities are synced every 30 minutes. Once the RescueTime app has synced with our servers, the data is immediately available in API results.
    """
    result = fetch_data("https://www.rescuetime.com/anapi/data", params)

    if not result or "rows" not in result:
        print("No data available.")
        return []

    row_headers = result.get("row_headers", [])
    rows = result.get("rows", [])
    return [dict(zip(row_headers, row)) for row in rows]


def format_time(seconds: int) -> str:
    """Format seconds into hours and minutes, e.g., '2h 13m'."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def main() -> None:
    """Main function to execute the script logic."""

    key = load_api_key(API_KEY_PATH)

    date_str = datetime.date.today().strftime("%Y-%m-%d")

    activities = rescuetime_activity_data(
        {
            "format": "json",
            "key": key,
            "resolution_time": "day",
            "restrict_begin": date_str,
            "restrict_end": date_str,
            "restrict_kind": "activity",
        },
    )
    pulse = fetch_data(
        "https://www.rescuetime.com/anapi/current_productivity_pulse.json",
        params={"key": key},
    )

    # Calculate total productive time
    productive_seconds = sum(
        activity["Time Spent (seconds)"]
        for activity in activities
        if activity["Productivity"] > 0
    )

    # Print header with total productive time and productivity pulse color
    print(f"{format_time(productive_seconds)} | color={pulse.get('color', '#000000')}")
    print("---")
    print("RescueTime | href=https://www.rescuetime.com/dashboard?src=bitbar")

    # Calculate totals for each productivity category
    categories = [
        ("Productive", lambda p: p > 0, 2),
        ("Neutral", lambda p: p == 0, 0),
        ("Distracting", lambda p: p < 0, -2),
    ]

    for name, condition, p_value in categories:
        total_seconds = sum(
            activity["Time Spent (seconds)"]
            for activity in activities
            if condition(activity["Productivity"])
        )
        print(
            f"{name}: {format_time(total_seconds)} | "
            f"font='Menlo' size=12 color={MAPPING_COLOR[p_value]}"
        )
    print("---")
    print("Activities")

    # Print top activities
    for activity in activities[:TOP_ACTIVITIES]:
        seconds = activity["Time Spent (seconds)"]
        name = activity["Activity"]
        productivity = activity["Productivity"]
        print(
            f"{format_time(seconds):>5} {name} | font='Menlo' size=12 trim=false color={MAPPING_COLOR[productivity]}"
        )


if __name__ == "__main__":
    main()

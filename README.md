# RescueTime Activities - An xbar Plugin

Monitor your RescueTime activities and distractions directly from the macOS menu bar with this xbar plugin.

![RescueTime Activities](./xbar-rescuetime-activities-screenshot.png)

## Requirements

- macOS 10.15 (Catalina) or later; tested on macOS 14.5 (Sonoma)
- [xbar](https://github.com/matryer/xbar) (formerly BitBar)
- [RescueTime](https://www.rescuetime.com/)

## Installation

1. Install [xbar](https://github.com/matryer/xbar) manually or via [Homebrew](https://brew.sh/): `brew install --cask xbar`
2. Open xbar and navigate to **xbar > Open Plugin Folder**
3. Copy `rescuetime-activities.1h.py` into the plugin folder
4. Refresh all plugins by selecting **xbar > Refresh All Plugins**
5. Generate a [RescueTime API key](https://www.rescuetime.com/anapi/manage)
6. Open the plugin in xbar preferences via **xbar > Open Plugin** and enter your RescueTime API key
7. (optional) Install `Pillow` to view the daily productivity chart; the plugin will provide specific instructions, e.g., `python3 -m pip install Pillow`

## Notes

This plugin is inspired by the [RescueTime plugin](https://xbarapp.com/docs/plugins/Dev/rescuetime.1h.py.html) by [Paul Traylor](https://github.com/kfdm).
I rewrote it to display a detailed list of activities, rather than just a summary of productive and distractive time.

Check out my earlier blog post: [ADHD Tech Stack: Auto Time Tracking](https://p.migdal.pl/blog/2020/05/adhd-tech-stack-auto-time-tracking).

## TODO

- Add a weekly productivity chart

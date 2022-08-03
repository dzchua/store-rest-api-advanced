"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.

If language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`.
"""
import json, os

default_locale = "en-gb"
cached_strings = {}


def refresh():
    print("Refreshing...")
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        # f = open(f"C:/Users/Dizzy/Documents/DA/algo/Rest-API/Adv-m/s/strings/{default_locale}.json")
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()

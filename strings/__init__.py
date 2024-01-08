#
# Copyright (C) 2021-present by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import os
import sys
from typing import List

import yaml

# Initialize dictionaries
languages = {}
commands = {}
languages_present = {}

# Function to get a command by value
def get_command(value: str) -> List:
    return commands["command"][value]

# Function to get a language string
def get_string(lang: str):
    return languages[lang]

# Load command strings
def load_commands(filename: str):
    language_name = filename[:-4]
    commands[language_name] = yaml.safe_load(open(f"./strings/{filename}", encoding="utf8"))

# Load languages and handle fallback to English
def load_languages(filename: str):
    language_name = filename[:-4]
    if language_name == "en":
        return
    languages[language_name] = yaml.safe_load(open(f"./strings/langs/{filename}", encoding="utf8"))
    for item in languages["en"]:
        if item not in languages[language_name]:
            languages[language_name][item] = languages["en"][item]

# Load English language as a fallback
if "en" not in languages:
    languages["en"] = yaml.safe_load(open(r"./strings/langs/en.yml", encoding="utf8"))
    languages_present["en"] = languages["en"]["name"]

# Load command and language files
for filename in os.listdir(r"./strings"):
    if filename.endswith(".yml"):
        load_commands(filename)

for filename in os.listdir(r"./strings/langs/"):
    if filename.endswith(".yml"):
        load_languages(filename)

# Get language names
for language_name in languages:
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except KeyError:
        print("There is some issue with the language file inside the bot. Please report it to the TeamYukki at @YukkiSupport on Telegram")
        sys.exit()

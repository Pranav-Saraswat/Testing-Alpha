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
import logging

def update_directories():
    assets_folder = "assets"
    downloads_folder = "downloads"
    cache_folder = "cache"

    if not os.path.exists(assets_folder):
        logging.warning(f"{assets_folder} Folder not found. Please clone the repository again.")
        sys.exit()

    for file in os.listdir():
        if file.endswith((".jpg", ".jpeg")):
            os.remove(file)

    if not os.path.exists(downloads_folder):
        os.mkdir(downloads_folder)

    if not os.path.exists(cache_folder):
        os.mkdir(cache_folder)

    logging.info("Directories updated.")

if __name__ == "__main__":
    update_directories()

# -*- coding: utf-8 -*-
# Module: check_update.py
"""
openSquat

* https://github.com/atenreiro/opensquat

software licensed under GNU version 3
"""
import requests
from colorama import Fore, Style
from opensquat import __VERSION__
from packaging import version
from datetime import datetime, timedelta
import os

class CheckUpdate:
    """
    This class verifies if there is a newer upgrade available.

    To use:
        CheckUpdate().main()

    Attributes:
        URL: The URL with the latest upgrade version.
        current: The current running version.
        update_cfg: The path to the update configuration file.
    """

    def __init__(self):
        """Initiator."""
        self.URL = "https://feeds.opensquat.com/latest_version.txt"
        self.current = __VERSION__
        self.update_cfg = "update.cfg"

    def check_last_update_time(self):
        """Check the last update timestamp from the file."""
        if os.path.exists(self.update_cfg):
            with open(self.update_cfg, "r") as file:
                last_update_str = file.read().strip()
                if last_update_str:
                    return datetime.fromisoformat(last_update_str)
        return None

    def save_update_time(self):
        """Save the current timestamp to the update configuration file."""
        with open(self.update_cfg, "w") as file:
            file.write(datetime.now().isoformat())

    def fetch_latest_version(self):
        """Fetch the latest version from the remote URL."""
        headers = {'User-Agent': f"openSquat-{self.current}"}
        try:
            response = requests.get(self.URL, headers=headers)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException:
            return None

    def check_for_update(self):
        """Check for a new version and print update information if available."""
        latest_ver = self.fetch_latest_version()
        if latest_ver and version.parse(latest_ver) > version.parse(self.current):
            self.print_update_info(latest_ver)
            return True
        return False

    def print_update_info(self, latest_ver):
        """Prints information about the available update."""
        info = (
            f"{Style.BRIGHT}{Fore.MAGENTA}[INFO] New version available!{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.WHITE}-> Current ver: {self.current}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.WHITE}-> Latest ver: {latest_ver}{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.WHITE}-> Changelog: https://github.com/atenreiro/opensquat/blob/master/CHANGELOG{Style.RESET_ALL}\n"
            f"{Style.BRIGHT}{Fore.WHITE}-> Update now: $ git pull{Style.RESET_ALL}\n"
        )
        print(info)

    def main(self):
        """Main method to check for updates."""
        last_update_time = self.check_last_update_time()
        if last_update_time and datetime.now() - last_update_time < timedelta(days=2):
            return False

        if self.check_for_update():
            self.save_update_time()

if __name__ == "__main__":
    CheckUpdate().main()

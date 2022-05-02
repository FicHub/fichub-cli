# Copyright 2021 Arbaaz Laskar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from typing import Tuple
import re
import os
import sys
import hashlib
import requests
from bs4 import BeautifulSoup

from colorama import Fore, Style
from tqdm import tqdm
from loguru import logger
import typer

from .fichub import FicHub
from .logging import downloaded_log


def get_format_type(_format: str = "epub") -> int:
    if re.search(r"\bepub\b", _format, re.I):
        format_type = 0

    elif re.search(r"\bmobi\b", _format, re.I):
        format_type = 1

    elif re.search(r"\bpdf\b", _format, re.I):
        format_type = 2

    elif re.search(r"\bhtml\b", _format, re.I):
        format_type = 3

    else:  # default epub format
        format_type = 0

    return format_type


def check_url(url: str, debug: bool = False,
              exit_status: int = 0) -> Tuple[bool, int]:

    if re.search(r"\barchiveofourown.org/series\b", url):
        unsupported_flag = True

    elif re.search(r"\bfanfiction.net/u\b", url):
        unsupported_flag = True

    else:
        unsupported_flag = False

    if unsupported_flag:
        with open("err.log", "a") as file:
            file.write(url)

        exit_status = 1

        if debug:
            logger.error(
                f"Skipping unsupported URL: {url}")
        tqdm.write(
            Fore.RED + f"\nSkipping unsupported URL: {url}" +
            Style.RESET_ALL + Fore.CYAN +
            "\nTo see the supported site list, use " + Fore.YELLOW +
            "fichub_cli -ss" + Style.RESET_ALL + Fore.CYAN +
            "\nReport the error if the URL is supported!\n")

        return False, exit_status

    else:  # for supported urls
        return True, exit_status


def save_data(out_dir: str, file_name:  str, download_url: str,
              debug: bool, force: bool, cache_hash: str,
              exit_status: int, automated: bool) -> int:

    ebook_file = os.path.join(out_dir, file_name)

    try:
        hash_flag = check_hash(ebook_file, cache_hash)

    except FileNotFoundError:
        hash_flag = False

    url_exit_status = 0
    if os.path.exists(ebook_file) and force is False and hash_flag is True:

        exit_status = url_exit_status = 1
        if debug:
            logger.warning(
                "The md5 hash of the local file & the remote file are the same.")

            logger.error(
                f"{ebook_file} is already the latest version. Skipping download. Use --force flag to overwrite.")

        tqdm.write(
            Fore.RED +
            f"{ebook_file} is already the latest version. Skipping download." +
            Style.RESET_ALL + Fore.CYAN + " Use --force flag to overwrite.")

    else:
        if force and debug:
            logger.warning(
                f"--force flag was passed. Overwriting {ebook_file}")

        fic = FicHub(debug, automated, exit_status)
        fic.get_fic_data(download_url)

        try:
            with open(ebook_file, "wb") as f:
                if debug:
                    logger.info(
                        f"Saving {ebook_file}")
                f.write(fic.response_data.content)
            downloaded_log(debug, file_name)
        except FileNotFoundError:
            tqdm.write(Fore.RED + "Output directory doesn't exist. Exiting!")
            sys.exit(1)

    return exit_status, url_exit_status


def check_hash(ebook_file: str, cache_hash: str) -> bool:

    with open(ebook_file, 'rb') as file:
        data = file.read()

    ebook_hash = hashlib.md5(data).hexdigest()

    return ebook_hash.strip() == cache_hash.strip()


def out_dir_exists_check(out_dir):
    """Check if the output directory exists"""
    if not os.path.isdir(out_dir):
        mkdir_prompt = typer.confirm(
            Fore.RED+"Output directory doesn't exist!" + Style.RESET_ALL +
            Fore.BLUE + f"\nShould the CLI create {out_dir}?", abort=False, show_default=True)
        if mkdir_prompt is True:
            os.makedirs(out_dir)


def appdir_exists_check(app_dirs):
    """Check if the app directory exists, if not, create it."""
    if not os.path.isdir(app_dirs.user_data_dir):
        tqdm.write(
            f"App directory: {app_dirs.user_data_dir} does not exist. Running makedirs.")
        os.makedirs(app_dirs.user_data_dir)


def list_diff(urls_input, urls_output):
    """ Make a list containing the difference between
        two lists
    """
    urls_output = set(urls_output)
    return [item for item in urls_input if item not in urls_output]


def check_output_log(urls_input, debug):
    if debug:
        logger.info("Checking output.log")
    try:
        urls_output = []
        if os.path.exists("output.log"):
            with open("output.log", "r") as f:
                urls_output = f.read().splitlines()

        urls = list_diff(urls_input, urls_output)

    # if output.log doesnt exist, when run 1st time
    except FileNotFoundError:
        urls = urls_input

    tqdm.write(
        Fore.BLUE + f"After comparing with output.log, total URLs: {len(urls)}")
    if debug:
        logger.info(
            f"After comparing with output.log, total URLs: {len(urls)}")
    return urls


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def check_cli_outdated(package: str, current_ver: str):
    res_html = requests.get(f"https://pypi.org/simple/{package}/")
    html_soup = BeautifulSoup(res_html.content, 'html.parser')

    latest_package = html_soup.find_all('a')[-1].get_text()
    latest_ver = re.search(
        r"(?:(\d+\.[.\d]*\d+))", latest_package, re.I).group(0)

    if versiontuple(current_ver) < versiontuple(latest_ver):
        tqdm.write(
            Fore.RED +
            f"The currently installed {package} v{current_ver} is outdated.\n"
            + Style.RESET_ALL + Fore.GREEN +
            f"Latest version is {latest_ver}\n"
            + Style.RESET_ALL + Fore.CYAN +
            f"Update using: pip install -U {package}\n"
        )


def urls_preprocessing(urls_input, debug):

    tqdm.write(Fore.BLUE + f"URLs found: {len(urls_input)}")
    urls_input_dedup = list(dict.fromkeys(urls_input))
    tqdm.write(
        Fore.BLUE + f"After removing duplicates, total URLs: {len(urls_input_dedup)}")

    if debug:
        logger.info(f"URLs found: {len(urls_input)}")
        logger.info(
            f"After Deduplication, total URLs: {len(urls_input_dedup)}")

    try:
        urls = check_output_log(urls_input_dedup, debug)

    # if output.log doesnt exist, when run 1st time
    except FileNotFoundError:
        urls = urls_input_dedup

    return urls, urls_input_dedup


def build_changelog(urls_input, urls_input_dedup, urls, downloaded_urls,
                    err_urls, no_updates_urls, out_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d T%H%M%S")
    with open(os.path.join(out_dir, f"CHANGELOG - {timestamp}.txt"), 'w') as file:
        file.write(f"""# Changelog
Total URLs given as input: {len(urls_input)}
Total URLs after removing duplicates: {len(urls_input_dedup)}
Total URLs after comparing with the output.log: {len(urls)}
Total URLs/Files downloaded: {len(downloaded_urls)}
Total URLs causing Download Errors: {len(err_urls)}
Total URLs without any updates: {len(no_updates_urls)}
""")

        if urls_input:
            file.write("\n\n## URLs given as Input")
            for url in urls_input:
                file.write(f"\n{url}")

        if urls_input_dedup:
            file.write("\n\n## URLs after removing duplicates")
            for url in urls_input_dedup:
                file.write(f"\n{url}")

        if urls:
            file.write("\n\n## URLs after comparing with the output.log")
            for url in urls:
                file.write(f"\n{url}")

        if downloaded_urls:
            file.write("\n\n## URLs/Files Downloaded")
            for url in downloaded_urls:
                file.write(f"\n{url}")

        if err_urls:
            file.write("\n\n## URLs causing Download Errors")
            for url in err_urls:
                file.write(f"\n{url}")

        if no_updates_urls:
            file.write("\n\n## URLs without any updates")
            for url in no_updates_urls:
                file.write(f"\n{url}")

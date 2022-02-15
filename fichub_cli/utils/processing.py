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

from typing import Tuple
import re
import os
import sys
import hashlib

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
        else:
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

    if os.path.exists(ebook_file) and force is False and hash_flag is True:

        exit_status = 1
        if debug:
            logger.warning(
                "The hash of the local file & the remote file is the same.")

            logger.error(
                f"{ebook_file} is already the latest version. Skipping download. Use --force flag to overwrite.")

        else:
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

    return exit_status


def check_hash(ebook_file: str, cache_hash: str) -> bool:

    with open(ebook_file, 'rb') as file:
        data = file.read()

    ebook_hash = hashlib.md5(data).hexdigest()

    if ebook_hash.strip() == cache_hash.strip():
        hash_flag = True
    else:
        hash_flag = False

    return hash_flag


def out_dir_exists_check(out_dir):
    """Check if the output directory exists"""
    if not os.path.isdir(out_dir):
        mkdir_prompt = typer.prompt(
            Fore.RED+"Output directory doesn't exist!" + Style.RESET_ALL +
            Fore.BLUE + f"\nShould the CLI create {out_dir}?(y/n)")
        if mkdir_prompt == 'y':
            os.mkdir(out_dir)

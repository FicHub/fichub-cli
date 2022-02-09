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

import re
import requests
from tqdm import tqdm
from colorama import Fore, Style
from loguru import logger
from bs4 import BeautifulSoup
from rich.console import Console

from .fichub import FicHub
from .logging import init_log, download_processing_log, \
    verbose_log
from .processing import check_url, save_data

bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}, {rate_fmt}{postfix}, ETA: {remaining}"
console = Console()


class FetchData:
    def __init__(self, format_type="epub", out_dir="", force=False,
                 debug=False, automated=False, verbose=False):
        self.format_type = format_type
        self.out_dir = out_dir
        self.force = force
        self.debug = debug
        self.automated = automated
        self.exit_status = 0
        self.verbose = verbose

    def get_fic_with_infile(self, infile: str):
        if self.debug:
            logger.debug("-i flag used!")
            logger.debug(f"Input file: {infile}")

        try:
            with open(infile, "r") as f:
                urls = f.read().splitlines()

        except FileNotFoundError:

            if self.debug:
                logger.error(
                    f"FileNotFoundError: {infile} file could not be found. Please enter a valid file path.")

            tqdm.write(
                Fore.RED +
                f"{infile} file could not be found. Please enter a valid file path.")
            exit(1)

        init_log(self.debug, self.force)
        with tqdm(total=len(urls), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in urls:

                download_processing_log(self.debug, url)
                supported_url, self.exit_status = check_url(
                    url, self.debug, self.exit_status)
                if supported_url:
                    try:
                        fic = FicHub(self.debug, self.automated,
                                     self.exit_status)
                        fic.get_fic_metadata(url, self.format_type)

                        if self.verbose:
                            verbose_log(self.debug, fic)

                        # update the exit status
                        self.exit_status = fic.exit_status

                        if fic.file_name is None:
                            self.exit_status = 1

                        else:
                            self.exit_status = save_data(
                                self.out_dir, fic.file_name,
                                fic.download_url, self.debug, self.force,
                                fic.cache_hash, self.exit_status,
                                self.automated)

                        pbar.update(1)

                    # Error: 'FicHub' object has no attribute 'file_name'
                    # Reason: Unsupported URL
                    except AttributeError:
                        with open("err.log", "a") as file:
                            file.write(url.strip()+"\n")
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    with open("err.log", "a") as file:
                        file.write(url.strip()+"\n")
                    pbar.update(1)
                    continue

    def get_fic_with_list(self, list_url: str):

        if self.debug:
            logger.debug("-l flag used!")

        urls = list_url.split(",")

        init_log(self.debug, self.force)
        with tqdm(total=len(urls), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in urls:
                download_processing_log(self.debug, url)
                supported_url,  self.exit_status = check_url(
                    url, self.debug, self.exit_status)

                if supported_url:
                    try:
                        fic = FicHub(self.debug, self.automated,
                                     self.exit_status)
                        fic.get_fic_metadata(url, self.format_type)

                        if self.verbose:
                            verbose_log(self.debug, fic)

                        # update the exit status
                        self.exit_status = fic.exit_status

                        if fic.file_name is None:
                            self.exit_status = 1

                        else:
                            self.exit_status = save_data(
                                self.out_dir, fic.file_name,
                                fic.download_url, self.debug, self.force,
                                fic.cache_hash, self.exit_status, self.automated)

                        pbar.update(1)

                    # Error: 'FicHub' object has no attribute 'file_name'
                    # Reason: Unsupported URL
                    except AttributeError:
                        with open("err.log", "a") as file:
                            file.write(url.strip()+"\n")
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    with open("err.log", "a") as file:
                        file.write(url.strip()+"\n")
                    pbar.update(1)
                    continue

    def get_fic_with_url(self, url: str):

        if self.debug:
            logger.debug("-u flag used!")

        init_log(self.debug, self.force)
        with tqdm(total=1, ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            download_processing_log(self.debug, url)
            supported_url, self.exit_status = check_url(
                url, self.debug, self.exit_status)

            if supported_url:
                try:
                    fic = FicHub(self.debug, self.automated, self.exit_status)
                    fic.get_fic_metadata(url, self.format_type)

                    if self.verbose:
                        verbose_log(self.debug, fic)

                    # update the exit status
                    self.exit_status = fic.exit_status

                    if fic.file_name is None:
                        self.exit_status = 1

                    else:
                        self.exit_status = save_data(
                            self.out_dir, fic.file_name,
                            fic.download_url, self.debug, self.force,
                            fic.cache_hash, self.exit_status, self.automated)

                    pbar.update(1)

                # Error: 'FicHub' object has no attribute 'file_name'
                # Reason: Unsupported URL
                except AttributeError:
                    with open("err.log", "a") as file:
                        file.write(url.strip()+"\n")
                    pbar.update(1)
                    self.exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                with open("err.log", "a") as file:
                    file.write(url.strip()+"\n")
                pbar.update(1)

    def get_urls_from_page(self, get_urls: str):

        if self.debug:
            logger.debug("--get-urls flag used!")

        with console.status("[bold green]Processing..."):
            response = requests.get(get_urls, timeout=(5, 300))

            if self.debug:
                logger.debug(f"GET: {response.status_code}: {response.url}")

            html_page = BeautifulSoup(response.content, 'html.parser')

            found_flag = False
            if re.search("https://archiveofourown.org/", get_urls):
                ao3_series_works_html = []
                ao3_works_list = []
                ao3_series_list = []

                ao3_series_works_html_h4 = html_page.findAll(
                    'h4', attrs={'class': 'heading'})

                for i in ao3_series_works_html_h4:
                    ao3_series_works_html.append(i)

                ao3_series_works_html = ""
                for i in ao3_series_works_html_h4:
                    ao3_series_works_html += str(i)

                ao3_urls = BeautifulSoup(ao3_series_works_html, 'html.parser')

                for tag in ao3_urls.findAll('a', {'href': re.compile('/works/')}):
                    ao3_works_list.append(
                        "https://archiveofourown.org"+tag['href'])

                for tag in ao3_urls.findAll('a', {'href': re.compile('/series/')}):
                    ao3_series_list.append(
                        "https://archiveofourown.org"+tag['href'])

                if ao3_works_list:
                    found_flag = True
                    tqdm.write(Fore.GREEN +
                               f"\nFound {len(ao3_works_list)} works urls." +
                               Style.RESET_ALL)
                    ao3_works_list = '\n'.join(ao3_works_list)
                    tqdm.write(ao3_works_list)

                if ao3_series_list:
                    found_flag = True
                    tqdm.write(Fore.GREEN +
                               f"\nFound {len(ao3_series_list)} series urls." +
                               Style.RESET_ALL)
                    ao3_series_list = '\n'.join(ao3_series_list)
                    tqdm.write(ao3_series_list)

            if found_flag is False:
                tqdm.write(Fore.RED + "\nFound 0 urls.")
                self.exit_status = 1

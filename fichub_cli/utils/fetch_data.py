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

import typer
from tqdm import tqdm
from colorama import Fore
from loguru import logger

from .fichub import FicHub
from .logging import init_log, download_processing_log, \
    verbose_log
from .processing import check_url, save_data, \
    urls_preprocessing, check_output_log, build_changelog

bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}, {rate_fmt}{postfix}, ETA: {remaining}"


class FetchData:
    def __init__(self, format_type=0, out_dir="", force=False,
                 debug=False, changelog=False, automated=False, verbose=False):
        self.format_type = format_type
        self.out_dir = out_dir
        self.force = force
        self.debug = debug
        self.changelog = changelog
        self.automated = automated
        self.exit_status = 0
        self.verbose = verbose

    def get_fic_with_infile(self, infile: str):
        if self.debug:
            logger.info("-i flag used!")
            logger.info(f"Input file: {infile}")

        try:
            with open(infile, "r") as f:
                urls_input = f.read().splitlines()

        except FileNotFoundError:

            if self.debug:
                logger.error(
                    f"FileNotFoundError: {infile} file could not be found. Please enter a valid file path.")

            tqdm.write(
                Fore.RED +
                f"{infile} file could not be found. Please enter a valid file path.")
            exit(1)

        urls, urls_input_dedup = urls_preprocessing(urls_input, self.debug)
        downloaded_urls, no_updates_urls, err_urls = [], [], []
        if urls:
            init_log(self.debug, self.force)
            with tqdm(total=len(urls), ascii=False,
                      unit="file", bar_format=bar_format) as pbar:

                for url in urls:
                    url_exit_status = 0
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
                                self.exit_status, url_exit_status = save_data(
                                    self.out_dir, fic.file_name,
                                    fic.download_url, self.debug, self.force,
                                    fic.cache_hash, self.exit_status,
                                    self.automated)

                                with open("output.log", "a") as file:
                                    file.write(f"{url}\n")

                                if url_exit_status == 0:
                                    downloaded_urls.append(url)
                                else:
                                    no_updates_urls.append(url)
                            pbar.update(1)

                        # Error: 'FicHub' object has no attribute 'file_name'
                        # Reason: Unsupported URL
                        except AttributeError:
                            with open("err.log", "a") as file:
                                file.write(url.strip()+"\n")
                            err_urls.append(url)
                            pbar.update(1)
                            self.exit_status = 1
                            pass  # skip the unsupported url

                    else:  # skip the unsupported url
                        with open("err.log", "a") as file:
                            file.write(url.strip()+"\n")
                        err_urls.append(url)
                        pbar.update(1)
                        continue

        else:
            typer.echo(Fore.RED +
                       "No new urls found! If output.log exists, please clear it.")

        if self.changelog:
            build_changelog(urls_input, urls_input_dedup, urls,
                            downloaded_urls, err_urls, no_updates_urls, self.out_dir)

    def get_fic_with_list(self, list_url: str):

        if self.debug:
            logger.info("-l flag used!")

        urls_input = list_url.split(",")
        urls, urls_input_dedup = urls_preprocessing(urls_input, self.debug)
        downloaded_urls, no_updates_urls, err_urls = [], [], []
        if urls:
            init_log(self.debug, self.force)
            with tqdm(total=len(urls), ascii=False,
                      unit="file", bar_format=bar_format) as pbar:

                for url in urls:
                    url_exit_status = 0
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
                                self.exit_status, url_exit_status = save_data(
                                    self.out_dir, fic.file_name,
                                    fic.download_url, self.debug, self.force,
                                    fic.cache_hash, self.exit_status, self.automated)

                                with open("output.log", "a") as file:
                                    file.write(f"{url}\n")

                                if url_exit_status == 0:
                                    downloaded_urls.append(url)
                                else:
                                    no_updates_urls.append(url)

                            pbar.update(1)

                        # Error: 'FicHub' object has no attribute 'file_name'
                        # Reason: Unsupported URL
                        except AttributeError:
                            with open("err.log", "a") as file:
                                file.write(url.strip()+"\n")
                            err_urls.append(url)
                            pbar.update(1)
                            self.exit_status = 1
                            pass  # skip the unsupported url

                    else:  # skip the unsupported url
                        with open("err.log", "a") as file:
                            file.write(url.strip()+"\n")
                        err_urls.append(url)
                        pbar.update(1)
                        continue
        else:
            typer.echo(Fore.RED +
                       "No new urls found! If output.log exists, please clear it.")

        if self.changelog:
            build_changelog(urls_input, urls_input_dedup, urls,
                            downloaded_urls, err_urls, no_updates_urls, self.out_dir)

    def get_fic_with_url(self, url_input: str):

        if self.debug:
            logger.info("-u flag used!")

        url = check_output_log([url_input], self.debug)

        if url:
            init_log(self.debug, self.force)
            with tqdm(total=1, ascii=False,
                      unit="file", bar_format=bar_format) as pbar:

                download_processing_log(self.debug, url[0])
                supported_url, self.exit_status = check_url(
                    url[0], self.debug, self.exit_status)

                if supported_url:
                    try:
                        fic = FicHub(self.debug, self.automated,
                                     self.exit_status)
                        fic.get_fic_metadata(url[0], self.format_type)

                        if self.verbose:
                            verbose_log(self.debug, fic)

                        # update the exit status
                        self.exit_status = fic.exit_status

                        if fic.file_name is None:
                            self.exit_status = 1

                        else:
                            self.exit_status, _ = save_data(
                                self.out_dir, fic.file_name,
                                fic.download_url, self.debug, self.force,
                                fic.cache_hash, self.exit_status, self.automated)
                            with open("output.log", "a") as file:
                                file.write(f"{url[0]}\n")
                        pbar.update(1)

                    # Error: 'FicHub' object has no attribute 'file_name'
                    # Reason: Unsupported URL
                    except AttributeError:
                        with open("err.log", "a") as file:
                            file.write(url[0].strip()+"\n")
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    with open("err.log", "a") as file:
                        file.write(url[0].strip()+"\n")
                    pbar.update(1)
        else:
            typer.echo(Fore.RED +
                       "No new urls found! If output.log exists, please clear it.")

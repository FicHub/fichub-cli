import click
import click_spinner
from tqdm import tqdm
from loguru import logger
from bs4 import BeautifulSoup
import requests
import re


from .fichub import FicHub
from .logging import init_log, download_processing_log
from .processing import check_url, save_data

bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}, {rate_fmt}{postfix}, ETA: {remaining}"


class FetchData:
    def __init__(self, format_type="epub", out_dir="", force=False,
                 debug=False, automated=False):
        self.format_type = format_type
        self.out_dir = out_dir
        self.force = force
        self.debug = debug
        self.automated = automated
        self.exit_status = 0

    def get_fic_with_infile(self, infile: str):

        try:
            with open(infile, "r") as f:
                urls = f.read().splitlines()

        except FileNotFoundError:
            click.secho(
                f"{infile} file could not be found. Please enter a valid file path.", fg="red")
            exit(1)

        init_log(self.debug, self.force)
        if self.debug:
            logger.debug("Calling get_fic_with_infile()")

        with tqdm(total=len(urls), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in urls:

                supported_url, self.exit_status = check_url(
                    pbar, url, self.debug, self.exit_status)
                if supported_url:
                    try:
                        download_processing_log(self.debug, url)
                        fic = FicHub(self.debug, self.automated,
                                     self.exit_status)
                        fic.get_fic_metadata(url, self.format_type, pbar)

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

                    except TypeError:
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    pass

    def get_fic_with_list(self, list_url: str):

        urls = list_url.split(",")

        init_log(self.debug, self.force)
        if self.debug:
            logger.debug("Calling get_fic_with_list()")

        with tqdm(total=len(urls), ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            for url in urls:

                supported_url,  self.exit_status = check_url(
                    pbar, url, self.debug, self.exit_status)
                if supported_url:
                    try:
                        download_processing_log(self.debug, url)
                        fic = FicHub(self.debug, self.automated,
                                     self.exit_status)
                        fic.get_fic_metadata(url, self.format_type, pbar)

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

                    except TypeError:
                        pbar.update(1)
                        self.exit_status = 1
                        pass  # skip the unsupported url

                else:  # skip the unsupported url
                    pass

    def get_fic_with_url(self, url: str):

        init_log(self.debug, self.force)
        if self.debug:
            logger.debug("Calling get_fic_with_url()")

        with tqdm(total=1, ascii=False,
                  unit="file", bar_format=bar_format) as pbar:

            supported_url, self.exit_status = check_url(
                pbar, url, self.debug, self.exit_status)
            if supported_url:
                try:
                    download_processing_log(self.debug, url)

                    fic = FicHub(self.debug, self.automated, self.exit_status)
                    fic.get_fic_metadata(url, self.format_type, pbar)

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

                except TypeError:
                    pbar.update(1)
                    self.exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    def get_urls_from_page(self, get_urls: str):

        with click_spinner.spinner():
            response = requests.get(get_urls)

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
                    click.secho(
                        f"\nFound {len(ao3_works_list)} works urls.", fg='green')
                    ao3_works_list = '\n'.join(ao3_works_list)
                    click.echo(ao3_works_list)

                if ao3_series_list:
                    found_flag = True
                    click.secho(
                        f"\nFound {len(ao3_series_list)} series urls.", fg='green')
                    ao3_series_list = '\n'.join(ao3_series_list)
                    click.echo(ao3_series_list)

            if found_flag is False:
                click.secho("Found 0 urls.", fg='red')
                self.exit_status = 1

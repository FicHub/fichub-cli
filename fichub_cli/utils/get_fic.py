from bs4 import BeautifulSoup
import requests
import re
import click
import click_spinner
from tqdm import tqdm
from loguru import logger

from .fichub import get_fic_metadata
from .logging import init_log, download_processing_log
from .processing import check_url, save_data


def get_fic_with_infile(infile: str, format_type: int = 0,
                        out_dir: str = "", debug: bool = False,
                        force: bool = False, automated: bool = False) -> int:

    exit_status = 0

    try:
        with open(infile, "r") as f:
            urls = f.read().splitlines()

    except FileNotFoundError:
        click.secho(
            f"{infile} file could not be found. Please enter a valid file path.", fg="red")
        exit(1)

    init_log(debug, force)
    if debug:
        logger.debug("Calling get_fic_with_infile()")

    with tqdm(range(len(urls)), ascii=False) as pbar:
        for url in urls:

            supported_url, exit_status = check_url(
                pbar, url, debug, exit_status)
            if supported_url:
                try:
                    download_processing_log(debug, url)
                    file_name, download_url, \
                        cache_hash, exit_status = get_fic_metadata(
                            url, format_type, debug, pbar,
                            exit_status, automated)

                    if file_name is None:
                        exit_status = 1

                    else:
                        exit_status = save_data(out_dir, file_name,
                                                download_url, debug, force,
                                                cache_hash, exit_status,
                                                automated)

                    pbar.update(1)

                except TypeError:
                    pbar.update(1)
                    exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    return exit_status


def get_fic_with_list(list_url: str, format_type: int = 0,
                      out_dir: str = "", debug: bool = False,
                      force: bool = False, automated: bool = False) -> int:

    exit_status = 0
    urls = list_url.split(",")

    init_log(debug, force)
    if debug:
        logger.debug("Calling get_fic_with_list()")

    with tqdm(range(len(urls)), ascii=False) as pbar:
        for url in urls:

            supported_url, exit_status = check_url(
                pbar, url, debug, exit_status)
            if supported_url:
                try:
                    download_processing_log(debug, url)
                    file_name, download_url, \
                        cache_hash, exit_status = get_fic_metadata(
                            url, format_type, debug, pbar,
                            exit_status, automated)

                    if file_name is None:
                        exit_status = 1

                    else:
                        exit_status = save_data(out_dir, file_name,
                                                download_url, debug, force,
                                                cache_hash, exit_status, automated)

                    pbar.update(1)

                except TypeError:
                    pbar.update(1)
                    exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    return exit_status


def get_fic_with_url(url: str, format_type: int = 0, out_dir: str = "",
                     debug: bool = False, force: bool = False,
                     automated: bool = False) -> int:

    exit_status = 0

    init_log(debug, force)
    if debug:
        logger.debug("Calling get_fic_with_url()")

    with tqdm(range(1), ascii=False) as pbar:

        supported_url, exit_status = check_url(pbar, url, debug, exit_status)
        if supported_url:
            try:
                download_processing_log(debug, url)

                file_name, download_url, cache_hash, \
                    exit_status = get_fic_metadata(
                        url, format_type, debug, pbar,
                        exit_status, automated)

                if file_name is None:
                    exit_status = 1

                else:
                    exit_status = save_data(out_dir, file_name,
                                            download_url, debug, force,
                                            cache_hash, exit_status, automated)

                pbar.update(1)

            except TypeError:
                pbar.update(1)
                exit_status = 1
                pass  # skip the unsupported url

        else:  # skip the unsupported url
            pass

    return exit_status


def get_urls_from_page(get_urls: str, debug: bool, automated: bool):

    with click_spinner.spinner():
        response = requests.get(get_urls)

        if debug:
            logger.debug(f"GET: {response.status_code}: {response.url}")

        html_page = BeautifulSoup(response.content, 'html.parser')

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

            ao3_works = BeautifulSoup(ao3_series_works_html, 'html.parser')

            for tag in ao3_works.findAll('a', {'href': re.compile('/works/')}):
                ao3_works_list.append(
                    "https://archiveofourown.org"+tag['href'])

            for tag in ao3_works.findAll('a', {'href': re.compile('/series/')}):
                ao3_series_list.append(
                    "https://archiveofourown.org"+tag['href'])

            found_flag = False
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

            return 0  # exit_status

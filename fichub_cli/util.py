import click
import re
from tqdm import tqdm

from loguru import logger
from .fichub import get_fic_data


def get_format_type(format):
    if format.startswith("epub"):
        format_type = 0

    elif format.startswith("mobi"):
        format_type = 1

    elif format.startswith("pdf"):
        format_type = 2

    elif format.startswith("html"):
        format_type = 3

    else:  # default epub format
        format_type = 0

    return format_type


def get_fic_with_infile(infile=None, format_type=0, out_dir="", debug=False):

    exit_status = 0
    with open(infile, "r") as f:
        urls = f.read().splitlines()

    if debug:
        logger.debug("Download Started")
    else:
        click.secho("Download Started", fg='green')

    with tqdm(range(len(urls)), ascii=True) as pbar:
        for url in urls:

            supported_url, exit_status = check_url(
                pbar, url, debug, exit_status)
            if supported_url:
                try:
                    fic_name, file_format, data, exit_status = get_fic_data(
                        url, format_type, debug, pbar, exit_status)

                    if fic_name is None:
                        exit_status = 1

                    if debug:
                        logger.debug(f"\n\nDownloading: {fic_name}")
                    else:
                        click.secho(
                            f"\n\nDownloading: {fic_name}", fg='green')

                    with open(out_dir+fic_name+file_format, "wb") as f:
                        f.write(data)

                    pbar.update(1)

                except TypeError:
                    pbar.update(1)
                    exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    return exit_status


def get_fic_with_list(list_url=None, format_type=0, out_dir="", debug=False):

    exit_status = 0
    urls = list_url.split(",")

    if debug:
        logger.debug("Download Started")
    else:
        click.secho("Download Started", fg='green')

    with tqdm(range(len(urls)), ascii=True) as pbar:
        for url in urls:

            supported_url, exit_status = check_url(
                pbar, url, debug, exit_status)
            if supported_url:
                try:
                    fic_name, file_format, data, exit_status = get_fic_data(
                        url, format_type, debug, pbar, exit_status)

                    if fic_name is None:
                        exit_status = 1

                    if debug:
                        logger.debug(f"\n\nDownloading: {fic_name}")
                    else:
                        click.secho(
                            f"\n\nDownloading: {fic_name}", fg='green')

                    with open(out_dir+fic_name+file_format, "wb") as f:
                        f.write(data)

                    pbar.update(1)

                except TypeError:
                    pbar.update(1)
                    exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    return exit_status


def get_fic_with_url(url, format_type=0, out_dir="", debug=False):

    exit_status = 0
    if debug:
        logger.debug("Download Started")
    else:
        click.secho("Download Started", fg='green')

    with tqdm(range(1), ascii=True) as pbar:

        supported_url, exit_status = check_url(pbar, url, debug, exit_status)
        if supported_url:
            try:
                fic_name, file_format, data, exit_status = get_fic_data(
                    url, format_type, debug, pbar, exit_status)

                if fic_name is None:
                    exit_status = 1

                else:
                    if debug:
                        logger.debug(f"\n\nDownloading: {fic_name}")
                    else:
                        click.secho(
                            f"\n\nDownloading: {fic_name}", fg='green')

                    with open(out_dir+fic_name+file_format, "wb") as f:
                        f.write(data)

                pbar.update(1)

            except TypeError:
                pbar.update(1)
                exit_status = 1
                pass  # skip the unsupported url

        else:  # skip the unsupported url
            pass

    return exit_status


def check_url(pbar, url, debug=False, exit_status=0):

    if re.search(r"\barchiveofourown.org/series\b", url):
        unsupported_flag = True

    elif re.search(r"\bfanfiction.net/u\b", url):
        unsupported_flag = True

    else:
        unsupported_flag = False

    if unsupported_flag:
        pbar.update(1)
        exit_status = 1

        if debug:
            logger.error(
                f"\n\nSkipping unsupported URL: {url}\nTo see the supported site list, fichub_cli -s")
        else:
            click.echo(click.style(
                f"\n\nSkipping unsupported URL: {url}", fg='red') + "\nTo see the supported site list, fichub_cli -s")

        return False, exit_status

    else:  # for supported urls
        return True, exit_status

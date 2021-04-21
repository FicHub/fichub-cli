import click
import re

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

    with open(infile, "r") as f:
        urls = f.read().splitlines()

    count = 1
    with click.progressbar(urls, label=f"Downloading {len(urls)} files", length=len(urls), show_eta=False) as bar:
        for url in bar:
            count += 1

            if check_url(url, debug):
                try:
                    fic_name, file_format, data = get_fic_data(
                        url, format_type, debug)

                    if debug:
                        logger.debug(
                            f"\nDownloading: {fic_name}")

                    with open(out_dir+fic_name+file_format, "wb") as f:
                        f.write(data)
                except TypeError:
                    pass

            else:  # skip the unsupported url
                pass


def get_fic_with_list(list_url=None, format_type=0, out_dir="", debug=False):

    urls = list_url.split(",")

    count = 1
    with click.progressbar(urls, label=f"Downloading {len(urls)} files",  length=len(urls), show_eta=False) as bar:
        for url in bar:
            count += 1

            if check_url(url, debug):
                try:
                    fic_name, file_format, data = get_fic_data(
                        url, format_type, debug)

                    if debug:
                        logger.debug(
                            f"\nDownloading: {fic_name}")

                    with open(out_dir+fic_name+file_format, "wb") as f:
                        f.write(data)
                except TypeError:
                    pass
            else:  # skip the unsupported url
                pass


def get_fic_with_url(url=None, format_type=0, out_dir="", debug=False):

    with click.progressbar(label="Downloaded 1 file",  length=1, show_eta=False) as bar:

        if check_url(url, debug):
            try:
                fic_name, file_format, data = get_fic_data(
                    url, format_type, debug)

                if debug:
                    logger.debug(f"\nDownloading: {fic_name}")

                with open(out_dir+fic_name+file_format, "wb") as f:
                    f.write(data)
                    bar.update(2)

            except TypeError:
                pass

        else:  # skip the unsupported url
            pass


def check_url(url, debug=False):
    if re.search(r"\barchiveofourown.org/series\b", url):
        unsupported_flag = True

    elif re.search(r"\bfanfiction.net/u\b", url):
        unsupported_flag = True

    else:
        unsupported_flag = False

    if unsupported_flag:
        if debug:
            logger.error(
                f"\nSkipping unsupported URL: {url}.\nTo see the supported site list, fichub_cli -s")
        else:
            click.echo(
                f"\nSkipping unsupported URL: {url}.\nTo see the supported site list, fichub_cli -s")

        return False

    else:  # for supported urls
        return True

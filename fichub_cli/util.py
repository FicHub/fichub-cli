import click
import re
import os
from tqdm import tqdm

from loguru import logger
from .fichub import get_fic_metadata, get_fic_data


def get_format_type(format):
    if re.search(r"\bepub\b", format, re.I):
        format_type = 0

    elif re.search(r"\bmobi\b", format, re.I):
        format_type = 1

    elif re.search(r"\bpdf\b", format, re.I):
        format_type = 2

    elif re.search(r"\bhtml\b", format, re.I):
        format_type = 3

    else:  # default epub format
        format_type = 0

    return format_type


def get_fic_with_infile(infile=None, format_type=0, out_dir="",
                        debug=False, force=False, automated=False):

    exit_status = 0
    with open(infile, "r") as f:
        urls = f.read().splitlines()

    init_log(debug, force)
    if debug:
        logger.info("Inside get_fic_with_infile() function")

    with tqdm(range(len(urls)), ascii=True) as pbar:
        for url in urls:

            supported_url, exit_status = check_url(
                pbar, url, debug, exit_status)
            if supported_url:
                try:
                    fic_name, file_format, download_url, exit_status = get_fic_metadata(
                        url, format_type, debug, pbar, exit_status, automated)

                    if fic_name is None:
                        exit_status = 1

                    if debug:
                        logger.info(f"\n\nDownloading: {fic_name}")
                    else:
                        click.secho(
                            f"\n\nDownloading: {fic_name}", fg='green')

                    exit_status = save_data(out_dir, fic_name, file_format,
                                            download_url, debug, force,
                                            exit_status, automated)

                    pbar.update(1)

                except TypeError:
                    pbar.update(1)
                    exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    return exit_status


def get_fic_with_list(list_url=None, format_type=0, out_dir="",
                      debug=False, force=False, automated=False):

    exit_status = 0
    urls = list_url.split(",")

    init_log(debug, force)
    if debug:
        logger.info("Inside get_fic_with_list() function")

    with tqdm(range(len(urls)), ascii=True) as pbar:
        for url in urls:

            supported_url, exit_status = check_url(
                pbar, url, debug, exit_status)
            if supported_url:
                try:
                    fic_name, file_format, download_url, exit_status = get_fic_metadata(
                        url, format_type, debug, pbar, exit_status, automated)

                    if fic_name is None:
                        exit_status = 1

                    if debug:
                        logger.info(f"\n\nDownloading: {fic_name}")
                    else:
                        click.secho(
                            f"\n\nDownloading: {fic_name}", fg='green')

                    exit_status = save_data(out_dir, fic_name, file_format,
                                            download_url, debug, force,
                                            exit_status, automated)

                    pbar.update(1)

                except TypeError:
                    pbar.update(1)
                    exit_status = 1
                    pass  # skip the unsupported url

            else:  # skip the unsupported url
                pass

    return exit_status


def get_fic_with_url(url, format_type=0, out_dir="",
                     debug=False, force=False, automated=False):

    exit_status = 0

    init_log(debug, force)
    if debug:
        logger.info("Inside get_fic_with_url() function")

    with tqdm(range(1), ascii=True) as pbar:

        supported_url, exit_status = check_url(pbar, url, debug, exit_status)
        if supported_url:
            try:
                fic_name, file_format, download_url, exit_status = get_fic_metadata(
                    url, format_type, debug, pbar, exit_status, automated)

                if fic_name is None:
                    exit_status = 1

                else:
                    if debug:
                        logger.info(f"\n\nDownloading: {fic_name}")
                    else:
                        click.secho(
                            f"\n\nDownloading: {fic_name}", fg='green')

                    exit_status = save_data(out_dir, fic_name, file_format,
                                            download_url, debug, force,
                                            exit_status, automated)

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


def save_data(out_dir, fic_name, file_format, download_url,
              debug, force, exit_status, automated):

    if os.path.exists(out_dir+fic_name+file_format) and force is False:
        exit_status = 1
        if debug:
            logger.error(
                f"\n{out_dir+fic_name+file_format} already exits. Skipping download. Use --force option to overwrite.")
        else:
            click.secho(
                f"\n{out_dir+fic_name+file_format} already exits. Skipping download. Use --force option to overwrite.", fg='red')
    else:
        if force and debug:
            logger.warning(
                "--force flag was passed. Files will be overwritten.")

        data = get_fic_data(download_url, automated)
        with open(out_dir+fic_name+file_format, "wb") as f:
            f.write(data)

    return exit_status


def init_log(debug, force):
    if debug:
        logger.info("Download Started")
        if force:
            logger.warning(
                "--force flag was passed. Files will be overwritten.")
    else:
        click.secho("Download Started", fg='green')
        if force:
            click.secho(
                "WARNING: --force flag was passed. Files will be overwritten.", fg='yellow')

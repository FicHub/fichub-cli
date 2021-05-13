from typing import Tuple
import re
import os
import hashlib

import click
from tqdm import tqdm
from loguru import logger

from .fichub import get_fic_metadata, get_fic_data
from .logging import init_log, downloaded_log, download_processing_log


def get_format_type(_format: str = "epub") -> int:
    if re.search(r"\bepub\b", _format, re.I):
        format_type = 0

    elif re.search(r"\bmobi\b", _format, re.I):
        format_type = 1

    elif re.search(r"\bpdf\b", _format, re.I):
        format_type = 2

    elif re.search(r"\bhtml\b", _format, re.I):
        format_type = 3

    else:  # default epub _format
        format_type = 0

    return format_type


def get_fic_with_infile(infile: str, format_type: int = 0,
                        out_dir: str = "", debug: bool = False,
                        force: bool = False, automated: bool = False) -> int:

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
                    download_processing_log(debug, url)
                    fic_name, file_format, download_url, \
                        cache_hash, exit_status = get_fic_metadata(
                            url, format_type, debug, pbar,
                            exit_status, automated)

                    if fic_name is None:
                        exit_status = 1

                    else:
                        exit_status = save_data(out_dir, fic_name, file_format,
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


def get_fic_with_list(list_url: str, format_type: int = 0,
                      out_dir: str = "", debug: bool = False,
                      force: bool = False, automated: bool = False) -> int:

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
                    download_processing_log(debug, url)
                    fic_name, file_format, download_url, \
                        cache_hash, exit_status = get_fic_metadata(
                            url, format_type, debug, pbar,
                            exit_status, automated)

                    if fic_name is None:
                        exit_status = 1

                    else:
                        exit_status = save_data(out_dir, fic_name, file_format,
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
        logger.info("Inside get_fic_with_url() function")

    with tqdm(range(1), ascii=True) as pbar:

        supported_url, exit_status = check_url(pbar, url, debug, exit_status)
        if supported_url:
            try:
                download_processing_log(debug, url)
                fic_name, file_format, download_url, cache_hash, \
                    exit_status = get_fic_metadata(
                        url, format_type, debug, pbar, exit_status, automated)

                if fic_name is None:
                    exit_status = 1

                else:
                    exit_status = save_data(out_dir, fic_name, file_format,
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


def check_url(pbar, url: str, debug: bool = False,
              exit_status: int = 0) -> Tuple[bool, int]:

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
                f"Skipping unsupported URL: {url}\nTo see the supported site list, fichub_cli -s")
        else:
            click.echo(click.style(
                f"Skipping unsupported URL: {url}", fg='red') + "\nstTo see the supported site list, fichub_cli -s")

        return False, exit_status

    else:  # for supported urls
        return True, exit_status


def save_data(out_dir: str, fic_name:  str, file_format: str, download_url: str,
              debug: bool, force: bool, cache_hash: str,
              exit_status: int, automated: bool) -> int:

    ebook_file = out_dir+fic_name+file_format
    try:
        hash_flag = check_hash(ebook_file, cache_hash)

    except FileNotFoundError:
        hash_flag = False

    if os.path.exists(out_dir+fic_name+file_format) and force is False and hash_flag is True:

        exit_status = 1
        if debug:
            logger.error(
                f"{out_dir+fic_name+file_format} is already the latest version. Skipping download. Use --force option to overwrite.")
            logger.warning(
                "The hash of the local file & the remote file is the same.")
        else:
            click.secho(
                f"{out_dir+fic_name+file_format} is already the latest version. Skipping download. Use --force option to overwrite.", fg='red')

    else:
        if force and debug:
            logger.warning(
                "--force flag was passed. Files will be overwritten.")

        data = get_fic_data(download_url, automated)
        downloaded_log(debug, fic_name)
        with open(ebook_file, "wb") as f:
            f.write(data)

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

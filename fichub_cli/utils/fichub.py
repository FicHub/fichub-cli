import requests
from typing import Tuple, Optional
import click
import re
from loguru import logger


def get_fic_metadata(
    url: str, format_type: int, debug: bool,
    pbar, exit_status: int = 0, automated: bool = False
) -> Tuple[Optional[str], Optional[str],
           Optional[str], Optional[str], int]:

    headers = {
        'User-Agent': 'fichub_cli/0.3.4a',
    }

    params = {'q': url}
    if automated:  # for internal testing
        params['automated'] = 'true'
        if debug:
            logger.debug(
                "--automated flag was passed. Internal Testing mode is on.")

    response = requests.get(
        "https://fichub.net/api/v0/epub", params=params,
        allow_redirects=True, headers=headers
    )

    if debug:
        logger.debug(f"GET: {response.status_code}: {response.url}")

    response = response.json()

    try:
        if format_type == 0:
            cache_url = response['epub_url']
            cache_hash = (
                re.search(r"\?h=(.*)", response['epub_url'])).group(1)
            file_format = ".epub"

        elif format_type == 1:
            cache_url = response['mobi_url']
            cache_hash = (
                re.search(r"\?h=(.*)", response['epub_url'])).group(1)
            file_format = ".mobi"

        elif format_type == 2:
            cache_url = response['pdf_url']
            cache_hash = (
                re.search(r"\?h=(.*)", response['epub_url'])).group(1)
            file_format = ".pdf"

        elif format_type == 3:
            cache_url = response['html_url']
            cache_hash = (
                re.search(r"\?h=(.*)", response['epub_url'])).group(1)
            file_format = ".zip"

        file_name = response['epub_url'].split("/")[4].split("?")[0]
        file_name = file_name.replace(".epub", file_format)
        download_url = "https://fichub.net"+cache_url
        return file_name, download_url, cache_hash, exit_status

    except KeyError:
        exit_status = 1
        if debug:
            logger.error(
                f"\n\nSkipping unsupported URL: {url}\nTo see the supported site list, fichub_cli -s")
        else:
            click.echo(click.style(
                f"\n\nSkipping unsupported URL: {url}", fg='red') + "\nTo see the supported site list, fichub_cli -s")

        return None, None, None, exit_status


def get_fic_data(download_url: str, automated: bool = False,
                 debug: bool = False) -> bytes:

    headers = {
        'User-Agent': 'fichub_cli/0.3.4a',
    }

    params = {}
    if automated:  # for internal testing
        params['automated'] = 'true'

    response = requests.get(
        download_url, allow_redirects=True, headers=headers, params=params)

    if debug:
        logger.debug(f"GET: {response.status_code}: {response.url}")

    return response.content
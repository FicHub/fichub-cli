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
        'User-Agent': 'fichub_cli/0.3.4',
    }

    params = {'q': url}
    if automated:  # for internal testing
        params['automated'] = 'true'
        if debug:
            logger.info("-a flag was passed. Internal Testing mode is on.")

    response = requests.get(
        "https://fichub.net/api/v0/epub", params=params,
        allow_redirects=True, headers=headers
    ).json()

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

        fic_name = response['epub_url'].split("/")[4].split("?")[0]
        fic_name = fic_name.replace(".epub", "")
        download_url = "https://fichub.net"+cache_url

        return fic_name, file_format, download_url, cache_hash, exit_status

    except KeyError:
        exit_status = 1
        if debug:
            logger.error(
                f"\n\nSkipping unsupported URL: {url}\nTo see the supported site list, fichub_cli -s")
        else:
            click.echo(click.style(
                f"\n\nSkipping unsupported URL: {url}", fg='red') + "\nTo see the supported site list, fichub_cli -s")

        return None, None, None, None, exit_status


def get_fic_data(download_url: str, automated: bool = False) -> bytes:

    headers = {
        'User-Agent': 'fichub_cli/0.3.4',
    }

    params = {}
    if automated:  # for internal testing
        params['automated'] = 'true'

    data = requests.get(
        download_url, allow_redirects=True, headers=headers, params=params).content

    return data

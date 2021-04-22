import requests
import click
from loguru import logger


def get_fic_data(url, format_type, debug, pbar, exit_status=0):

    headers = {
        'User-Agent': 'fichub_cli/0.2.5',
    }

    response = requests.get(
        "https://fichub.net/api/v0/epub", params={'q': url},
        allow_redirects=True, headers=headers
    ).json()

    try:
        if format_type == 0:
            cache_url = response['epub_url']
            file_format = ".epub"

        elif format_type == 1:
            cache_url = response['mobi_url']
            file_format = ".mobi"

        elif format_type == 2:
            cache_url = response['pdf_url']
            file_format = ".pdf"

        elif format_type == 3:
            cache_url = response['html_url']
            file_format = ".zip"

        fic_name = response['epub_url'].split("/")[4].split("?")[0]
        fic_name = fic_name.replace(".epub", "")
        download_url = "https://fichub.net"+cache_url
        data = requests.get(
            download_url, allow_redirects=True, headers=headers).content

        return fic_name, file_format, data, exit_status

    except KeyError:
        exit_status = 1
        if debug:
            logger.error(
                f"\n\nSkipping unsupported URL: {url}\nTo see the supported site list, fichub_cli -s")
        else:
            click.echo(click.style(
                f"\n\nSkipping unsupported URL: {url}", fg='red') + "\nTo see the supported site list, fichub_cli -s")

        return None, None, None, exit_status

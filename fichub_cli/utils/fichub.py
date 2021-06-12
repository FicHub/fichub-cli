import requests
import click
import re
from loguru import logger

headers = {
    'User-Agent': 'fichub_cli/0.3.4b',
}


class FicHub:
    def __init__(self, debug, automated, exit_status):
        self.debug = debug
        self.automated = automated
        self.exit_status = exit_status

    def get_fic_metadata(self, url: str, format_type: int, pbar):

        params = {'q': url}
        if self.automated:  # for internal testing
            params['automated'] = 'true'
            if self.debug:
                logger.debug(
                    "--automated flag was passed. Internal Testing mode is on.")

        response = requests.get(
            "https://fichub.net/api/v0/epub", params=params,
            allow_redirects=True, headers=headers
        )

        if self.debug:
            logger.debug(f"GET: {response.status_code}: {response.url}")

        response = response.json()

        try:
            if format_type == 0:
                cache_url = response['epub_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", response['epub_url'])).group(1)
                self.file_format = ".epub"

            elif format_type == 1:
                cache_url = response['mobi_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", response['epub_url'])).group(1)
                self.file_format = ".mobi"

            elif format_type == 2:
                cache_url = response['pdf_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", response['epub_url'])).group(1)
                self.file_format = ".pdf"

            elif format_type == 3:
                cache_url = response['html_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", response['epub_url'])).group(1)
                self.file_format = ".zip"

            self.file_name = response['epub_url'].split("/")[4].split("?")[0]
            self.file_name = self.file_name.replace(".epub", self.file_format)
            self.download_url = "https://fichub.net"+cache_url

        except KeyError:
            self.exit_status = 1
            if self.debug:
                logger.error(
                    f"\n\nSkipping unsupported URL: {url}\nTo see the supported site list, fichub_cli -s")
            else:
                self.click.echo(click.style(
                    f"\n\nSkipping unsupported URL: {url}", fg='red') + "\nTo see the supported site list, fichub_cli -s")

    def get_fic_data(self, download_url: str):

        params = {}
        if self.automated:  # for internal testing
            params['automated'] = 'true'

        self.response_data = requests.get(
            download_url, allow_redirects=True, headers=headers, params=params)

        if self.debug:
            logger.debug(
                f"GET: {self.response_data.status_code}: {self.response_data.url}")

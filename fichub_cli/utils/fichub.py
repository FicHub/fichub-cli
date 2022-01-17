import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import re
from colorama import Fore, Style
from tqdm import tqdm
from loguru import logger

headers = {
    'User-Agent': 'fichub_cli/0.5.0',
}

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)


class FicHub:
    def __init__(self, debug, automated, exit_status):
        self.debug = debug
        self.automated = automated
        self.exit_status = exit_status
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http = requests.Session()
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def get_fic_metadata(self, url: str, format_type: int):

        params = {'q': url}
        if self.automated:  # for internal testing
            params['automated'] = 'true'
            if self.debug:
                logger.debug(
                    "--automated flag was passed. Internal Testing mode is on.")

        response = self.http.get(
            "https://fichub.net/api/v0/epub", params=params,
            allow_redirects=True, headers=headers, timeout=(6.1, 300)
        )

        if self.debug:
            logger.debug(f"GET: {response.status_code}: {response.url}")

        self.response = response.json()

        try:
            if format_type == 0:
                cache_url = self.response['epub_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", self.response['epub_url'])).group(1)
                self.file_format = ".epub"

            elif format_type == 1:
                cache_url = self.response['mobi_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", self.response['epub_url'])).group(1)
                self.file_format = ".mobi"

            elif format_type == 2:
                cache_url = self.response['pdf_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", self.response['epub_url'])).group(1)
                self.file_format = ".pdf"

            elif format_type == 3:
                cache_url = self.response['html_url']
                self.cache_hash = (
                    re.search(r"\?h=(.*)", self.response['epub_url'])).group(1)
                self.file_format = ".zip"

            self.file_name = self.response['epub_url'].split(
                "/")[4].split("?")[0]
            self.file_name = self.file_name.replace(".epub", self.file_format)
            self.download_url = "https://fichub.net"+cache_url

        # Error: 'epub_url'
        # Reason: Unsupported URL
        except KeyError:

            self.exit_status = 1
            if self.debug:
                logger.error(
                    f"Skipping unsupported URL: {url}")
            else:
                tqdm.write(
                    Fore.RED + f"Skipping unsupported URL: {url}" +
                    Style.RESET_ALL + Fore.CYAN +
                    "\nTo see the supported site list, use -s flag")

    def get_fic_data(self, download_url: str):

        params = {}
        if self.automated:  # for internal testing
            params['automated'] = 'true'

        self.response_data = self.http.get(
            download_url, allow_redirects=True, headers=headers,
            params=params, timeout=(6.1, 300))

        if self.debug:
            logger.debug(
                f"GET: {self.response_data.status_code}: {self.response_data.url}")

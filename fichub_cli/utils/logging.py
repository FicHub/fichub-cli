from colorama import Fore
from loguru import logger
from tqdm import tqdm
from datetime import datetime


def init_log(debug: bool, force: bool):
    if debug:
        if force:
            logger.warning(
                "--force flag was passed. Files will be overwritten.")
    else:
        if force:
            tqdm.write(
                Fore.YELLOW +
                "WARNING: --force flag was passed. Files will be overwritten.")


def downloaded_log(debug: bool, file_name: str):
    if debug:
        logger.info(f"Downloaded {file_name}")
    else:
        tqdm.write(Fore.GREEN + f"Downloaded {file_name}")


def download_processing_log(debug: bool, url: str):
    if debug:
        logger.info(f"Processing {url.strip()}")
    else:
        tqdm.write(Fore.BLUE + f"\nProcessing {url.strip()}")


def verbose_log(debug: bool, fic):
    try:
        if debug:
            logger.info("Total Chapters: " +
                        str(fic.response['meta']['chapters'])
                        + " | Last Scrape: " + datetime
                        .strptime(str(fic.response['meta']['updated']), "%Y-%m-%dT%H:%M:%S")
                        .strftime("%d %b, %Y at %H:%M:%S"))
        else:
            tqdm.write(Fore.MAGENTA
                       + "Total Chapters: " +
                       str(fic.response['meta']['chapters'])
                       + "\nLast Updated: " + datetime
                       .strptime(str(fic.response['meta']['updated']), "%Y-%m-%dT%H:%M:%S")
                       .strftime("%d %b, %Y at %H:%M:%S"))
    # Error: KeyError: 'meta'
    # Reason: Unsupported url
    except KeyError:
        pass


def meta_fetched_log(debug: bool, url: str):
    if debug:
        logger.info(f"Metadata fetched for {url}")
    else:
        tqdm.write(Fore.GREEN + f"Metadata fetched for {url}")

from colorama import Fore
from loguru import logger
from tqdm import tqdm


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
        logger.info(f"Processing {url}")
    else:
        tqdm.write(Fore.BLUE + f"\nProcessing {url}")

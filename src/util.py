import click
from fichub import get_fic_data


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


def get_fic_with_infile(infile=None, format_type=0):

    with open(infile, "r") as f:
        urls = f.read().splitlines()

    count = 1
    with click.progressbar(urls, label=f"Downloading {len(urls)} files", length=len(urls)) as bar:
        for url in bar:
            count += 1
            file_name, data = get_fic_data(url, format_type)
            with open(file_name, "wb") as f:
                f.write(data)


def get_fic_with_list(list_url=None, format_type=0):

    urls = list_url.split(",")

    count = 1
    with click.progressbar(urls, label=f"Downloading {len(urls)} files",  length=len(urls)) as bar:
        for url in bar:
            count += 1
            file_name, data = get_fic_data(url, format_type)
            with open(file_name, "wb") as f:
                f.write(data)


def get_fic_with_url(url=None, format_type=0):

    with click.progressbar(label="Downloading 1 file",  length=1) as bar:
        file_name, data = get_fic_data(url, format_type)
        with open(file_name, "wb") as f:
            f.write(data)
            bar.update(2)

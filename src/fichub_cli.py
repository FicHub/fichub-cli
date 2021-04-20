import click
from util import get_fic_with_infile, get_fic_with_list, \
    get_fic_with_url, get_format_type


@click.command()
@click.option('-i', '--INFILE', default=None, help='Give a filename to read URLs from')
@click.option('-f', '--FORMAT', default="epub", help='Download Format: epub(default), mobi, pdf or html')
@click.option('-l', '--list_URL', default=None, help='Enter a list of urls to download separated by comma enclosed in quotes')
@click.option('-u', '--URL', default=None, help='The url of the fanfiction')
def cli(INFILE, URL, list_URL, FORMAT):

    format_type = get_format_type(FORMAT)
    if INFILE:
        get_fic_with_infile(INFILE, format_type)

    elif list_URL:
        get_fic_with_list(list_URL, format_type)

    elif URL:
        get_fic_with_url(URL, format_type)

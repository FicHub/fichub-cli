import click
from util import get_fic_with_infile, get_fic_with_list, \
    get_fic_with_url, get_format_type


@click.command()
@click.option('-i', '--infile', default=None, help='Give a filename to read URLs from')
@click.option('-o', '--out_dir', default="", help='Output directory for files')
@click.option('-f', '--format', default="epub", help='Download Format: epub(default), mobi, pdf or html')
@click.option('-l', '--list_url', default=None, help='Enter a list of urls to download separated by comma enclosed in quotes')
@click.option('-u', '--url', default=None, help='The url of the fanfiction')
@click.option('-d', '--debug', default=False, help='Debug mode', is_flag=True)
@click.option('-v', '--version', default=False, help='Display version & quit.', is_flag=True)
def cli(infile, url, list_url, format, out_dir, debug, version):

    format_type = get_format_type(format)
    if infile:
        get_fic_with_infile(infile, format_type, out_dir, debug)

    elif list_url:
        get_fic_with_list(list_url, format_type, out_dir, debug)

    elif url:
        get_fic_with_url(url, format_type, out_dir, debug)

    if version:
        click.echo("Version: 0.1")

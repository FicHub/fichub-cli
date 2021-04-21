import click
from loguru import logger

from .util import get_fic_with_infile, get_fic_with_list, \
    get_fic_with_url, get_format_type


@click.command()
@click.option('-i', '--infile', default=None, help='Give a filename to read URLs from')
@click.option('-o', '--out_dir', default="", help='Output directory for files')
@click.option('-f', '--format', default="epub", help='Download Format: epub(default), mobi, pdf or html')
@click.option('-l', '--list_url', default=None, help='Enter a list of urls to download separated by comma enclosed in quotes')
@click.option('-u', '--url', default=None, help='The url of the fanfiction')
@click.option('-s', '--supported_sites', default=False, help='List of supported sites', is_flag=True)
@click.option('-d', '--debug', default=False, help='Debug mode', is_flag=True)
@click.option('-v', '--version', default=False, help='Display version & quit.', is_flag=True)
def run_cli(infile, url, list_url, format, out_dir, debug, version, supported_sites):

    if debug:
        logger.debug("Download Started")

    format_type = get_format_type(format)
    if infile:
        get_fic_with_infile(infile, format_type, out_dir, debug)

    elif list_url:
        get_fic_with_list(list_url, format_type, out_dir, debug)

    elif url:
        get_fic_with_url(url, format_type, out_dir, debug)

    if version:
        click.echo("Version: 0.2")

    if supported_sites:
        click.echo("""
    Supported Sites

        - SpaceBattles, SufficientVelocity, QuestionableQuesting (XenForo)
        - FanFiction.net, FictionPress (temporarily fragile)
        - Archive Of Our Own
        - Royal Road
        - Harry Potter Fanfic Archive
        - Sink Into Your Eyes
        - AdultFanfiction.org
        - Worm, Ward

    Partial support (or not tested recently):

        - XenForo based sites (Bulbagarden Forums, The Fanfiction Forum, Fanfic Paradise)
        - Fiction Alley
        - Fiction Hunt
        - The Sugar Quill (largely untested)
        - FanficAuthors (minimal)
        - Harry Potter Fanfiction (archive from pre-revival)
""")


run_cli()

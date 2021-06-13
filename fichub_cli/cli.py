import click
import sys
from loguru import logger

from .utils.fetch_data import FetchData
from .utils.processing import get_format_type


# @logger.catch  # for internal debugging
@click.command(no_args_is_help=True)
@click.option('-u', '--url', help='The url of the fanfiction enclosed within quotes ')
@click.option('-i', '--infile', help='Give a filename to read URLs from')
@click.option('-l', '--list-url', 'list_url',  help='Enter a comma separated list of urls to download, enclosed within quotes')
@click.option('-o', '--out-dir', 'out_dir', default="", help='Absolute path to the Output directory for files (default: Current Directory)')
@click.option('-f', '--format', '_format', default="epub", help='Download Format: epub (default), mobi, pdf or html')
@click.option('--force', default=False, help=' Force overwrite of an existing file', is_flag=True)
@click.option('--get-urls', 'get_urls', default=False, help='Get all story urls found from a page. Currently supports archiveofourown.org only.')
@click.option('-s', '--supported-sites', 'supported_sites', default=False, help='List of supported sites', is_flag=True)
@click.option('-d', '--debug', default=False, help='Show the log in the console for debugging', is_flag=True)
@click.option('--log', default=False, help='Save the logfile for debugging', is_flag=True)
@click.option('-a', '--automated', default=False, help='For internal testing only', is_flag=True, hidden=True)
@click.option('-v', '--version', default=False, help='Display version & quit.', is_flag=True)
def run_cli(infile: str, url: str, list_url: str, _format: str, get_urls: str,
            out_dir: str, debug: bool, version: bool, log: bool,
            supported_sites: bool, force: bool, automated: bool):
    """
    A CLI for the fichub.net API

    To report issues upstream for supported sites, visit https://fichub.net/#contact

    To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues
    """

    if log:
        debug = True
        logger.add("fichub_cli.log")

    format_type = get_format_type(_format)
    if infile:
        fic = FetchData(format_type, out_dir, force,
                        debug, automated)
        fic.get_fic_with_infile(infile)

    elif list_url:
        fic = FetchData(format_type, out_dir, force,
                        debug, automated)
        fic.get_fic_with_list(list_url)

    elif url:
        fic = FetchData(format_type, out_dir, force,
                        debug, automated)
        fic.get_fic_with_url(url)

    elif get_urls:
        fic = FetchData(debug)
        fic.get_urls_from_page(get_urls)

    if version:
        click.echo("Version: 0.3.4b")
        sys.exit(0)

    if supported_sites:
        click.echo("""
    Supported Sites

        - SpaceBattles, SufficientVelocity, QuestionableQuesting (XenForo)
        - FanFiction.net, FictionPress
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

    To report issues upstream for these sites, visit https://fichub.net/#contact
""")
        sys.exit(0)

    if log:  # To separate each run
        logger.info(f"{20*'-'}EXITING{20*'-'}")

    sys.exit(fic.exit_status)

import click
import sys
from loguru import logger
from datetime import datetime
from colorama import init, Fore, Style

from .utils.processing import get_format_type
from .utils.fetch_data import FetchData

init(autoreset=True)  # colorama init
timestamp = datetime.now().strftime("%Y-%m-%d T%H%M%S")


# @logger.catch  # for internal debugging
@click.command(no_args_is_help=True)
@click.option('-u', '--url', help='The url of the fanfiction enclosed within quotes')
@click.option('-i', '--infile', help='Give a filename to read URLs from')
@click.option('-l', '--list-url', 'list_url',  help='Enter a comma separated list of urls to download, enclosed within quotes')
@click.option('-v', '--verbose', default=False, help='Verbose progressbar', is_flag=True)
@click.option('-o', '--out-dir', 'out_dir', default="", help='Absolute path to the Output directory for files (default: Current Directory)')
@click.option('-f', '--format', '_format', default="epub", help='Download Format: epub (default), mobi, pdf or html')
@click.option('--force', default=False, help=' Force overwrite of an existing file', is_flag=True)
@click.option('--get-urls', 'get_urls', default=None, help='Get all story urls found from a page. Currently supports archiveofourown.org only')
@click.option('-s', '--supported-sites', 'supported_sites', default=False, help='List of supported sites', is_flag=True)
@click.option('-d', '--debug', default=False, help='Show the log in the console for debugging', is_flag=True)
@click.option('--meta-json', 'meta_json', default=None, help='Fetch only the metadata for the fanfiction in json format')
@click.option('--log', default=False, help='Save the logfile for debugging', is_flag=True)
@click.option('-a', '--automated', default=False, help='For internal testing only', is_flag=True, hidden=True)
@click.option('--pytest', default=False, help='To run pytest on the CLI for internal testing', is_flag=True, hidden=True)
@click.option('--version', default=False, help='Display version & quit', is_flag=True)
def run_cli(infile: str, url: str, list_url: str, _format: str, get_urls: str,
            out_dir: str, debug: bool, version: bool, log: bool,
            supported_sites: bool, force: bool, automated: bool,
            meta_json: str, verbose: bool, pytest: bool):
    """
    A CLI for the fichub.net API

    To report issues upstream for supported sites, visit https://fichub.net/#contact

    To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

    Failed downloads will be saved in the `err.log` file in the current directory.
    """
    if pytest:  # for internal testing
        import pytest
        pytest.main(['-v'])

    if log:
        debug = True
        click.echo(
            Fore.GREEN + f"Creating fichub_cli - {timestamp}.log in the current directory")
        logger.add(f"fichub_cli - {timestamp}.log")

    format_type = get_format_type(_format)
    if infile:
        fic = FetchData(format_type, out_dir, force,
                        debug, automated, verbose)
        fic.get_fic_with_infile(infile)

    elif list_url:
        fic = FetchData(format_type, out_dir, force,
                        debug, automated, verbose)
        fic.get_fic_with_list(list_url)

    elif url:
        fic = FetchData(format_type, out_dir, force,
                        debug, automated, verbose)
        fic.get_fic_with_url(url)

    elif get_urls:
        fic = FetchData(debug=debug, automated=automated)
        fic.get_urls_from_page(get_urls)

    elif meta_json:
        fic = FetchData(debug=debug, automated=automated,
                        out_dir=out_dir)
        fic.get_metadata(meta_json)

    if version:
        click.echo("Version: 0.4.4")

    if supported_sites:
        click.echo(Fore.GREEN + """
Supported Sites:""" + Style.RESET_ALL + """

    - SpaceBattles, SufficientVelocity, QuestionableQuesting (XenForo)
    - FanFiction.net, FictionPress
    - Archive Of Our Own
    - Harry Potter Fanfic Archive
    - Sink Into Your Eyes
    - AdultFanfiction.org
    - Worm, Ward
""" + Fore.GREEN + """
Partial support (or not tested recently):""" + Style.RESET_ALL + """

    - XenForo based sites
        - Bulbagarden Forums
        - The Fanfiction Forum
        - Fanfic Paradise
    - Fiction Alley
    - Fiction Hunt
    - The Sugar Quill(largely untested)
    - FanficAuthors(minimal)
    - Harry Potter Fanfiction(archive from pre-revival)
""" + Fore.BLUE + """
To report issues upstream for these sites, visit https://fichub.net/#contact
""")
    try:
        if fic.exit_status == 1:
            click.echo(Fore.RED + """
Unsupported URLs found! Check err.log in the current directory!""" + Style.RESET_ALL)
        sys.exit(fic.exit_status)
    except UnboundLocalError:
        sys.exit(0)

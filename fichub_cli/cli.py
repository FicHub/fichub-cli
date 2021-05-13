import click
import sys

from .util.processing import get_fic_with_infile, get_fic_with_list, \
    get_fic_with_url, get_format_type


@click.command(no_args_is_help=True)
@click.option('-u', '--url', help='The url of the fanfiction enclosed within quotes ')
@click.option('-i', '--infile', help='Give a filename to read URLs from')
@click.option('-l', '--list-url', 'list_url',  help='Enter a comma separated list of urls to download, enclosed within quotes')
@click.option('-o', '--out-dir', 'out_dir', default="", help='Absolute/Relative path to the Output directory for files (default: Current Directory)')
@click.option('-f', '--format', '_format', default="epub", help='Download Format: epub (default), mobi, pdf or html')
@click.option('--force', default=False, help=' Force overwrite of an existing file', is_flag=True)
@click.option('-s', '--supported-sites', 'supported_sites', default=False, help='List of supported sites', is_flag=True)
@click.option('-d', '--debug', default=False, help='Debug mode', is_flag=True)
@click.option('-a', '--automated', default=False, help='For internal testing only', is_flag=True, hidden=True)
@click.option('-v', '--version', default=False, help='Display version & quit.', is_flag=True)
def run_cli(infile: str, url: str, list_url: str, _format: str,
            out_dir: str, debug: bool, version: bool,
            supported_sites: bool, force: bool, automated: bool):
    """
    A CLI for the fichub.net API

    To report issues upstream for supported sites, visit https://fichub.net/#contact 

    To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues
    """
    exit_status = 0
    format_type = get_format_type(_format)
    if infile:
        exit_status = get_fic_with_infile(
            infile, format_type, out_dir, debug, force, automated)

    elif list_url:
        exit_status = get_fic_with_list(
            list_url, format_type, out_dir, debug, force, automated)

    elif url:
        exit_status = get_fic_with_url(
            url, format_type, out_dir, debug, force, automated)

    if version:
        click.echo("Version: 0.3.4")

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

    sys.exit(exit_status)

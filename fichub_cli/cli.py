import click
import sys

from .util import get_fic_with_infile, get_fic_with_list, \
    get_fic_with_url, get_format_type


@click.command(no_args_is_help=True)
@click.option('-u', '--url', default=None, help='The url of the fanfiction enclosed within quotes ')
@click.option('-i', '--infile', default=None, help='Give a filename to read URLs from')
@click.option('-l', '--list_url', default=None, help='Enter a comma separated list of urls to download, enclosed within quotes')
@click.option('-o', '--out_dir', default="", help='Output directory for files (default: Current Directory)')
@click.option('-f', '--format', default="epub", help='Download Format: epub (default), mobi, pdf or html')
@click.option('-s', '--supported_sites', default=False, help='List of supported sites', is_flag=True)
@click.option('-d', '--debug', default=False, help='Debug mode', is_flag=True)
@click.option('-v', '--version', default=False, help='Display version & quit.', is_flag=True)
def run_cli(infile, url, list_url, format, out_dir, debug, version, supported_sites):
    """
    A CLI for the fichub.net API

    To report issues upstream for supported sites, visit https://fichub.net/#contact 

    To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues
    """
    exit_status = 0
    format_type = get_format_type(format)

    if infile:
        exit_status = get_fic_with_infile(
            infile, format_type, out_dir, debug)

    elif list_url:
        exit_status = get_fic_with_list(
            list_url, format_type, out_dir, debug)

    elif url:
        exit_status = get_fic_with_url(
            url, format_type, out_dir, debug)

    if version:
        click.echo("Version: 0.2.5")

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

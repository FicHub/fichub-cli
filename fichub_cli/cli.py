# Copyright 2021 Arbaaz Laskar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typer
import sys
from loguru import logger
from datetime import datetime
from colorama import init, Fore, Style

import importlib
import pkgutil

from .utils.fetch_data import FetchData
from .utils.processing import get_format_type, out_dir_exists_check


init(autoreset=True)  # colorama init
timestamp = datetime.now().strftime("%Y-%m-%d T%H%M%S")

app = typer.Typer(add_completion=False)

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('fichub_cli_')
}

for plugin in discovered_plugins.values():
    app.add_typer(plugin.app)


# @logger.catch  # for internal debugging
@app.callback(no_args_is_help=True, invoke_without_command=True)
def default(
    ctx: typer.Context,
    url: str = typer.Option(
        "", "-u", "--url", help="The url of the fanfiction enclosed within quotes"),

    infile: str = typer.Option(
        "", "-i", "--infile", help="Path to a file to read URLs from"),

    list_url: str = typer.Option(
        "", "-l", "--list-url", help="Enter a comma separated list of urls to download, enclosed within quotes"),

    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Verbose", is_flag=True),

    out_dir: str = typer.Option(
        "", "-o", " --out-dir", help="Path to the Output directory for files (default: Current Directory)"),

    format: str = typer.Option(
        "epub", help="Download Format: epub (default), mobi, pdf or html"),

    force: bool = typer.Option(
        False, help="Force overwrite of an existing file", is_flag=True),

    get_urls: str = typer.Option(
        "", help="Get all story urls found from a page. Currently supports archiveofourown.org only"),

    supported_sites: bool = typer.Option(
        False, "-ss", "--supported-sites", help="List of supported sites", is_flag=True),

    debug: bool = typer.Option(
        False, "-d", " --debug", help="Show the log in the console for debugging", is_flag=True),

    log: bool = typer.Option(
        False, help="Save the logfile for debugging", is_flag=True),

    automated: bool = typer.Option(
        False, "-a", "--automated", help="For internal testing only", is_flag=True, hidden=True),

    version: bool = typer.Option(
        False, help="Display version & quit", is_flag=True)
):
    """
    A CLI for the fichub.net API

    To report issues upstream for supported sites, visit https://fichub.net/#contact

    To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

    Failed downloads will be saved in the `err.log` file in the current directory
    """
    # Check if the output directory exists if input is given
    if not out_dir == "":
        out_dir_exists_check(out_dir)

    if ctx.invoked_subcommand is not None:
        if debug:
            typer.echo(
                Fore.BLUE + "Skipping default command to run sub-command.")
        return

    if log:
        # debug = True
        typer.echo(
            Fore.GREEN + "Creating " + Style.RESET_ALL + Fore.YELLOW +
            f"fichub_cli - {timestamp}.log" + Style.RESET_ALL +
            Fore.GREEN + " in the current directory!" + Style.RESET_ALL)
        logger.add(f"fichub_cli - {timestamp}.log")

    format_type = get_format_type(format)
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

    if version:
        typer.echo("fichub-cli: v0.5.3")

    if supported_sites:
        typer.echo(Fore.GREEN + """
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
            typer.echo(
                Fore.RED +
                "\nDownload failed for one or more URLs! Check " + Style.RESET_ALL +
                Fore.YELLOW + "err.log" + Style.RESET_ALL + Fore.RED +
                " in the current directory!" + Style.RESET_ALL)
        sys.exit(fic.exit_status)
    except UnboundLocalError:
        sys.exit(0)

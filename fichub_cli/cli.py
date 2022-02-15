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

import argparse
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


def create_parser():
    cli_parser = argparse.ArgumentParser(prog='fichub-cli',
                                         description="""
A CLI for the fichub.net API

To report issues upstream for supported sites, visit https://fichub.net/#contact

To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

Failed downloads will be saved in the `err.log` file in the current directory
        """, formatter_class=argparse.RawTextHelpFormatter)

    cli_parser.add_argument("-u", "--url", type=str, default="",
                            help="The url of the fanfiction enclosed within quotes")

    cli_parser.add_argument("-i", "--infile", type=str, default="",
                            help="Path to a file to read URLs from")

    cli_parser.add_argument("-l", "--list-url", type=str, default="",
                            help="Enter a comma separated list of urls to download, enclosed within quotes")

    cli_parser.add_argument("-v", "--verbose", type=bool, default=False,
                            help="Verbose")

    cli_parser.add_argument("-o", "--out-dir", type=str, default="",
                            help="Path to the Output directory for files (default: Current Directory)")

    cli_parser.add_argument("--format", type=str, default="epub",
                            help="Download Format: epub (default), mobi, pdf or html")

    cli_parser.add_argument('--force', action='store_true',
                            help="Force overwrite of an existing file")

    cli_parser.add_argument("--get-urls", action='store_true',
                            help="Get all story urls found from a page. Currently supports archiveofourown.org only")

    cli_parser.add_argument("-ss", "--supported-sites", action='store_true',
                            help="List of supported sites")

    cli_parser.add_argument("-d", "--debug", action='store_true',
                            help="Show the log in the console for debugging")

    cli_parser.add_argument("--log", action='store_true',
                            help="Save the logfile for debugging")

    cli_parser.add_argument("-a", "--automated", action='store_true',
                            help=argparse.SUPPRESS)

    cli_parser.add_argument("--version", action='store_true',
                            help="Display version & quit")

    # discovered_plugins = {
    #     name: importlib.import_module(name)
    #     for finder, name, ispkg
    #     in pkgutil.iter_modules()
    #     if name.startswith('fichub_cli_')
    # }

    # for plugin in discovered_plugins.values():
    #     app.add_typer(plugin.app)

    return cli_parser


# @logger.catch  # for internal debugging
def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    parser = create_parser()
    args = parser.parse_args(argv)

    # if no args is given, invoke help
    if len(argv) == 0:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Check if the output directory exists if input is given
    if not args.out_dir == "":
        out_dir_exists_check(args.out_dir)

    if args.log:
        # debug = True
        print(
            Fore.GREEN + "Creating " + Style.RESET_ALL + Fore.YELLOW +
            f"fichub_cli - {timestamp}.log" + Style.RESET_ALL +
            Fore.GREEN + " in the current directory!" + Style.RESET_ALL)
        logger.add(f"fichub_cli - {timestamp}.log")

    format_type = get_format_type(args.format)
    if args.infile:
        fic = FetchData(format_type, args.out_dir, args.force,
                        args.debug, args.automated, args.verbose)
        fic.get_fic_with_infile(args.infile)

    elif args.list_url:
        fic = FetchData(format_type, args.out_dir, args.force,
                        args.debug, args.automated, args.verbose)
        fic.get_fic_with_list(args.list_url)

    elif args.url:
        fic = FetchData(format_type, args.out_dir, args.force,
                        args.debug, args.automated, args.verbose)
        fic.get_fic_with_url(args.url)

    elif args.get_urls:
        fic = FetchData(debug=args.debug, automated=args.automated)
        fic.get_urls_from_page(args.get_urls)

    if args.version:
        print("fichub-cli: v0.5.3")

    if args.supported_sites:
        print(Fore.GREEN + """
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
            print(
                Fore.RED +
                "\nDownload failed for one or more URLs! Check " + Style.RESET_ALL +
                Fore.YELLOW + "err.log" + Style.RESET_ALL + Fore.RED +
                " in the current directory!" + Style.RESET_ALL)
            sys.exit(fic.exit_status)
    except UnboundLocalError:
        sys.exit(0)

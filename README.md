<h1 align="center">fichub-cli</h1>

A CLI for the fichub.net API<br><br>

To report issues upstream for the supported sites, visit https://fichub.net/#contact<br>

To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

# Installation

Install the package using pip

```
pip install -U fichub_cli
```

# Usage

```
> fichub_cli
Usage: fichub_cli [OPTIONS]

  A CLI for the fichub.net API

  To report issues upstream for supported sites, visit
  https://fichub.net/#contact

  To report issues for the CLI, open an issue at
  https://github.com/FicHub/fichub-cli/issues

Options:
  -i, --infile TEXT      Give a filename to read URLs from
  -o, --out_dir TEXT     Output directory for files
  -f, --format TEXT      Download Format: epub(default), mobi, pdf or html
  -l, --list_url TEXT    Enter a comma separated list of urls to download, enclosed within quotes
  -u, --url TEXT         The url of the fanfiction enclosed within quotes
  -s, --supported_sites  List of supported sites
  -d, --debug            Debug mode
  -v, --version          Display version & quit.
  --help                 Show this message and exit.
```

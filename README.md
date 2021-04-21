<h1 align="center">fichub-cli</h1>

A CLI for the fichub.net API<br>

# Installation

Install the package using pip

```
pip install -U fichub_cli
```

# Usage

```
> fichub_cli --help
Usage: fichub_cli [OPTIONS]

Options:
  -i, --infile TEXT      Give a filename to read URLs from
  -o, --out_dir TEXT     Output directory for files
  -f, --format TEXT      Download Format: epub(default), mobi, pdf or html
  -l, --list_url TEXT    Enter a list of urls to download separated by comma enclosed in quotes
  -u, --url TEXT         The url of the fanfiction
  -s, --supported_sites  List of supported sites
  -d, --debug            Debug mode
  -v, --version          Display version & quit.
  --help                 Show this message and exit.
```

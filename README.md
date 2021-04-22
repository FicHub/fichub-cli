<h1 align="center">fichub-cli</h1>

A CLI tool for the fichub.net API<br><br>

To report issues upstream for the supported sites, visit https://fichub.net/#contact<br>

To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

# Installation

Install the package using pip

```
pip install -U fichub-cli
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
  -u, --url TEXT         The url of the fanfiction enclosed within quotes
  -i, --infile TEXT      Give a filename to read URLs from
  -l, --list_url TEXT    Enter a comma separated list of urls to download, enclosed within quotes
  -o, --out_dir TEXT     Output directory for files (default: Current Directory)
  -f, --format TEXT      Download Format: epub (default), mobi, pdf or html
  -s, --supported_sites  List of supported sites
  -d, --debug            Debug mode
  -v, --version          Display version & quit.
  --help                 Show this message and exit.
```

## Example

- To download using a URL

```
fichub_cli -u https://archiveofourown.org/works/10916730/chapters/24276864

```

- To download using a file containing URLs

```
fichub_cli -i urls.txt
```

- To download using a comma separated list of URLs

```
fichub_cli -l "https://www.fanfiction.net/s/11191235/1/Harry-Potter-and-the-Prince-of-Slytherin,https://www.fanfiction.net/s/13720575/1/A-Cadmean-Victory-Remastered"
```

### Default Configuration

- The fanfiction will be downloaded in epub format. To change it, use `-f` followed by the format.
- The fanfiction will be downloaded in the current directory. To change it, use `-o` followed by the path to the directory.

Check `fichub_cli --help` for more info.

# Links

- [Official Discord Server](https://discord.gg/sByBAhX)

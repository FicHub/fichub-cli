<h1 align="center">fichub-cli</h1>

A CLI for the fichub.net API<br><br>

To report issues upstream for the supported sites, visit https://fichub.net/#contact<br>

To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

# Installation

## Using pip (Recommended)

```
pip install -U fichub-cli
```

## From Source (Might have bugs, for testing only)

```
pip install git+https://github.com/FicHub/fichub-cli@main
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
  -l, --list-url TEXT    Enter a comma separated list of urls to download, enclosed within quotes
  -v, --verbose          Verbose progressbar
  -o, --out-dir TEXT     Absolute path to the Output directory for files (default: Current Directory)
  -f, --format TEXT      Download Format: epub (default), mobi, pdf or html
  --force                Force overwrite of an existing file
  --get-urls TEXT        Get all story urls found from a page.Currently supports archiveofourown.org only
  -s, --supported-sites  List of supported sites
  -d, --debug            Show the log in the console for debugging
  --meta-json TEXT       Fetch only the metadata for the fanfiction in json format
  --log                  Save the logfile for debugging
  --version              Display version & quit
  --help                 Show this message and exit
```

# Default Configuration

- The fanfiction will be downloaded in epub format. To change it, use `-f` followed by the format.
- The fanfiction will be downloaded in the current directory. To change it, use `-o` followed by the path to the directory.
- Failed downloads will be saved in the `err.log` file in the current directory.
- `--meta-json` takes either URL or a file containing a list of URLs. `--out-dir` can be used to select an output directory.

Check `fichub_cli --help` for more info.

# Example

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

---

**NOTE**
`--out-dir` can be used in all the above commands to select an output directory.

---

- To get all story urls found from a page. Currently supports archiveofourown.org only.

```
fichub_cli --get-urls https://archiveofourown.org/users/flamethrower/
```

- To fetch only the metadata for the fanfiction in json format.

```
fichub_cli --meta-json "https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind"
```

```
fichub_cli --meta-json urls.txt
```

```
fichub_cli --meta-json urls.txt --out-dir "~/Desktop/books"
```

# Links

- [Official Discord Server](https://discord.gg/sByBAhX)

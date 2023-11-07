<h1 align="center">fichub-cli </h1>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/arzkar)

A CLI for the fichub.net API<br>
To report issues upstream for the supported sites, visit https://fichub.net/#contact<br>
To report issues for the CLI, open an issue at https://github.com/FicHub/fichub-cli/issues

# Installation

## From pip (Recommended)

```
pip install -U fichub-cli
```

## From Github Source (Pre-release, for testing new features by Beta testers)

```
pip install git+https://github.com/FicHub/fichub-cli@main
```

# Usage

```
> fichub_cli
Usage: fichub_cli [OPTIONS] COMMAND [ARGS]...

  A CLI for the fichub.net API

  To report issues upstream for supported sites, visit
  https://fichub.net/#contact

  To report issues for the CLI, open an issue at
  https://github.com/FicHub/fichub-cli/issues

  Failed downloads will be saved in the `err.log` file in the current
  directory

Options:
  -u, --url TEXT          The url of the fanfiction enclosed within quotes
  -i, --infile TEXT       Path to a file to read URLs from
  -l, --list-url TEXT     Enter a comma separated list of urls to download,
                          enclosed within quotes
  -v, --verbose           Show fic stats
  -o,  --out-dir TEXT     Path to the Output directory for files (default:
                          Current Directory)
  --format TEXT           Download Formats, comma separated if multiple: epub (default), mobi, pdf or html
  --force                 Force overwrite of an existing file
  -ss, --supported-sites  List of supported sites
  -d,  --debug            Show the log in the console for debugging
  --changelog             Save the changelog file
  --debug-log             Save the logfile for debugging
  --config-init           Initialize the CLI config files
  --config-info           Show the CLI config info
  --version               Display version & quit
  --help                  Show this message and exit.
```

# Default Configuration

- The fanfiction will be downloaded in epub format. To change it, use `--format` followed by the format. Multiple formats can be selected by separating them by commas.
- The fanfiction will be downloaded in the current directory. To change it, use `-o` followed by the path to the directory.
- Failed downloads will be saved in the `err.log` file in the current directory.

Check `fichub_cli --help` for more info.

# Example

- To download using an URL

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

- To download multiple formats

```
fichub_cli -u "https://www.fanfiction.net/s/13720575/1/A-Cadmean-Victory-Remastered" --format epub,mobi
```

- To generate a changelog of the download

```
fichub_cli -i urls.txt --changelog
```

---

**NOTE**

- `--out-dir` or `-o` can be used in all the above commands to select an output directory.

- Using the `--config-init` flag, users can re-initialize/overwrite the config files to default.

- Using the `--config-info` flag, users can get all the info about the config file and its settings.

---

# Configuration

- Users can configure centain things like `db_up_time_format`, `fic_up_time_format`, `delete_output_log` & `filename_format` by editing the `config.json` file in the app directory.

- Filename format props (case-sensitive):
  `author, fichubAuthorId, authorId, chapters, created, fichubId, genres, id, language, rated, fandom, status, updated, title`

  Example:

  ```
  "filename_format": "[title] by [author]"
  ```

- To locate the config file, run `fichub_cli --config-info` and open the `config.json` file in an editor and make the necessary changes.

## Notes

- For `db_up_time_format` & `fic_up_time_format`:
  - Only use valid datetime formats
- For `delete_output_log`:
  - Default is blank so it will always prompt for confirmation
  - Set it to `"false"` to always keep the file
  - Set it to `"true"` to always delete the file

# Plugin Support

Read the [wiki](https://github.com/FicHub/fichub-cli/wiki/Plugins) for more info.

# Helper Scripts

Helper scripts can be found [here](https://github.com/fichub-cli-contrib/helper-scripts/). They can add small functionalities to the CLI without needing to create full-fledged plugins.

# Links

- [Github Wiki](https://github.com/FicHub/fichub-cli/wiki/)
- [Github Plugins Repo](https://github.com/fichub-cli-contrib/)
- [Official Discord Server](https://discord.gg/sByBAhX)

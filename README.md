![](https://img.shields.io/github/actions/workflow/status/BenPortner/pydbk/install-lint-test.yml?label=tests) ![](https://img.shields.io/github/actions/workflow/status/BenPortner/pydbk/release-pypi.yml?label=release) ![](https://img.shields.io/github/license/BenPortner/pydbk) ![](https://img.shields.io/pypi/pyversions/pydbk)

# Pydbk: A Python tool to extract .dbk archives

Pydbk consists of a python module `pydbk.py` and a command line tool `pydbk_cli.py`.

- [Installation](#Installation)
- [Usage](#Usage)
- [What is a .dbk file?](#what-is-a-dbk-file)

## Installation

Install using pip:

```sh
pip install pydbk
```
## Usage

Extract a .dbk archive:

```sh
pydbk path/to/file.dbk destination/dir
```

If no destination is specified, pydbk will create a directory `./extracted`:

```sh
pydbk path/to/file.dbk
```

Get help:

```sh
pydbk --help
```

```sh
usage: pydbk_cli.py [-h] [-v] [-c] [-d] source [destination]

Pydbk: A Python tool to extract .dbk archives.

positional arguments:
  source         source file to extract files from (.dbk)
  destination    destination directory to extract files to

options:
  -h, --help     show this help message and exit
  -v, --verbose  verbose mode (print detailed output)
  -c, --check    check if .dbk archive is complete
  -d, --dry-run  run program without writing files to the destination
```

## What is a .dbk file?

> A DBK file is a mobile phone backup file created by Sony Ericsson PC Suite, a program used to manage Sony Ericsson mobile phones. It contains multiple Zip-compression files that store various phone information such as the names and phone numbers of contacts. DBK files are used to back up phone information in the event that the phone is lost or broken. ([fileinfo.com](https://fileinfo.com/extension/dbk))
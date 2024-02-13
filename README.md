<p align="center">
  <img src="https://i.imgur.com/NcjxDgn.png" width="240" alt="Doky Logo">
  <br>
  <b>Doky Tool</b>
  <br>
  A intuitive CLI tool and Python Library for manage your Docker-In-Docker instances<br>
  from <a href="https://labs.play-with-docker.com/">Play With Docker</a>
  <br><br>
  <a href="test"><b>Any questions? Open an issue!</b></a>
</p>

<p align="center">
  <a href="LICENSE.md"><img src="https://img.shields.io/github/license/d3cryptofc/doky?color=1e90ff"></a>
  <a href="https://pypi.org/project/doky/"><img src="https://img.shields.io/pypi/dm/doky?color=1e90ff"></a>
  <a href="https://pypi.org/project/doky/"><img src="https://img.shields.io/pypi/v/doky?color=1e90ff"></a>
  <a href="https://d3cryptofc.github.io/Doky"><img src="https://img.shields.io/badge/Documentation-1e90ff"></a>
</p>



## Usage

```
$ doky

Usage: doky [OPTIONS] COMMAND [ARGS]...

  Doky is a intuitive library and CLI tool for manage your Docker-In-Docker
  instances from Play With Docker Lab

Options:
  -h, --help  Show this message and exit.

Commands:
  version  Show current app version.

  User authentication management:
    auth me                       Show your authentication user informations.
    auth oauth [--provider NAME]  Request for an OAuth URL to authenticate with a provider.
    auth providers                List available OAuth providers to request an OAuth URL.
    auth token <TOKEN>            Set the authentication session ID.
```

## Installation

Will you only use the CLI? Then install with **pipx**:

```bash
$ pipx install doky
```

Will you use both? Then you can install with **pip/poetry/etc**:

```bash
$ pip install doky
$ poetry add doky
```

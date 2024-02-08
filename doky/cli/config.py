import functools
from pathlib import Path
from typing import Dict
import yaml

from appdirs import user_config_dir
import click
from doky import metadatas
import rich
import rich.traceback

# Getting rich console object.
console = rich.get_console()

# Installing rich traceback handler.
rich.traceback.install()

# Getting the app user configuration directory path.
doky_config_dir_path = Path(user_config_dir(appname='doky'))

# Creating a path to app config file.
doky_config_path = doky_config_dir_path / 'config.yml'


def write_config(data: Dict) -> None:
    """
    Writes data to app configuration.
    """
    # Opening the configuration file as write-mode.
    with open(str(doky_config_path), 'w') as file:
        # Writing data to the configuration file as YML.
        yaml.safe_dump(data, file)


def read_config() -> Dict:
    """
    Reads data from app configuration.
    """
    # Opening the configuration file as read-mode.
    with open(str(doky_config_path), 'r') as file:
        # Reading data from configuration file as dictionary.
        return yaml.safe_load(file)


def prepare_config_file(function):
    """
    Decorator to prepare the app configuration file.
    """
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        # Creating app configuration directory if it doesn't exist.
        doky_config_dir_path.mkdir(parents=True, exist_ok=True)

        # If app configuration file doesn´t exist or it's empty.
        if not doky_config_path.exists() or not read_config():
            # Writing a default configuration.
            write_config(dict(
                auth_token=''
            ))

        # Calling the decorated function.
        return function(*args, **kwargs)

    # Returning the wrapper.
    return decorator


@click.group(
    help=metadatas.DESCRIPTION,
    context_settings=dict(help_option_names=('-h', '--help'))
)
def main_group():
    """
    Main group of commands.
    """


@main_group.command(help='Show current app version.')
def version():
    """
    Command that shows the current app version.
    """
    # Showing the current ap version.
    click.echo(f'Version {metadatas.VERSION}')

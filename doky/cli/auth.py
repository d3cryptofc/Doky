"""
COMMANDS TO DO:

[X] doky auth me
    Show your authentication user informations.

[X] doky auth oauth [--provider NAME]
    Request for an OAuth URL to authenticate with a provider.

[X] doky auth providers
    List available OAuth providers to request an OAuth URL.

[X] doky auth token <TOKEN>
    Set the authentication session ID.
"""

from http import HTTPStatus

import click
import httpx
import doky

from .config import (
    console,
    main_group,
    prepare_config_file,
    read_config,
    write_config
)


@main_group.group('auth', help='User authentication management.')
def auth_group():
    """
    User authentication management command group.
    """


@auth_group.command(
    help='List available OAuth providers to request an OAuth URL.'
)
def providers():
    """
    Command that lists available OAuth providers to request
    an OAuth URL
    """
    # Showing request in progress.
    with console.status('Getting available OAuth providers, please wait.'):
        # Getting OAuth providers list.
        providers = doky.AuthSession.get_providers()

    # Building successful text.
    text = (
        '\n[b]Success! These are the available OAuth providers:[/]\n\n'
        + '\n'.join(f'[b cyan]-[/] {provider}' for provider in providers)
        + '\n'
    )

    # Showing successful text.
    console.print(text)


@auth_group.command(
    help='Request for an OAuth URL to authenticate with a provider.'
)
@click.option('--provider', default='docker', help='The OAuth provider name.')
def oauth(provider: str):
    """
    That command requests for an OAuth URL to authenticate with
    a provider
    """
    # Showing request in progress.
    with console.status('Requesting for an OAuth URL, please wait.'):
        # Getting OAuth URL.
        oauth_url = doky.AuthSession.request_oauth_url(provider)

    # Building successful text.
    text = (
        '\n[b]The OAuth URL was obtained successfully![/]\n\n'
        f'{oauth_url}\n\n'
        '[b]Follow these steps:[/]\n\n'
        '  1. Open the OAuth URL in your browser to authenticate.\n'
        '  2. When authenticated, copy the cookie value named \'id\', '
        'you may need to use DevTools.\n'
        '  3. Set the token typing in your terminal: '
        '[b]doky auth token[/b] <TOKEN>\n'
    )

    # Showing successful text.
    console.print(text)


@auth_group.command(help='Show your authentication user informations.')
@prepare_config_file
def me():
    """
    Command that shows your authentication user informations
    """
    # Reading data from app configuration.
    config = read_config()

    # Setting broken session message error.
    message_broken_session = (
        '\n[b red]It looks like you are not logged in, perhaps '
        'your session has expired or it was a typo :([/]\n'
    )

    # Setting request progress message.
    message_request_progress = (
        'Requesting for your authentication user informations, please wait.'
    )

    # Showing request in progress.
    with console.status(message_request_progress):
        # Trying to get authentication user informations.
        try:
            # Getting authentication user informations.
            me = doky.AuthSession(config.get('auth_token')).get_me()
        # Whether an HTTPStatusError exception was raised.
        except httpx.HTTPStatusError as exception:
            # If exception status code response is UNAUTRHORIZED.
            if exception.response.status_code == HTTPStatus.UNAUTHORIZED:
                # Showing broken session message.
                console.print(message_broken_session)
            else:
                # Raising same exception again.
                raise
            # Finishing the function.
            return

    # Showing successful text.
    console.print(
        '\n[b green]Congratulations! You are logged :)[/]\n'
        '\nThis is your authentication user informations:\n'
    )

    # Iterating authentication user informations.
    for key, value in me.items():
        # Showing authentication user information
        console.print(f'- [b]{key}[/]: {value}', highlight=False)

    # Showing breakline.
    print()


@auth_group.command(help='Set the authentication session ID.')
@click.argument('token')
@prepare_config_file
def token(token: str):
    """
    Command that sets the authentication session ID
    """
    # Reading data from app configuration.
    config = read_config()

    # Setting 'auth_token' configuration.
    config['auth_token'] = token

    # Saving data to app configuration.
    write_config(config)

    # Showing successful text.
    console.print(
        '\n[b blue]Token saved successfully![/]\n'
        'Try to run [b]doky auth me[/] to check your session.\n'
    )

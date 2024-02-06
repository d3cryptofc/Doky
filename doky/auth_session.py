from typing import List
from urllib.parse import quote as urlencode
from http import HTTPStatus

import httpx

from . import metadatas, errors


def create_http_client() -> httpx.Client:
    """
    A doky default HTTP Client Session creator.
    """
    return httpx.Client(
        # Setting the http session base URL.
        base_url='https://labs.play-with-docker.com',

        # Enabling HTTP 2 protocol version.
        http2=True,

        # Setting a http session default headers.
        headers={
            'User-Agent': 'Doky/' + metadatas.VERSION
        }
    )


class AuthSession:
    """
    Creates an object to manage the authentication session.

    Parameters:
        session_id:
            Your session ID from labs.play-with-docker.com
    """
    def __init__(self, session_id: str) -> None:
        # Checking if the `session_id` parameter is a string type.
        if not isinstance(session_id, str):
            raise errors.type_error(('session_id', session_id), str)

        # Creating a http client session.
        self._http_client = create_http_client()

        # Using the same cookie from navigator.
        self._http_client.cookies['id'] = session_id

    @staticmethod
    def get_providers() -> List[str]:
        """
        Static method that requests for a list of available providers.

        Returns:
            List of available providers.

        Return Example:
            ```python3
            ['docker']
            ```

        Raises:
            httpx.HTTPStatusError:
                Bad response HTTP status code.
        """
        # Creating a http client session and requesting for a providers list.
        request = create_http_client().get('/oauth/providers')

        try:
            # Raise if response status code is bad.
            request.raise_for_status()
        except httpx.HTTPStatusError as exception:
            # Adding an exception message note.
            exception.add_note('\n' + errors.OPEN_AN_ISSUE)
            # Raising the same exception again.
            raise

        # Returning providers list.
        return request.json()

    @staticmethod
    def request_oauth_url(provider: str = 'docker') -> str:
        """
        Static method that requests an OAuth URL to a provider.

        Parameters:
            provider:
                The OAuth available provider.

        Returns:
            The OAuth URL for authentication.

        Return Example:
            ```
            https://login.docker.com/authorize/?client_id=XXXXXX&nonce=XXXXXX&redirect_uri=XXXXXX&response_type=code&scope=XXXXXX&state=XXXXXX
            ```

        Raises:
            RuntimeError: Some unexpected error.
        """
        # Checking if the `provider` parameter is a string type.
        if not isinstance(provider, str):
            raise errors.type_error(('provider', provider), str)

        # Creating a http client session and requesting OAuth URL from the
        # provider specified.
        request = create_http_client().get(
            url='/oauth/providers/' + urlencode(provider) + '/login',
            follow_redirects=False
        )

        # Raise an exception if the response status code is not 302 FOUND.
        if request.status_code != HTTPStatus.FOUND:
            raise RuntimeError(
                'The authentication provider endpoint is not redirecting, '
                'perhaps it is broken.\n\n' + errors.OPEN_AN_ISSUE
            )

        # Getting OAuth URL from redirect header Location.
        oauth_url = request.headers.get('Location')

        # Raise an exception if the redirect header location doesn't exists.
        if not oauth_url:
            raise RuntimeError(
                'It appears that the server is not returning the '
                'authentication URL.\n\n' + errors.OPEN_AN_ISSUE
            )

        # Returning the OAuth URL.
        return oauth_url

    def get_me(self) -> dict:
        """
        Bound method that requests for current user session informations.

        Returns:
            Current user session informations.

        Return Example:
            ```python3
            {
                'id': 'XXXXXX',
                'name': 'd3cryptofc',
                'provider_user_id': '1000XXX',
                'avatar': 'https://avatars.io/twitter/d3cryptofc',
                'provider': 'docker',
                'email': 'd3cryptofc@gmail.com',
                'banned': False
            }
            ```

        Raises:
            httpx.HTTPStatusError:
                Bad response HTTP status code.
        """
        # Requesting for current user session informations.
        request = self._http_client.get('/users/me')

        try:
            # Raise if response status code is bad.
            request.raise_for_status()
        except httpx.HTTPStatusError as exception:
            # Adding an exception message note.
            exception.add_note('\n' + errors.OPEN_AN_ISSUE)
            # Raising the same exception again.
            raise

        # Returning the current user session informations.
        return request.json()

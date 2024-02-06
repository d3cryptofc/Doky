from typing import List
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


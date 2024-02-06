import httpx

from . import metadatas


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


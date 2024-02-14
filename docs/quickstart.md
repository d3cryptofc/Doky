# Quickstart

## User Session Authentication Manager

These are the user authentication features. [See more](reference.md#doky.AuthSession).


### Listing available OAuth providers

Want to know which OAuth authentication providers are available? Just do it:
!!! example
    === "CLI"
        **Usage:**

        ```bash
        $ doky auth providers
        ```
        
        **Result:**

        !!! note ""
            **Success! These are the available OAuth providers:**

            **-** docker
    === "Python"
        **Code:**

        ```{.python linenums=1}
        from doky import AuthSession
        print(AuthSession.get_providers())
        ```

        **Result:**

        ```python
        ['docker']
        ```

        [See more](reference.md#doky.AuthSession.get_providers)


### Requesting for an OAuth URL

Save time by generating the authentication URL, default provider is docker:

!!! example
    === "CLI"
        **Usage:**

        ```bash
        $ doky auth oauth [--provider NAME]
        ```

        **Result:**

        !!! note ""
            **The OAuth URL was obtained successfully!**

            <u style='word-wrap: break-word'>https://login.docker.com/authorize/?client_id=XXXXXX&nonce=XXXXXX&redirect_uri=XXXXXX&response_type=code&scope=XXXXXX&state=XXXXXX</u>

            **Follow these steps:**

            1. Open the OAuth URL in your browser to authenticate.
            2. When authenticated, copy the cookie value named `id`, you may need to use DevTools.
            3. Set the token typing in your terminal: doky token <TOKEN>

    === "Python"
        **Code:**

        ```{.python linenums=1}
        from doky import AuthSession
        print(AuthSession.request_oauth_url())
        ```

        **Result:**

        ```python
        'https://login.docker.com/authorize/?client_id=XXXXXX&nonce=XXXXXX&redirect_uri=XXXXXX&response_type=code&scope=XXXXXX&state=XXXXXX'
        ```

        [See more](reference.md#doky.AuthSession.request_oauth_url)

!!! note "It's not yet possible to automate authentication :("

    Unfortunately, no way was found to wait for authentication to complete or even obtain the necessary authentication credentials so that it could be fully automated.

    If you find a way that isn't as complicated as setting up a proxy, using webdrivers or browser extensions, **feel free to open a pull request or an issue to discuss it**.


### Configuring authentication token and getting authentication information

After authenticating to [Play With Docker](https://labs.play-with-docker.com/), copy the cookie value named `id` and insert it below:

!!! example
    === "CLI"
        **Usage:**

        ```bash
        $ doky auth token <YOUR-TOKEN-HERE> && doky auth me
        ```

        **Result:**

        !!! note ""
            **Token saved successfully!**

            Try to run **doky auth me** to check your session.
            <br>
            <br>
            **Congratulations! You are logged :)**

            This is your authentication user informations:

            **- id:** XXXXXX<br>
            **- name:** d3cryptofc<br>
            **- provider_user_id:** 1000XXX<br>
            **- avatar:** https://avatars.io/twitter/d3cryptofc<br>
            **- provider:** docker<br>
            **- email:** d3cryptofc@gmail.com<br>
            **- banned:** False
    === "Python"
        **Code:**

        ```{.python linenums=1}
        from doky import AuthSession
        auth = AuthSession('<YOUR SESSION ID HERE>')
        ```

        ... but this alone does not guarantee that you are logged in, to find out, do this:

        ```{.python linenums=1}
        from httpx import HTTPStatusError

        try:
            print(auth.get_me())
        except HTTPStatusError as exception:
            # Checking if status code response is not 401 Unauthorized.
            if exception.response.status_code != 401:
                # Raising same exception again.
                raise

            # Else, authentication definitely failed.
            print("Authentication failed :(")
        ```

        **Result:**

        ```python
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

        [See more](reference.md#doky.AuthSession.get_me)


from typing import Tuple, Any

from . import metadatas


# Defining variable for 'Open An Issue' message error.
OPEN_AN_ISSUE = (
    'Please open an issue in the project\'s github repository:\n\n'
    + metadatas.REPOSITORY_ISSUE_URL
)


def type_error(parameter: Tuple[str, Any], expected_type: type) -> TypeError:
    """
    Create a TypeError exception containing a custom message error
    for parameters.

    Parameters:
        parameter:
            A 2-tuple in order: parameter name, parameter value.

        expected_type:
            The expected type of data.

    Returns:
        The custom message error exception.
    """
    # Unpacking parameter name and parameter value.
    name, value = parameter

    # Returning the custom message type error object.
    return TypeError(
        'Parameter `{}` must be type `{}`, not `{}`'.format(
            name,
            expected_type,
            type(value)
        )
    )

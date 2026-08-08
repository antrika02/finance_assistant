from tests.auth import auth_headers


def authenticated_headers(client):
    """
    Returns Authorization headers for an authenticated user.
    """

    return auth_headers(client)

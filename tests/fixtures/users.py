from tests.auth import auth_headers


class AuthenticatedUser:
    """
    Represents an authenticated test user.
    """

    def __init__(self, headers):
        self.headers = headers


def create_authenticated_user(client, **kwargs):
    """
    Creates a brand-new authenticated user.
    """

    headers = auth_headers(client, **kwargs)

    return AuthenticatedUser(headers)
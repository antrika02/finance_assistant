from tests.auth import create_category


def create_user_category(
    client,
    user,
    **kwargs,
):
    """
    Creates a category belonging to a user.
    """

    return create_category(
        client,
        user.headers,
        **kwargs,
    )
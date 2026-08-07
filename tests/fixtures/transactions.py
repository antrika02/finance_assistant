from tests.auth import create_transaction


def create_user_transaction(
    client,
    user,
    category_id,
    **kwargs,
):
    """
    Creates a transaction for a user.
    """

    return create_transaction(
        client,
        user.headers,
        category_id,
        **kwargs,
    )
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App
    from ...graphql.core import SaleorContext


def get_user_or_app_from_context(context: "SaleorContext") -> "App | User | None":
    """Return the app or user that made the request.

    The order is important: the app can be None, but if the user is None, the
    request is treated as anonymous.
    """
    return context.app or context.user

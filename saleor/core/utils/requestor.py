from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App


class RequestorContext(Protocol):
    """Request context carrying the authenticated app and/or user."""

    app: "App | None"
    user: "User | None"


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    """Return the requestor of the context, preferring the app over the user.

    The order is important: `app` can be None, while a missing user is passed as
    anonymous.
    """
    return context.app or context.user

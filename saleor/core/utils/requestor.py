from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App


class RequestorContext(Protocol):
    """Request context that carries the authenticated app and user."""

    app: "App | None"
    user: "User | None"


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    """Return the app or user that made the request.

    The app takes precedence over the user, as both may be set on the context.
    """
    return context.app or context.user

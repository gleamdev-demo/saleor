from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App


class RequestorContext(Protocol):
    app: "App | None"
    user: "User | None"


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    """Return the app or user making the request.

    App takes precedence; the user can be None for anonymous requests.
    """
    return context.app or context.user

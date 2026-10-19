from typing import TYPE_CHECKING, Optional, Protocol

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App


class RequestorContext(Protocol):
    app: Optional["App"]
    user: Optional["User"]


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    """Return the app or user that performs the request.

    App takes precedence; it can be None while the user is passed as anonymous.
    """
    return context.app or context.user

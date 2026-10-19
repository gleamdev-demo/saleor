from typing import TYPE_CHECKING, Optional, Protocol, Union

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App


class RequestorContext(Protocol):
    app: Optional["App"]
    user: Optional["User"]


def get_user_or_app_from_context(
    context: RequestorContext,
) -> Union["App", "User", None]:
    """Return the app or user that performs the request.

    The order is important: app can be None, but if user is None the request is
    treated as anonymous.
    """
    return context.app or context.user

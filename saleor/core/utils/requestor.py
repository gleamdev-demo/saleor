from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ...account.models import User
    from ...app.models import App


class RequestorContext(Protocol):
    app: "App | None"
    user: "User | None"


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    # order is important
    # app can be None but user if None then is passed as anonymous
    return context.app or context.user

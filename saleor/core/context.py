from typing import TYPE_CHECKING, Protocol

from promise import Promise

if TYPE_CHECKING:
    from ..account.models import User
    from ..app.models import App


class RequestorContext(Protocol):
    app: "App | None"
    user: "User | None"


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    # order is important
    # app can be None but user if None then is passed as anonymous
    return context.app or context.user


def with_promise_context(func):
    """Execute function within Promise context.

    Allow to use dataloaders inside the function.
    """

    def wrapper(*args, **kwargs):
        def promise_executor(_):
            return func(*args, **kwargs)

        # Create promise chain
        promise = Promise.resolve(None).then(promise_executor)
        return promise.get()

    return wrapper

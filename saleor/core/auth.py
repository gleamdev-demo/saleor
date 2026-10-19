from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

if TYPE_CHECKING:
    from ..account.models import User
    from ..app.models import App

SALEOR_AUTH_HEADER = "HTTP_AUTHORIZATION_BEARER"
DEFAULT_AUTH_HEADER = "HTTP_AUTHORIZATION"
AUTH_HEADER_PREFIXES = ["JWT", "BEARER"]


class RequestorContext(Protocol):
    """Request context carrying the authenticated app and user."""

    @property
    def app(self) -> "App | None": ...

    @property
    def user(self) -> "User | None": ...


def get_token_from_request(request: HttpRequest) -> str | None:
    auth_token: str | None = request.META.get(SALEOR_AUTH_HEADER)

    if not auth_token:
        auth = request.META.get(DEFAULT_AUTH_HEADER, "").split(maxsplit=1)

        if len(auth) == 2 and auth[0].upper() in AUTH_HEADER_PREFIXES:
            auth_token = auth[1]
    return auth_token


def get_user_or_app_from_context(context: RequestorContext) -> "App | User | None":
    """Return the app or user that performs the request.

    App takes precedence over user. If there is no app, the user is returned;
    it is None for an anonymous request.
    """
    return context.app or context.user

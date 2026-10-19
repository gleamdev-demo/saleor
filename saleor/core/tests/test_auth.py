from types import SimpleNamespace

import pytest

from ..auth import get_user_or_app_from_context


@pytest.mark.parametrize(
    ("_case", "app_fixture", "user_fixture", "expected_fixture"),
    [
        ("app takes precedence over user", "app", "staff_user", "app"),
        ("app without user", "app", None, "app"),
        ("user without app", None, "staff_user", "staff_user"),
    ],
)
def test_get_user_or_app_from_context(
    request, _case, app_fixture, user_fixture, expected_fixture
):
    # given
    app = request.getfixturevalue(app_fixture) if app_fixture else None
    user = request.getfixturevalue(user_fixture) if user_fixture else None
    context = SimpleNamespace(app=app, user=user)

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor == request.getfixturevalue(expected_fixture)


def test_get_user_or_app_from_context_anonymous():
    # given
    context = SimpleNamespace(app=None, user=None)

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor is None

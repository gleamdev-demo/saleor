from types import SimpleNamespace

import pytest

from ..requestor import get_user_or_app_from_context


@pytest.mark.parametrize(
    ("_case", "with_app", "with_user"),
    [
        ("app_only", True, False),
        ("app_takes_precedence_over_user", True, True),
    ],
)
def test_returns_app(_case, with_app, with_user, app, staff_user):
    # given
    context = SimpleNamespace(
        app=app if with_app else None, user=staff_user if with_user else None
    )

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor == app


def test_returns_user_when_no_app(staff_user):
    # given
    context = SimpleNamespace(app=None, user=staff_user)

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor == staff_user


def test_returns_none_when_no_app_and_no_user():
    # given
    context = SimpleNamespace(app=None, user=None)

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor is None

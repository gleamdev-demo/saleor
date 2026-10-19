from types import SimpleNamespace

from ..context import get_user_or_app_from_context


def test_returns_app_when_app_and_user_set(app, staff_user):
    # given
    context = SimpleNamespace(app=app, user=staff_user)

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


def test_returns_none_for_anonymous_request():
    # given
    context = SimpleNamespace(app=None, user=None)

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor is None

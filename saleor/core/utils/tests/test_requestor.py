from types import SimpleNamespace

import pytest

from ..requestor import get_user_or_app_from_context


@pytest.mark.parametrize(
    ("_case", "has_app", "has_user", "expected"),
    [
        ("app_takes_precedence", True, True, "app"),
        ("app_only", True, False, "app"),
        ("user_only", False, True, "user"),
        ("anonymous", False, False, None),
    ],
)
def test_get_user_or_app_from_context(
    _case, has_app, has_user, expected, app, staff_user
):
    # given
    context = SimpleNamespace(
        app=app if has_app else None, user=staff_user if has_user else None
    )
    expected_requestor = {"app": app, "user": staff_user, None: None}[expected]

    # when
    requestor = get_user_or_app_from_context(context)

    # then
    assert requestor == expected_requestor

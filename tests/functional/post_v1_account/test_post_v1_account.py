import pytest

from checkers.context_manager import check_status_code_http
from checkers.post_v1_account import PostV1Account
from generic.utilites.rand_utils import (generate_user_name,
    generate_password, get_random_string, random_string)


def test_post_v1_account(account_mh, prepare_user):
    account_mh.account.account_api.register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_mh.activate_user(
        login=prepare_user.login
    )
    response = account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )
    PostV1Account.check_response_values(response, starts_with_='TestName_')


@pytest.mark.parametrize('login, email, password, status_code, check', [
    (generate_user_name(), get_random_string() + '@mail.ru', random_string(1, 5), 400, {"Password": ["Short"]}),
    (random_string(1, 1), get_random_string() + '@mail.ru', generate_password(), 400, {"Login": ["Short"]}),
    (generate_user_name(), 'jack69@', generate_password(), 400, {"Email": ["Invalid"]}),
    (generate_user_name(), 'jack69makarevich', generate_password(), 400, {"Email": ["Invalid"]})
])
def test_post_v1_account_negative(
        account_mh,
        login,
        email,
        password,
        status_code,
        check
):
    with check_status_code_http(status_code, 'Validation failed', check):
        account_mh.account.account_api.register_new_user(
            login=login,
            password=password,
            email=email
        )



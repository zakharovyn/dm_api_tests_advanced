from datetime import datetime

import pytest
from hamcrest import (assert_that, has_property, starts_with, all_of,
    instance_of, has_properties, equal_to)

from generic.utilites.context_manager import check_status_code_http
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
    assert_that(response, all_of(
        has_property('resource', has_property(
            'login', starts_with('TestName_'))
        ),
        has_property('resource', has_property(
            'registration', instance_of(datetime))
        ),
        has_property(
            'resource', has_properties(
                {
                    'rating': has_properties(
                        {
                            'enabled': equal_to(True),
                            'quality': equal_to(0),
                            'quantity': equal_to(0)
                        }
                    )
                }
            )
        )
    ))


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



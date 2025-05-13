from datetime import datetime

from hamcrest import (assert_that, has_property, starts_with, all_of,
    instance_of, has_properties, equal_to)

from generic.utilites.context_manager import check_status_code_http


def test_get_v1_account_auth(auth_account):
    with check_status_code_http():
        response = auth_account.service.account.account_api.get_current_user_info()

    assert_that(response, all_of(
        has_property('resource', has_property(
            'login', starts_with('test_user_advanced_'))
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


def test_get_v1_account_no_auth(dm_account):
    with check_status_code_http(401, 'User must be authenticated'):
        dm_account.account_api.get_current_user_info()

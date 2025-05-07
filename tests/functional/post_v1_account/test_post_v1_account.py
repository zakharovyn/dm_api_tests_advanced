from datetime import datetime

from hamcrest import (assert_that, has_property, starts_with, all_of,
    instance_of, has_properties, equal_to)


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

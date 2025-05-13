from datetime import datetime

from hamcrest import (assert_that, has_property, starts_with, all_of,
    instance_of, has_properties, equal_to)
import assertpy

from checkers.context_manager import check_status_code_http
from services.dm_api_account.models.user_envelope_model import UserRole


def test_get_v1_account_auth(auth_account):
    with check_status_code_http():
        response = auth_account.service.account.account_api.get_current_user_info()

    # Мягкие проверки с помощью либы assertpy
    with assertpy.soft_assertions():
        assertpy.assert_that(response.resource.login).starts_with('test_user_advanced_')
        assertpy.assert_that(response.resource.online).is_instance_of(datetime)
        assertpy.assert_that(response.resource.roles).contains(UserRole.guest, UserRole.player)

    # Проверки с помощью либы hamcrest
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

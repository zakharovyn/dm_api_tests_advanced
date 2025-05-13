from datetime import datetime

import assertpy
from hamcrest import (assert_that, all_of, has_property, instance_of,
    has_properties, equal_to, starts_with)

from services.dm_api_account.models.user_envelope_model import UserRole


class GetV1Account:
    @classmethod
    def check_response_values(cls, response):
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

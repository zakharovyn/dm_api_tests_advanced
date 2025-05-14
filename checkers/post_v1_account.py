from datetime import datetime

from hamcrest import (assert_that, starts_with, all_of, has_property,
    instance_of, has_properties, equal_to)


class PostV1Account:
    @classmethod
    def check_response_values(cls, response, starts_with_: str):
        today = datetime.now().strftime('%Y-%m-%d')
        assert_that(response, all_of(
            has_property('resource', has_property(
                'login', starts_with(starts_with_))
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
        assert_that(str(response.resource.registration), starts_with(today))

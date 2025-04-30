from requests import Response

from generic.utilites.validate_utils import (
    validate_request_json,
    validate_status_code,
    validate_model_response,
)
from restclient.client import RestClient
from services.dm_api_account.models import *


class AccountApi:

    def __init__(self, client: RestClient):
        self.client = client

    def _post_v1_account(
            self,
            json: Registration,
            status_code: int = 201,
            **kwargs
    ) -> Response:
        """
        Register new user

        :param status_code: статус код ответа сервера
        :param json Registration
        :return:
        """
        response = self.client.post(
            path=f"/v1/account",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)

        return response

    def _get_v1_account(
            self,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserDetailsEnvelope:
        """
        Get current user

        :return:
        """
        response = self.client.get(
            path=f"/v1/account",
            **kwargs
        )
        validate_status_code(response, status_code)

        response = validate_model_response(
            response=response,
            obj_model=UserDetailsEnvelope,
            status_code=status_code
        )

        return response

    def _put_v1_account_token(
            self,
            token: str,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Activate registered user

        :return:
        """
        response = self.client.put(
            path=f"/v1/account/{token}",
            **kwargs
        )
        print(response.json())
        validate_status_code(response, status_code)

        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            status_code=status_code
        )

        return response

    def _post_v1_account_password(
            self,
            json: ResetPassword,
            status_code: int = 201,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Reset registered user password

        :return:
        """
        response = self.client.post(
            path=f"/v1/account/password",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)

        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            status_code=status_code
        )

        return response

    def _put_v1_account_password(
            self,
            json: ChangePassword,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Change registered user password

        :return:
        """
        response = self.client.put(
            path=f"/v1/account/password",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)

        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            status_code=status_code
        )

        return response

    def _put_v1_account_email(
            self,
            json: ChangeEmail,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Change registered user email

        :return:
        """
        response = self.client.put(
            path=f"/v1/account/email",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)

        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            status_code=status_code
        )

        return response

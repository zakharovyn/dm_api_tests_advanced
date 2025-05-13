from requests import Response

from logging import getLogger

from generic.utilites.data_utils import get_json
from generic.utilites.validate_utils import (
    validate_request_json,
    validate_status_code,
    validate_model_response,
)
from restclient.client import RestClient
from services.dm_api_account.models import *

logger = getLogger(__name__)


class AccountApi:

    def __init__(self, client: RestClient):
        self.client = client

    def _post_v1_account(
            self,
            json: Registration,
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
        return response

    def _get_v1_account(
            self,
            validate_response: bool = True,
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
        response = validate_model_response(
            response=response,
            obj_model=UserDetailsEnvelope,
            validate_response=validate_response
        )
        return response

    def _put_v1_account_token(
            self,
            token: str,
            validate_response: bool = True,
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
        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            validate_response=validate_response
        )
        return response

    def _post_v1_account_password(
            self,
            json: ResetPassword,
            validate_response: bool = True,
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
        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            validate_response=validate_response
        )
        return response

    def _put_v1_account_password(
            self,
            json: ChangePassword,
            validate_response: bool = True,
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
        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            validate_response=validate_response
        )
        return response

    def _put_v1_account_email(
            self,
            json: ChangeEmail,
            validate_response: bool = True,
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
        response = validate_model_response(
            response=response,
            obj_model=UserEnvelope,
            validate_response=validate_response
        )
        return response

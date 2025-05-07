from requests import Response

from services.dm_api_account.models import UserEnvelope, LoginCredentials
from generic.utilites.validate_utils import (
    validate_request_json,
    validate_status_code,
)
from restclient.client import RestClient


class LoginApi:
    def __init__(self, client: RestClient):
        self.client = client

    def _post_v1_account_login(
            self,
            json: LoginCredentials,
            status_code: int = 200,
            need_json: bool = True,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Authenticate via credentials
        :return:
        """
        response = self.client.post(
            path=f"/v1/account/login",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)

        if response.status_code == 200:
            UserEnvelope(**response.json())

        if need_json is True:
            return response
        else:
            return UserEnvelope(**response.json())

    def _delete_v1_account_login(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        """
        Logout as current user
        :return:
        """
        response = self.client.delete(
            path=f"/v1/account/login",
            **kwargs
        )
        validate_status_code(response, status_code)

        return response

    def _delete_v1_account_login_all(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        """
        Logout from every device
        :return:
        """
        response = self.client.delete(
            path=f"/v1/account/login/all",
            **kwargs
        )
        validate_status_code(response, status_code)

        return response

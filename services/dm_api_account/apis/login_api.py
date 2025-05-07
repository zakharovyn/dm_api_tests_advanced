from requests import Response

from logging import getLogger

from generic.utilites.data_utils import get_json
from services.dm_api_account.models import UserEnvelope, LoginCredentials
from generic.utilites.validate_utils import (
    validate_request_json,
    validate_status_code,
)
from restclient.client import RestClient

logger = getLogger(__name__)


class LoginApi:
    def __init__(self, client: RestClient):
        self.client = client

    def _post_v1_account_login(
            self,
            json: LoginCredentials,
            status_code: int = 200,
            validate_response: bool = True,
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

        if response.status_code == 200:
            logger.info(
                f'DMApiAccount. Логин пользователя {json.login} с паролем '
                f'{json.password}'
            )
        else:
            logger.error(
                f'DMApiAccount. Ошибка при логине пользователя {json.login} '
                f'с паролем {json.password}'
                f'Статус код ответа: {response.status_code}. '
                f'Тело ответа: {get_json(response)}'
            )

        validate_status_code(response, status_code)

        if response.status_code == 200:
            UserEnvelope(**response.json())

        if validate_response:
            return UserEnvelope(**response.json())
        else:
            return response

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

        if response.status_code == 201:
            logger.info(f'DMApiAccount. Разлогин текущего пользователя')
        else:
            logger.error(
                f'DMApiAccount. Ошибка при разлогине текущего пользователя. '
                f'Статус код ответа: {response.status_code}. '
                f'Тело ответа: {get_json(response)}'
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

        if response.status_code == 201:
            logger.info(
                f'DMApiAccount. Разлогин текущего пользователя со всех '
                f'устройств'
            )
        else:
            logger.error(
                f'DMApiAccount. Ошибка при разлогине текущего пользователя со '
                f'всех устройств. '
                f'Статус код ответа: {response.status_code}. '
                f'Тело ответа: {get_json(response)}'
            )

        validate_status_code(response, status_code)

        return response

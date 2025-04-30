import json
import time

from restclient.client import RestClient


class MailhogApi(RestClient):

    def get_api_v2_messages(
            self,
            limit: int = 10
    ):
        """
        Get users emails
        :return:
        """
        params = {
            'limit': limit
        }
        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response

    def get_token_by_login(
            self,
            login: str,
            attempt: int = 5,
            reset_password: bool = False
    ):
        """
        Getting a token by login
        :param attempt:
        :param reset_password:
        :param login: login
        :return: token
        """
        if attempt == 0:
            raise AssertionError(
                f'Не удалось получить письмо с логином {login}'
            )

        emails = self.get_api_v2_messages(limit=15).json()['items']

        for email in emails:
            user_data = json.loads(email['Content']['Body'])
            if login == user_data.get('Login') and reset_password is False:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                return token
            elif login == user_data.get('Login') and reset_password is True:
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
                return token

        time.sleep(2)
        return self.get_token_by_login(login=login, attempt=attempt - 1)

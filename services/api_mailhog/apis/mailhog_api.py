import json
import time

from restclient.client import RestClient


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена номер {count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError(
                    'Превышено количество попыток получения активационного токена'
                )
            if token:
                return token
            time.sleep(1)

    return wrapper


class MailhogApi:

    def __init__(self, client: RestClient, headers: dict = None):
        self.client = client

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
        response = self.client.get(
            path=f'/api/v2/messages',
            params=params
        )
        return response

    def get_token_from_last_email(
            self,
            reset_password: bool = False
    ) -> str:
        """
        Get user activation token from last email
        :return:
        """
        time.sleep(2)
        email = self.get_api_v2_messages(limit=1).json()
        if reset_password is False:
            token_url = json.loads(email['items'][0]['Content']['Body'])[
                'ConfirmationLinkUrl']
        else:
            token_url = json.loads(email['items'][0]['Content']['Body'])[
                'ConfirmationLinkUri']

        token = token_url.split('/')[-1]

        return token

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

    def delete_all_messages(self):
        response = self.client.delete(path='/api/v1/messages')
        return response

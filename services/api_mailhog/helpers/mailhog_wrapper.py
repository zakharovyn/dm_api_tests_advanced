import json
import time
from logging import getLogger

from services.api_mailhog.apis.mailhog_api import MailhogApi

logger = getLogger(__name__)


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            logger.info(f'Попытка получения токена номер {count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError(
                    'Превышено количество попыток получения активационного '
                    'токена'
                )
            if token:
                return token
            time.sleep(1)

    return wrapper


class MailhogWrapper(MailhogApi):
    def get_messages(self, limit: int):
        """Получить последнние письма"""
        params = {
            'limit': limit
        }
        response = self.get_api_v2_messages(params=params)
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
        email = self.get_messages(limit=1).json()
        if reset_password is False:
            token_url = json.loads(email['items'][0]['Content']['Body'])[
                'ConfirmationLinkUrl']
        else:
            token_url = json.loads(email['items'][0]['Content']['Body'])[
                'ConfirmationLinkUri']

        token = token_url.split('/')[-1]
        logger.info(
            f'Mailhog. Получение токена из последнего письма. Сброс пароля: '
            f'{reset_password}. Токен: {token}'
        )
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
        logger.info(
            f'Mailhog. Получение токена для пользователя по логину. Логин: '
            f'{login}. Текущая попытка: {attempt}. Сброс пароля: '
            f'{reset_password}'
        )
        if attempt == 0:
            raise AssertionError(
                f'Не удалось получить письмо с логином {login}'
            )

        emails = self.get_messages(limit=15).json()['items']

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
        logger.info('Mailhog. Удаление всех писем')
        return response

from logging import getLogger

from generic.utilites.data_utils import get_json
from restclient.client import RestClient

logger = getLogger(__name__)


class MailhogApi:

    def __init__(self, client: RestClient, headers: dict = None):
        self.client = client

    def get_api_v2_messages(
            self,
            params: dict
    ):
        """
        Get users emails
        :return:
        """
        response = self.client.get(
            path=f'/api/v2/messages',
            params=params
        )

        if response.status_code == 200:
            logger.info(
                f'Mailhog. Получение писем пользователя в количестве '
                f'{params.get('limit')} '
            )
        else:
            logger.error(
                f'Mailhog. Ошибка при получении писем пользователя в '
                f'количестве {params.get('limit')} '
                f'Статус код ответа: {response.status_code}. '
                f'Тело ответа: {get_json(response)}'
            )

        return response

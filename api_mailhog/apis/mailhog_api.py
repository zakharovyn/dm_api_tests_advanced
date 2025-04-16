import requests


class MailhogApi:
    def __init__(
            self,
            host: str = 'http://5.63.153.31:5025',
            headers: dict = None
    ):
        self.host = host
        self.headers = headers

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
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params,
            verify=False
        )
        return response

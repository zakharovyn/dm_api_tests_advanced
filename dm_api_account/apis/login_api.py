import requests


class LoginApi:
    def __init__(
            self,
            host: str = 'http://5.63.153.31:5051',
            headers: dict = None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account_login(
            self,
            json_data: dict
    ):
        """
        Authenticate via credentials.
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data,
            verify=False
        )
        return response

import requests


class AccountApi:
    def __init__(
            self,
            host: str = 'http://5.63.153.31:5051',
            headers: dict = None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data: dict
    ):
        """
        Register new user.
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data,
            verify=False
        )
        return response

    def put_v1_account_token(
            self,
            token: str
    ):
        """
        Activate registered user.
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain'
        }
        response = requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=headers,
            verify=False
        )
        return response

    def put_v1_account_email(
            self,
            json_data: dict
    ):
        """
        Change registered user email.
        :param json_data:
        :return:
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data,
            verify=False
        )
        return response

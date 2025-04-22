from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data: dict
    ):
        """
        Register new user.
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
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
        response = self.put(
            path=f'/v1/account/{token}',
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
        response = self.put(
            path=f'/v1/account/email',
            json=json_data,
            verify=False
        )
        return response

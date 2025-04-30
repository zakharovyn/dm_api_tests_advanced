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

    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :param kwargs:
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return response

    def post_v1_account_password(
            self,
            json_data: dict,
            **kwargs
    ):
        """
        Reset registered user password.
        :param json_data:
        :param kwargs:
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response

    def put_v1_account_password(
            self,
            json_data: dict,
            **kwargs
    ):
        """
        Change registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response

    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :return:
        """
        response = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :param kwargs:
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response

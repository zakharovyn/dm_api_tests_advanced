from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            json_data: dict
    ):
        """
        Authenticate via credentials.
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=json_data,
            verify=False
        )
        return response

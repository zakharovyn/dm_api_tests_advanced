from restclient.client import RestClient


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
        return response

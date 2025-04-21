from restclient.client import RestClient


class MailhogApi(RestClient):

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
        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response

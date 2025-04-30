from restclient.client import RestClient
from restclient.configuration import Configuration
from services.api_mailhog.apis.mailhog_api import MailhogApi
from services.dm_api_account.helpers.account import Account
from services.dm_api_account.helpers.login import Login


class DMApiAccountFacade:
    def __init__(
            self,
            configuration: Configuration,
            client: RestClient,
            mailhog: MailhogApi
    ):
        self.__client = client
        self.configuration = configuration
        self.account = Account(self, client=client)
        self.login = Login(self, client=client)
        self.mailhog = mailhog

    def set_headers(self, headers):
        self.__client.session.headers.update(headers)

    def get_headers(self):
        return self.__client.session.headers

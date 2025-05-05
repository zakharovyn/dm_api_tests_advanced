from restclient.client import RestClient
from restclient.configuration import Configuration
from services.dm_api_account.helpers.account_wrapper import AccountWrapper
from services.dm_api_account.helpers.login_wrapper import LoginWrapper


class DMApiAccountFacade:
    def __init__(
            self,
            configuration: Configuration,
            client: RestClient
    ):
        self.__client = client
        self.configuration = configuration
        self.account_api = AccountWrapper(client=self.__client)
        self.login_api = LoginWrapper(client=self.__client)

    def set_headers(self, headers):
        self.__client.session.headers.update(headers)

    def get_headers(self):
        return self.__client.session.headers

    def auth_client(self, login: str, password: str):
        """Авторизовация клиента"""
        token = self.login_api.get_auth_token(login=login, password=password)
        self.set_headers(token)

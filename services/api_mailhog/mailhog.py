from restclient.client import RestClient
from restclient.configuration import Configuration
from services.api_mailhog.helpers.mailhog_wrapper import MailhogWrapper


class ApiMailhog:
    def __init__(
            self,
            configuration: Configuration,
            client: RestClient
    ):
        self.__client = client
        self.configuration = configuration
        self.mailhog_api = MailhogWrapper(client=self.__client)

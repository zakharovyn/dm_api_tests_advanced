from restclient.client import RestClient
from services.dm_api_account.apis.login_api import LoginApi
from services.dm_api_account.models import LoginCredentials


class LoginWrapper(LoginApi):

    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = True,
            **kwargs
    ):
        """Залогинить пользователя"""
        response = self._post_v1_account_login(
            json=LoginCredentials(
                login=login,
                password=password,
                rememberMe=remember_me
            ),
            validate_response=validate_response,
            **kwargs
        )
        return response

    def logout_user(
            self,
            **kwargs
    ):
        """Разлогинить пользователя."""
        response = self._delete_v1_account_login(
            **kwargs
        )
        return response

    def logout_user_from_all_devices(
            self,
            **kwargs
    ):
        """Разлогинить пользователя на всех устройствах"""
        response = self._delete_v1_account_login_all(
            **kwargs
        )
        return response

# ------------------------- Вспомогательные методы -----------------------------

    def get_auth_token(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        response = self.login_user(
            login=login,
            password=password,
            remember_me=remember_me,
            validate_response=False
        )
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }

        return token

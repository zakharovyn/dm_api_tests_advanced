import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена номер {count}')
            response = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError(
                    'Превышено количество попыток получения активационного токена'
                )
            if token:
                return response
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    @retrier
    def get_activation_token_by_login(
            self,
            login
    ):
        """Получение токена активации по логину"""
        response = self.get_messages()
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        assert token is not None, f'Токен для пользователя {login} не был получен'
        return token

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            status_code: int = 200
    ):
        """Логин пользователя"""
        json_data = {
            "login": login,
            "password": password,
            "rememberMe": remember_me
        }
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data=json_data
        )
        assert response.status_code == status_code, \
            f'Неожиданный сценарий при авторизации пользователя {response.status_code=}'
        return response

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        """Регистрация пользователя"""
        json_data = {
            'login': login,
            'password': password,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account(
            json_data=json_data
        )
        assert response.status_code == 201, f'Пользователь не был создан {response.json()}'
        return response

    def full_register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        """Регистрация нового пользователя"""
        self.register_new_user(login=login, password=password, email=email)
        token = self.get_activation_token_by_login(login=login)
        response = self.activate_user(token=token)
        return response

    def change_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        """Изменение почты"""
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(
            json_data=json_data
        )
        assert response.status_code == 200, 'При смене email произошла ошибка'
        return response

    def get_messages(
            self,
            limit: int = 10
            ):
        """Получение писем"""
        response = self.mailhog.mailhog_api.get_api_v2_messages(limit=limit)
        assert response.status_code == 200, 'Письма не были получены'
        return response

    def activate_user(
            self,
            token: str
            ):
        """Активация пользователя"""
        response = self.dm_account_api.account_api.put_v1_account_token(
            token=token
            )
        assert response.status_code == 200, 'Пользователь не был активирован'
        return response

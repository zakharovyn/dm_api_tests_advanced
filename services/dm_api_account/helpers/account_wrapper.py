from services.dm_api_account.apis.account_api import AccountApi
from services.dm_api_account.models import (
    ResetPassword,
    ChangeEmail,
    ChangePassword,
    Registration,
)


class AccountWrapper(AccountApi):

    def register_new_user(
            self,
            login: str,
            email: str,
            password: str,
            **kwargs
    ):
        response = self._post_v1_account(
            json=Registration(
                login=login,
                email=email,
                password=password
            ),
            **kwargs
        )
        return response

    def get_current_user_info(
            self,
            **kwargs
    ):
        response = self._get_v1_account(
            **kwargs
        )
        return response

    def activate_user(
            self,
            token: str,
            validate_response: bool = True,
            **kwargs
    ):
        response = self._put_v1_account_token(
            validate_response=validate_response,
            token=token,
            **kwargs
        )
        return response

    def reset_password(
            self,
            login: str,
            email: str,
            validate_response: bool = True,
            **kwargs
    ):
        response = self._post_v1_account_password(
            json=ResetPassword(
                login=login,
                email=email
            ),
            validate_response=validate_response,
            **kwargs
        )
        return response

    def change_password(
            self,
            login: str,
            old_password: str,
            new_password: str,
            token: str,
            validate_response: bool = True,
            **kwargs
    ):
        response = self._put_v1_account_password(
            json=ChangePassword(
                login=login,
                token=token,
                oldPassword=old_password,
                newPassword=new_password
            ),
            validate_response=validate_response,
            **kwargs
        )
        return response

    def change_email(
            self,
            login: str,
            password: str,
            new_email: str,
            validate_response: bool = True,
            **kwargs
    ):
        response = self._put_v1_account_email(
            json=ChangeEmail(
                login=login,
                password=password,
                email=new_email
            ),
            validate_response=validate_response,
            **kwargs
        )
        return response

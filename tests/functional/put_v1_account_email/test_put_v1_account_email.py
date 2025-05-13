from data.data.function.put_v1_account_email_data import PutV1AccountEmailData
from generic.utilites.context_manager import check_status_code_http


def test_put_v1_account_email(account_mh, prepare_user):
    TD = PutV1AccountEmailData

    account_mh.register_and_activate_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

    # Изменить почту
    new_email = TD.new_email
    account_mh.account.account_api.change_email(
        login=prepare_user.login,
        password=prepare_user.password,
        new_email=new_email
    )

    # Авторизоваться
    with check_status_code_http(
            403,
            'User is inactive. Address the technical support for more details'
    ):
        account_mh.account.login_api.login_user(
            login=prepare_user.login,
            password=prepare_user.password,
            validate_response=False
        )

    # Активация пользователя
    account_mh.activate_user(login=prepare_user.login)

    # Авторизоваться
    account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

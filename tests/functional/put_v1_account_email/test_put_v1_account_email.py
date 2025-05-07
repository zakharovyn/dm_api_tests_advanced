from data.data.function.put_v1_account_email_data import PutV1AccountEmailData


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
    account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=prepare_user.password,
        status_code=403
    )

    # Активация пользователя
    account_mh.activate_user(login=prepare_user.login)

    # Авторизоваться
    account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

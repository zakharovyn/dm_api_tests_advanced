from data.data.function.put_v1_account_email_data import PutV1AccountEmailData


def test_put_v1_account_email(dm_account, prepare_user):
    TD = PutV1AccountEmailData

    dm_account.account.register_and_activate_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    dm_account.login.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

    # Изменить почту
    new_email = TD.rand_str.format(prepare_user.email)
    dm_account.account.change_email(
        login=prepare_user.login,
        password=prepare_user.password,
        new_email=new_email
    )

    # Авторизоваться
    dm_account.login.login_user(
        login=prepare_user.login,
        password=prepare_user.password,
        status_code=403
    )

    # Активация пользователя
    dm_account.account.activate_user(login=prepare_user.login)

    # Авторизоваться
    dm_account.login.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

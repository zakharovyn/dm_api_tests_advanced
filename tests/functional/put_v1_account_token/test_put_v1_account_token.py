def test_put_v1_account_token(dm_account, prepare_user):
    dm_account.account.register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )

    # Получить активационный токен
    dm_account.mailhog.get_token_by_login(login=prepare_user.login)

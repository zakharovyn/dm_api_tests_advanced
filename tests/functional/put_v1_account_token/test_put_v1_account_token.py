def test_put_v1_account_token(account_mh, prepare_user):
    account_mh.account.account_api.register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )

    # Получить активационный токен
    account_mh.mailhog.mailhog_api.get_token_by_login(login=prepare_user.login)

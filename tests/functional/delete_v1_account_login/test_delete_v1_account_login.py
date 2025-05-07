def test_delete_v1_account_login(auth_account):
    auth_account.service.account.login_api.logout_user()
    # Возвращаем пользователя в первоначальное состоияние
    auth_account.service.account.auth_client(
        login=auth_account.user.login,
        password=auth_account.user.password
    )

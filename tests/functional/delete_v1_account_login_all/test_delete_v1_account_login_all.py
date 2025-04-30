def test_delete_v1_account_login_all(auth_account):
    auth_account.account.login.logout_user_from_all_devices()
    # Возвращаем пользователя в первоначальное состоияние
    auth_account.account.login.auth_client(
        login=auth_account.user.login,
        password=auth_account.user.password
    )

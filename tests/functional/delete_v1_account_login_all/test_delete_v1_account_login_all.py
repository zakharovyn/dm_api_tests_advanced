def test_delete_v1_account_login_all(auth_account):
    auth_account.service.account.login_api.logout_user_from_all_devices()
    # Возвращаем пользователя в первоначальное состоияние
    auth_account.service.account.auth_client(
        login=auth_account.user.login,
        password=auth_account.user.password
    )

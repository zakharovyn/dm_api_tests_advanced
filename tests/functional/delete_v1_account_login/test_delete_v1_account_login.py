def test_delete_v1_account_login(auth_account_helper):
    auth_account_helper.account_helper.user_login(
        login=auth_account_helper.user.login,
        password=auth_account_helper.user.password
    )
    auth_account_helper.account_helper.logout_user()

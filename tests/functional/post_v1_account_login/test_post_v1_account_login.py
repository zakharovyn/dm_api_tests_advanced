def test_post_v1_account_login(account_mh, prepare_user):
    account_mh.account.account_api.register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_mh.activate_user(
        login=prepare_user.login
    )
    account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

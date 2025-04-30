def test_post_v1_account(dm_account, prepare_user):
    dm_account.account.register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    dm_account.account.activate_user(
        login=prepare_user.login
    )
    dm_account.login.login_user(
        login=prepare_user.login,
        password=prepare_user.password
    )

def test_post_v1_account(account_helper, prepare_user):
    account_helper.full_register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password
    )

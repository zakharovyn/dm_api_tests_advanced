def test_get_v1_account_auth(auth_account_helper):
    auth_account_helper.account_helper.get_current_user_info()


def test_get_v1_account_no_auth(account_helper):
    response = account_helper.get_current_user_info(status_code=401)

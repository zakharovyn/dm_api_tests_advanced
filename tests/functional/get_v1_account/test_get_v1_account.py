def test_get_v1_account_auth(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_no_auth(account_helper):
    response = account_helper.get_current_user_info(status_code=401)

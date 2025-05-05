def test_get_v1_account_auth(auth_account):
    auth_account.service.account.account_api.get_current_user_info()


def test_get_v1_account_no_auth(dm_account):
    dm_account.account_api.get_current_user_info(status_code=401)

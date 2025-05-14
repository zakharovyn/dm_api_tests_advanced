from checkers.context_manager import check_status_code_http
from checkers.get_v1_account import GetV1Account


def test_get_v1_account_auth(auth_account):
    with check_status_code_http():
        response = auth_account.service.account.account_api.get_current_user_info()
        GetV1Account.check_response_values(
            response=response,
            starts_with_='test_user_advanced_'
        )


def test_get_v1_account_no_auth(dm_account):
    with check_status_code_http(401, 'User must be authenticated'):
        dm_account.account_api.get_current_user_info()

from data.data.function.put_v1_account_password_data import PutV1AccountPasswordData


def test_put_v1_account_password(account_mh, prepare_user):
    TD = PutV1AccountPasswordData

    account_mh.register_and_activate_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_mh.account.auth_client(
        login=prepare_user.login,
        password=prepare_user.password
    )
    account_mh.account.account_api.reset_password(
        login=prepare_user.login,
        email=prepare_user.email
    )
    new_password = TD.new_password
    account_mh.change_password(
        login=prepare_user.login,
        old_password=prepare_user.password,
        new_password=new_password
    )
    account_mh.account.login_api.login_user(
        login=prepare_user.login,
        password=new_password
    )

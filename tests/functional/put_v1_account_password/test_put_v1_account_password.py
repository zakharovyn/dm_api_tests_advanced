from data.data.function.put_v1_account_password_data import PutV1AccountPasswordData


def test_put_v1_account_password(dm_account, prepare_user):
    TD = PutV1AccountPasswordData

    dm_account.account.register_and_activate_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    dm_account.login.auth_client(
        login=prepare_user.login,
        password=prepare_user.password
    )
    dm_account.account.reset_password(
        login=prepare_user.login,
        email=prepare_user.email
    )
    new_password = TD.new_password
    dm_account.account.change_password(
        login=prepare_user.login,
        old_password=prepare_user.password,
        new_password=new_password
    )
    dm_account.login.login_user(
        login=prepare_user.login,
        password=new_password
    )

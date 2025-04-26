from datetime import datetime


def test_put_v1_account_password(account_helper, prepare_user):
    account_helper.full_register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_helper.auth_client(
        login=prepare_user.login,
        password=prepare_user.password
    )
    account_helper.reset_password(
        login=prepare_user.login,
        email=prepare_user.email
    )
    date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    new_password = str(f'NewPassWord{date}')
    account_helper.change_password(
        login=prepare_user.login,
        old_password=prepare_user.password,
        new_password=new_password
    )
    account_helper.user_login(
        login=prepare_user.login,
        password=new_password
    )

import random


def test_put_v1_account_email(account_helper, prepare_user):
    account_helper.full_register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password
    )

    # Изменить почту
    new_email = str(random.randint(a=0, b=1000)) + prepare_user.email
    account_helper.change_email(
        login=prepare_user.login,
        password=prepare_user.password,
        new_email=new_email
    )

    # Авторизоваться
    account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password,
        status_code=403
    )

    # Получить активационный токен
    token = account_helper.get_activation_token_by_login(
        login=prepare_user.login
    )

    # Активация пользователя
    account_helper.activate_user(token=token)

    # Авторизоваться
    account_helper.user_login(
        login=prepare_user.login,
        password=prepare_user.password
    )

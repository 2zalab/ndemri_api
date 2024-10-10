from vendors.cache import get_cache, set_cache
from vendors.db_models import User
from vendors.quries import add_record


default_pin = 2022


def check_phone(_app, username):
    return

    # user = User.query.get(username)
    #
    # if user:
    #     set_cache(username, default_pin)
    #
    #     return True
    #
    # else:
    #     user = User(username)
    #     add_record(_app, user)


def check_pin_against_phone(_app, pin, username):

    user = User.query.get(username)

    if user and get_cache(username) == pin:
        user.authenticated = True

        add_record(_app, user)

        return user
        # return login_user(user, remember=True)
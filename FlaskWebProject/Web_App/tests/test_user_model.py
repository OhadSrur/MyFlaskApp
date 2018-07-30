import pytest
from passlib.hash import sha256_crypt


def test_user_password(app_ctx,user):
    psw = '$5$rounds=535000$SYi4G8EOI240Va4C$9YbgGlA.DSnCK693RQoULKAW5TnLUETaQlxxORUUw0B'
    assert psw == user.password
    #assert u.verify_password(psw)

def test_user_get_id(app_ctx,user):
    assert user.get_id() == 5

def test_user_get_username(app_ctx,user):
    assert user.get_username() == 'jonedoe'
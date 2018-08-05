import pytest
from passlib.hash import sha256_crypt
from Web_App.models import UserAccount


def test_user_password(app_ctx,user):
    assert user.verify_password('123456')

def test_user_get_id(app_ctx,user):
    assert user.get_id() == 5

def test_user_get_username(app_ctx,user):
    assert user.get_username() == 'jonedoe'

def test_password_salts_are_random(app_ctx,user):
    u = user.set_password('test')
    u2 = user.set_password('test')
    print (u.password)
    assert u.password != u2.password
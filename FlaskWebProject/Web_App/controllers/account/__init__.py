from flask import Blueprint

account_blueprint = Blueprint(
    'account',
    __name__,
    template_folder='../templates/app/account')

from . import account
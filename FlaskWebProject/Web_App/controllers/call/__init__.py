from flask import Blueprint

call_blueprint = Blueprint(
    'call',
    __name__,
    template_folder='../templates/app/call')

from . import call

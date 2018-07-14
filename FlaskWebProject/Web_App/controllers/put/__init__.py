from flask import Blueprint

put_blueprint = Blueprint(
    'put',
    __name__,
    template_folder='../templates/app/put')

from . import put

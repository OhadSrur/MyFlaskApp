from flask import Blueprint

graph_blueprint = Blueprint(
    'graph',
    __name__,
    template_folder='../templates/app/Graph')

from . import graph

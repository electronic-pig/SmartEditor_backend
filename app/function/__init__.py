from flask import Blueprint

function = Blueprint('function', __name__)

from . import views

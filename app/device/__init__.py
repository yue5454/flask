from flask import Blueprint

device = Blueprint('device', __name__,)

from app.device import views
from flask import Blueprint
from flask import render_template


setting = Blueprint('setting', __name__)


@setting.route('/')
def index():
    """
    setting
    """
    return render_template('setting.html', active_page="setting")

from flask import Blueprint
from flask import render_template


about = Blueprint('about', __name__)


@about.route('/')
def index():
    return render_template('about.html', active_page="about")

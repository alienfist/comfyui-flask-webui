from flask import Blueprint, jsonify, render_template
from datetime import datetime
from utils.workflow_process import WorkflowProcess
from config import STATIC_FOLDER


home = Blueprint('home', __name__)
WP = WorkflowProcess(output_folder=f'{STATIC_FOLDER}{datetime.now().strftime("%Y%m%d")}/stickers/')


@home.route('/')
def web_index():
    return render_template('home.html', active_page="home")


@home.route('/interrupt', methods=['POST'])
def interrupt():
    res = WP.interrupt_task()
    if res:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'interrupt task failed.'}), 400

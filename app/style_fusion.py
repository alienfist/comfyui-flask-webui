from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from config import WORKFLOW_FOLDER
from .tools import save_original_image, save_generate_images


style_fusion = Blueprint('style_fusion', __name__)


@style_fusion.route('/')
def index():
    return render_template('style_fusion.html', active_page="style_fusion")


@style_fusion.route('/generate', methods=['POST'])
def style_fusion_api():
    source_image_file = request.files.get('source_image_file')
    style_image_file = request.files.get('style_image_file')

    source_image_path = save_original_image(source_image_file)
    if not source_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    style_image_path = save_original_image(style_image_file)
    if not style_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    gen_params = {
        "source_image": source_image_path,
        "style_image": style_image_path,
    }

    workflow_json = f"{WORKFLOW_FOLDER}workflow_style_fusion.json"
    gen_images = WP.process_change_style(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen style fusion failed.'}), 400

    image_type = 7
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save style fusion failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})

from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from config import WORKFLOW_FOLDER
from .tools import save_original_image, save_generate_images


change_face = Blueprint('change_face', __name__)


@change_face.route('/')
def index():
    return render_template('change_face.html', active_page="change_face")


@change_face.route('/generate', methods=['POST'])
def change_face_api():
    source_image_file = request.files.get('source_image_file')
    target_image_file = request.files.get('target_image_file')
    remove_bg = request.form.get('remove_bg')

    source_image_path = save_original_image(source_image_file)
    if not source_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    target_image_path = save_original_image(target_image_file)
    if not target_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    gen_params = {
        "source_image": source_image_path,
        "target_image": target_image_path,
    }

    if remove_bg == "true":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_change_face_rmbg.json"
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_change_face.json"

    gen_images = WP.process_change_face(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen change face failed.'}), 400

    image_type = 4
    images_url_list = save_generate_images(gen_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save change face failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})

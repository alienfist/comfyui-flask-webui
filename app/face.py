import os
import time
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from utils.pic_tool import resize_image
from config import TEMP_FOLDER, WORKFLOW_FOLDER, STATIC_FOLDER


face = Blueprint('face', __name__)


@face.route('/')
def change_face_index():
    return render_template('face.html', active_page="face")


@face.route('/generate', methods=['POST'])
def change_face_api():
    source_image_file = request.files.get('source_image_file')
    target_image_file = request.files.get('target_image_file')
    remove_bg = request.form.get('remove_bg')

    filename = int(time.time() * 1000000)
    temp_folder = f'{TEMP_FOLDER}image/{datetime.now().strftime("%Y%m%d")}/'
    os.makedirs(temp_folder, exist_ok=True)

    source_suffix = source_image_file.filename.split(".")[-1]
    target_suffix = target_image_file.filename.split(".")[-1]
    source_temp_filepath = f'{temp_folder}{filename}_source.{source_suffix}'
    target_temp_filepath = f'{temp_folder}{filename}_target.{target_suffix}'

    res_source_resize = resize_image(source_image_file, source_temp_filepath, max_width=1000)
    res_target_resize = resize_image(target_image_file, target_temp_filepath, max_width=1000)
    if not res_source_resize or not res_target_resize:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    gen_params = {
        "source_image": source_temp_filepath,
        "target_image": target_temp_filepath,
    }

    if remove_bg == "true":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_change_face_rmbg.json"
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_change_face.json"

    res_gen_images = WP.process_change_face(gen_params, workflow_json)
    if not res_gen_images:
        return jsonify({'status': 'error', 'message': 'gen face failed.'}), 400

    images_list = [x.replace(f'{STATIC_FOLDER}', '/static/') for x in res_gen_images]
    return jsonify({'status': 'success', "images_list": images_list})

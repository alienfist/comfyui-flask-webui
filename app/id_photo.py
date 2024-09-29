from flask import Blueprint, render_template, request, jsonify

from .workflow import WP
from utils.common import baidu_translate_tool
from utils.pic_tool import layout_pic
from .tools import save_original_image, save_generate_images

from constants import PHOTO_SIZE_DICT, DEFAULT_CHECKPOINT
from config import WORKFLOW_FOLDER


id_photo = Blueprint("id_photo", __name__)


@id_photo.route('/')
def index():
    return render_template('id_photo.html', active_page="id_photo")


@id_photo.route('/generate', methods=['POST'])
def gen_id_photo_api():
    face_image_file = request.files.get('face_image_file')
    pose_image_file = request.files.get('pose_image_file')
    id_photo_color = request.form.get('id_photo_color')
    id_photo_clothing = request.form.get('id_photo_clothing')
    id_photo_size = request.form.get('id_photo_size')
    id_photo_exposure = request.form.get('id_photo_exposure')
    id_photo_lay_num = int(request.form.get('id_photo_lay_num'))
    desc_prompt = request.form.get('desc_prompt')
    beauty = request.form.get('beauty')

    original_face_image_path = save_original_image(face_image_file)
    if not original_face_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    original_pose_image_path = save_original_image(pose_image_file)
    if not original_pose_image_path:
        return jsonify({'status': 'error', 'message': 'resize image failed.'}), 400

    if desc_prompt:
        desc_prompt_translate = baidu_translate_tool(desc_prompt)
        positive_prompt = f'({desc_prompt_translate["text"]})' if desc_prompt_translate["code"] == 1 else desc_prompt
    else:
        positive_prompt = ""

    gen_params = {
        "face_img_path": original_face_image_path,
        "pose_img_path": original_pose_image_path,
        "positive_prompt": positive_prompt,
        "model": DEFAULT_CHECKPOINT["id_photo"],
        "background_color": id_photo_color,
        "dress": id_photo_clothing + "(no sideburns:1.5), ",
        "id_photo_exposure": id_photo_exposure,
    }

    if beauty == "true":
        workflow_json = f"{WORKFLOW_FOLDER}workflow_id_photo.json"
    else:
        workflow_json = f"{WORKFLOW_FOLDER}workflow_id_photo_no_beauty.json"
    gen_images = WP.process_id_photo(gen_params, workflow_json)
    if not gen_images:
        return jsonify({'status': 'error', 'message': 'gen id photo failed.'}), 400

    photo_path = gen_images[0]
    photo_size = PHOTO_SIZE_DICT[id_photo_size]
    paper_path = layout_pic(photo_path, id_photo_color, photo_size=photo_size, photo_num=id_photo_lay_num)
    if not paper_path:
        return jsonify({'status': 'error', 'message': 'layout id photo failed.'}), 400

    temp_images = [photo_path, paper_path]
    image_type = 5
    images_url_list = save_generate_images(temp_images, gen_params, image_type)
    if not images_url_list:
        return jsonify({'status': 'error', 'message': 'save id photo failed.'}), 400
    return jsonify({'status': 'success', "images_list": images_url_list})

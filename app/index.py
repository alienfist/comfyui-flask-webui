from flask import Blueprint, jsonify, render_template, request

from utils.workflow_process import WorkflowProcess
from .tools import clear_temp_folder
from models import get_images_by_page_and_user, delete_image, get_user_by_username
from constants import IMG_TYPE_MAPPING, IMG_SCALE
from config import USER_INFO


index = Blueprint('index', __name__)
WP = WorkflowProcess()


@index.route('/api/get_user_uuid')
def get_user_uuid():
    try:
        user_name = USER_INFO["username"]
        user_uuid = get_user_by_username(user_name).uuid
        return jsonify({"user_uuid": user_uuid}), 200
    except Exception as e:
        print(f"Error getting user UUID: {e}")
        return jsonify({"error": "Failed to get user UUID"})

@index.route('/')
def web_index():
    clear_temp_folder()
    return render_template('index.html', active_page="index")


@index.route('/interrupt', methods=['POST'])
def interrupt():
    res = WP.interrupt_task()
    if res:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'interrupt task failed.'}), 400


@index.route('/api/images')
def get_images_api():
    user_uuid = request.args.get('user_uuid', None)
    if not user_uuid:
        return {"error": "User UUID is required"}, 400

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    images = get_images_by_page_and_user(per_page, offset, user_uuid)

    if images is None:
        return {"error": "Error fetching images"}, 500

    images_data = [{"id": image.id, "image_url": image.image_url, "create_time": image.create_time.strftime('%Y-%m-%d %H:%M:%S')} for image in images]
    return {"images": images_data, "page": page, "per_page": per_page}


@index.route('/api/delete_image', methods=['POST'])
def delete_image_api():
    image_id = request.args.get('image_id', None)
    if not image_id:
        return {"error": "Image UUID is required"}, 400
    image_id = int(image_id)
    res_delete = delete_image(image_id)
    if not res_delete:
        return jsonify({"error": "delete image failed."}), 404
    return jsonify({"success": True}), 200


@index.route('/api/constants', methods=['POST'])
def get_constants():
    constants_dict = {
        "image_type_mapping": IMG_TYPE_MAPPING,
        "image_scale": IMG_SCALE,
    }
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    constant_name = data.get('name')
    if constant_name in constants_dict:
        return jsonify({constant_name: constants_dict[constant_name]})
    else:
        return jsonify({"error": "Constant not found"}), 404

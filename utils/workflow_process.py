import os
import io
import json
import time
import uuid
import requests
import websocket
from PIL import Image
from datetime import datetime
from requests_toolbelt import MultipartEncoder

from utils.common import gen_random_seed
from constants import IMG_SCALE, LORA_PROMPT_MAPPING
from config import COMFYUI_URL, COMFYUI_WS_URL, CLIENT_ID, TEMP_FOLDER


class WorkflowProcess(object):
    def __init__(self):
        self.client_id = CLIENT_ID
        self.temp_folder = f'{TEMP_FOLDER}{datetime.now().strftime("%Y%m%d")}/'
        os.makedirs(self.temp_folder, exist_ok=True)

    @staticmethod
    def gen_client_id():
        """生成客户ID"""
        client_id = str(uuid.uuid4())
        return client_id

    def open_websocket_connection(self):
        """建立websocket连接"""
        ws = websocket.WebSocket()
        ws_url = f"{COMFYUI_WS_URL}ws?clientId={self.client_id}"
        ws.connect(ws_url)
        return ws

    def interrupt_task(self):
        """取消当前任务"""
        try:
            result = requests.post(f"{COMFYUI_URL}interrupt")
            result.raise_for_status()
            if result.status_code == 200:
                return True
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return None

    def queue_prompt(self, prompt):
        """
        提交队列任务
        返回数据格式如下：
        {
            "prompt_id": "bd2cfa2c-de87-4258-89cc-d8791bc13a61",
            "number": 501,
            "node_errors": {}
        }
        """
        try:
            p = {"prompt": prompt, "client_id": self.client_id}
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(p).encode('utf-8')
            result = requests.post(f"{COMFYUI_URL}prompt", headers=headers, data=data)
            result.raise_for_status()
            return result.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return None

    def get_history(self, prompt_id):
        """获取历史信息"""
        url = f"{COMFYUI_URL}history/{prompt_id}"
        try:
            result = requests.get(url)
            result.raise_for_status()
            data = result.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return None

    def save_image(self, image_info, image_path):
        """存储图片"""
        try:
            url = f"{COMFYUI_URL}view"
            result = requests.get(url, params=image_info)
            image_data = result.content
            image = Image.open(io.BytesIO(image_data))
            image.save(image_path)
            return image_path
        except Exception as e:
            print(f"发生错误：{e}")
            return None

    def get_images(self, prompt_id):
        """获取图片"""
        output_images = []
        history = self.get_history(prompt_id)
        outputs_info = history[prompt_id]['outputs']
        for node_id in outputs_info:
            node_output = outputs_info[node_id]
            if 'images' in node_output:
                for index, image_info in enumerate(node_output['images']):
                    if image_info['type'] == 'temp':
                        continue
                    image_path = f"{self.temp_folder}{int(time.time() * 1000000)}.png"
                    self.save_image(image_info, image_path)
                    output_images.append(image_path)
        return output_images

    def process_change_face(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            name = str(int(time.time()))
            source_image_name = f"{name}_source.png"
            source_image_path = gen_params.get("source_image")
            res_upload_source = self.upload_image(source_image_path, source_image_name)
            prompt["582"]["inputs"]["image"] = source_image_name

            target_image_name = f"{name}_target.png"
            target_image_path = gen_params.get("target_image")
            res_upload_target = self.upload_image(target_image_path, target_image_name)
            prompt["498"]["inputs"]["image"] = target_image_name

            if not res_upload_source or not res_upload_target:
                print("upload image failed.")
                return None

            prompt["763"]["inputs"]["seed"] = gen_random_seed()
            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_change_style(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            name = str(int(time.time()))
            source_image_name = f"{name}_source.png"
            source_image_path = gen_params.get("source_image")
            res_upload_source = self.upload_image(source_image_path, source_image_name)
            prompt["2"]["inputs"]["image"] = source_image_name

            style_image_name = f"{name}_style.png"
            style_image_path = gen_params.get("style_image")
            res_upload_style = self.upload_image(style_image_path, style_image_name)
            prompt["11"]["inputs"]["image"] = style_image_name

            if not res_upload_source or not res_upload_style:
                print("upload image failed.")
                return None

            prompt["12"]["inputs"]["seed"] = gen_random_seed()
            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_stickers(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            filename = f"{str(int(time.time()))}.png"
            input_path = gen_params.get("img_path")
            self.upload_image(input_path, filename)
            prompt["18"]["inputs"]["image"] = filename
            positive_prompt = gen_params.get("positive_prompt", "")

            if gen_params.get("batch_size"):
                prompt["15"]["inputs"]["batch_size"] = gen_params.get("batch_size")
                prompt["46"]["inputs"]["batch_size"] = gen_params.get("batch_size")
                prompt["63"]["inputs"]["max_frames"] = gen_params.get("batch_size")

            # 设定风格
            style_lora = gen_params.get("style_lora", "")
            if style_lora:
                prompt["17"]["inputs"]["lora_name"] = style_lora
                positive_prompt = LORA_PROMPT_MAPPING.get(style_lora, "") + positive_prompt

            sticker_lora = gen_params.get("sticker_lora")
            if sticker_lora:
                prompt["64"]["inputs"]["lora_name"] = sticker_lora
                positive_prompt = LORA_PROMPT_MAPPING.get(sticker_lora, "") + positive_prompt

            # 正向提示词
            prompt["31"]["inputs"]["text"] = positive_prompt

            # 设定随机
            prompt["10"]["inputs"]["seed"] = gen_random_seed()
            prompt["43"]["inputs"]["seed"] = gen_random_seed()

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_couple(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            # 设定模型
            if gen_params.get("model"):
                prompt["14"]["inputs"]["ckpt_name"] = gen_params.get("model")

            # 设定lora
            if gen_params.get("lora1"):
                prompt["89"]["inputs"]["lora_name"] = gen_params.get("lora1")

            if gen_params.get("lora2"):
                prompt["81"]["inputs"]["lora_name"] = gen_params.get("lora2")

            # 设定种子
            seed = gen_random_seed()
            prompt["25"]["inputs"]["seed"] = seed
            prompt["77"]["inputs"]["seed"] = seed

            # 设定图片
            file_left_name = f"{str(int(time.time()))}_left.png"
            input_left_path = gen_params.get("img_left_path")
            self.upload_image(input_left_path, file_left_name)
            prompt["13"]["inputs"]["image"] = file_left_name

            file_right_name = f"{str(int(time.time()))}_right.png"
            input_right_path = gen_params.get("img_right_path")
            self.upload_image(input_right_path, file_right_name)
            prompt["21"]["inputs"]["image"] = file_right_name

            file_pose_name = f"{str(int(time.time()))}_pose.png"
            input_pose_path = gen_params.get("img_pose_path")
            self.upload_image(input_pose_path, file_pose_name)
            prompt["84"]["inputs"]["image"] = file_pose_name

            # positive_prompt
            if gen_params.get("positive_prompt"):
                prompt["23"]["inputs"]["text"] += gen_params.get("positive_prompt")

            # negative_prompt
            if gen_params.get("negative_prompt"):
                prompt["22"]["inputs"]["text"] += gen_params.get("negative_prompt")

            # 设定张数
            if gen_params.get("batch_size"):
                prompt["26"]["inputs"]["batch_size"] = gen_params.get("batch_size")

            output_size = gen_params.get("output_size")
            prompt["26"]["inputs"]["width"] = output_size[0]
            prompt["26"]["inputs"]["height"] = output_size[1]

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_img2img(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            # 设定模型
            if gen_params.get("model"):
                prompt["1"]["inputs"]["ckpt_name"] = gen_params.get("model")

            # 发散度
            if gen_params.get("divergence"):
                prompt["169"]["inputs"]["threshold"] = float(gen_params.get("divergence"))

            # 设定lora
            if gen_params.get("lora"):
                prompt["154"]["inputs"]["lora_name"] = gen_params.get("lora")

            # 设定图片
            filename = f"{str(int(time.time()))}.png"
            input_path = gen_params.get("img_path")
            self.upload_image(input_path, filename)
            prompt["3"]["inputs"]["image"] = filename

            # 设定lora prompt
            if gen_params.get("lora_prompt"):
                prompt["157"]["inputs"]["text"] = gen_params.get("lora_prompt")

            # positive_prompt
            if gen_params.get("positive_prompt"):
                prompt["158"]["inputs"]["text"] = gen_params.get("positive_prompt")

            # negative_prompt
            if gen_params.get("negative_prompt"):
                prompt["160"]["inputs"]["text"] = gen_params.get("negative_prompt")

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_id_photo(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            # 设定模型
            if gen_params.get("model"):
                prompt["6"]["inputs"]["ckpt_name"] = gen_params.get("model")

            # 设定背景颜色
            if gen_params.get("background_color"):
                prompt["29"]["inputs"]["fill_color"] = gen_params.get("background_color")

            # 设定衣服
            if gen_params.get("dress"):
                prompt["81"]["inputs"]["text"] += gen_params.get("dress")

            # 设定曝光
            if gen_params.get("id_photo_exposure"):
                prompt["74"]["inputs"]["temperature"] = int(gen_params.get("id_photo_exposure"))

            # 设定人脸图片
            face_filename = f"{str(int(time.time()))}_face.png"
            face_input_path = gen_params.get("face_img_path")
            self.upload_image(face_input_path, face_filename)
            prompt["1"]["inputs"]["image"] = face_filename

            # 设定姿态图片
            pose_filename = f"{str(int(time.time()))}_pose.png"
            pose_input_path = gen_params.get("pose_img_path")
            self.upload_image(pose_input_path, pose_filename)
            prompt["2"]["inputs"]["image"] = pose_filename

            # 设定prompt
            if gen_params.get("positive_prompt"):
                prompt["81"]["inputs"]["text"] += gen_params.get("positive_prompt")

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_txt2img(self, gen_params, workflow_json):
        """
        文字生成图片
        gen_params =
        "positive_prompt": "1girl, beautiful face, on street, smile",
        "negative_prompt": "text, watermark, nsfw, soft, nude, ugly, broken, oversaturated",
        "batch_size": 4,
        "scale": "1:1",
        "style": "",
        "seed": ""
        """
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            # 随机种子
            prompt["46"]["inputs"]["noise_seed"] = gen_random_seed()

            # 设定模型
            if gen_params.get("checkpoint"):
                prompt["4"]["inputs"]["ckpt_name"] = gen_params.get("checkpoint")

            # 设定样式
            if gen_params.get("style"):
                prompt["43"]["inputs"]["style"] = gen_params.get("style")

            # 设定lora
            lora1_name = gen_params.get("lora1", "").strip()
            if lora1_name:
                prompt["40"]["inputs"]["switch"] = "On"
                prompt["40"]["inputs"]["lora_name"] = lora1_name
                prompt["40"]["inputs"]["strength_model"] = float(gen_params.get("lora1_weight", "1.0"))

            lora2_name = gen_params.get("lora2", "").strip()
            if lora2_name:
                prompt["47"]["inputs"]["switch"] = "On"
                prompt["47"]["inputs"]["lora_name"] = lora2_name
                prompt["47"]["inputs"]["strength_model"] = float(gen_params.get("lora2_weight", "1.0"))

            lora3_name = gen_params.get("lora3", "").strip()
            if lora3_name:
                prompt["41"]["inputs"]["switch"] = "On"
                prompt["41"]["inputs"]["lora_name"] = lora3_name
                prompt["41"]["inputs"]["strength_model"] = float(gen_params.get("lora3_weight", "1.0"))

            # 正向提示词
            positive_prompt = gen_params.get("positive_prompt", "")
            if positive_prompt:
                prompt["43"]["inputs"]["text_positive"] = positive_prompt

            # 反向提示词
            negative_prompt = gen_params.get("negative_prompt", "")
            if negative_prompt:
                prompt["43"]["inputs"]["text_negative"] = negative_prompt

            # 设定比例
            scale = gen_params.get("scale")
            prompt["5"]["inputs"]["width"], prompt["5"]["inputs"]["height"] = IMG_SCALE[scale]

            # 设定张数
            prompt["5"]["inputs"]["batch_size"] = gen_params.get("batch_size")

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_art_photo(self, gen_params, workflow_json):
        """艺术照"""
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            # 设定模型
            if gen_params.get("checkpoint"):
                prompt["1"]["inputs"]["ckpt_name"] = gen_params.get("checkpoint")

            # 设定图片
            filename = f"{str(int(time.time()))}.png"
            input_path = gen_params.get("img_path")
            self.upload_image(input_path, filename)
            prompt["17"]["inputs"]["image"] = filename

            # 设定比例
            scale = gen_params.get("scale")
            prompt["6"]["inputs"]["width"], prompt["6"]["inputs"]["height"] = IMG_SCALE[scale]

            # 设定张数
            if gen_params.get("image_count"):
                prompt["6"]["inputs"]["batch_size"] = gen_params.get("image_count")

            # 正向提示词
            positive_prompt = gen_params.get("positive_prompt", "")
            if positive_prompt:
                prompt["28"]["inputs"]["text2"] += positive_prompt

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def process_art_photo_male(self, gen_params, workflow_json):
        """艺术照-男性"""
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            # 设定模型
            if gen_params.get("checkpoint"):
                prompt["1"]["inputs"]["ckpt_name"] = gen_params.get("checkpoint")

            # 设定图片
            filename = f"{str(int(time.time()))}.png"
            input_path = gen_params.get("img_path")
            self.upload_image(input_path, filename)
            prompt["17"]["inputs"]["image"] = filename

            # 设定比例
            scale = gen_params.get("scale")
            prompt["6"]["inputs"]["width"], prompt["6"]["inputs"]["height"] = scale

            # 设定张数
            if gen_params.get("image_count"):
                prompt["6"]["inputs"]["batch_size"] = gen_params.get("image_count")

            # 正向提示词
            positive_prompt = gen_params.get("positive_prompt", "")
            if positive_prompt:
                prompt["46"]["inputs"]["string"] += positive_prompt

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)
            images = self.get_images(prompt_id)
            if not images:
                return []
            else:
                return images
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def get_image_desc(self, gen_params, workflow_json):
        try:
            self.open_websocket_connection()
            with open(workflow_json, 'r', encoding='utf-8') as file:
                prompt = json.load(file)

            filename = f"{str(int(time.time()))}.png"
            input_path = gen_params.get("img_path")
            self.upload_image(input_path, filename)
            prompt["1"]["inputs"]["image"] = filename

            prompt_json = self.queue_prompt(prompt)
            prompt_id = prompt_json["prompt_id"]
            self.track_progress(prompt_id)

            history = self.get_history(prompt_id)
            image_desc = history[prompt_id]['outputs']['11']['text'][0].split(",")
            return image_desc
        except Exception as e:
            print(f"请求失败：{e}")
            return None

    def track_progress(self, prompt_id):
        """任务进度追踪"""
        while True:
            time.sleep(1)
            history = self.get_history(prompt_id)
            if history:
                return
            else:
                continue

    def track_progress_detail(self, prompt, ws, prompt_id):
        """任务进度追踪"""
        node_ids = list(prompt.keys())
        finished_nodes = []
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'progress':
                    data = message['data']
                    current_step = data['value']
                    print('In K-Sampler -> Step: ', current_step, ' of: ', data['max'])
                if message['type'] == 'execution_cached':
                    data = message['data']
                    for itm in data['nodes']:
                        if itm not in finished_nodes:
                            finished_nodes.append(itm)
                            print('Progess: ', len(finished_nodes), '/', len(node_ids), ' Tasks done')
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] not in finished_nodes:
                        finished_nodes.append(data['node'])
                        print('Progess: ', len(finished_nodes), '/', len(node_ids), ' Tasks done')
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break  # Execution is done
            else:
                continue
        return

    @classmethod
    def get_object_info(self):
        """获取Comfy全部参数"""
        url = f"{COMFYUI_URL}object_info"
        try:
            result = requests.get(url)
            result.raise_for_status()
            data = result.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return None

    def get_node_info(self, node_class):
        """获取组件参数"""
        url = f"{COMFYUI_URL}object_info/{node_class}"
        try:
            result = requests.get(url)
            result.raise_for_status()
            data = result.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            return None

    def upload_image(self, input_path, name, image_type="input", overwrite=False):
        try:
          with open(input_path, 'rb') as file:
            multipart_data = MultipartEncoder(
              fields={
                'image': (name, file, 'image/png'),
                'type': image_type,
                'overwrite': str(overwrite).lower()
              }
            )
            data = multipart_data
            headers = {'Content-Type': multipart_data.content_type}
            result = requests.post(f"{COMFYUI_URL}upload/image", data=data, headers=headers)
            return result.content
        except Exception as e:
            print(f"异常错误：{e}")
            return None

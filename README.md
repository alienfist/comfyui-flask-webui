# comfyui-flask-webui
An ai image generate website using flask base on comfyui

<p align="center">
    <img src="assets/screenshot-home.jpg" alt="Home">
</p>

## Introduce
An offline image generation website, converts Comfyui workflow into website functionality, making it easier to use.

**Tips:**  

This project was written for my friend. The code needs to be stripped of some settings, and it is expected to upload all the code within 30 days.

**Website Features：**

1. **Stickers** Generate stickers from a photo
2. **Txt2img**
3. **Img2img**
4. **Fusion** The fusion of two photo styles
5. **ChangeFace**
6. **IDPhoto** Generate one inch or two inch ID photos from one photo

**Website Screenshot：**

1. Txt2img Page Screenshot
<p align="center">
    <img src="assets/screenshot-txt2img.jpg" alt="txt2img" width="80%">
</p>

2. Stickers Page Screenshot
<p align="center">
    <img src="assets/screenshot-stickers.jpg" alt="stickers" width="80%">
</p>

3. Fusion Page Screenshot
<p align="center">
    <img src="assets/screenshot-fusion.jpg" alt="fusion" width="80%">
</p>

4. Idphoto Page Screenshot
<p align="center">
    <img src="assets/screenshot-idphoto.jpg" alt="idphoto" width="80%">
</p>

## ComfyUI Setup

To start your comfyui, make sure the comfyui workflow can be used normally.  
You can find more information at the following link:  
https://github.com/comfyanonymous/ComfyUI

## How to install

1. **create venv**
```bash
conda create -n comfyui-flask-webui python=3.10
conda activate comfyui-flask-webui
cd comfyui-flask-webui
pip install -r requirements.txt
```

2. **sql init**
```bash
flask db init
flask db migrate
flask db upgrade
```

3. **create user** (modify config.py userinfo)
```bash
python test/create_user.py
```

4. **run project**
```bash
python manage.py
```




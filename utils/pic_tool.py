import os
import io
import glob
import time
import cairosvg

from PIL import Image, ImageOps
from config import TEMP_FOLDER


def get_all_image_paths(folder_path):
    image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tiff', '*.webp')
    image_path_list = []
    for extension in image_extensions:
        image_path_list.extend(glob.glob(os.path.join(folder_path, extension)))
    return image_path_list


def gen_pure_pic(pic_size, pic_color, save_pic_path):
    try:
        bg_img = Image.new('RGB', pic_size, pic_color)
        bg_img.save(save_pic_path)
        return save_pic_path
    except Exception as e:
        print(e)
        return None


def layout_pic(photo_path, photo_color, output_path=None, photo_num=None, photo_size=(25, 35), paper_size=(210, 297),
               dpi=300):
    if not os.path.isfile(photo_path):
        print("Photo path does not exist.")
        return None

    # transform mm to px
    paper_width_px = int(paper_size[0] / 25.4 * dpi)  # 25.4 mm = 1 inch
    paper_height_px = int(paper_size[1] / 25.4 * dpi)
    photo_width_px = int(photo_size[0] / 25.4 * dpi)
    photo_height_px = int(photo_size[1] / 25.4 * dpi)

    photo = Image.open(photo_path)
    if photo_size:
        photo = ImageOps.fit(photo, (photo_width_px, photo_height_px), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    else:
        max_photo_width_px = int(50 / 25.4 * dpi)        # 如果照片宽度超过50mm，则进行等比例缩放
        if photo.width > max_photo_width_px:
            scale_factor = max_photo_width_px / photo.width
            new_width = max_photo_width_px
            new_height = int(photo.height * scale_factor)
            photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo_width_px = new_width
            photo_height_px = new_height

    paper_image = Image.new('RGB', (paper_width_px, paper_height_px), 'white')
    border_size = 1 if photo_color == "white" else 0

    # paper pos
    positions = []
    rows = 2
    cols = int(photo_num / rows) if photo_num else int(paper_size[0] / photo_size[0])
    margin_x = 0
    margin_y = 0

    margin_top = 100
    margin_left = int((paper_width_px - photo_width_px * cols) / 2)
    for row in range(rows):
        for col in range(cols):
            x = margin_left + margin_x + col * (photo_width_px + 2 * border_size + margin_x)
            y = margin_top + margin_y + row * (photo_height_px + 2 * border_size + margin_y)
            positions.append((x, y))

    # stick photo to pos
    for pos in positions:
        bordered_photo = ImageOps.expand(photo.resize((photo_width_px, photo_height_px)), border=border_size, fill='#F0F0F0')
        paper_image.paste(bordered_photo, pos)

    if not output_path:
        output_folder = f"{TEMP_FOLDER}id_photo/"
        os.makedirs(output_folder, exist_ok=True)
        output_path = f"{output_folder}{time.time()}.png"
    paper_image.save(output_path)
    return output_path


def analyze_image_orientation(image_path):
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = width / height
    return aspect_ratio


def svg_to_png(svg_path, png_path):
    cairosvg.svg2png(url=svg_path, write_to=png_path)


def resize_image(input_image_file, output_file_path, max_width=1000):
    try:
        image_bytes = input_image_file.read()
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)
        width, height = image.size
        if width > max_width:
            scale = max_width / width
            new_height = int(height * scale)
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        image.save(output_file_path)
        image_stream.close()
        return output_file_path
    except Exception as e:
        print(e)
        return None

BASE_PROMPT = {
    "positive_prompt": "high quality, best quality, ultra highres, ",
    "negative_prompt": """(worst quality:2), (low quality:2), (normal quality:2), lowres, nude, nsfw, blurry, watermark, text, ugly, soft, broken, bad hands, doubled face, double hands, bad feets, bad anatomy, missing fingers, """
}

IMG_SCALE = {
    "16:9": (1344, 768),
    "3:2": (1216, 832),
    "5:4": (1152, 896),
    "1:1": (1024, 1024),
    "4:5": (896, 1152),
    "2:3": (832, 1216),
    "9:16": (768, 1344),
}

IMG_TYPE_MAPPING = {
    0: "original",
    1: "stickers",
    2: "txt2img",
    3: "img2img",
    4: "change_face",
    5: "id_photo",
    6: "couple",
    7: "change_style",
    8: "art_photo",
}

PHOTO_SIZE_DICT = {
    "A4": [210, 297],
    "1寸": [25, 35],
    "2寸": [35, 53],
    "4寸": [102, 152],
    "6寸": [152, 102],
    "5寸": [127, 89],
    "7寸": [178, 127],
    "8寸": [203, 152],
    "10寸": [254, 203],
    "12寸": [305, 254],
    "14寸": [355, 279],
    "16寸": [406, 305],
    "18寸": [457, 356],
    "20寸": [508, 406],
    "24寸": [610, 508]
}

DEFAULT_CHECKPOINT = {
    "txt2img": "dreamshaperXL_v21TurboDPMSDE.safetensors",
    "img2img": "xxmix9realisticsdxl_v10.safetensors",
    "sticks": "dreamshaperXL_lightningDPMSDE.safetensors",
    "id_photo": "dreamshaperXL_lightningDPMSDE.safetensors",
    "art_photo": "xxmix9realisticsdxl_v10.safetensors"
}

LORA_PROMPT_MAPPING = {
    "StudioGhibli.Redmond-StdGBRRedmAF-StudioGhibli.safetensors": "<lora:StdGBRedmAFPashDebiCOMTE:1>, ",
    "国风插画SDXL.safetensors": "<lora:国风插画SDXL:1>, ",
    "SDXLFaeTastic2400.safetensors": "<lora:SDXLFaeTastic2400:1>, ",
    "CLAYMATE_V2.03_.safetensors": "<lora:CLAYMATE_V2.03_:1>, ",
    "princess_xl_v2.safetensors": "<lora:princess_xl_v2:0.9>, ",
    "xl_more_art-full_v1.safetensors": "<lora:xl_more_art-full_v1:1>, ",
    "LineAniRedmondV2-Lineart-LineAniAF.safetensors": "<lora:LineAniRedmondV2-Lineart-LineAniAF:1>, ",
    "3D模型丨可爱化SDXL版_v2.0.safetensors": "<lora:3D模型丨可爱化SDXL版_v2.0:1>, ",
    "cutedoodle_XL-000012.safetensors": "<lora:cutedoodle_XL-000012:0.8>, ",
    "StickersRedmond.safetensors": "<lora:StickersRedmond:1>, ",
    "Harrlogos_v2.0.safetensors": "<lora:Harrlogos_v2.0:0.8>, ",
    "stampsticker.safetensors": " <lora:stampsticker:1>, ",
    "LogoRedmondV2-Logo-LogoRedmAF.safetensors": "logo, LogoRedAF, <lora:LogoRedmondV2-Logo-LogoRedmAF:1>, ",
    "Cartoon_Logo_SDXL.safetensors": 'cartoon logo, text ["%s"], ',
    "Fresh Ideas@LOGO DESIGNER_SDXL.safetensors": 'logo, <lora:Fresh Ideas@LOGO DESIGNER_SDXL:1>, ',
    "RibbonLogo_XL-E10R16.safetensors": 'ribbon logo, <lora:RibbonLogo_XL:1>, ',
    "dvr-ftl.safetensors": '<lora:dvr-ftl:0.8>, ',
    "logomkrdsxl.safetensors": '<lora:logomkrdsxl:1>, ',
    "[XL]Logo.safetensors": '<lora:[XL]Logo:1>LOGO, ',
    "logo-xl.safetensors": '<lora:logo-000001:1>, ',
    "texta.safetensors": 'text "%s", <lora:texta:1>, ',
    "RoundLogo_XL_E10R16.safetensors": 'round logo, <lora:RoundLogo_XL_E10R16:1>, ',
    "MengX girl_Mix_V40.safetensors": "<lora:MengX girl_Mix_V40:0.9>, ",
    "last.safetensors": "tshirt design <lora:last:1>, ",
    "DFunk_SDXL.safetensors": "<lora:DFunk_SDXL:1>, ",
    "t-shirt_design-sdxl.safetensors": "<lora:wildlife-sdxl:1> t-shirt_design, ",
    "retro_tshirt.safetensors": "<lora:retro_tshirt:1>, ",
    "TShirtDesignRedmondV2-Tshirtdesign-TshirtDesignAF.safetensors": "<lora:TShirtDesignRedmondV2-Tshirtdesign-TshirtDesignAF:1>, TshirtDesignAF, ",
}

const TXT2IMAGE_STYLE = [
    { value: "base", text: "无" },
    { value: "sai-3d-model", text: "3d模型" },
    { value: "sai-analog film", text: "胶片" },
    { value: "sai-anime", text: "动漫" },
    { value: "sai-cinematic", text: "电影" },
    { value: "sai-comic book", text: "漫画" },
    { value: "sai-craft clay", text: "工艺黏土" },
    { value: "sai-digital art", text: "数字艺术" },
    { value: "sai-enhance", text: "增强" },
    { value: "sai-fantasy art", text: "幻想艺术" },
    { value: "sai-isometric", text: "等轴" },
    { value: "sai-line art", text: "艺术线条" },
    { value: "sai-lowpoly", text: "低方块" },
    { value: "sai-neonpunk", text: "朋克" },
    { value: "sai-origami", text: "折纸" },
    { value: "sai-photographic", text: "摄影" },
    { value: "sai-pixel art", text: "像素艺术" },
    { value: "sai-texture", text: "纹理" },
];

const ID_PHOTO_CLOTHING = [
    { value: "(White dress shirt:1.5), ", text: "白色衬衫" },
    { value: "(Black dress shirt:1.5), ", text: "黑色衬衫" },
    { value: "(White T-shirt:1.5), ", text: "白色T恤" },
    { value: "(Black T-shirt:1.5), ", text: "黑色T恤" },
    { value: "(Black suit jacket with white dress shirt underneath:1.5), ", text: "黑西服白衬衫" },
    { value: "(Black suit jacket with black dress shirt underneath:1.5), ", text: "黑西服黑衬衫" },
];

const ID_PHOTO_SIZE = [
    { value: "1寸", text: "一寸照片" },
    { value: "2寸", text: "二寸照片" },
    { value: "4寸", text: "四寸照片" },
    { value: "6寸", text: "六寸照片" },
];

const ID_PHOTO_COLOR = [
    { value: "white", text: "白色" },
    { value: "black", text: "黑色" },
    { value: "red", text: "红色" },
    { value: "green", text: "绿色" },
    { value: "blue", text: "蓝色" },
    { value: "yellow", text: "黄色" },
    { value: "cyan", text: "青色" },
    { value: "magenta", text: "洋红色" },
    { value: "orange", text: "橙色" },
    { value: "purple", text: "紫色" },
    { value: "pink", text: "粉色" },
    { value: "brown", text: "棕色" },
    { value: "gray", text: "灰色" },
    { value: "lightgray", text: "浅灰色" },
    { value: "darkgray", text: "深灰色" },
    { value: "olive", text: "橄榄色" },
    { value: "lime", text: "酸橙色" },
    { value: "teal", text: "水鸭色" },
    { value: "navy", text: "海军蓝" },
    { value: "maroon", text: "栗色" },
    { value: "fuchsia", text: "紫红色" },
    { value: "aqua", text: "水色" },
    { value: "silver", text: "银色" },
    { value: "gold", text: "金色" },
    { value: "turquoise", text: "绿松石色" },
    { value: "lavender", text: "薰衣草色" },
    { value: "violet", text: "紫罗兰色" },
    { value: "coral", text: "珊瑚色" },
    { value: "indigo", text: "靛蓝色" }
];

const STICKER_STYLE = [
    { value: "cartoon", text: "卡通风格(推荐)" },
    { value: "cute", text: "可爱风格" },
    { value: "pure", text: "清纯风格" },
    { value: "gorgeous", text: "艳丽风格" },
    { value: "realistic", text: "写实风格" },
];

const IMG2IMG_STYLE = [
    { value: "anime", text: "日式动漫" },
    { value: "chinese", text: "国风插画" },
    { value: "fantasy", text: "奇妙幻想" },
    { value: "mud", text: "泥偶风格" },
    { value: "princess", text: "美式公主" },
    { value: "pvc", text: "pvc手办" },
    { value: "line", text: "手绘风格" },
];

const CHECKPOINTS = [
    { value: "sd_xl_base_1.0.safetensors", text: "基础模型" },
    { value: "dreamshaperXL_v21TurboDPMSDE.safetensors", text: "Dreamshaper通用" },
    { value: "juggernautXL_XIRundiffusion.safetensors", text: "Juggernaut通用" },
    { value: "xxmix9realisticsdxl_v10.safetensors", text: "Realistic写实" },
    { value: "realvisxlV40_v40LightningBakedvae.safetensors", text: "realvisxlV40写实" },
    { value: "realcartoonXL_v6.safetensors", text: "Realcartoon卡通" },
    { value: "4Guofeng4XL_v12.safetensors", text: "Guofeng国风" },
    { value: "autismmixSDXL_autismmixPony.safetensors", text: "autismmixSDXL二次元" },
]

const COUPLE_CHECKPOINTS = [
    { value: "dreamshaperXL_lightningDPMSDE.safetensors", text: "DreamshaperLight" },
    { value: "juggernautXL_v9Rdphoto2Lightning.safetensors", text: "JuggernautLight" },
    { value: "realvisxlV40_v40LightningBakedvae.safetensors", text: "realvisxlLight" },
]

const LORAS = [
    { value: "", text: "无" },
    { value: "国风插画SDXL.safetensors", text: "国风插画" },
    { value: "3D模型丨可爱化SDXL版_v2.0.safetensors", text: "3D模型" },
    { value: "SDXLFaeTastic2400.safetensors", text: "FaeTastic幻想" },
    { value: "princess_xl_v2.safetensors", text: "princess公主" },
    { value: "LineAniRedmondV2-Lineart-LineAniAF.safetensors", text: "Line线条" },
    { value: "last.safetensors", text: "last" },
    { value: "cutedoodle_XL-000012.safetensors", text: "cutedoodle可爱" },
    { value: "StudioGhibli.Redmond-StdGBRRedmAF-StudioGhibli.safetensors", text: "StudioGhibli漫画" },
    { value: "StickersRedmond.safetensors", text: "Stickers贴纸" },
    { value: "xl_more_art-full_v1.safetensors", text: "more_art艺术" },
    { value: "CLAYMATE_V2.03_.safetensors", text: "CLAYMATE泥偶" },
    { value: "Harrlogos_v2.0.safetensors", text: "Harrlogos哈利波特" },
    { value: "ChineseDragon_v2.safetensors", text: "中国龙" },
    { value: "momoko_new.safetensors", text: "二次元画风桃子" },
    { value: "p4tr0nusXLP.safetensors", text: "Patronus" },
    { value: "add-detail-xl.safetensors", text: "增加细节" },
    { value: "MJ52.safetensors", text: "Midjourney" },
    { value: "LogoRedmondV2-Logo-LogoRedmAF.safetensors", text: "logo" },
]

const IMAGE_SCALE = {
    "1": "16:9",
    "2": "3:2",
    "3": "5:4",
    "4": "1:1",
    "5": "4:5",
    "6": "2:3",
    "7": "9:16"
};

const ART_PHOTO_SCALE = [
    { value: "1024:768", text: "横版" },
    { value: "1024:1024", text: "正方形" },
    { value: "768:1024", text: "竖版" },
]

const IMG2IMG_DIVERGENCE = [
    { value: "0.35", text: "低" },
    { value: "0.5", text: "中" },
    { value: "0.75", text: "高" },
]

const ID_PHOTO_EXPOSURE = [
    { value: "8", text: "低" },
    { value: "10", text: "中" },
    { value: "15", text: "高" },
]

const ID_PHOTO_LAY_NUM = [
    { value: "6", text: "6张" },
    { value: "8", text: "8张" },
    { value: "12", text: "12张" },
    { value: "16", text: "16张" },
]

const WS_URL = "ws://127.0.0.1:8188/ws?clientId=alienfist"

const STICKERS_TIMEOUT = 240000
const ID_PHOTO_TIMEOUT = 200000
const IMG2IMG_TIMEOUT = 180000
const TXT2IMG_TIMEOUT = 100000
const CHANGE_FACE_TIMEOUT = 120000

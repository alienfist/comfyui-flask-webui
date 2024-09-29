import re
import random
import hashlib
import requests
from datetime import datetime, timedelta
from config import BD_FY_CONFIG, TEMP_FOLDER


def gen_random_seed():
    return random.randint(10 ** 14, 10 ** 15 - 1)


def get_past_temp_folders(days=7):
    now = datetime.now()
    return [
        f'{TEMP_FOLDER}image/{(now - timedelta(days=i + 1)).strftime("%Y%m%d")}/'
        for i in range(days)
    ]


def include_chinese(content):
    cn_str = r'[\u4e00-\u9fa5]'
    return bool(re.search(cn_str, content))


def baidu_translate_tool(content, method="zh_to_en"):
    res_dict = {
        "code": 0,
        "text": "",
    }
    if method == "zh_to_en" and not include_chinese(content):
        res_dict["code"] = 1
        res_dict["text"] = content
        return res_dict
    try:
        content = content.strip()
        baidu_url =  BD_FY_CONFIG["url"]
        appid = BD_FY_CONFIG["appid"]
        secretKey = BD_FY_CONFIG["secretKey"]
        salt = random.randint(12345, 99999)  # 随机salt
        sign = appid + str(content) + str(salt) + secretKey  # 签名=appid+q+salt+密钥，MD5加密
        md = hashlib.md5()
        md.update(sign.encode())
        sign = md.hexdigest()
        if method == "en_to_zh":
            params = {
                'q': content,
                'from': 'en',
                'to': 'zh',
                'appid': appid,
                'salt': salt,
                'sign': sign
            }
        else:
            params = {
                'q': content,
                'from': 'zh',
                'to': 'en',
                'appid': appid,
                'salt': salt,
                'sign': sign
            }
        try_time = 0
        while True:
            if try_time >= 5:
                print("bd_translate_tool try time over: %s" % content)
                res_dict["text"] = "try time over"
                return res_dict
            try:
                res = requests.get(baidu_url, params=params, timeout=10)
                res.raise_for_status()
                res.encoding = 'utf-8'
                temp_json = res.json()
                if temp_json.get("error_code") == "54004":
                    print("baidu key is no money: %s" % BD_FY_CONFIG.get("appid"))
                    res_dict["text"] = "no money"
                    return res_dict
                if temp_json.get("error_code") == "54000":
                    res_dict["code"] = 1
                    res_dict["text"] = content
                    return res_dict
                text = temp_json["trans_result"][0]["dst"]  # 获取返回结果
                res_dict["code"] = 1
                res_dict["text"] = text
                return res_dict
            except:
                try_time += 1
                continue
    except Exception as e:
        print("Exception bd_translate_tool %s" % e)
        res_dict["text"] = "exception happen"
        return res_dict


def get_md5(text, num=16):
    try:
        m = hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
        res = m[0:num]
        return res
    except Exception as e:
        print(e)
        time_str = datetime.now().strftime("%Y%m%d%H%M%s")
        res = time_str[:num]
        return res

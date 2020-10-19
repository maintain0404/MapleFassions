import requests
import base64
import numpy as np
import cv2
from PIL import Image
from io import BytesIO

URL_BASE = 'https://maplestory.io/api'

def get_images(item_id, max_tries = 3, motion = 'stand1',
    region = 'kms', version = '338'):
    tries = 0
    base64_img_parts = []
    url = f'{URL_BASE}/{region}/{version}/item/{item_id}'
    while True:
        res = requests.get(url)
        if res.status_code is 200:
            break
        elif tries < max_tries:
            tries += 1
        else:
            raise Exception(f'download failed with status_code{res.status_code} from url')
    
    res_dct = res.json()
    # 1프레임의 이미지 부분들만 수집
    base64_img_parts = res_dct['frameBooks'][motion]['frames'][0]['effects'].values()
    img_arrays = []
    for img_info in base64_img_parts:
        img_arrays.append(np.asarray(Image.open(BytesIO(base64.b64decode(img_info['image'])))))
    return img_arrays

def get_list(category, subCategory, is_cash = True, region = 'kms', version = '338', max_tries = 3):
    url = f'{URL_BASE}/{region}/item/list'
    querystring = {
        'overallCategory' : 'Equip',
        'category' : category,
        'subcategory' : subCategory,
        'cash' : is_cash
        }
    while True:
        res = requests.get(url, params = querystring)
        if res.status_code is 200:
            break
        elif tries < max_tries:
            tries += 1
        else:
            raise Exception(f'download failed with status_code{res.status_code} from url')


def show_image(img):
    img_to_show = Image.fromarray(imgs, 'RGBA')
    img_to_show.show()
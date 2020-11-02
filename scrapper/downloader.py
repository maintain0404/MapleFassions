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

def get_stand_img(item_id, max_tries = 3):
    url = 'https://maplestory.io/api/character/{"itemId":2000,"alpha":0,"region":"KMS","version":"338"},{"itemId":12000,"alpha":0,"region":"KMS","version":"338"},{"itemId":' + str(item_id) + ',"region":"KMS","version":"338"}/stand1/'
    
    res = None
    tries = 0
    while True:
        res = requests.get(url)
        if res.status_code is 200:
            break
        elif tries < max_tries:
            tries += 1
        else:
            raise Exception(f'download failed with status_code{res.status_code} from url')
    
    img_array = np.asarray(Image.open(BytesIO(res.content)))
    return img_array

def get_name(item_id, max_tries = 3):
    url = f'https://maplestory.io/api/KMS/339/item/{item_id}'
    res = None
    tries = 0
    while True:
        res = requests.get(url)
        if res.status_code is 200:
            break
        elif tries < max_tries:
            tries += 1
        else:
            raise Exception(f'download failed with status_code{res.status_code} from url')
    
    return res.json()['name']

def get_list(category, subCategory, is_cash = True, region = 'kms', version = '338', max_tries = 3):
    url = f'{URL_BASE}/{region}/{version}/item/list'
    querystring = {
        'overallCategoryFilter' : 'Equip',
        'categoryFilter' : category,
        'subCategoryFilter' : subCategory,
        'cash' : is_cash
        }

    res = {}
    tries = 0
    while True:
        res = requests.get(url, params = querystring)
        if res.status_code is 200:
            break
        elif tries < max_tries:
            tries += 1
        else:
            raise Exception(f'download failed with status_code{res.status_code} from url')
    
    if res is not None:
        return res

def show_image(img):
    img_to_show = Image.fromarray(imgs, 'RGBA')
    img_to_show.show()
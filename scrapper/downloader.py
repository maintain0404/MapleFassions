import requests
import base64
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import settings

class Downloader:
    def __init__(self, version = settings.VERSION,
        region = settings.REGION, max_tries = 3, raise_error = True):
        self.version = version
        self.max_tries = max_tries
        self.raise_error = raise_error

    def execute(self, url, querystring = {}):
        result = None
        tries = 0
        while True:
            result = requests.get(url, params=querystring)
            if result.status_code is 200:
                break
            elif tries < self.max_tries:
                tries += 1
            else:
                if self.raise_error:
                    raise Exception(f'Request failed with statuc code {result.status_code} from {url}')
                else:
                    result = None
                    break
        
        return result

    def get_image_frames(self, item_id, motion = 'stand1'):
        tries = 0
        base64_img_parts = []
        url = f'{settings.URL_BASE}/{self.region}/{self.version}/item/{item_id}/{motion}'
        res = self.execute(url)    
        res_dct = res.json()
        # 1프레임의 이미지 부분들만 수집
        base64_img_parts = res_dct['frameBooks'][motion]['frames'][0]['effects'].values()
        img_arrays = []
        for img_info in base64_img_parts:
            img_arrays.append(np.asarray(Image.open(BytesIO(base64.b64decode(img_info['image'])))))
        
        return img_arrays

    def get_image(self, item_id, motion = 'stand1', show = False):
        urlbase = f'{settings.URL_BASE}/character/'
        base = f'{{"itemId":2000,"alpha":0,"region":"{self.region}","version":"{self.version}"}},'
        base2 = f'{{"itemId":12000,"alpha":0,"region":"{self.region}","version":"{self.version}"}},'
        item = f'{{"itemId":{item_id},"region":"{self.region}","version":"{self.version}"}}/{motion}/'
        url = urlbase + base + base2 + item

        result = self.execute(url)
        img_array = np.asarray(Image.open(BytesIO(result.content)))
        if show:
            Image.fromarray(img_array, 'RGBA').show()
        return img_array

    def get_name(self, item_id)
        url = f'https://maplestory.io/api/KMS/339/item/{item_id}'
        result = self.execute(url)
        return result.json()['name']

    def get_list(category, subCategory, is_cash = True):
        url = f'{settings.URL_BASE}/{self.region}/{self.version}/item/list'
        querystring = {
            'overallCategoryFilter' : 'Equip',
            'categoryFilter' : category,
            'subCategoryFilter' : subCategory,
            'cash' : is_cash
            }

        res = self.execute(url, querystring = querystring)
        if res is not None:
            return res

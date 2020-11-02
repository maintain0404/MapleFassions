import db
from classifier import hsi_classify
from downloader import get_list, get_stand_img, get_name
import json

def add_item(item_id, name, category):
    img = get_stand_img(item_id)
    hsi_dict = dict(hsi_classify(img))
    HSI = ', '.join(map(lambda k, v: f'"{int(k)}":{v}', hsi_dict.keys(), hsi_dict.values()))
    db.create(
        '''
        INSERT INTO item (id, name, category, HSI)
        VALUES (%s, %s, %s, %s)
        ''', (item_id, name, category, '{' + HSI + '}',)
    )
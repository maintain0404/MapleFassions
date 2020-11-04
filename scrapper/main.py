import db
from classifier import hsi_classify
from downloader import Downloader
import psycopg2.errors
import json

downloader = Downloader()

def add_item(item_id, name, category):
    errors = {}
    try:
        img = downloader.get_image(item_id)
        hsi_dict = dict(hsi_classify(img))
        HSI = ', '.join(map(lambda k, v: f'"{int(k)}":{v}', hsi_dict.keys(), hsi_dict.values()))
        db.write(
            '''
            INSERT INTO item (id, name, category, HSI)
            VALUES (%s, %s, %s, %s)
            ''', (item_id, name, category, '{' + HSI + '}',)
        )
    except psycopg2.errors.UniqueViolation:
        print('중복')
        pass
    except Exception as err:
        errors[item_id] = err
    else:
        print(name)
    finally:
        return errors

def update_items(item_list):
    errors = {}
    
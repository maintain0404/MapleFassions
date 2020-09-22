import numpy as np
import json
from collections import OrderedDict

COLORS = json.load(open('rgb_colors.json', 'r'))

def classify(img):
    color_distances = {}
    for name, rgbcode in COLORS.items():
        color_distance = np.sqrt(
            np.sum(
                np.power(
                    np.array(img[:,:,0:3], dtype=np.uint32) - rgbcode,
                    2
                ),
                axis = 2
            )
        ) * img[:,:,3] / 255
        color_distances[name] = color_distance
    temp = np.array(list(color_distances.values()))
    print(temp.shape)
    res = np.full(temp.shape[1:3], 20, dtype = np.int64)
    print(res.shape)
    for i in range(temp.shape[1]):
        for j in range(temp.shape[2]):
            res[i, j] = np.argmin(temp[:,i,j])
    print(res)
    color_indexes = np.bincount(np.ravel(res))
    print(color_indexes)
    return list(COLORS.keys())[color_indexes.argmax()]

    ## 과도하게 흰색으로 추정되고 있음
    ## 투명한 곳이 흰색으로 판정되는 문제가 있는듯
    ## 또한 없는 색이 컬러 인덱스에서 누락되어 잘못된 판정이 있을 수 있음
    

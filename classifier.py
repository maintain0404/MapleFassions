import numpy as np
import json
from collections import OrderedDict, Counter

COLORS = json.load(open('rgb_colors.json', 'r'))

def rgb_classify(img):
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
        )
        color_distances[name] = color_distance
    temp = np.array(list(color_distances.values()))
    print(temp.shape)
    res = np.full(temp.shape[1:3], 20, dtype = np.int64)
    print(res.shape)
    for i in range(temp.shape[1]):
        for j in range(temp.shape[2]):
            if img[i,j,3] != 0:
                res[i, j] = np.argmin(temp[:,i,j])
            else:
                res[i, j] = -1
    color_indexes = Counter(np.ravel(res))
    return color_indexes

    ## 과도하게 흰색으로 추정되고 있음
    ## 투명한 곳이 흰색으로 판정되는 문제가 있는듯
    ## 또한 없는 색이 컬러 인덱스에서 누락되어 잘못된 판정이 있을 수 있음

def hsi_classify(img):
    color_distances = []
    R, G, B, A = (img[:,:,0].astype(np.float128), img[:,:,1].astype(np.float128),
        img[:,:,2].astype(np.float128), img[:,:,3].astype(np.float128))
    
    # 채도 구하기
    saturation = 1 - 3 * (np.amin(img[:,:,0:3], axis = 2)/(R + G + B))

    # 색상 구하기
    hue_numerator = ((R - G) + (R - B)) * 0.5
    print(hue_numerator)
    hue_denominator = np.sqrt(np.square(R - G) + (R - B) * (G - B))
    print(hue_denominator)
    print(hue_numerator / hue_denominator)
    hue = np.rad2deg(np.arccos(hue_numerator / hue_denominator))
    idx_to_reverse = np.where(img[:,:,2] > img[:,:,1])
    x, y = idx_to_reverse
    for idx in range(len(idx_to_reverse[0])):
        hue[x[idx], y[idx]] = 360 - hue[x[idx], y[idx]]

    # 명도 구하기
    intensity = (R + G + B) / 3

    # hsia
    hsia = np.array([hue, saturation, intensity, A])   

    return hsia

import numpy as np
import json
from collections import OrderedDict, Counter
from settings import COLOR_CODE, COLOR_HUE

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

def hue_distance(a, b):
    dstnc = abs(a - b)
    return dstnc if dstnc < 180 else abs(360 - dstnc)

def define_hue_color(hue_value):
    for k, v in HSI_COLORS.items():
        if hue_distance(hue_value, v) <= 15:
            return k
    
def hsi_classify(img):
    color_distances = []
    R, G, B, A = (img[:,:,0].astype(np.float128), img[:,:,1].astype(np.float128),
        img[:,:,2].astype(np.float128), img[:,:,3].astype(np.float128))
    
    # 채도 구하기
    saturation = 1 - 3 * (np.amin(img[:,:,0:3], axis = 2)/(R + G + B))

    # 색상 구하기
    hue_numerator = ((R - G) + (R - B)) * 0.5
    hue_denominator = np.sqrt(np.square(R - G) + (R - B) * (G - B))
    hue = np.rad2deg(np.arccos(hue_numerator / hue_denominator))
    idx_to_reverse = np.where(img[:,:,2] > img[:,:,1])
    for x, y in zip(idx_to_reverse[0], idx_to_reverse[1]):
        hue[x, y] = 360 - hue[x, y]
    # x, y = idx_to_reverse
    # for idx in range(len(idx_to_reverse[0])):
    #     hue[x[idx], y[idx]] = 360 - hue[x[idx], y[idx]]

    # 명도 구하기
    intensity = (R + G + B) / 3

    # hsia
    hsia = np.array([hue, saturation, intensity, A])
    
    nans = np.where(np.isnan(hue) == True)
    # nan지점을 -30 초기화
    for x, y in zip(nans[0], nans[1]):
        hue[x, y] = -30
    
    # 색상코드로 변환
    result = np.add(np.rint(np.divide(hue, 30)), 1)
    reds = np.where(result == 13)
    for x, y in zip(reds[0], reds[1]):
        result[x, y] = 1

    # 무채색 분리
    achromatic = np.where(saturation < 0.1)
    for x, y in zip(achromatic[0], achromatic[1]):
        if intensity[x, y] > 192:
            result[x, y] = COLOR_CODE.WHITE
        elif intensity[x, y] < 64:
            result[x, y] = COLOR_CODE.BLACK
        else:
            result[x, y] = COLOR_CODE.GRAY

    return Counter(np.ravel(result))
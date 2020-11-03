URL_BASE = 'https://maplestory.io/api'
VERSION = '339'
REGION = 'KMS'

class IntTypes:
    @classmethod
    def code2type(cls, code_):
        if isinstance(code_, int):
            for k, v in cls.__dict__.items():
                if v is code_:
                    return k
            raise ValueError(f'Invalid {cls.__name__} code')
        else:
            raise TypeError(f'{cls.__name__} code must be int')
        

    @classmethod
    def type2code(cls, type_):
        if isinstance(type_, str) and '_' in type_:
            result = cls.__dict__.get(type_.upper())
            if result:
                return result
            else:
                raise ValueError(f'Invalid {cls.__name__} type')
        else:
            raise TypeError(f'{cls.__name__} type must be string')
        

class COLOR_CODE(IntTypes):
    TRANSPARENT = 0
    RED = 1
    ORANGE = 2
    YELLOW = 3
    YELLOWGREEN = 4
    GREEN = 5
    TURQUOISE = 6
    CYAN = 7
    COBALT = 8
    BLUE = 9
    PURPLE = 10
    MARGENTA = 11
    ROSE = 12
    BLACK = 13
    WHITE = 14
    GRAY = 15

class COLOR_RGB(IntTypes):
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    GRAY = [128, 128, 128]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    YELLOW = [255, 255, 0]
    PURPLE = [0, 128, 128]
    SKYBLUE = [135, 206, 235]
    YELLOWGREEN = [173, 255, 47]
    PINK = [255, 192, 203]
    BROWN = [139, 69, 19]
    ORANGE = [255, 140, 0]
    NAVY = [0, 0, 128]
    VIOLET = [238, 130, 238]

class COLOR_HUE(IntTypes):
    RED = 0
    ORANGE = 30
    YELLOW = 60
    YELLOWGREEN = 90
    GREEN = 120
    TURQUOISE = 150
    CYAN = 180
    COBALT = 210
    BLUE = 240
    PURPLE = 270
    MARGENTA = 300
    ROSE = 330

class ITEM(IntTypes):
    HAT = 100
    FACE = 101
    EYE = 102
    EAR = 103
    TOP = 104
    OVERALL = 105
    BOTTOM = 106
    SHOES = 107
    GLOVE = 108
    SHIELD = 109
    CAPE = 110
    CASHWEAPON = 170
    

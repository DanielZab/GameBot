#Imports
import logging
import discord
import os
from dotenv import load_dotenv
from PIL import Image
import numpy
import cv2
from copy import deepcopy
from moviepy.editor import VideoFileClip

# pylint: disable=no-member

class Img:
    '''
    Image Class containing the image
    '''
    generator = 0
    def __init__(self, img, x_size=0, y_size=0, pos_x=0, pos_y=0):
        '''
        Initialize instance
        '''
        if not Img.generator:
            Img.generator = Img.generate()
        self.id = next(Img.generator)
        if isinstance(img, Image.Image):
            self.image = img
        if isinstance(img, Img):
            self.image = img.image
            self.pos_x = img.pos_x
            self.pos_y = img.pos_y
        else:
            self.image = Image.open(img)
            self.pos_x = pos_x
            self.pos_y = pos_y
            if x_size and y_size:
                self.image = self.image.resize((x_size, y_size))

    @staticmethod
    def generate():
        '''
        Generate unique id
        '''
        i = 0
        while True:
            yield i
            i += 1


    def __add__(self, other):
        '''
        Merge images when adding
        '''
        s = deepcopy(self)
        o = deepcopy(other)
        s.image.paste(o.image, (round(o.pos_x), round(o.pos_y)), o.image)
        return s

    def __hash__(self):
        '''
        Defined to enable the use as a key in a dictionary
        '''
        return hash(self.id)

    def __eq__(self, other):
        '''
        Defined to enable the use as a key in a dictionary
        '''
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def convert(self):
        '''
        Convert from RGB to BGR format
        '''
        pil_image = self.image.convert('RGB') 
        open_cv_image = numpy.array(pil_image) 
        # Convert RGB to BGR
        self.image = open_cv_image[:, :, ::-1].copy()
        return self

    def move(self, x, y):
        '''
        Reassign position
        '''
        self.pos_x = x
        self.pos_y = y


def make_video(MAP, dic):
    '''
    Creates video
    '''
    #Get length of longest list
    moves = max(len(e) for e in dic.values())
    images = []
    frame = MAP
    #Make image of starting positions
    for img, pos_list in dic.items():
        img.move(*pos_list[0])
        frame = frame + img
    
    for x in range(5):
        images.append(deepcopy(frame))

    #Make frames of every move
    for m in range(moves - 1):
        move_list = dict()
        for img, pos_list in dic.items():
            try:
                temp_move = (pos_list[m], pos_list[m + 1])
                move_list[img] = temp_move
            except IndexError:
                pass
        logging.info(f'Visualizing move {m}')
        images.extend(make_move(move_list, MAP))
        logging.info(f'Finished visualizing move {m}')

    #Creating videowriter
    logging.info('Creating Videowriter')
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25, (MAP.image.width, MAP.image.height))
    logging.info('Created Videowriter')
 
    #Writing video
    logging.info('Writing video')
    for i in range(len(images)):
        x = images[i]
        x = x.convert()
        out.write(x.image)
    logging.info('Finished writing video')
    out.release()

def make_move(li, MAP):
    '''
    Create images of a single move
    '''
    splitted_moves = dict()
    for img, pos_list in li.items():
        splitted_moves[img] = split(pos_list)
    frames = []
    for i in range(max(len(e) for e in splitted_moves.values())):
        frame = MAP
        for img, pos_list in splitted_moves.items():
            img.move(*pos_list[i])
            frame = frame + img
        frames.append(frame)
    return frames

        
        
def split(li):
    '''
    Splits the vector in smaller splits
    '''
    split = 20 #Divide vecotr in how many sections
    extra = 5 #Add how many extra frames at the end

    #Determine step per frame
    step_x = (li[1][0] - li[0][0]) / split
    step_y = (li[1][1] - li[0][1]) / split

    #Define starting coordinates
    start_x = li[0][0]
    start_y = li[0][1]

    splits = []

    #Add smaller splits to list
    for i in range(1, split + 1):
        splits.append((i * step_x + start_x, i * step_y + start_y))

    #Add extra coordinates, which will serve as pausing frames
    for i in range(extra):
        splits.append(li[1])
    return splits




if __name__ == '__main__':
    #Logging setup
    FORMAT = '[%(levelname)s] - %(asctime)s: %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=FORMAT,
                        filename='debug.log',
                        datefmt='%H:%M:%S')

    logging.info('-----------New Boot-----------')

    #Load environment variables
    load_dotenv()
    logging.info('Loading environment variables')
    AUTH_TOKEN = os.getenv('TOKEN')
    logging.info('Finished loading environment variables')

    #Load images
    logging.info('Loading assets')
    MAP = Img('Assets\\Map.jpg')
    red = Img('Assets\\Red.png', 80, 80)
    white = Img('Assets\\White.png', 80, 80)
    logging.info('Finished loading assets')
    
    destinations = {
        1: (1373, 121),
        2: (1983, 76),
        3: (2375, 87),
        4: (2611, 71),
        5: (3568, 92),
        6: (3863, 94),
        7: (4166, 107),
        8: (1254, 257),
        9: (1492, 271),
        10: (2183, 258),
        11: (2362, 291),
        12: (2511, 264),
        13: (2784, 243),
        14: (3063, 189),
        15: (3353, 163),
        16: (3630, 262),
        17: (4147, 353),
        18: (1115, 370),
        19: (1337, 400),
        20: (1628, 336),
        21: (1913, 453),
        22: (2372, 499),
        23: (2600, 381),
        24: (2952, 387),
        25: (3104, 428),
        26: (3337, 252),
        27: (3378, 390),
        28: (3484, 340),
        29: (3872, 422),
        30: (4245, 399),
        31: (1206, 479),
        32: (1526, 561),
        33: (1783, 519),
        34: (2201, 564),
        35: (2447, 630),
        36: (2546, 649),
        37: (2706, 504),
        38: (3031, 519),
        39: (3179, 485),
        40: (3433, 588),
        41: (3544, 549),
        42: (4156, 554),
        43: (1055, 608),
        44: (1390, 674),
        45: (1614, 722),
        46: (1822, 654),
        47: (1990, 618),
        48: (2252, 732),
        49: (2628, 744),
        50: (2783, 639),
        51: (3107, 656),
        52: (3275, 608),
        53: (3463, 419),
        54: (3589, 682),
        55: (3878, 677),
        56: (4260, 709),
        57: (1158, 735),
        58: (1481, 774),
        59: (1548, 853),
        60: (1671, 833),
        61: (1885, 865),
        62: (1998, 826),
        63: (2276, 970),
        64: (2445, 937),
        65: (2620, 898),
        66: (2727, 876),
        67: (2909, 846),
        68: (3139, 794),
        69: (3349, 777),
        70: (3609, 824),
        71: (3838, 822),
        72: (4080, 842),
        73: (1157, 866),
        74: (1272, 1003),
        75: (1428, 958),
        76: (1633, 948),
        77: (1770, 1052),
        78: (1931, 1032),
        79: (2051, 1008),
        80: (2327, 1064),
        81: (2558, 1103),
        82: (2642, 1042),
        83: (2869, 1013),
        84: (3019, 941),
        85: (3151, 893),
        86: (3382, 979),
        87: (3624, 1036),
        88: (3729, 1063),
        89: (3819, 986),
        90: (3990, 987),
        91: (4225, 988),
        92: (1069, 1111),
        93: (1084, 1210),
        94: (1290, 1167),
        95: (1386, 1152),
        96: (1870, 1224),
        97: (1976, 1187),
        98: (2115, 1141),
        99: (2247, 1160),
        100: (2478, 1228),


    }
    moves = {
        white: [(200, 500),(1100, 1800),(3000, 90),(200, 10)],
        red: [(100, 100), (200, 200), (300, 300), (400, 400)]
    }

    logging.info('Making video')
    make_video(MAP, moves)
    logging.info('Finished making video')

    #clip = (VideoFileClip("project.avi"))
    #clip.write_gif("output.gif")
#TODO Setup Bot
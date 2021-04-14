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
    for m in range(moves - 1):
        move_list = dict()
        for img, pos_list in dic.items():
            try:
                temp_move = (pos_list[m], pos_list[m + 1])
                move_list[img] = temp_move
            except IndexError:
                pass
        images.extend(make_move(move_list, MAP))

    #Make video
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25, (MAP.image.width/2, MAP.image.height))
 
    for i in range(len(images)):
        x = images[i]
        x = x.convert()
        out.write(x.image)
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
    logging.basicConfig(level=logging.DEBUG,
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
    MAP = Img('Assets\\Map.jpg')
    red = Img('Assets\\Red.png', 80, 80)
    
    moves = {
        red: [(200, 500),(1100, 1800),(3000, 90),(200, 10)]
    }

    make_video(MAP, moves)

    #clip = (VideoFileClip("project.avi"))
    #clip.write_gif("output.gif")
#TODO Setup Bot
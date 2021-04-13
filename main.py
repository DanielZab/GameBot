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

class Img:
    '''
    Image Class containing the image
    '''
    def __init__(self, img, x_size=0, y_size=0, pos_x=0, pos_y=0):
        if isinstance(img, Image.Image):
            self.img = img
        elif isinstance(img, Img):
            self.image = img.image
            self.x_size = img.x_size
            self.y_size = img.y_size
            self.pos_x = img.pos_x
            self.pos_y = img.pos_y
        else:
            self.image = Image.open(img)
            self.x_size = x_size
            self.y_size = y_size
            self.pos_x = pos_x
            self.pos_y = pos_y
            if x_size and y_size:
                self.image = self.image.resize((x_size, y_size))

    def __add__(self, other):
        '''
        Merge images when adding
        '''
        s = deepcopy(self)
        o = deepcopy(other)
        s.image.paste(o.image, (o.pos_x, o.pos_y), o.image)
        return s

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
    maps = []
    for x in range(10):
        red.move(x*10, x*10)
        temp = MAP + red
        maps.append(temp.convert())
    
    #Make video
    out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, (4400, 2600))
 
    for i in range(len(maps)):
        out.write(maps[i].image)
    out.release()
    clip = (VideoFileClip("project.avi"))
    clip.write_gif("output.gif")
#TODO Setup Bot
import logging
import discord
import os
from dotenv import load_dotenv

#Logging setup
FORMAT = '[%(levelname)s] - %(asctime)s: %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT,
                    filename='debug.log',
                    datefmt='%H:%M:%S')

#Load environment variables
load_dotenv()
AUTH_TOKEN = os.getenv('TOKEN')
if __name__ == '__main__':
    pass
#TODO Setup Bot
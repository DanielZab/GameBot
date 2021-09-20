import requests
from dotenv import load_dotenv
import os

url = "https://discord.com/api/v8/applications/831611998641848330/guilds/387214698757750784/commands/"

load_dotenv()
AUTH_TOKEN = os.getenv('TOKEN')

json = {
    "name": "blep",
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Dog",
                    "value": "animal_dog"
                },
                {
                    "name": "Cat",
                    "value": "animal_cat"
                },
                {
                    "name": "Penguin",
                    "value": "animal_penguin"
                }
            ]
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False
        }
    ]
}
start = {
    "name": "start",
    "description": "Start a game",
    "options": [
        {
            "name": "game",
            "description": "Which game to play",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Scotland Yard",
                    "value": "Scotland Yard"
                }
            ]
        },
        {
            "name": "play_along",
            "description": "Do you want to be automatically added to the player list. Default is false",
            "type": 5,
            "required": False
        }
    ]
}

join = {
    "name": "join",
    "description": "Add player to current game's player list",
    "options": [
        {
            "name": "eligible",
            "description": "Whether or not eligible to become Mr. X. Default is True",
            "type": 5,
            "required": False
        },
        {
            "name": "who",
            "description": "Whom to add, self if not specified",
            "type": 6,
            "required": False
        }
    ]
}
confirm = {
    "name": "confirm",
    "description": "Confirm game settings and start the game"
}

colors = {
    "name": "colors",
    "description": "Show players and their matching colors"
}

pick = {
    "name": "pick",
    "description": "Pick a color",
    "options": [
         {
            "name": "color",
            "description": "Which color do you want?",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Red",
                    "value": "red"
                },
                {
                    "name": "Blue",
                    "value": "blue"
                },
                {
                    "name": "Yellow",
                    "value": "yellow"
                },
                {
                    "name": "Green",
                    "value": "green"
                },
                {
                    "name": "Orange",
                    "value": "orange"
                }
            ]
        },
        {
            "name": "who",
            "description": "Choose color for whom",
            "type": 6,
            "required": False
        }
    ]
}

end = {
    "name": "end",
    "description": "End the current game and create a video"
}

move = {
    "name": "move",
    "description": "Move to a certain position",
    "options": [
        {
            "name": "pos",
            "description": "Number of the station you want to move to",
            "type": 4,
            "required": True
        },
        {
            "name": "color",
            "description": "Which color do you want to move? (Use this to move bots)",
            "type": 3,
            "required": False,
            "choices": [
                {
                    "name": "Red",
                    "value": "red"
                },
                {
                    "name": "Blue",
                    "value": "blue"
                },
                {
                    "name": "Yellow",
                    "value": "yellow"
                },
                {
                    "name": "Green",
                    "value": "green"
                },
                {
                    "name": "Orange",
                    "value": "orange"
                }
            ]
        },
        {
            "name": "boost",
            "description": "Number of the second station, in case you want to move twice. (For Mr.X only)",
            "type": 4,
            "required": False
        }
    ]
}
# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {AUTH_TOKEN}"
}

commands = [pick, end, move]
def post(js):
    global url
    global headers

    r = requests.post(url, headers=headers, json=js)
    print(r.content)

def get():
    global url
    global headers
    global json
    r = requests.get(url, headers=headers)
    print(r.text)

for e in commands:
    post(e)
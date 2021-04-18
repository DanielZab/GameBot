import requests
from dotenv import load_dotenv
import os

url = "https://discord.com/api/v8/applications/831611998641848330/guilds/456109062833176598/commands"

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

# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {AUTH_TOKEN}"
}

def post():
    global url
    global headers
    global json

    r = requests.post(url, headers=headers, json=json)
    print(r.content)

def get():
    global url
    global headers
    global json
    r = requests.get(url, headers=headers)
    print(r.text)

get()
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import json
import random

app = Flask(__name__)
@app.route('/mm', methods = ['POST'])

def bot():
    def get_mood(inc_msg):
        moods = ['good', 'happy', 'sad', 'sed', 'cool', 'emotional', 'angry', 'great', 'ecstatic']
        for word in moods:
            if word in inc_msg:
                return word
        return 'greet'

    def get_song(curr_mood):
        CLIENT_ID = ''
        CLIENT_SECRET = ''
        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
        results = spotify.search(q=curr_mood, type='track', limit=10)
        rand_index = random.randint(0, 9)
        return results["tracks"]["items"][rand_index]["external_urls"]["spotify"]
    
    def get_weather(city):
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        API_KEY = ''
        moods = ['good', 'happy', 'sad', 'sed', 'cool', 'emotional', 'angry', 'great', 'ecstatic']

        if city.lower() != 'hi' and city.lower() != 'hello' and city.lower() not in moods :
            weather = json.loads(requests.get(base_url, params = {'q' : city, 'appid' : API_KEY}).content)
            weather_desc = weather['weather'][0]['description']
            cloud_perc = weather['clouds']['all']
            return (weather_desc, cloud_perc, city)
        else:
            return 'no_weather_data'
    

    incoming_msg = request.values.get('Body', '').lower()
    res = MessagingResponse()
    msg = res.message()
    responded = False
    curr_mood = get_mood(incoming_msg)
    moods = ['good', 'happy', 'sad', 'sed', 'cool', 'emotional', 'angry', 'great', 'ecstatic']
    curr_weather = get_weather(incoming_msg)
    ops = [curr_mood, curr_weather]
    ran = random.randint(0, 1)
    query = ops[ran]

    print(curr_mood)
    if(curr_mood != 'greet'):
        msg.body(f'''So, you're feeling {curr_mood} right now?\n''')
        msg.body(f'''And where are you located right now🛐''')
        responded = True
    elif(curr_mood == 'greet' and curr_weather == 'no_weather_data'):
        if 'hi' in incoming_msg or 'hello' in incoming_msg:
            msg.body('Hello to you, too!\nHow are you feeling right now?\n')
            responded = True
        else:
            msg.body("Sorry! I am just a rule-based bot right now. I can't understand that.😢")
            responded = True
    else:
        msg.body(f'''Alright. It feels like {curr_weather[0]} in {curr_weather[2]}.\nLet me suggest you this beautiful song:{get_song(query)}''')
        responded = True
    return str(res)

if __name__ == '__main__':
    app.run()

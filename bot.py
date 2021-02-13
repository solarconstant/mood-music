from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
@app.route('/mm', methods = ['POST'])

def bot():

    def get_mood(inc_msg):
        moods = ['good', 'happy', 'sad', 'sed', 'cool', 'emotional', 'angry', 'great', 'ecstatic']
        for word in moods:
            if word in inc_msg:
                return word
        return
    
    

    incoming_msg = request.values.get('Body', '').lower()
    res = MessagingResponse()
    msg = res.message()
    responded = False
    curr_mood = get_mood(incoming_msg)
    print(curr_mood)
    if(curr_mood):
        msg.body(f'''So, you're feeling {curr_mood} right now?\n
                Let me suggest this song: \n''')
    else:
        if 'hi' in incoming_msg or 'hello' in incoming_msg:
            msg.body('Hello to you, too!\nHow are you feeling right now?\n')
            responded = True
        else:
            msg.body("Sorry! I am just a rule-based bot right now. I can't understand that.😢")
            responded = True
    
    return str(res)

if __name__ == '__main__':
    app.run()
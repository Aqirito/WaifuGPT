from flask import (Blueprint, request)
import os
import json
from app.engine.chat import userInput
from app.voicevox_api.voicevox_engine_api import textInput
import pyaudio
import wave
import re
bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')

project_path = "c:\\users\\aqirito\\playground\\waifugpt\\backend\\app\\"

"""
"char_name"       : "Shikoku Metan"
"Normal"          : 2
"sweet"           : 0
"tsuntsun"        : 6
"Sexy"            : 4
"Whisper closely" : 36
"Whisper"         : 37
"""

def Synthesize(message):
    bot_response = userInput(message)
    bot_reply = bot_response.split(': ')[1]

    # Remove text between asterisks
    bot_reply_only = re.sub(r'\*.*?\*', '', bot_reply)
    if not bot_reply_only:
        bot_reply_only = bot_reply
    print("_____________________re", bot_reply_only)

    # Extract text between asterisks (*)
    emotions_raw = re.search(r'\*(.*?)\*', bot_reply)
    if emotions_raw:
        emotions = emotions_raw.group(1).split(" ")
        with open(os.path.join(project_path + "voicevox_api",'emotions.json'), 'r', encoding='utf-8') as f:
            emotions_data = json.load(f)
            happy_emotions = [word for word in emotions if word in emotions_data['happy_words']]
            sad_emotions = [word for word in emotions if word in emotions_data['sad_words']]
            anger_emotions = [word for word in emotions if word in emotions_data['anger_words']]
            
            if happy_emotions:
                print("___HAPPY___", happy_emotions)
                speaker_emotion = "0"
            elif sad_emotions:
                print("___SAD___", sad_emotions)
                speaker_emotion = "37"
            elif anger_emotions:
                print("___ANGER___", anger_emotions)
                speaker_emotion = "6"
            else:
                speaker_emotion = "2"
            textInput(speaker_emotion, bot_reply_only)
    else:
        textInput("2", bot_reply_only)
        playAudio()

    print("split name before", bot_reply)
    bot_reply.replace("\n", "<br>")
    return bot_reply

def playAudio():
    chunk = 1024
    wf = wave.open('app/voicevox_api/audio.wav', 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()


@bp.post('/chats')
def chats():
    params = request.get_json()
    messageText = params.get('messageText')
    get_reply = Synthesize(messageText)
    # TODO audio as blob and send it with text in the same object
    return {"bot_res": get_reply}
    # return send_file(os.path.join('api/output.wav'), mimetype='audio/wav', as_attachment=False)
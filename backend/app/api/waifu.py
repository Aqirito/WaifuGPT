from flask import (Blueprint, request)
import json
from app.engine.chat import userInput
from app.voicevox_api.voicevox_engine_api import textInput
import re
import base64
bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')
from dotenv import dotenv_values

config = dotenv_values(".env")
project_path = config["FLASK_PROJECT_PATH"]

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

    # Extract text between asterisks (*)
    emotions_raw = re.search(r'\*(.*?)\*', bot_reply)
    if emotions_raw:
        emotions = emotions_raw.group(1).split(" ")
        with open(project_path + "voicevox_api/emotions.json", 'r', encoding='utf-8') as f:
            emotions_data = json.load(f)
            happy_emotions = [word for word in emotions if word in emotions_data['happy_words']]
            sad_emotions = [word for word in emotions if word in emotions_data['sad_words']]
            anger_emotions = [word for word in emotions if word in emotions_data['anger_words']]
            closeup_emotions = [word for word in emotions if word in emotions_data['whisper_words']]
            
            if happy_emotions:
                print("___HAPPY___", happy_emotions)
                speaker_emotion = "0"
            elif sad_emotions:
                print("___SAD___", sad_emotions)
                speaker_emotion = "37"
            elif anger_emotions:
                print("___ANGER___", anger_emotions)
                speaker_emotion = "6"
            elif closeup_emotions:
                print("___WHISPER___", closeup_emotions)
                speaker_emotion = "36"
            else:
                speaker_emotion = "0"
            audio_data = textInput(speaker_emotion, bot_reply_only)
            # with open(project_path + '\\voicevox_api\\audio.wav', 'wb') as f:
            #     f.write(audio_data)
            # print("____________________________________", audio_data)
    else:
        audio_data = textInput("0", bot_reply_only)
        # with open(project_path + '\\voicevox_api\\audio.wav', 'wb') as f:
        #     f.write(audio_data)
        # print("____________________________________", audio_data)
        # playAudio()

    print("split name before", bot_reply)
    bot_reply.replace("\n", "<br>")
    # TODO send the emotions to the cleint seperately
    reply_splitted_emotions = {
        "reply": bot_reply_only,
        "emotions": emotions_raw.group(1).split(" ") if emotions_raw else None
    }

    print("________EMOTIONS REPLY__________")
    print(reply_splitted_emotions)

    # assuming the audio bytes are stored in a bytes object called 'audioBytes'
    audioBase64 = base64.b64encode(audio_data).decode('utf-8')

    bot_replies = json.dumps({'bot_reply': bot_reply, 'audio': audioBase64})
    # print(bot_replies)
    return bot_replies

# def playAudio():
#     chunk = 1024
#     wf = wave.open('app/voicevox_api/audio.wav', 'rb')

#     p = pyaudio.PyAudio()

#     stream = p.open(
#         format=p.get_format_from_width(wf.getsampwidth()),
#         channels=wf.getnchannels(),
#         rate=wf.getframerate(),
#         output=True
#     )

#     data = wf.readframes(chunk)

#     while data:
#         stream.write(data)
#         data = wf.readframes(chunk)

#     stream.close()
#     p.terminate()


@bp.post('/chats')
def chats():
    params = request.get_json()
    messageText = params.get('messageText')
    get_reply = Synthesize(messageText)
    return get_reply
    # return send_file(os.path.join('voicevox_api/output.wav'), mimetype='audio/wav', as_attachment=False)
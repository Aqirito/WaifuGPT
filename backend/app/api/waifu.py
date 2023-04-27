from flask import (Blueprint, request)
import json
from app.engine.chat import userInput
from app.voicevox_api.voicevox_engine_api import textInput
import re
import base64
import os
bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')
from googletrans import Translator
translator = Translator()

"""
"char_name"       : "Shikoku Metan"
"Normal"          : 2
"sweet"           : 0
"tsuntsun"        : 6
"Sexy"            : 4
"Whisper closely" : 36
"Whisper"         : 37
"""

"""
"char_name"       : "Kyūshū sora"
"Normal"          : 16
"sweet"           : 15
"tsuntsun"        : 18
"Sexy"            : 17
"Whisper closely" : 19
"""

def Synthesize(message):
    bot_response = userInput(message)
    bot_reply_split_name = bot_response.split(': ')[1]

    # Remove text between asterisks
    bot_reply_no_name = re.sub(r'\*.*?\*', '', bot_reply_split_name)
    print("_______________bot_reply_no_name______________", bot_reply_no_name)
    
    bot_reply_remove_newline = bot_reply_no_name.replace("\n", "")
    print("____________bot_reply_remove_newline__________", bot_reply_remove_newline)

    # Remove text between asterisks
    bot_reply_with_name = re.sub(r'\*.*?\*', '', bot_response)
    if not bot_reply_with_name:
        bot_reply_with_name = bot_response

    # Extract text between asterisks (*)
    emotions_raw = re.findall(r'\*(.*?)\*', bot_response)
    emotions_string = ' '.join(emotions_raw)
    print("_______________emotions_raw___________")
    print(emotions_raw)
    if emotions_string:
        emotions = emotions_string.split(" ")
        print("________emotions______")
        print(emotions)
        with open(os.path.abspath(os.path.join("app/voicevox_api", "emotions.json")), 'r', encoding='utf-8') as f:
            emotions_data = json.load(f)
            happy_emotions = [word for word in emotions if word in emotions_data['happy_words']]
            sad_emotions = [word for word in emotions if word in emotions_data['sad_words']]
            anger_emotions = [word for word in emotions if word in emotions_data['anger_words']]
            closeup_emotions = [word for word in emotions if word in emotions_data['whisper_words']]
            
            if closeup_emotions:
                print("___WHISPER___", closeup_emotions)
                speaker_emotion = "19"
            elif sad_emotions:
                print("___SAD___", sad_emotions)
                speaker_emotion = "16"
            elif anger_emotions:
                print("___ANGER___", anger_emotions)
                speaker_emotion = "18"
            elif happy_emotions:
                print("___HAPPY___", happy_emotions)
                speaker_emotion = "15"
            else:
                speaker_emotion = "16"
            audio_data = textInput(speaker_emotion, bot_reply_remove_newline)
            # with open(project_path + '\\voicevox_api\\audio.wav', 'wb') as f:
            #     f.write(audio_data)
            # print("____________________________________", audio_data)
    else:
        audio_data = textInput("16", bot_reply_remove_newline)
        # with open(project_path + '\\voicevox_api\\audio.wav', 'wb') as f:
        #     f.write(audio_data)
        # print("____________________________________", audio_data)
        # playAudio()

    replace_newline = bot_response.replace("\n", "<br>")

    # assuming the audio bytes are stored in a bytes object called 'audioBytes'
    audioBase64 = base64.b64encode(audio_data).decode('utf-8') if audio_data else None
    reply_splitted_emotions = {
        "bot_reply": replace_newline,
        "emotions": emotions_raw if emotions_raw else None,
        'audio': audioBase64
    }

    bot_replies = json.dumps(reply_splitted_emotions)
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
    translated_data = translator.translate(messageText, dest='en')
    translated_text = translated_data.text
    get_reply = Synthesize(translated_text)
    return get_reply
    # return send_file(os.path.join('voicevox_api/output.wav'), mimetype='audio/wav', as_attachment=False)
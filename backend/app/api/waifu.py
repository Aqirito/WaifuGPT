from flask import (Blueprint, request)
import json
from app.engine.chat import userInput
from app.voicevox_api.voicevox_engine_api import textInput
import re
import base64
import os

from dotenv import dotenv_values
config = dotenv_values(".env")
GGML_NAME = config["FLASK_GGML_NAME"]

from googletrans import Translator
translator = Translator()

bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')

# load GGML Model
from llama_cpp import Llama
print("loading model...")
model_path = os.path.abspath(os.path.join("app/models", GGML_NAME))
llm = Llama(model_path=model_path, n_ctx=2048)
print("model loaded success")

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
                speaker_emotion = "36"
            elif sad_emotions:
                print("___SAD___", sad_emotions)
                speaker_emotion = "37"
            elif anger_emotions:
                print("___ANGER___", anger_emotions)
                speaker_emotion = "6"
            elif happy_emotions:
                print("___HAPPY___", happy_emotions)
                speaker_emotion = "0"
            else:
                speaker_emotion = "2"
            audio_data = textInput(speaker_emotion, bot_reply_remove_newline)
            # with open(project_path + '\\voicevox_api\\audio.wav', 'wb') as f:
            #     f.write(audio_data)
            # print("____________________________________", audio_data)
    else:
        audio_data = textInput("2", bot_reply_remove_newline)
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


@bp.post('/chats')
def chats():
    params = request.get_json()
    messageText = params.get('messageText')
    translated_data = translator.translate(messageText, dest='en')
    translated_text = translated_data.text
    get_reply = Synthesize(translated_text)
    return get_reply
    # return send_file(os.path.join('voicevox_api/output.wav'), mimetype='audio/wav', as_attachment=False)

@bp.post('/questions')
def questions():
    params = request.get_json()
    messageText = params.get('messageText')
    output = llm(
        "Q:{} A: ".format(messageText),
        max_tokens=1024,
        stop=["Q:", "###"],
        echo=True,
        temperature=0.7,
        repeat_penalty=1.1
    )
    generated_text = output["choices"][0]["text"]
    questions = generated_text.split(" A: ")[0][2:].lstrip()
    answers = generated_text.split(" A: ")[1][1:].lstrip()
    # replace_newline = answers.replace("\n", "<br>")
    # remove_newline = answers.replace("\n", ",")

    # audio_data = textInput("2", remove_newline)

    # audioBase64 = base64.b64encode(audio_data).decode('utf-8') if audio_data else None

    with open(os.path.abspath(os.path.join("app/engine", "character.json")), "r") as f:
        f.seek(0)  # Move to the beginning of the file
        file_data = json.loads(f.read())

    output_json = {
        "questions": file_data['user_name'] + ": " + questions,
        "bot_reply": answers,
        "audio": None,
        "emotions": None,
    }
    return json.dumps(output_json)
from flask import (Blueprint, request, url_for, abort, send_file, jsonify)
from TTS.api import TTS
import os
import json
model_name = TTS.list_models()[12]
from app.engine.chat import userInput
import pyaudio
import wave
# Init TTS
tts = TTS(model_name)
bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')
def Synthesize(message):
    bot_answer = userInput(message)
    split_name = bot_answer.split(': ')[1]
    print("split name before", split_name)
    tts.tts_to_file(text=split_name, file_path=os.path.join('app/api/output.wav'))
    playAudio()
    split_name.replace("\n", "<br>")
    return split_name

def playAudio():
    chunk = 1024
    wf = wave.open('app/api/output.wav', 'rb')

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
    split_name = Synthesize(messageText)
    return {"bot_res": split_name}
    # return send_file(os.path.join('api/output.wav'), mimetype='audio/wav', as_attachment=False)
from flask import (Blueprint, request, url_for, abort, send_file)
from TTS.api import TTS
import os
model_name = TTS.list_models()[12]
from app.engine.persona import userInput
# Init TTS
tts = TTS(model_name)
bp = Blueprint('waifu', __name__, url_prefix='/api/waifu')

def Synthesize(message):
    bot_answer = userInput(message)
    tts.tts_to_file(text=bot_answer, file_path=os.path.join('app/api/output.wav'))

@bp.post('/chats')
def chats():
    try:
        params = request.get_json()
        messageText = params.get('messageText')
        Synthesize(messageText)
        return send_file(os.path.join('api/output.wav'), mimetype='audio/wav', as_attachment=False)
    
    except BaseException as err:
        return abort(400, err)
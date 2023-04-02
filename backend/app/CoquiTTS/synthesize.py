from TTS.api import TTS

model_name = TTS.list_models()[12]

# Init TTS
tts = TTS(model_name)

def Synthesize(message):
    tts.tts_to_file(text=message, speaker=tts.speakers[1], language=tts.languages[0], file_path="output.wav")
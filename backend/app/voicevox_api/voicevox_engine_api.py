import requests
import json
import re
from googletrans import Translator
from dotenv import dotenv_values

config = dotenv_values(".env")
url = config["FLASK_VX_API_URL"]
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


def textInput(speaker: str, text: str):
    assert isinstance(speaker, str), 'speaker must be a string'
    assert isinstance(text, str), 'text must be a string'

    print("______________textInput_________________")
    print(text)
    translated_data = translator.translate(text, dest='ja') if text else None
    translated_text = translated_data.text if translated_data else "..."
    params = {'speaker': speaker, 'text': translated_text}

    audio_query_response = requests.post(url + 'audio_query', params=params)

    if audio_query_response.status_code == 200:
        query_data = json.loads(audio_query_response.content.decode('utf-8'))
        kana_text = query_data['kana']
        if kana_text:
            print("_"*50+"kana"+"_"*50)
            print(kana_text)
            # accentPhrases(query_data, kana_text, speaker=speaker)
            params = {'speaker': speaker, 'is_kana': 'true', 'text': kana_text}

            accent_phrases_response = requests.post(url + 'accent_phrases', params=params)
            if accent_phrases_response.status_code == 200:
                new_phrases_str = accent_phrases_response.content.decode('utf-8')
                query_data_str = json.dumps(query_data)
                # replaceOldContent(new_phrases_str, query_data_str, speaker=kwargs['speaker'])
                new_query_data = re.sub(r'\[{.*}\]', new_phrases_str, query_data_str)
                """
                The regular expression r'\[{.*}\]' matches a string that begins with [{ and ends with }], and may contain any characters in between.
                The re.sub() function takes three arguments: the regular expression to match, the replacement string, and the input string.
                In this case, we use the contents of the newphrases.json file as the replacement string,
                and the contents of the query.json file as the input string.
                Finally, we write the updated data to the newquery.json file.
                """
                if new_query_data:
                    # synthesis(new_query_data, speaker=kwargs['speaker'])
                    params = {'speaker': speaker}
                    headers = {'Content-Type': 'application/json'}

                    synthesis_response = requests.post(
                        url + 'synthesis', params=params, headers=headers, data=new_query_data.encode('utf-8'))
                    # with open(project_path + '\\voicevox_api\\audio.wav', 'wb') as f:
                    #     f.write(response.content)
                    return synthesis_response.content
                else:
                    print("Error: Could not find pattern in query_data")
            else:
                print(accent_phrases_response.content)
        else:
            print("_"*50+"kana not found"+"_"*50)
    else:
        print(audio_query_response.content)

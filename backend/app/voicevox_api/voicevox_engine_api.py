import requests
import json
import re
from googletrans import Translator
url = 'http://localhost:50021/'
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

    print("_______________________________")
    print(text)

    translated_data = translator.translate(text, dest='ja')
    translated_text = translated_data.text

    params = {'speaker': speaker, 'text': translated_text}

    response = requests.post(url + 'audio_query', params=params)

    if response.status_code == 200:
        query_data = json.loads(response.content.decode('utf-8'))
        kana_text = query_data['kana']
        if kana_text:
            print("_"*50+"kana"+"_"*50)
            print(kana_text)
            accentPhrases(query_data, kana_text, speaker=speaker)
        else:
            print("_"*50+"kana not found"+"_"*50)
    else:
        print(response.content)

def accentPhrases(query_data: dict, kana_text: str, **kwargs):
    assert isinstance(query_data, dict), 'query_data must be a dictionary'
    assert isinstance(kana_text, str), 'kana_text must be a string'

    params = {'speaker': kwargs['speaker'], 'is_kana': 'true', 'text': kana_text}

    response = requests.post(url + 'accent_phrases', params=params)
    if response.status_code == 200:
        new_phrases_str = response.content.decode('utf-8')
        query_data_str = json.dumps(query_data)
        replaceOldContent(new_phrases_str, query_data_str, speaker=kwargs['speaker'])
    else:
        print(response.content)

def replaceOldContent(new_phrases_str, query_data_str, **kwargs):
    """
    In this example, we use the re.sub() function to replace the contents of the query.
    json file with the contents of the newphrases.json file.
    The regular expression r'\[{.*}\]' matches a string that begins with [{ and ends with }], and may contain any characters in between.
    The re.sub() function takes three arguments: the regular expression to match, the replacement string, and the input string.
    In this case, we use the contents of the newphrases.json file as the replacement string,
    and the contents of the query.json file as the input string.
    Finally, we write the updated data to the newquery.json file.
    """

    new_query_data = re.sub(r'\[{.*}\]', new_phrases_str, query_data_str)
    if new_query_data:
        synthesis(new_query_data, speaker=kwargs['speaker'])
    else:
        print("Error: Could not find pattern in query_data")


def synthesis(new_query_data, **kwargs):
    assert isinstance(new_query_data, str), 'new_query_data must be a string'

    params = {'speaker': kwargs['speaker']}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url + 'synthesis', params=params, headers=headers, data=new_query_data.encode('utf-8'))

    with open('audio.wav', 'wb') as f:
        f.write(response.content)


# if __name__=='__main__':
#     textInput(
#         text="hello, my name is sagiri.",
#         speaker="37"
#     )
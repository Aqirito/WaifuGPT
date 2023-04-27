import json
from .parsing import parse_messages_from_str
from .prompting import build_prompt_for
import os
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
CKPT_NAME = config["FLASK_CKPT_NAME"]
FILE_PATH = os.path.abspath(os.path.join("app/models", CKPT_NAME))

current_path = dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_path, "character.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    file_data = json.loads(f.read())

with open(os.path.join(current_path, "generation_settings.json"), "r") as f:
    f.seek(0)  # Move to the beginning of the file
    generation_settings = json.loads(f.read())


if FILE_PATH:
    from .model import build_model_and_tokenizer_for, run_raw_inference
    model, tokenizer = build_model_and_tokenizer_for(FILE_PATH)
else:
    model, tokenizer = None, None
if len(file_data["history"]) == 0 and file_data["char_greeting"] is not None:
    print(f"{file_data['char_name']}: {file_data['char_greeting']}")

def userInput(user_input: str):
      
    prompt = build_prompt_for(history=file_data['history'],
                              user_message=user_input,
                              char_name=file_data['char_name'],
                              char_persona=file_data['char_persona'],
                              example_dialogue=file_data['example_dialogue'],
                              world_scenario=file_data['world_scenario'])
    
    if model and tokenizer:
        model_output = run_raw_inference(model, tokenizer, prompt,
                                          user_input, **generation_settings)
    else:
        raise Exception(
            "Not using model,"
            "Nowhere to perform inference on.")

    generated_messages = parse_messages_from_str(model_output,
                                                  ["You", file_data['char_name']])
    logger.debug("Parsed model response is: `%s`", generated_messages)
    bot_message = generated_messages[0]
    replace_name = bot_message.replace('<USER>', file_data['user_name'])

    # # temporarry comment out
    # file_data['history'].append(f"You: {user_input}")
    # file_data['history'].append(bot_message)

    # # temporarry comment out
    # # Write the data to a JSON file
    # with open(os.path.join(current_path, "character.json"), "w") as outfile:
    #     json.dump(file_data, outfile)
    print("from chat_____________________", replace_name)
    return replace_name
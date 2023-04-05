from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
tokenizer = GPT2Tokenizer.from_pretrained("af1tang/personaGPT")
model = GPT2LMHeadModel.from_pretrained("af1tang/personaGPT")
if torch.cuda.is_available():
    model = model.cuda()
## utility functions ##
flatten = lambda l: [item for sublist in l for item in sublist]

def to_data(x):
    if torch.cuda.is_available():
        x = x.cpu()
    return x.data.numpy()

def to_var(x):
    if not torch.is_tensor(x):
        x = torch.Tensor(x)
    if torch.cuda.is_available():
        x = x.cuda()
    return x

def display_dialog_history(dialog_hx):
    for j, line in enumerate(dialog_hx):
        msg = tokenizer.decode(line)
        if j %2 == 0:
            print(">> User: "+ msg)
        else:
            print("Bot: "+msg)
            print()

def generate_next(bot_input_ids, do_sample=True, top_k=10, top_p=.92,max_length=1000, pad_token=tokenizer.eos_token_id):
    full_msg = model.generate(
        bot_input_ids,
        do_sample=do_sample,
        top_k=top_k,
        top_p=top_p, 
        max_length=max_length,
        pad_token_id=pad_token
    )
    msg = to_data(full_msg.detach()[0])[bot_input_ids.shape[-1]:]
    return msg

# get personality facts for conversation
personas = [
    "My name Is Chiharu Yamada" + tokenizer.eos_token,
    "I am 20 years old" + tokenizer.eos_token,
    "I work as a computer engineer" + tokenizer.eos_token,
    "My hobby is playing video games and watching romcom anime" + tokenizer.eos_token,
    "My favorite food is Bakso Ayam" + tokenizer.eos_token,
    "My favorite color is orange" + tokenizer.eos_token,
]
personas = tokenizer.encode(''.join(['<|p2|>'] + personas + ['<|sep|>'] + ['<|start|>']))


dialog_hx = []
def userInput(user_input=""):
    # encode the user input
    user_inp = tokenizer.encode(user_input + tokenizer.eos_token)
    # append to the chat history
    dialog_hx.append(user_inp)
        
    # generated a response while limiting the total chat history to 1000 tokens, 
    bot_input_ids = to_var([personas + flatten(dialog_hx)]).long()
    msg = generate_next(bot_input_ids)
    dialog_hx.append(msg)
    return tokenizer.decode(msg, skip_special_tokens=True)

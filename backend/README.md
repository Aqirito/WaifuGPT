
#  WaifuGPT Backend
## Character
*You can edit the character.json file inside app/engine/ folder suitable of your taste. hehe~*
*You can edit the emotions.json file inside app/voicevox_api folder.*
## Downloading models
*ONLY USE GGML LLAMA MODEL type for "expert mode"*
*ONLY USE PygmalionAI MODEL type for "Waifu mode"*
1. download model
- You can download any GGML model. im using [eachadea/ggml-vicuna-13b-1.1 at main (huggingface.co)](https://huggingface.co/eachadea/ggml-vicuna-13b-1.1/tree/main)or [TheBloke/wizardLM-7B-GGML · Hugging Face](https://huggingface.co/TheBloke/wizardLM-7B-GGML)
- You can **only use** PygmalionAI model. im using [PygmalionAI/pygmalion-6b · Hugging Face](https://huggingface.co/PygmalionAI/pygmalion-6b) or [PygmalionAI/pygmalion-350m · Hugging Face](https://huggingface.co/PygmalionAI/pygmalion-350m) for testing
2. move the downloaded models inside app/models *note that GGML model are choose one model.bin from repo. for example ggml-vic13b-uncensored-q5_1.bin* and *PygmalionAI model are the must be include entire folder cloned from repo.*
3. don't forget to edit the .env file

##  Installing and running voicevox/voicevox_engine API
1. Goto the official [voicevox/voicevox_engine github](https://github.com/VOICEVOX/voicevox_engine)
2. Goto release tabs and select one that are compatible in your workspace. I'm using windows so I choose windows with GPU + CUDA and download it.
3. open terminal and goto the downloaded file earlier.
```
$ cd D:\playground\windows-nvidia

$ .\run.exe

```
4. If you see something like below means your installations and running success
```
INFO: Started server process [29360]
INFO: Waiting for application startup.
reading C:\Users\Aqirito\AppData\Local\voicevox-engine\voicevox-engine\tmp6_prectj ... 62
emitting double-array: 100% |###########################################|
done!
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:50021 (Press CTRL+C to quit)
```
###  Installing and running using docker
*We will using voicevox API to synthesize the text*
*read the voicevox before install*
[voicevox/voicevox_engine github](https://github.com/VOICEVOX/voicevox_engine)
[voicevox/voicevox_engine docker hub](https://hub.docker.com/r/voicevox/voicevox_engine)
####  CPU
```
$ docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
$ docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```
####  GPU
```
$ docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
$ docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```
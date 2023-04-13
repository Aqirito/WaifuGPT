# WaifuGPT
### Installing and running voicevox/voicevox_engine API using docker
*We will using voicevox API to synthesize the text*
*read the voicevox before install* 
[voicevox/voicevox_engine github](https://github.com/VOICEVOX/voicevox_engine)
[voicevox/voicevox_engine docker hub](https://hub.docker.com/r/voicevox/voicevox_engine)
#### CPU
```
$ docker pull voicevox/voicevox_engine:cpu-ubuntu20.04-latest
$ docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-ubuntu20.04-latest
```
#### GPU
```
$ docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
$ docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```
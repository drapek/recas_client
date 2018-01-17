# ReCas Camera - client
This code is for devices which you want to connect to ReCaS system. It could be any device with linux based OS.
It was designed to work on Raspberry Rpi3 device. This device should be in the local network. For external use
I recommend to configure VPN.

# Requirements
* Python 2.7 (not tested on Python3)
* openCV v2

# Configure
Before running the program you should set the default settings in src/settings.py.
The most important parameters to manual coinfiguration are:
```python
"STREAM_IP": "<ip adress of your server>",
"STREAM_PORT": <server port on which will be listening for streamed video>,
"CAMERA_NAME": "<camera name>",
```
# Running
```bash
pip install -f requirements.txt
# now configure the settings variables
python run_recas_client.py
```

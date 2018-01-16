# ReCas Camera - client
This code is for devices which you want to connect to ReCaS system. It could be any device with linux based OS.
It was designed to work on Raspberry Rpi3 device. This device should be in the local network. For external use
I recommend configure VPN.

# Requirements
* Python 2.7 (not tested on Python3)
* openCV v2

# Running
```bash
pip install -f requirements.txt
# now configure the settings variables
python run_recas_client.py
```
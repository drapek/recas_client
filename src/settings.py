settings = {
    "STREAM_END_TIME": 0,  # This is time(), which says the stream worker if it should stream the video to server
    "STREAM_BASE_UNIT_LENGTH": 30,  # In seconds - how long will be stream provided
    "TRESHOLD": 8,  # Treshold (sensitivity of the motion capturing)
    "MIN_NOTIFICATION_FREQUENCY_TIME": 5,  # in seconds - waiting time before sending next notification
    "STREAM_IP": "192.168.1.30",
    "STREAM_PORT": 8089,
    "CAMERA_NAME": "camera1",  # TODO in future it should automatically assign the name
}

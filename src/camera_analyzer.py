import json
import time
import cv2
import pickle
import socket
import struct
import requests

from datetime import datetime

from settings import settings


class CameraAnalyzer:
    image_splitter = None  # splitter is initialized in constructor
    socket = None  # socket is initialized in constructor

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.capture = cv2.cv.CaptureFromCAM(0)
        self.frame = cv2.cv.QueryFrame(self.capture)

        # This parameter are for motion recognition
        self.frame1gray = cv2.cv.CreateMat(self.frame.height, self.frame.width, cv2.CV_8U)  # Gray frame at t-1
        cv2.cv.CvtColor(self.frame, self.frame1gray, cv2.cv.CV_RGB2GRAY)
        # Will hold the thresholded result
        self.res = cv2.cv.CreateMat(self.frame.height, self.frame.width, cv2.CV_8U)
        self.frame2gray = cv2.cv.CreateMat(self.frame.height, self.frame.width, cv2.CV_8U)  # Gray frame at t

        self.width = self.frame.width
        self.height = self.frame.height
        self.nb_pixels = self.width * self.height
        self.sending_notification_time = 0
        self.socket_open = False  # Manage streaming the images to the server

    def run(self):
        started = time.time()
        while True:
            instant = time.time()  # Get timestamp o the frame
            frame = cv2.cv.QueryFrame(self.capture)
            self._process_image(frame)  # Process the image

            if self._something_has_moved():
                if instant > started + 5:  # Wait 5 second after the webcam start for luminosity adjusting etc..
                    self._send_notification_to_server()
                    settings["STREAM_END_TIME"] = instant + settings["STREAM_BASE_UNIT_LENGTH"]

            # Stream image when streaming is Open
            if time.time() <= settings["STREAM_END_TIME"]:
                self._open_socket()
                self._send_image_to_server(frame)
            else:
                self._close_socket()

            cv2.cv.Copy(self.frame2gray, self.frame1gray)

            # quit using 'q' key
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    def _send_image_to_server(self, frame):
        frame_jpg = cv2.cv.EncodeImage('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40]).tostring()
        frame_serialized = pickle.dumps(frame_jpg)
        if self.verbose:
            print("[LOG] Frame size: {}", len(frame_serialized))
        self.socket.sendall(struct.pack("q", len(frame_serialized)) + frame_serialized)

    def _open_socket(self):
        if not self.socket_open:
            self.socket = socket.socket(socket.AF_INET,  # Internet
                                        socket.SOCK_STREAM)  # Stream
            connected = False
            while not connected:
                try:
                    self.socket.connect((settings["STREAM_IP"], settings["STREAM_PORT"]))
                    connected = True
                except Exception as e:
                    print(e)
                    print ("Oh snap! I can't connect to the server. Retrying after 5 seconds.")
                    time.sleep(5)
            self.socket_open = True

    def _close_socket(self):
        if self.socket_open:
            self.socket.close()
            self.socket_open = False

    def _process_image(self, frame):
        cv2.cv.CvtColor(frame, self.frame2gray, cv2.cv.CV_RGB2GRAY)
        # Absdiff to get the difference between to the frames
        cv2.cv.AbsDiff(self.frame1gray, self.frame2gray, self.res)
        # Remove the noise and do the threshold
        cv2.cv.Smooth(self.res, self.res, cv2.cv.CV_BLUR, 5, 5)
        cv2.cv.MorphologyEx(self.res, self.res, None, None, cv2.cv.CV_MOP_OPEN)
        cv2.cv.MorphologyEx(self.res, self.res, None, None, cv2.cv.CV_MOP_CLOSE)
        cv2.cv.Threshold(self.res, self.res, 10, 255, cv2.cv.CV_THRESH_BINARY_INV)

    def _something_has_moved(self):
        nb = 0  # Will hold the number of black pixels
        min_threshold = (self.nb_pixels / 100) * settings["TRESHOLD"]  # Number of pixels for current threshold
        nb = self.nb_pixels - cv2.cv.CountNonZero(self.res)
        if (nb) > min_threshold:
            return True
        else:
            return False

    def _send_notification_to_server(self):
        now = time.time()
        if now > self.sending_notification_time + settings["MIN_NOTIFICATION_FREQUENCY_TIME"]:
            if self.verbose:
                print(datetime.now().strftime("%b %d, %H:%M:%S"), "Something is moving !")
            headers = {"Content-Type": "application/json"}
            data = json.dumps({"notification_type": "motion_alert"})
            try:
                r = requests.post("http://{}:8000/api/notification".format(settings["STREAM_IP"]), data=data, headers=headers)
            except Exception as e:
                print("Excepiton: ", e)
            self.sending_notification_time = now


if __name__ == '__main__':
    CameraAnalyzer(verbose=True).run()

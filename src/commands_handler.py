#!/usr/bin/env python
"""
Very simple HTTP server in python to handle ReCaS camera commands.
Usage:
  * GET on /settings
    returns all settings in json
  * POST on /settings
    changes settings defined in response (json)
  * POST on /start-server
    start stream transmission on port defined in settings. It will last for X seconds (set by /settings endpoint)
"""
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import time

from settings import settings


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == '/settings':
            self._return_actual_settings()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()

        if self.path == '/start-stream':
            self._start_streaming_video()

        if self.path == '/settings':
            self._change_settings()

    def _start_streaming_video(self):
        settings["STREAM_END_TIME"] = time.time() + settings["STREAM_BASE_UNIT_LENGTH"]
        self.wfile.write(json.dumps({'success': True,
                                     'data': "Stream opened until {}".format(settings["STREAM_END_TIME"])}))

    def _change_settings(self):
        json_length = int(self.headers.getheader('Content-Length'))
        if json_length == 0:
            self.wfile.write(json.dumps({'success': False, 'data': 'no json content'}))
            return
        settings_that_changed = json.loads(self.rfile.read(json_length))
        for setting in settings_that_changed:
            if setting in settings:
                settings[setting] = settings_that_changed[setting]
        self.wfile.write(json.dumps({'success': True}))

    def _return_actual_settings(self):
        data = json.dumps(settings)
        self.wfile.write(str(data))


def run(server_class=HTTPServer, handler_class=S, port=5555):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Command server is listening now.'
    httpd.serve_forever()


if __name__ == '__main__':
    run()

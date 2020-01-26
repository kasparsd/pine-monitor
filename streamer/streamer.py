#!/usr/bin/python
import io
import picamera
import logging
import datetime as dt
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
  def _set_mjpeg_headers(self):
    self.send_response(200)
    self.send_header('Age', 0)
    self.send_header('Cache-Control', 'no-cache, private')
    self.send_header('Pragma', 'no-cache')
    self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
    self.end_headers()

  def _write_frame(self, frame):
    self.wfile.write(b'--FRAME\r\n')
    self.send_header('Content-Type', 'image/jpeg')
    self.send_header('Content-Length', len(frame))
    self.end_headers()
    self.wfile.write(frame)
    self.wfile.write(b'\r\n')

  def do_GET(self):
    self._set_mjpeg_headers()
    stream=io.BytesIO()
    with picamera.PiCamera(resolution='640x480', framerate=1) as camera:
      try:
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text_size = 16
        for foo in camera.capture_continuous(stream,'jpeg'):
          camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          self._write_frame(stream.getvalue())
          stream.truncate()
          stream.seek(0)
      except Exception as e:
        logging.warning('Camera exception: %s', str(e))

try:
  server = HTTPServer(('',8000), RequestHandler)
  server.serve_forever()
except Exception as e:
  logging.warning('Main exception: %s', str(e))
finally:
  server.socket.close()


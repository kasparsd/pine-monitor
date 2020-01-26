import io
import picamera
import logging
import socketserver
import threading
from threading import Condition
from http import server

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def _set_mjpeg_headers(self):
        self.send_response(200)
        self.send_header('Age', 0)
        self.send_header('Cache-Control', 'no-cache, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
        self.end_headers()

    def _on_join(self):
        print("Join", threading.active_count())
        if not camera.recording:
            camera.start_recording(output, format='mjpeg')

    def _on_leave(self):
        print("Leave", threading.active_count())
        if 3 > threading.active_count() and camera.recording:
            print("Stopped recording")
            camera.stop_recording()

    def do_GET(self):
        if self.path == '/stream.mjpg':
            self._on_join()
            self._set_mjpeg_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
            finally:
                self._on_leave()
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=6) as camera:
    print("Go", threading.active_count())
    try:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    except Exception as e:
        logging.warning('Main exception: %s', str(e))
    finally:
        server.server_close()

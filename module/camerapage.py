import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2, controls
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

from libcamera import Transform

# HTML page for the MJPEG streaming demo
PAGE = """\
<html>
<head>
<title>Greenhope</title>
</head>
<body>
<h1>GreenHope Module Camerafeed</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

# Class to handle streaming output
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

# Class to handle HTTP requests
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect root path to index.html
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Serve the HTML page
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            # Set up MJPEG streaming
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
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
        else:
            # Handle 404 Not Found
            self.send_error(404)
            self.end_headers()

# Class to handle streaming server
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Create Picamera2 instance
picam2 = Picamera2()

tfrm = Transform(hflip=1, vflip=1)

# Set up the camera configuration for video with specific modifications
config = picam2.create_video_configuration(main={"size": (640, 480)}, transform = tfrm)

# Set exposure mode (e.g., 'auto', 'night', 'backlight')
# Set metering mode (e.g., 'average', 'spot', 'matrix')
# Adjust contrast (range typically -100 to 100, check documentation)
picam2.set_controls({
    #"Saturation": 0,
    "AwbEnable": True#,
    #"vertical_flip": True,
    #"horizontal_flip": True
})

# Apply the configuration
picam2.configure(config)

output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    # Set up and start the streaming server
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    # Stop recording when the script is interrupted
    picam2.stop_recording()

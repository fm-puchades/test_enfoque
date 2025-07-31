#import io
import cv2
import logging
import socketserver

from time import sleep
from threading import Condition, Thread, Timer
from http import server
from base64 import b64decode

from enfoque import Enfoque

PAGE = """\
<html>
<head>
<title>STREAMING CAMERA</title>
</head>
<body>
<center><h1>Streaming Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

# Define username and password
USERNAME = "cameraman"
PASSWORD = "cam46610"

# Tiempo en segundos antes de detener el servidor (1 hora = 3600 segundos)
RUN_TIME = 3600

def validate_credentials(headers):
    auth_header = headers.get('Authorization')
    if auth_header and auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ', 1)[1]
        decoded_credentials = b64decode(encoded_credentials).decode('utf-8')
        user, sep, pwd = decoded_credentials.partition(':')
        return user == USERNAME and pwd == PASSWORD
    return False

class StreamingOutput:
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def update_frame(self, frame):
        with self.condition:
            self.frame = frame
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def authenticate(self):
        if not validate_credentials(self.headers):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Streaming"')
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Unauthorized</h1></body></html>")
            return True # Pongo True para no autenticar de momento
        return True

    def do_GET(self):
        #if not self.authenticate():        COMENTADO POR AHORA
        #    return

        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
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
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def capture_frames(device=0, op_varianza=0.75):
    enfocador = Enfoque(device=device, op_varianza=op_varianza)
    enfocador.iniciar()
    frame = enfocador.frame

    while True:
        sleep(24/1000)
        frame = enfocador.frame
        if not enfocador.ready:
            logging.error('Error al leer un fotograma de la cámara.')
            continue
        _, jpeg = cv2.imencode('.jpg', frame)
        output.update_frame(jpeg.tobytes())

if __name__ == '__main__':
    output = StreamingOutput()
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)

    # Ejecuta la captura de la cámara en un hilo separado
    thread = Thread(target=capture_frames(0, 0.75), daemon=True)
    thread.start()

    # Configura un temporizador para detener el servidor después de RUN_TIME
    def stop_server():
        print("Deteniendo el servidor...")
        server.shutdown()

    timer = Timer(RUN_TIME, stop_server)
    timer.start()

    try:
        print(f"Servidor iniciado por {RUN_TIME/3600} horas en http://localhost:8000")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Servidor detenido.")
    finally:
        timer.cancel()

####################### DETERMINA EL ENFOQUE #######################
# Autor: F. Martínez
# 23/01/2025
# Versión 1.2

import cv2
import requests
import numpy as np
import json
#import matplotlib as plt

from time import sleep
from os import path, sep, makedirs, name, system
#from picamera import PiCamera
#from picamera.array import PiRGBArray

from modules.timestamp import timestamp

# pyinstaller --distpath DISTRO --collect-data palettable  --noconfirm  -n  TEST_ENFOQUE enfoque.py

def limpiar_consola():
    """
    Limpia la consola de manera compatible con Windows y Linux.
    """
    if name == 'nt':  # Para Windows
        system('cls')
    else:  # Para Linux/Unix/Mac
        system('clear')

def listar_dispositivos():
    """
    Lista los dispositivos de captura disponibles.
    Returns:
        dispositivos: Lista de índices de dispositivos detectados.
    """
    dispositivos = []
    for i in range(10):  # Intentar detectar hasta 10 dispositivos
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            dispositivos.append(i)
            cap.release()
    return dispositivos

class Enfoque:
    """
    Versión de 'ENFOQUE' cliente HTTP.
    """
    def __init__(self, espera=50, db_lv=0, op_varianza=0.5):
        title = """
        #######################################################
        #                TEST DE ENFOQUE   v1                 #
        #  ------------------------------------------------   #
        #                                                     #
        # Francisco Martinez Puchades          ENERO 2025     #
        #                                                     #
        #######################################################
        """
        print(title)
        print("       ", timestamp())
        self.stream_url = ""
        self.db_lv = db_lv
        self.espera = espera
        #self.cap = cv2.VideoCapture(device)
        resolucion = (640, 480)
        # Establece una resolución de 640x480
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolucion[0])  # Ancho 640
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucion[1])  # Alto 480
        self.roi = None
        self.frame = cv2.imread("cartaajuste.png")
        self.frame = cv2.resize(self.frame, resolucion)
        self.op_varianza = op_varianza
        self.path = "LOG"
        self.ready = True
        #if not self.cap.isOpened():
        #    print("Error al abrir la cámara")
        #    self.ready = False
        #    exit()

        # Forzamos un ROI fijo en lugar de solicitarlo
        self.framse_size = resolucion
        self.roi = (int(resolucion[0]*0.15), int(resolucion[1]*0.15), int(resolucion[0]*0.70), int(resolucion[1]*0.70))

        print("\nResolución de imagen:", resolucion)

    def cargar_conf_desde_json(self, ruta_json="config.json"):
        """Lee el archivo JSON y devuelve los datos como un diccionario."""
        try:
            with open(ruta_json, 'r') as archivo:
                data = json.load(archivo)

            for param in data['params']:
                url = param["url"]
                op_varianza = param["varianza"]

            self.stream_url = url
            self.op_varianza = op_varianza
            print("--> Lectura de", ruta_json)
            print("    URL:", url)
            print("    Varianza para análisis del enfoque:", op_varianza)

        except Exception as e:
            print(">> Error al cargar PADS desde json.")
            print("Fichero esperado:", ruta_json)
            print(e)
    
    def fetch_frame(self):
        """
        Fetch a single frame from the MJPEG stream.

        Args:
            stream_url (str): The URL of the MJPEG stream.
            default stream_url = "http://10.10.51.211:8000/stream.mjpg"

        Returns:
            np.ndarray: The frame as an OpenCV image (BGR format).
        """
        if self.stream_url == "": self.stream_url = "http://10.10.51.211:8000/stream.mjpg"
        frame = cv2.imread("cartaajuste.png")
        frame = cv2.resize(frame, self.framse_size)
        response = requests.get(self.stream_url, stream=True, auth=("cameraman", "cam46610"))

        if response.status_code != 200:
            raise RuntimeError(f"Failed to connect to stream: {response.status_code}")

        bytes_data = b''
        for chunk in response.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # JPEG start
            b = bytes_data.find(b'\xff\xd9')  # JPEG end
            if a != -1 and b != -1:
                jpg = bytes_data[a:b + 2]
                bytes_data = bytes_data[b + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                return frame

    def file_mk(self):
        try:
            if not path.exists(self.path):
                makedirs(self.path)
                print("Se ha creado el directorio:", self.path)
                sleep(2)
        except FileNotFoundError as e:
            print(f"Error: {e}")   

    def registrar(self, frame):
        cv2.imwrite("captura.jpg", self.frame)
        

    def seleccionar_roi(self, frame):
        """
        Permite seleccionar manualmente una ROI en el primer fotograma.
        """
        r = cv2.selectROI("Selecciona la ROI", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Selecciona la ROI")
        return r

    def calcular_umbral_dinamico(self, roi_gray):
        """
        Calcula un umbral dinámico basado en la varianza del Laplaciano de la ROI.

        Args:
            roi_gray: Imagen en escala de grises de la ROI.

        Returns:
            umbral: Umbral dinámico calculado (mínimo forzado: 50).
        """
        laplacian = cv2.Laplacian(roi_gray, cv2.CV_64F)
        varianza = laplacian.var()
        umbral = varianza * self.op_varianza  # Ajustar este factor según el escenario
        
        #LIMITADORES
        umbral = max(umbral, 50.0)
        return umbral

    def evaluar_enfoque(self, image, umbral=150):
        """
        Evalúa si la imagen está enfocada calculando la varianza del Laplaciano.

        Args:
            image: Imagen en escala de grises.
            umbral: Valor umbral para decidir si la imagen está enfocada.

        Returns:
            nitidez: Varianza del Laplaciano.
            enfocada: True si la varianza supera el umbral, False en caso contrario.
        """
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        nitidez = laplacian.var()
        enfocada = nitidez > umbral
        return nitidez, enfocada

    def iniciar(self):
        umbral_dinamico = 100  # Valor inicial del umbral
        self.cargar_conf_desde_json()
        while True:
            #ret, frame = self.cap.read()
            #if not ret:
            #    print("No se pudo leer el fotograma.")
            #    self.ready = False
            #    break
            try:
                frame = self.fetch_frame()
                if frame is not None:
                    if self.roi is None:
                        self.roi = self.seleccionar_roi(frame)

                # Extrae la ROI del fotograma
                x, y, w, h = map(int, self.roi)
                roi_frame = frame[y:y+h, x:x+w]
                roi_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

                # Calcula el umbral dinámico basado en la ROI
                umbral_dinamico = self.calcular_umbral_dinamico(roi_gray)

                # Evalúa el enfoque en toda la imagen
                #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #nitidez, enfocada = self.evaluar_enfoque(gray, umbral=umbral_dinamico)

                # Evalúa el enfoque solo en el ROI
                nitidez, enfocada = self.evaluar_enfoque(roi_gray, umbral=umbral_dinamico)

                # Detección de bordes con Canny solo en la ROI
                edges = cv2.Canny(roi_gray, 90, 160)
                edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

                # Combina el resultado de la ROI con el fotograma original
                frame_roi = frame.copy()
                frame_roi[y:y+h, x:x+w] = cv2.addWeighted(roi_frame, 0.5, edges_colored, 1.0, 0)

                # Dibujar la ROI y mostrar información de enfoque
                time_photo = timestamp()
                cv2.rectangle(frame_roi, (x, y), (x+w, y+h), (0, 255, 0) if enfocada else (0, 0, 255), 1)
                texto1 = f"Nitidez: {nitidez:.2f} - Umbral: {umbral_dinamico:.2f} - {'ENFOCADA' if enfocada else 'DESENFOCADA'}"
                texto2 = "Pulsa 'q' para salir"
                texto3 = f"Pulsa 'r' para registrar             var:{self.op_varianza}          {time_photo}"
                cv2.putText(frame_roi, texto1, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if enfocada else (0, 0, 255), 2)
                cv2.putText(frame_roi, texto2, (10, self.framse_size[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame_roi, texto3, (10, self.framse_size[1]-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                self.frame = frame_roi.copy()
                if self.db_lv >= 0:
                    # Mostrar el frame con la ROI resaltada
                    cv2.imshow('TEST DE ENFOQUE', frame_roi)
                    key = cv2.waitKey(self.espera)
                    if key & 0xFF == ord('q') or key & 0xFF == 27:
                        break

                    elif key & 0xFF == ord('r'):
                        self.file_mk()
                        #self.file_path = f"{self.path}{path.sep}capture_{im_num}.jpg"
                        self.file_path = f"{self.path}{sep}registo_enfoque_{time_photo}.jpg"
                        cv2.imwrite(self.file_path, frame_roi)
                        print("Guadando:", self.file_path)
            except Exception as e:
                print(f"Error fetching frame: {e}")
                self.ready = False
                break

        # Libera la cámara y cierra las ventanas
        #self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":

    enfoque = Enfoque(op_varianza=0.75)
    #enfoque.stream_url = "http://10.10.51.211:8000/stream.mjpg"
    enfoque.iniciar()

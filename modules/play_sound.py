import time
from playsound import playsound  # O usa pygame.mixer para más control

# Estado inicial
person_detected = False
detection_start_time = None
CONFIRMATION_FRAMES = 3  # Número de fotogramas consecutivos para confirmar detección
frame_counter = 0

def detect_objects(frame):
    """
    Simula la detección de objetos. Sustituye por tu modelo real de detección.
    Devuelve True si se detectan personas en el fotograma.
    """
    # Reemplaza esto con la detección real
    # Por ejemplo, usando un modelo como YOLO o SSD
    detected = True  # Simula detección para el ejemplo
    return detected

def play_audio(file_path):
    """Reproduce un archivo de audio."""
    playsound(file_path)

# Bucle principal de procesamiento de video
while True:
    frame = None  # Sustituye con tu captura real del frame, e.g., de OpenCV
    person_in_frame = detect_objects(frame)
    
    if person_in_frame:
        frame_counter += 1
        if not person_detected and frame_counter >= CONFIRMATION_FRAMES:
            # Confirmación de detección y reproducción del audio
            print("¡Persona detectada! Reproduciendo audio...")
            play_audio("audio.mp3")
            person_detected = True
            detection_start_time = time.time()
    else:
        frame_counter = 0
        if person_detected:
            # Reinicia el estado cuando ya no hay personas
            if time.time() - detection_start_time > 2:  # Tiempo mínimo sin detección
                print("Persona ya no detectada, listo para nuevo audio.")
                person_detected = False

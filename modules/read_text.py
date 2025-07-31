### Lectura de texto
import pyttsx3


def read_this(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Ajusta la velocidad de habla
    engine.setProperty('volume', 1.0)  # Ajusta el volumen (1.0 es el máximo)
    #mixer.music.load("person.mp3")
    #mixer.music.play().

    #print(f"Reproduciendo sonido: {text}")
    engine.say(text)
    engine.runAndWait()

#####################################################3
if __name__ == "__main__":
    text = "Este es el texto que estoy probando. ¿Te suena bien?"
    repeticiones = 2

    for i in range(0, repeticiones):
        print(i+1)
        read_this(text)


### GPT

import cv2

def reescalar_y_crop(imagen, nuevo_formato):
    """
    Reescala la imagen en función de su medida mayor, conserva la relación de aspecto
    y recorta la imagen para ajustarla a las nuevas dimensiones.
    
    :param imagen: Matriz de la imagen cargada (por ejemplo, usando cv2.imread()).
    :param nuevo_formato: Ancho, alto deseado para la imagen resultante.
    :return: La imagen ajustada con las nuevas dimensiones.
    """
    nueva_ancho, nueva_alto = nuevo_formato

    # Dimensiones originales
    alto_original, ancho_original = imagen.shape[:2]
    aspecto_original = ancho_original / alto_original
    aspecto_nuevo = nueva_ancho / nueva_alto

    # Determinar el tamaño intermedio respetando la relación de aspecto
    if aspecto_original > aspecto_nuevo:
        # La imagen es más ancha, ajustamos por altura
        escala = nueva_alto / alto_original
    else:
        # La imagen es más alta, ajustamos por ancho
        escala = nueva_ancho / ancho_original

    nuevo_ancho_intermedio = int(ancho_original * escala)
    nuevo_alto_intermedio = int(alto_original * escala)
    
    # Redimensionar la imagen
    imagen_redimensionada = cv2.resize(imagen, (nuevo_ancho_intermedio, nuevo_alto_intermedio), interpolation=cv2.INTER_AREA)
    
    # Calcular el recorte necesario
    exceso_ancho = max(0, nuevo_ancho_intermedio - nueva_ancho)
    exceso_alto = max(0, nuevo_alto_intermedio - nueva_alto)
    
    inicio_x = exceso_ancho // 2
    inicio_y = exceso_alto // 2
    fin_x = inicio_x + nueva_ancho
    fin_y = inicio_y + nueva_alto

    # Recortar la imagen
    imagen_crop = imagen_redimensionada[inicio_y:fin_y, inicio_x:fin_x]

    return imagen_crop

if __name__ == "__main__":
    ruta_imagen = "modules/imagen.jpg"
    imagen = cv2.imread(ruta_imagen)

    if imagen is not None:
        nuevo_formato = (320, 320)  # Ancho, alto deseado
        imagen_final = reescalar_y_crop(imagen, nuevo_formato)

        # Mostrar la imagen resultante
        cv2.imshow("Imagen Final", imagen_final)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Guardar la imagen resultante
        cv2.imwrite("imagen_final.jpg", imagen_final)
    else:
        print("No se pudo cargar la imagen. Verifica la ruta.")

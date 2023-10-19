# Importa las librerías
import cv2
import numpy as np


def segmentar_imagen(imagen_path):
    # Carga la imagen que quieres procesar usando la función imread
    imagen_original = cv2.imread(imagen_path)

    # Convierte la imagen a formato HSV
    imagen_hsv = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2HSV)

    # Define 10 rangos de colores que abarcan todo el espectro
    rangos_colores = [
        (np.array([0, 50, 50]), np.array([20, 255, 255])),  # Rojo
        (np.array([20, 50, 50]), np.array([40, 255, 255])),  # Naranja
        (np.array([40, 50, 50]), np.array([80, 255, 255])),  # Amarillo
        (np.array([80, 50, 50]), np.array([140, 255, 255])),  # Verde
        (np.array([140, 50, 50]), np.array([180, 255, 255])),  # Azul
        (np.array([0, 0, 0]), np.array([180, 50, 50])),  # Negro
        (np.array([0, 0, 50]), np.array([180, 50, 200])),  # Gris
        (np.array([0, 0, 200]), np.array([180, 50, 255])),   # Blanco
        # Rojo (segundo tono)
        (np.array([0, 50, 50]), np.array([10, 255, 255])),
        (np.array([150, 50, 50]), np.array([170, 255, 255]))   # Morado
    ]

    # Lista para almacenar las capas resultantes
    capas = []

    # Genera capas para cada rango de color
    for i, rango_color in enumerate(rangos_colores):
        # Crea una máscara para el rango de color actual
        mascara = cv2.inRange(imagen_hsv,
                              rango_color[0],
                              rango_color[1])

        # Aplica la máscara a la imagen original para obtener la capa
        capa = cv2.bitwise_and(imagen_original,
                               imagen_original,
                               mask=mascara)

        # Convierte la capa a formato RGBA
        capa_rgba = cv2.cvtColor(capa,
                                 cv2.COLOR_BGR2BGRA)

        # Establece los píxeles negros como transparentes
        capa_rgba[mascara == [0]] = [0, 0, 0, 0]

        # Agrega la capa a la lista
        capas.append(capa_rgba)

        # Guarda cada capa como una imagen separada en el directorio 'uploads/capas'
        cv2.imwrite(f'uploads/capas/capa{i +1}.png', capa_rgba)

    return capas

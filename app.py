# Importa las librerías necesarias
from flask import Flask, request, render_template, send_from_directory
from segmentador_imagenes import segmentar_imagen
from PIL import Image
import cv2
import numpy as np
import os

app = Flask(__name__)

# Ruta principal de la aplicación


@app.route('/', methods=['GET', 'POST'])
def segmentador_imagenes():
    if request.method == 'POST':
        imagen = request.files['imagen']
        # Asegura que se haya enviado una imagen
        if 'imagen' not in request.files:
            return render_template('index.html', error='No se ha seleccionado una imagen')

        # Verifica que sea un archivo de imagen
        if imagen and allowed_file(imagen.filename):
            # Procesa la imagen
            imagen_path = os.path.join('uploads', imagen.filename)
            imagen.save(imagen_path)

            # Crea el directorio 'uploads/capas' si no existe
            if not os.path.exists('uploads/capas'):
                os.makedirs('uploads/capas')

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
                (np.array([0, 0, 200]), np.array([180, 50, 255])),  # Blanco
                # Rojo (segundo tono)
                (np.array([0, 50, 50]), np.array([10, 255, 255])),
                (np.array([150, 50, 50]), np.array([170, 255, 255]))   # Morado
            ]

            # Lista para almacenar las capas resultantes
            capas = []

            # Genera capas para cada rango de color
            for i, rango_color in enumerate(rangos_colores):
                # Crea una máscara para el rango de color actual
                mascara = cv2.inRange(
                    imagen_hsv, rango_color[0], rango_color[1])

                # Aplica la máscara a la imagen original para obtener la capa
                capa = cv2.bitwise_and(imagen_original, imagen_original,
                                       mask=mascara)

                # Agrega la capa a la lista
                capas.append(capa)

                # Guarda cada capa como una imagen separada en el directorio 'uploads/capas'
                cv2.imwrite(f'uploads/capas/capa{i + 1}.png', capa)

            # Pasa la lista de capas a la plantilla
            # Pasa la lista de capas a la plantilla después de convertirlas a listas de Python
            capas_list = [capa.tolist() for capa in capas]
            return render_template('resultado.html', capas=capas_list)

        else:
            return render_template('index.html', error='Formato de archivo no válido')

    return render_template('index.html', error=None)


@app.route('/capas/<nombre_capa>')
def mostrar_capa(nombre_capa):
    return send_from_directory('uploads/capas', nombre_capa)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    app.run(debug=True)

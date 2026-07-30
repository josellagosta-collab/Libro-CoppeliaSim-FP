import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


AREA_MINIMA = 100


def obtener_imagen_bgr(sim, vision_sensor):
    image, resolution = sim.getVisionSensorImg(vision_sensor)

    imagen = np.frombuffer(image, dtype=np.uint8)

    if imagen.size != resolution[0] * resolution[1] * 3:
        raise ValueError("Imagen recibida con tamano inesperado.")

    imagen = imagen.reshape(resolution[1], resolution[0], 3)

    # CoppeliaSim entrega la imagen en RGB y con origen vertical invertido.
    imagen = cv2.flip(imagen, 0)
    return cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)


def detectar_objetos_verdes(imagen_bgr):
    imagen_hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)

    verde_bajo = np.array([40, 60, 60])
    verde_alto = np.array([85, 255, 255])

    mascara = cv2.inRange(imagen_hsv, verde_bajo, verde_alto)

    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    contornos = [
        contorno
        for contorno in contornos
        if cv2.contourArea(contorno) > AREA_MINIMA
    ]

    return mascara, contornos


def analizar_contornos(contornos, centro_imagen):
    detecciones = []

    for indice, contorno in enumerate(contornos, start=1):
        x, y, ancho, alto = cv2.boundingRect(contorno)
        centro_x = x + ancho // 2
        centro_y = y + alto // 2
        area = cv2.contourArea(contorno)
        distancia_centro = math.dist((centro_x, centro_y), centro_imagen)

        detecciones.append(
            {
                "indice": indice,
                "rectangulo": (x, y, ancho, alto),
                "centro": (centro_x, centro_y),
                "area": area,
                "distancia_centro": distancia_centro,
            }
        )

    detecciones.sort(key=lambda deteccion: deteccion["centro"][0])
    return detecciones


def dibujar_detecciones(imagen_bgr, detecciones, objeto_mas_centrado):
    resultado = imagen_bgr.copy()

    for deteccion in detecciones:
        x, y, ancho, alto = deteccion["rectangulo"]
        centro_x, centro_y = deteccion["centro"]

        es_mas_centrado = deteccion is objeto_mas_centrado
        color_rectangulo = (0, 255, 255) if es_mas_centrado else (0, 255, 0)
        grosor = 3 if es_mas_centrado else 2

        cv2.rectangle(
            resultado,
            (x, y),
            (x + ancho, y + alto),
            color_rectangulo,
            grosor,
        )

        cv2.circle(resultado, (centro_x, centro_y), 5, (0, 0, 255), -1)

        texto = f"Obj {deteccion['indice']}: ({centro_x}, {centro_y})"
        cv2.putText(
            resultado,
            texto,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color_rectangulo,
            2,
            cv2.LINE_AA,
        )

    return resultado


def mostrar_datos(detecciones, objeto_mas_centrado):
    print(f"Objetos verdes detectados: {len(detecciones)}")

    for deteccion in detecciones:
        x, y, ancho, alto = deteccion["rectangulo"]
        centro_x, centro_y = deteccion["centro"]
        print(
            f"Objeto {deteccion['indice']}: "
            f"rectangulo=(x={x}, y={y}, ancho={ancho}, alto={alto}), "
            f"centro=({centro_x}, {centro_y})"
        )

    if objeto_mas_centrado is not None:
        centro_x, centro_y = objeto_mas_centrado["centro"]
        distancia = objeto_mas_centrado["distancia_centro"]
        print(
            "Objeto mas proximo al centro de la imagen: "
            f"Objeto {objeto_mas_centrado['indice']} "
            f"en ({centro_x}, {centro_y}), distancia={distancia:.2f} px"
        )


client = RemoteAPIClient()
sim = client.require("sim")

visionSensor = sim.getObject("/visionSensor")

sim.setArrayParam(sim.arrayparam_background_color1, [0.0, 0.0, 0.0])
sim.setArrayParam(sim.arrayparam_background_color2, [0.0, 0.0, 0.0])

# Vista frontal de las figuras.
sim.setObjectPosition(visionSensor, -1, [0.0, -1.35, 0.55])
sim.setObjectOrientation(
    visionSensor,
    -1,
    [math.radians(-90), 0.0, math.radians(-180)],
)

simulacion_iniciada_por_script = False
captura_guardada = False
datos_mostrados = False

if sim.getSimulationState() == sim.simulation_stopped:
    sim.startSimulation()
    simulacion_iniciada_por_script = True

time.sleep(0.2)

print("Pulsa ESC o q para cerrar la ventana.")

try:
    while True:
        imagen_bgr = obtener_imagen_bgr(sim, visionSensor)
        mascara_verde, contornos_verdes = detectar_objetos_verdes(imagen_bgr)

        alto, ancho = imagen_bgr.shape[:2]
        centro_imagen = (ancho / 2, alto / 2)

        detecciones = analizar_contornos(contornos_verdes, centro_imagen)
        objeto_mas_centrado = min(
            detecciones,
            key=lambda deteccion: deteccion["distancia_centro"],
            default=None,
        )

        resultado = dibujar_detecciones(
            imagen_bgr,
            detecciones,
            objeto_mas_centrado,
        )

        cv2.circle(
            resultado,
            (int(centro_imagen[0]), int(centro_imagen[1])),
            6,
            (255, 0, 255),
            2,
        )

        if not datos_mostrados:
            mostrar_datos(detecciones, objeto_mas_centrado)
            datos_mostrados = True

        if not captura_guardada:
            cv2.imwrite("mascara_verde.png", mascara_verde)
            cv2.imwrite("captura_practica14_1.png", resultado)
            captura_guardada = True

        cv2.imshow("Practica 14.1 - Objetos verdes", resultado)
        cv2.imshow("Mascara verde", mascara_verde)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

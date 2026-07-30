import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


AREA_MINIMA_PELOTA = 100
VENTANA_RESULTADO = "Practica 15.1 - Error visual"
VENTANA_MASCARA = "Mascara pelota roja"
ESCALA_TEXTO = 0.5
GROSOR_TEXTO = 1


def fijar_sensor_al_pioneer(sim, vision_sensor, pioneer):
    sim.setObjectParent(vision_sensor, pioneer, True)

    inclinacion_abajo = math.radians(15)

    matriz_sensor = [
        0.0,
        math.sin(inclinacion_abajo),
        math.cos(inclinacion_abajo),
        0.15,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        math.cos(inclinacion_abajo),
        -math.sin(inclinacion_abajo),
        0.35,
    ]

    sim.setObjectMatrix(vision_sensor, pioneer, matriz_sensor)


def obtener_imagen_bgr(sim, vision_sensor):
    image, resolution = sim.getVisionSensorImg(vision_sensor)

    imagen = np.frombuffer(image, dtype=np.uint8)

    if imagen.size != resolution[0] * resolution[1] * 3:
        raise ValueError("Imagen recibida con tamano inesperado.")

    imagen = imagen.reshape(resolution[1], resolution[0], 3)

    # CoppeliaSim entrega la imagen en RGB y con origen vertical invertido.
    imagen = cv2.flip(imagen, 0)
    return cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)


def detectar_pelota_roja(imagen_bgr):
    imagen_hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)

    rojo_bajo_1 = np.array([0, 80, 80])
    rojo_alto_1 = np.array([10, 255, 255])
    rojo_bajo_2 = np.array([170, 80, 80])
    rojo_alto_2 = np.array([180, 255, 255])

    mascara_1 = cv2.inRange(imagen_hsv, rojo_bajo_1, rojo_alto_1)
    mascara_2 = cv2.inRange(imagen_hsv, rojo_bajo_2, rojo_alto_2)
    mascara = cv2.bitwise_or(mascara_1, mascara_2)

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
        if cv2.contourArea(contorno) > AREA_MINIMA_PELOTA
    ]

    if not contornos:
        return mascara, None

    pelota = max(contornos, key=cv2.contourArea)
    return mascara, pelota


def obtener_centro_pelota(contorno):
    x, y, ancho, alto = cv2.boundingRect(contorno)
    centro_x = x + ancho // 2
    centro_y = y + alto // 2
    return (centro_x, centro_y), (x, y, ancho, alto)


def dibujar_seguimiento(
    imagen_bgr,
    centro_imagen,
    centro_pelota,
    rectangulo_pelota,
    error_x,
    error_y,
):
    resultado = imagen_bgr.copy()
    alto, ancho = resultado.shape[:2]

    cv2.circle(resultado, centro_imagen, 6, (255, 0, 255), 2)
    cv2.putText(
        resultado,
        "Centro imagen",
        (15, alto - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        ESCALA_TEXTO,
        (255, 0, 255),
        GROSOR_TEXTO,
        cv2.LINE_AA,
    )

    if centro_pelota is not None:
        x, y, ancho, alto = rectangulo_pelota

        cv2.rectangle(
            resultado,
            (x, y),
            (x + ancho, y + alto),
            (0, 255, 0),
            2,
        )
        cv2.circle(resultado, centro_pelota, 6, (0, 0, 255), -1)
        cv2.line(resultado, centro_imagen, centro_pelota, (0, 255, 255), 2)

        cv2.putText(
            resultado,
            "Centro pelota",
            (
                min(centro_pelota[0] + 10, ancho - 170),
                max(centro_pelota[1] - 10, 20),
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            ESCALA_TEXTO,
            (0, 0, 255),
            GROSOR_TEXTO,
            cv2.LINE_AA,
        )

        texto_error = f"Ex:{error_x}px  Ey:{error_y}px"
    else:
        texto_error = "Pelota no detectada"

    (texto_ancho, texto_alto), _ = cv2.getTextSize(
        texto_error,
        cv2.FONT_HERSHEY_SIMPLEX,
        ESCALA_TEXTO,
        GROSOR_TEXTO,
    )
    cv2.rectangle(
        resultado,
        (10, 10),
        (min(20 + texto_ancho, ancho - 10), 20 + texto_alto),
        (0, 0, 0),
        -1,
    )
    cv2.putText(
        resultado,
        texto_error,
        (15, 15 + texto_alto),
        cv2.FONT_HERSHEY_SIMPLEX,
        ESCALA_TEXTO,
        (255, 255, 255),
        GROSOR_TEXTO,
        cv2.LINE_AA,
    )

    return resultado


def preparar_ventanas():
    cv2.namedWindow(VENTANA_RESULTADO, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(VENTANA_RESULTADO, 1000, 750)

    cv2.namedWindow(VENTANA_MASCARA, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(VENTANA_MASCARA, 500, 400)


client = RemoteAPIClient()
sim = client.require("sim")

visionSensor = sim.getObject("/visionSensor")
pioneer = sim.getObject("/PioneerP3DX")

fijar_sensor_al_pioneer(sim, visionSensor, pioneer)

simulacion_iniciada_por_script = False
captura_guardada = False

if sim.getSimulationState() == sim.simulation_stopped:
    sim.startSimulation()
    simulacion_iniciada_por_script = True

time.sleep(0.2)

print("Pulsa ESC o q para cerrar la ventana.")
preparar_ventanas()

try:
    while True:
        imagen_bgr = obtener_imagen_bgr(sim, visionSensor)
        alto, ancho = imagen_bgr.shape[:2]

        centro_imagen = (ancho // 2, alto // 2)
        mascara, contorno_pelota = detectar_pelota_roja(imagen_bgr)

        centro_pelota = None
        rectangulo_pelota = None
        error_x = 0
        error_y = 0

        if contorno_pelota is not None:
            centro_pelota, rectangulo_pelota = obtener_centro_pelota(
                contorno_pelota
            )
            error_x = centro_pelota[0] - centro_imagen[0]
            error_y = centro_pelota[1] - centro_imagen[1]

            print(
                f"Centro imagen: {centro_imagen} | "
                f"Centro pelota: {centro_pelota} | "
                f"Error X: {error_x} px | Error Y: {error_y} px",
                end="\r",
            )

        resultado = dibujar_seguimiento(
            imagen_bgr,
            centro_imagen,
            centro_pelota,
            rectangulo_pelota,
            error_x,
            error_y,
        )

        if not captura_guardada:
            cv2.imwrite("mascara_practica15_1.png", mascara)
            cv2.imwrite("captura_practica15_1.png", resultado)
            captura_guardada = True

        cv2.imshow(VENTANA_RESULTADO, resultado)
        cv2.imshow(VENTANA_MASCARA, mascara)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    print()
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

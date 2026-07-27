import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


def detectar_color(imagen_hsv, rangos):
    mascara = np.zeros(imagen_hsv.shape[:2], dtype=np.uint8)

    for limite_inferior, limite_superior in rangos:
        mascara_rango = cv2.inRange(imagen_hsv, limite_inferior, limite_superior)
        mascara = cv2.bitwise_or(mascara, mascara_rango)

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    contornos = [
        contorno
        for contorno in contornos
        if cv2.contourArea(contorno) > 100
    ]

    return mascara, contornos


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

rango_azul = [
    (
        np.array([100, 80, 80]),
        np.array([130, 255, 255]),
    )
]

rango_rojo = [
    (
        np.array([0, 80, 80]),
        np.array([10, 255, 255]),
    ),
    (
        np.array([170, 80, 80]),
        np.array([180, 255, 255]),
    ),
]

simulacion_iniciada_por_script = False
captura_guardada = False

if sim.getSimulationState() == sim.simulation_stopped:
    sim.startSimulation()
    simulacion_iniciada_por_script = True

time.sleep(0.2)

print("Pulsa ESC o q para cerrar la ventana.")

try:
    while True:
        image, resolution = sim.getVisionSensorImg(visionSensor)

        imagen = np.frombuffer(image, dtype=np.uint8)

        if imagen.size != resolution[0] * resolution[1] * 3:
            print("Imagen recibida con tamano inesperado.")
            break

        imagen = imagen.reshape(resolution[1], resolution[0], 3)

        # CoppeliaSim entrega la imagen en RGB y con origen vertical invertido.
        imagen = cv2.flip(imagen, 0)
        imagen_bgr = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
        imagen_hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)

        mascara_azul, contornos_azules = detectar_color(imagen_hsv, rango_azul)
        mascara_roja, contornos_rojos = detectar_color(imagen_hsv, rango_rojo)

        resultado = imagen_bgr.copy()

        cv2.drawContours(
            resultado,
            contornos_azules,
            -1,
            (0, 255, 255),
            2,
        )
        cv2.drawContours(
            resultado,
            contornos_rojos,
            -1,
            (0, 255, 255),
            2,
        )

        texto_azul = f"Azules: {len(contornos_azules)}"
        texto_rojo = f"Rojos: {len(contornos_rojos)}"

        cv2.putText(
            resultado,
            texto_azul,
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            resultado,
            texto_rojo,
            (15, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        if not captura_guardada:
            print(f"Objetos azules encontrados: {len(contornos_azules)}")
            print(f"Objetos rojos encontrados: {len(contornos_rojos)}")
            cv2.imwrite("mascara_azul.png", mascara_azul)
            cv2.imwrite("mascara_roja_practica13_1.png", mascara_roja)
            cv2.imwrite("captura_practica13_1.png", resultado)
            captura_guardada = True

        cv2.imshow("Practica 13.1 - Deteccion por color", resultado)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

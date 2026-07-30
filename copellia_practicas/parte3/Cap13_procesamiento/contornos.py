import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

visionSensor = sim.getObject("/visionSensor")

sim.setArrayParam(sim.arrayparam_background_color1, [0.0, 0.0, 0.0])
sim.setArrayParam(sim.arrayparam_background_color2, [0.0, 0.0, 0.0])

# Vista frontal de las tres figuras: cilindro, esfera y cubo.
sim.setObjectPosition(visionSensor, -1, [0.0, -1.35, 0.55])
sim.setObjectOrientation(
    visionSensor,
    -1,
    [math.radians(-90), 0.0, math.radians(-180)],
)

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

        # Mascara binaria: figuras coloreadas en blanco y fondo/mesa en negro.
        _, mascara = cv2.threshold(
            imagen_hsv[:, :, 1],
            50,
            255,
            cv2.THRESH_BINARY,
        )

        contornos, _ = cv2.findContours(
            mascara,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        for contorno in contornos:
            print(contorno)

        imagen_contornos = imagen_bgr.copy()
        cv2.drawContours(
            imagen_contornos,
            contornos,
            -1,
            (0, 255, 0),
            2,
        )

        if not captura_guardada:
            cv2.imwrite("captura_contornos.png", imagen_contornos)
            captura_guardada = True

        cv2.imshow("Contornos detectados", imagen_contornos)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

visionSensor = sim.getObject("/visionSensor")

sim.setObjectPosition(visionSensor, -1, [0.0, 0.05, 1.6])
sim.setObjectOrientation(visionSensor, -1, [0.0, math.radians(180), 0.0])

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
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)

        if not captura_guardada:
            cv2.imwrite("captura.png", imagen)
            captura_guardada = True

        cv2.imshow("Vision Sensor", imagen)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

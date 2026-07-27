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

if sim.getSimulationState() == sim.simulation_stopped:
    sim.startSimulation()
    simulacion_iniciada_por_script = True

time.sleep(0.2)

print("Pulsa ESC o q para cerrar la ventana.")

try:
    image, resolution = sim.getVisionSensorImg(visionSensor)

    imagen = np.frombuffer(image, dtype=np.uint8)

    if imagen.size != resolution[0] * resolution[1] * 3:
        raise ValueError("Imagen recibida con tamano inesperado.")

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

    imagen_area = imagen_bgr.copy()
    cv2.drawContours(
        imagen_area,
        contornos,
        -1,
        (0, 255, 0),
        2,
    )

    for indice, contorno in enumerate(contornos, start=1):
        area = cv2.contourArea(contorno)
        print(f"Figura {indice}: area = {area:.2f} pixeles cuadrados")

        momentos = cv2.moments(contorno)
        if momentos["m00"] != 0:
            centro_x = int(momentos["m10"] / momentos["m00"])
            centro_y = int(momentos["m01"] / momentos["m00"])
            cv2.putText(
                imagen_area,
                f"{area:.0f}",
                (centro_x - 25, centro_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )

    cv2.imwrite("captura_areas.png", imagen_area)

    while True:
        cv2.imshow("Areas de figuras detectadas", imagen_area)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

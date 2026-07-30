import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


AREA_MINIMA_PELOTA = 100
TOLERANCIA_ERROR_X = 35
ERROR_PRECISION = 12
VELOCIDAD_PRECISION = 0.35
VELOCIDAD_AVANCE_MEDIA = 0.8
VELOCIDAD_AVANCE_LENTA = 0.45
VELOCIDAD_GIRO_MAXIMA = 0.45
GANANCIA_GIRO = 0.006
FACTOR_SUAVIZADO_ERROR = 0.25
VENTANA_RESULTADO = "Practica 15.4 - Seguimiento preciso de pelota"
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


def limitar(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))


def calcular_velocidad_avance(error_x):
    error_absoluto = abs(error_x)

    if error_absoluto <= ERROR_PRECISION:
        return VELOCIDAD_PRECISION
    if error_absoluto <= TOLERANCIA_ERROR_X:
        return VELOCIDAD_AVANCE_MEDIA
    return VELOCIDAD_AVANCE_LENTA


def decidir_movimiento(error_x):
    velocidad_avance = calcular_velocidad_avance(error_x)

    if abs(error_x) <= ERROR_PRECISION:
        return "Centrado preciso", velocidad_avance, velocidad_avance

    if abs(error_x) <= TOLERANCIA_ERROR_X:
        return "Centrado", velocidad_avance, velocidad_avance

    correccion = limitar(
        error_x * GANANCIA_GIRO,
        -VELOCIDAD_GIRO_MAXIMA,
        VELOCIDAD_GIRO_MAXIMA,
    )

    velocidad_izquierda = velocidad_avance + correccion
    velocidad_derecha = velocidad_avance - correccion

    if error_x < 0:
        movimiento = "Corrige izquierda"
    else:
        movimiento = "Corrige derecha"

    return movimiento, velocidad_izquierda, velocidad_derecha


def aplicar_velocidades(sim, motor_izquierdo, motor_derecho, v_izquierda, v_derecha):
    sim.setJointTargetVelocity(motor_izquierdo, v_izquierda)
    sim.setJointTargetVelocity(motor_derecho, v_derecha)


def dibujar_seguimiento(
    imagen_bgr,
    centro_imagen,
    centro_pelota,
    rectangulo_pelota,
    error_x,
    movimiento,
):
    resultado = imagen_bgr.copy()
    alto, ancho = resultado.shape[:2]

    cv2.circle(resultado, centro_imagen, 6, (255, 0, 255), 2)

    if centro_pelota is not None:
        x, y, ancho_rect, alto_rect = rectangulo_pelota

        cv2.rectangle(
            resultado,
            (x, y),
            (x + ancho_rect, y + alto_rect),
            (0, 255, 0),
            2,
        )
        cv2.circle(resultado, centro_pelota, 6, (0, 0, 255), -1)
        cv2.line(resultado, centro_imagen, centro_pelota, (0, 255, 255), 2)

        cv2.putText(
            resultado,
            "Centro objeto",
            (
                min(centro_pelota[0] + 10, ancho - 160),
                max(centro_pelota[1] - 10, 20),
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            ESCALA_TEXTO,
            (0, 0, 255),
            GROSOR_TEXTO,
            cv2.LINE_AA,
        )

        velocidad_base = calcular_velocidad_avance(error_x)
        texto = f"Error X:{error_x}px  V:{velocidad_base:.2f}  {movimiento}"
    else:
        texto = "Pelota roja no detectada - robot parado"

    (texto_ancho, texto_alto), _ = cv2.getTextSize(
        texto,
        cv2.FONT_HERSHEY_SIMPLEX,
        ESCALA_TEXTO,
        GROSOR_TEXTO,
    )
    cv2.rectangle(
        resultado,
        (10, 10),
        (min(20 + texto_ancho, ancho - 10), 24 + texto_alto),
        (0, 0, 0),
        -1,
    )
    cv2.putText(
        resultado,
        texto,
        (15, 17 + texto_alto),
        cv2.FONT_HERSHEY_SIMPLEX,
        ESCALA_TEXTO,
        (255, 255, 255),
        GROSOR_TEXTO,
        cv2.LINE_AA,
    )

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
motorIzquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motorDerecho = sim.getObject("/PioneerP3DX/rightMotor")

fijar_sensor_al_pioneer(sim, visionSensor, pioneer)

simulacion_iniciada_por_script = False
captura_guardada = False
error_x_suavizado = 0

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
        movimiento = "Parado"
        velocidad_izquierda = 0
        velocidad_derecha = 0

        if contorno_pelota is not None:
            centro_pelota, rectangulo_pelota = obtener_centro_pelota(
                contorno_pelota
            )
            error_x_medido = centro_pelota[0] - centro_imagen[0]
            error_x_suavizado = (
                FACTOR_SUAVIZADO_ERROR * error_x_medido
                + (1 - FACTOR_SUAVIZADO_ERROR) * error_x_suavizado
            )
            error_x = int(round(error_x_suavizado))
            movimiento, velocidad_izquierda, velocidad_derecha = decidir_movimiento(
                error_x
            )

        aplicar_velocidades(
            sim,
            motorIzquierdo,
            motorDerecho,
            velocidad_izquierda,
            velocidad_derecha,
        )

        print(
            f"Error X: {error_x:>4} px | "
            f"Movimiento: {movimiento:<17} | "
            f"V base: {calcular_velocidad_avance(error_x):>4.2f} | "
            f"V izq: {velocidad_izquierda:>5.2f} | "
            f"V der: {velocidad_derecha:>5.2f}",
            end="\r",
        )

        resultado = dibujar_seguimiento(
            imagen_bgr,
            centro_imagen,
            centro_pelota,
            rectangulo_pelota,
            error_x,
            movimiento,
        )

        if not captura_guardada:
            cv2.imwrite("mascara_practica15_4.png", mascara)
            cv2.imwrite("captura_practica15_4.png", resultado)
            captura_guardada = True

        cv2.imshow(VENTANA_RESULTADO, resultado)
        cv2.imshow(VENTANA_MASCARA, mascara)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    print()
    aplicar_velocidades(sim, motorIzquierdo, motorDerecho, 0, 0)
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

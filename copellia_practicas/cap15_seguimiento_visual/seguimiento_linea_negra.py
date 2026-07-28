import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


AREA_MINIMA_LINEA = 250
TOLERANCIA_ERROR_X = 25
VELOCIDAD_AVANCE_RAPIDA = 1.1
VELOCIDAD_AVANCE_MEDIA = 0.8
VELOCIDAD_AVANCE_LENTA = 0.45
VELOCIDAD_BUSQUEDA = 0.35
VELOCIDAD_GIRO_MAXIMA = 0.65
GANANCIA_GIRO = 0.007
FACTOR_SUAVIZADO_ERROR = 0.30
INICIO_ROI = 0.55
FIN_ROI = 0.95
VENTANA_RESULTADO = "Seguimiento de linea negra"
VENTANA_MASCARA = "Mascara linea negra"
ESCALA_TEXTO = 0.5
GROSOR_TEXTO = 1


def fijar_sensor_al_pioneer(sim, vision_sensor, pioneer):
    sim.setObjectParent(vision_sensor, pioneer, True)

    inclinacion_abajo = math.radians(45)

    matriz_sensor = [
        0.0,
        math.sin(inclinacion_abajo),
        math.cos(inclinacion_abajo),
        0.18,
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


def detectar_linea_negra(imagen_bgr):
    alto, ancho = imagen_bgr.shape[:2]
    y_inicio = int(alto * INICIO_ROI)
    y_fin = int(alto * FIN_ROI)
    roi = imagen_bgr[y_inicio:y_fin, :]

    grises = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    grises = cv2.GaussianBlur(grises, (5, 5), 0)

    _, mascara = cv2.threshold(
        grises,
        80,
        255,
        cv2.THRESH_BINARY_INV,
    )

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
        if cv2.contourArea(contorno) > AREA_MINIMA_LINEA
    ]

    if not contornos:
        mascara_completa = np.zeros((alto, ancho), dtype=np.uint8)
        mascara_completa[y_inicio:y_fin, :] = mascara
        return mascara_completa, None, (0, y_inicio, ancho, y_fin - y_inicio)

    linea = max(contornos, key=cv2.contourArea)

    mascara_completa = np.zeros((alto, ancho), dtype=np.uint8)
    mascara_completa[y_inicio:y_fin, :] = mascara

    linea_desplazada = linea.copy()
    linea_desplazada[:, :, 1] += y_inicio

    return mascara_completa, linea_desplazada, (0, y_inicio, ancho, y_fin - y_inicio)


def obtener_centro_linea(contorno):
    momentos = cv2.moments(contorno)

    if momentos["m00"] == 0:
        x, y, ancho, alto = cv2.boundingRect(contorno)
        return (x + ancho // 2, y + alto // 2), (x, y, ancho, alto)

    centro_x = int(momentos["m10"] / momentos["m00"])
    centro_y = int(momentos["m01"] / momentos["m00"])
    rectangulo = cv2.boundingRect(contorno)
    return (centro_x, centro_y), rectangulo


def limitar(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))


def calcular_velocidad_avance(error_x):
    error_absoluto = abs(error_x)

    if error_absoluto < 20:
        return VELOCIDAD_AVANCE_RAPIDA
    if error_absoluto < 80:
        return VELOCIDAD_AVANCE_MEDIA
    return VELOCIDAD_AVANCE_LENTA


def decidir_movimiento(error_x):
    velocidad_avance = calcular_velocidad_avance(error_x)

    if abs(error_x) <= TOLERANCIA_ERROR_X:
        return "Linea centrada", velocidad_avance, velocidad_avance

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


def buscar_linea(ultimo_error_x):
    if ultimo_error_x < 0:
        return "Buscando izquierda", -VELOCIDAD_BUSQUEDA, VELOCIDAD_BUSQUEDA
    return "Buscando derecha", VELOCIDAD_BUSQUEDA, -VELOCIDAD_BUSQUEDA


def aplicar_velocidades(sim, motor_izquierdo, motor_derecho, v_izquierda, v_derecha):
    sim.setJointTargetVelocity(motor_izquierdo, v_izquierda)
    sim.setJointTargetVelocity(motor_derecho, v_derecha)


def dibujar_seguimiento(
    imagen_bgr,
    centro_imagen,
    centro_linea,
    rectangulo_linea,
    contorno_linea,
    roi,
    error_x,
    movimiento,
):
    resultado = imagen_bgr.copy()
    alto, ancho = resultado.shape[:2]
    x_roi, y_roi, ancho_roi, alto_roi = roi

    cv2.rectangle(
        resultado,
        (x_roi, y_roi),
        (x_roi + ancho_roi, y_roi + alto_roi),
        (255, 0, 255),
        2,
    )
    cv2.circle(resultado, centro_imagen, 6, (255, 0, 255), 2)

    if centro_linea is not None:
        x, y, ancho_rect, alto_rect = rectangulo_linea

        cv2.drawContours(resultado, [contorno_linea], -1, (0, 255, 0), 2)
        cv2.rectangle(
            resultado,
            (x, y),
            (x + ancho_rect, y + alto_rect),
            (0, 255, 255),
            2,
        )
        cv2.circle(resultado, centro_linea, 6, (0, 0, 255), -1)
        cv2.line(resultado, centro_imagen, centro_linea, (0, 255, 255), 2)

        velocidad_base = calcular_velocidad_avance(error_x)
        texto = f"Ex:{error_x}px  V:{velocidad_base:.1f}  {movimiento}"
    else:
        texto = f"Linea no detectada - {movimiento}"

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
        "Centro ROI",
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
ultimo_error_x = 1

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

        mascara, contorno_linea, roi = detectar_linea_negra(imagen_bgr)
        x_roi, y_roi, ancho_roi, alto_roi = roi
        centro_imagen = (ancho // 2, y_roi + alto_roi // 2)

        centro_linea = None
        rectangulo_linea = None
        error_x = int(round(error_x_suavizado))

        if contorno_linea is not None:
            centro_linea, rectangulo_linea = obtener_centro_linea(contorno_linea)
            error_x_medido = centro_linea[0] - centro_imagen[0]
            error_x_suavizado = (
                FACTOR_SUAVIZADO_ERROR * error_x_medido
                + (1 - FACTOR_SUAVIZADO_ERROR) * error_x_suavizado
            )
            error_x = int(round(error_x_suavizado))
            ultimo_error_x = error_x

            movimiento, velocidad_izquierda, velocidad_derecha = decidir_movimiento(
                error_x
            )
        else:
            movimiento, velocidad_izquierda, velocidad_derecha = buscar_linea(
                ultimo_error_x
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
            f"Movimiento: {movimiento:<18} | "
            f"V izq: {velocidad_izquierda:>5.2f} | "
            f"V der: {velocidad_derecha:>5.2f}",
            end="\r",
        )

        resultado = dibujar_seguimiento(
            imagen_bgr,
            centro_imagen,
            centro_linea,
            rectangulo_linea,
            contorno_linea,
            roi,
            error_x,
            movimiento,
        )

        if not captura_guardada:
            cv2.imwrite("mascara_linea_negra.png", mascara)
            cv2.imwrite("captura_linea_negra.png", resultado)
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

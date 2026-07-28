import cv2
import math
import numpy as np
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


AREA_MINIMA_OBJETO = 120
TOLERANCIA_ERROR_X = 35
ERROR_PRECISION = 12
VELOCIDAD_PRECISION = 0.35
VELOCIDAD_AVANCE_MEDIA = 0.8
VELOCIDAD_AVANCE_LENTA = 0.45
VELOCIDAD_BUSQUEDA = 0.30
VELOCIDAD_GIRO_MAXIMA = 0.50
GANANCIA_GIRO = 0.006
FACTOR_SUAVIZADO_ERROR = 0.25
VENTANA_RESULTADO = "Capitulo 16 - Proyecto final"
VENTANA_MASCARA = "Mascara objetivo seleccionado"
ESCALA_TEXTO = 0.5
GROSOR_TEXTO = 1

OBJETIVOS = [
    {
        "clave": "rojo",
        "nombre": "pelota roja",
        "color_bgr": (0, 0, 255),
        "rangos_hsv": [
            (np.array([0, 80, 80]), np.array([10, 255, 255])),
            (np.array([170, 80, 80]), np.array([180, 255, 255])),
        ],
    },
    {
        "clave": "azul",
        "nombre": "objeto azul",
        "color_bgr": (255, 0, 0),
        "rangos_hsv": [
            (np.array([95, 80, 80]), np.array([130, 255, 255])),
        ],
    },
]


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


def crear_mascara_color(imagen_hsv, rangos_hsv):
    mascara = np.zeros(imagen_hsv.shape[:2], dtype=np.uint8)

    for limite_bajo, limite_alto in rangos_hsv:
        mascara_rango = cv2.inRange(imagen_hsv, limite_bajo, limite_alto)
        mascara = cv2.bitwise_or(mascara, mascara_rango)

    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    return mascara


def seleccionar_color_objetivo():
    while True:
        opcion = input("Que color quieres seguir? Escribe rojo o azul: ")
        opcion = opcion.strip().lower()

        for objetivo in OBJETIVOS:
            if opcion == objetivo["clave"]:
                return objetivo

        print("Opcion no valida. Debes escribir rojo o azul.")


def detectar_objetos(imagen_bgr, objetivo_seguido):
    imagen_hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)
    detecciones = []

    mascara = crear_mascara_color(imagen_hsv, objetivo_seguido["rangos_hsv"])

    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    contornos = [
        contorno
        for contorno in contornos
        if cv2.contourArea(contorno) > AREA_MINIMA_OBJETO
    ]

    for contorno in contornos:
        detecciones.append(
            {
                "objetivo": objetivo_seguido,
                "contorno": contorno,
                "mascara": mascara,
                "area": cv2.contourArea(contorno),
            }
            )

    return detecciones


def seleccionar_objetivo(detecciones):
    if not detecciones:
        return None

    return max(detecciones, key=lambda deteccion: deteccion["area"])


def obtener_centro_objeto(contorno):
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


def buscar_objetivo(ultimo_error_x):
    if ultimo_error_x < 0:
        return "Buscando izquierda", -VELOCIDAD_BUSQUEDA, VELOCIDAD_BUSQUEDA
    return "Buscando derecha", VELOCIDAD_BUSQUEDA, -VELOCIDAD_BUSQUEDA


def aplicar_velocidades(sim, motor_izquierdo, motor_derecho, v_izquierda, v_derecha):
    sim.setJointTargetVelocity(motor_izquierdo, v_izquierda)
    sim.setJointTargetVelocity(motor_derecho, v_derecha)


def dibujar_detecciones(resultado, detecciones, deteccion_seleccionada):
    for deteccion in detecciones:
        objetivo = deteccion["objetivo"]
        contorno = deteccion["contorno"]
        color = objetivo["color_bgr"]
        x, y, ancho, alto = cv2.boundingRect(contorno)

        grosor = 3 if deteccion is deteccion_seleccionada else 1

        cv2.rectangle(
            resultado,
            (x, y),
            (x + ancho, y + alto),
            color,
            grosor,
        )
        cv2.putText(
            resultado,
            objetivo["nombre"],
            (x, max(y - 8, 18)),
            cv2.FONT_HERSHEY_SIMPLEX,
            ESCALA_TEXTO,
            color,
            GROSOR_TEXTO,
            cv2.LINE_AA,
        )


def dibujar_panel(resultado, texto):
    _, ancho = resultado.shape[:2]

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


def dibujar_resultado(
    imagen_bgr,
    detecciones,
    deteccion_seleccionada,
    centro_imagen,
    centro_objeto,
    error_x,
    movimiento,
):
    resultado = imagen_bgr.copy()
    alto, _ = resultado.shape[:2]

    dibujar_detecciones(resultado, detecciones, deteccion_seleccionada)
    cv2.circle(resultado, centro_imagen, 6, (255, 0, 255), 2)

    if deteccion_seleccionada is not None and centro_objeto is not None:
        objetivo = deteccion_seleccionada["objetivo"]
        color = objetivo["color_bgr"]

        cv2.drawContours(
            resultado,
            [deteccion_seleccionada["contorno"]],
            -1,
            color,
            2,
        )
        cv2.circle(resultado, centro_objeto, 6, (0, 255, 255), -1)
        cv2.line(resultado, centro_imagen, centro_objeto, (0, 255, 255), 2)

        texto = (
            f"Objetivo: {objetivo['nombre']} | "
            f"Error X:{error_x}px | "
            f"{movimiento}"
        )
    else:
        texto = f"Objetivo no detectado | {movimiento}"

    dibujar_panel(resultado, texto)

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

objetivo_seguido = seleccionar_color_objetivo()

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
print(f"Objetivo seleccionado: {objetivo_seguido['nombre']}.")
print("Si hay varios objetos de ese color, el robot seguira el de mayor tamano.")
preparar_ventanas()

try:
    while True:
        imagen_bgr = obtener_imagen_bgr(sim, visionSensor)
        alto, ancho = imagen_bgr.shape[:2]

        centro_imagen = (ancho // 2, alto // 2)
        detecciones = detectar_objetos(imagen_bgr, objetivo_seguido)
        deteccion_seleccionada = seleccionar_objetivo(detecciones)

        centro_objeto = None
        error_x = int(round(error_x_suavizado))

        if deteccion_seleccionada is not None:
            centro_objeto, _ = obtener_centro_objeto(
                deteccion_seleccionada["contorno"]
            )
            error_x_medido = centro_objeto[0] - centro_imagen[0]
            error_x_suavizado = (
                FACTOR_SUAVIZADO_ERROR * error_x_medido
                + (1 - FACTOR_SUAVIZADO_ERROR) * error_x_suavizado
            )
            error_x = int(round(error_x_suavizado))
            ultimo_error_x = error_x

            movimiento, velocidad_izquierda, velocidad_derecha = decidir_movimiento(
                error_x
            )
            mascara = deteccion_seleccionada["mascara"]
            objetivo_nombre = deteccion_seleccionada["objetivo"]["nombre"]
        else:
            movimiento, velocidad_izquierda, velocidad_derecha = buscar_objetivo(
                ultimo_error_x
            )
            mascara = np.zeros((alto, ancho), dtype=np.uint8)
            objetivo_nombre = "ninguno"

        aplicar_velocidades(
            sim,
            motorIzquierdo,
            motorDerecho,
            velocidad_izquierda,
            velocidad_derecha,
        )

        print(
            f"Objetivo: {objetivo_nombre:<12} | "
            f"Error X: {error_x:>4} px | "
            f"Movimiento: {movimiento:<17} | "
            f"V izq: {velocidad_izquierda:>5.2f} | "
            f"V der: {velocidad_derecha:>5.2f}",
            end="\r",
        )

        resultado = dibujar_resultado(
            imagen_bgr,
            detecciones,
            deteccion_seleccionada,
            centro_imagen,
            centro_objeto,
            error_x,
            movimiento,
        )

        if not captura_guardada:
            cv2.imwrite("mascara_proyecto_final.png", mascara)
            cv2.imwrite("captura_proyecto_final.png", resultado)
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

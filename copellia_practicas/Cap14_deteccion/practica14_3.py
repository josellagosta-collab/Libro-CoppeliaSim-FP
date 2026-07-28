import cv2
import math
import numpy as np
import time
from collections import Counter
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


AREA_MINIMA = 100
UMBRAL_AREA_MEDIANA = 2500
UMBRAL_AREA_GRANDE = 5000


def obtener_imagen_bgr(sim, vision_sensor):
    image, resolution = sim.getVisionSensorImg(vision_sensor)

    imagen = np.frombuffer(image, dtype=np.uint8)

    if imagen.size != resolution[0] * resolution[1] * 3:
        raise ValueError("Imagen recibida con tamano inesperado.")

    imagen = imagen.reshape(resolution[1], resolution[0], 3)

    # CoppeliaSim entrega la imagen en RGB y con origen vertical invertido.
    imagen = cv2.flip(imagen, 0)
    return cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)


def detectar_objetos(imagen_bgr):
    imagen_hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)

    # Detecta los objetos coloreados separandolos del fondo por saturacion.
    _, mascara = cv2.threshold(
        imagen_hsv[:, :, 1],
        50,
        255,
        cv2.THRESH_BINARY,
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
        if cv2.contourArea(contorno) > AREA_MINIMA
    ]

    return imagen_hsv, mascara, contornos


def obtener_color_predominante(imagen_hsv, contorno):
    mascara_contorno = np.zeros(imagen_hsv.shape[:2], dtype=np.uint8)
    cv2.drawContours(mascara_contorno, [contorno], -1, 255, -1)

    media_hsv = cv2.mean(imagen_hsv, mask=mascara_contorno)
    tono, saturacion, valor = media_hsv[:3]

    if saturacion < 50 or valor < 50:
        return "Desconocido"
    if tono < 10 or tono >= 170:
        return "Rojo"
    if tono < 25:
        return "Naranja"
    if tono < 35:
        return "Amarillo"
    if tono < 85:
        return "Verde"
    if tono < 130:
        return "Azul"
    if tono < 170:
        return "Morado"
    return "Desconocido"


def clasificar_tamano(area):
    if area >= UMBRAL_AREA_GRANDE:
        return "Grande"
    if area >= UMBRAL_AREA_MEDIANA:
        return "Mediano"
    return "Pequeno"


def clasificar_forma(contorno):
    perimetro = cv2.arcLength(contorno, True)

    if perimetro == 0:
        return "Desconocida"

    aproximacion = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)
    vertices = len(aproximacion)

    if vertices == 3:
        return "Triangular"
    if vertices == 4:
        x, y, ancho, alto = cv2.boundingRect(contorno)
        proporcion = ancho / float(alto)

        if 0.85 <= proporcion <= 1.15:
            return "Cuadrada"
        return "Rectangular"
    if vertices == 5:
        return "Pentagonal"
    return "Circular"


def analizar_objetos(imagen_hsv, contornos):
    objetos = []

    for indice, contorno in enumerate(contornos, start=1):
        x, y, ancho, alto = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        centro_x = x + ancho // 2
        centro_y = y + alto // 2

        color = obtener_color_predominante(imagen_hsv, contorno)
        tamano = clasificar_tamano(area)
        forma = clasificar_forma(contorno)
        categoria = f"{color} {tamano} {forma}"

        objetos.append(
            {
                "indice": indice,
                "rectangulo": (x, y, ancho, alto),
                "centro": (centro_x, centro_y),
                "area": area,
                "color": color,
                "tamano": tamano,
                "forma": forma,
                "categoria": categoria,
            }
        )

    objetos.sort(key=lambda objeto: objeto["centro"][0])
    return objetos


def dibujar_objetos(imagen_bgr, objetos):
    resultado = imagen_bgr.copy()

    for objeto in objetos:
        x, y, ancho, alto = objeto["rectangulo"]
        centro_x, centro_y = objeto["centro"]

        cv2.rectangle(
            resultado,
            (x, y),
            (x + ancho, y + alto),
            (0, 255, 0),
            2,
        )

        cv2.circle(resultado, (centro_x, centro_y), 5, (0, 0, 255), -1)

        texto = objeto["categoria"]
        cv2.putText(
            resultado,
            texto,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        coordenadas = f"({centro_x}, {centro_y})"
        cv2.putText(
            resultado,
            coordenadas,
            (x, y + alto + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    return resultado


def mostrar_datos(objetos):
    print(f"Objetos detectados: {len(objetos)}")

    for objeto in objetos:
        x, y, ancho, alto = objeto["rectangulo"]
        centro_x, centro_y = objeto["centro"]
        print(
            f"Objeto {objeto['indice']}: "
            f"area={objeto['area']:.2f}, "
            f"centro=({centro_x}, {centro_y}), "
            f"rectangulo=(x={x}, y={y}, ancho={ancho}, alto={alto}), "
            f"color={objeto['color']}, "
            f"tamano={objeto['tamano']}, "
            f"forma={objeto['forma']}, "
            f"categoria={objeto['categoria']}"
        )

    conteo_categorias = Counter(objeto["categoria"] for objeto in objetos)

    print("Conteo por categoria:")
    for categoria, cantidad in conteo_categorias.items():
        print(f"- {categoria}: {cantidad}")


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
        imagen_hsv, mascara, contornos = detectar_objetos(imagen_bgr)
        objetos = analizar_objetos(imagen_hsv, contornos)
        resultado = dibujar_objetos(imagen_bgr, objetos)

        cv2.putText(
            resultado,
            f"Objetos: {len(objetos)}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        if not datos_mostrados:
            mostrar_datos(objetos)
            datos_mostrados = True

        if not captura_guardada:
            cv2.imwrite("mascara_practica14_3.png", mascara)
            cv2.imwrite("captura_practica14_3.png", resultado)
            captura_guardada = True

        cv2.imshow("Practica 14.3 - Clasificacion de objetos", resultado)
        cv2.imshow("Mascara de objetos", mascara)

        tecla = cv2.waitKey(30) & 0xFF

        if tecla == 27 or tecla == ord("q"):
            break

finally:
    cv2.destroyAllWindows()

    if simulacion_iniciada_por_script:
        sim.stopSimulation()

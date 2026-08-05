import time
import math
import os
import subprocess
from pathlib import Path

import cv2
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


TOTAL_NARANJAS = 15
NARANJAS_A_RECOGER_EN_ESTA_FASE = TOTAL_NARANJAS

RUTA_SCRIPT_NARANJAS = "/controlador_naranjas"
RUTA_CINTA = "/CONV_001_CINTA_INDUSTRIAL"
RUTA_SCRIPT_CINTA = "/CONV_001_CINTA_INDUSTRIAL/controlador_cinta"
RUTA_SENSOR_FINAL_CINTA = "/Sensor_final_cinta"
RUTA_PUNTO_CAIDA = "/HOP_007_NARANJAS/OUTLET"
RUTA_GRUPO_NARANJAS = "/ORANGES"
RUTA_UR3 = "/UR3"
RUTA_RG2 = "/UR3/RG2"
RUTA_SCRIPT_RG2 = "/UR3/RG2/Script"
RUTA_ATTACH_POINT_RG2 = "/UR3/RG2/attachPoint"
RUTA_DEDO_IZQUIERDO_RG2 = "/UR3/RG2/leftTouch"
RUTA_DEDO_DERECHO_RG2 = "/UR3/RG2/rightTouch"
RUTA_TARGET_UR3 = "/UR3/UR3_target"
RUTA_TIP_UR3 = "/UR3/UR3_tip"
RUTA_SCRIPT_IK_UR3 = "/UR3/IK"
RUTA_VISION_SENSOR = "/VIS_001_SOPORTE_VISOR/visionSensor"

POSTGRES_PSQL = Path(r"C:\Program Files\PostgreSQL\15\bin\psql.exe")
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_USUARIO = "postgres"
POSTGRES_PASSWORD = "Alquife+1"
POSTGRES_BASE_MAESTRA = "postgres"
POSTGRES_BASE_NARANJAS = "naranjas"
POSTGRES_TABLA_DATOS = "datos_naranjas"

POSICION_TARGET_UR3_INICIAL = [-0.475, 0.0, 0.86]
ORIENTACION_TARGET_UR3_INICIAL = [0.0, 0.0, 0.0]
POSICION_BASE_UR3_INICIAL = 0.0

Y_CAIDA_CINTA = 0.0
Z_CAIDA_CINTA = 0.52

VELOCIDAD_CINTA = 0.20
TOLERANCIA_X_SENSOR = 0.04
TOLERANCIA_CENTRADO_SENSOR = 0.01

RETARDO_INICIAL = 0.5
INTERVALO_ENTRE_NARANJAS = 1.2
VELOCIDAD_BAJADA = 0.35
TIEMPO_TRAS_LIBERACION = 0.25
TIEMPO_MAXIMO_TRANSPORTE = 45.0
TIEMPO_MAXIMO_ESPERA_ROBOT = 120.0
TIEMPO_ESPERA_FINAL_SIMULACION = 30.0
ALTURA_MINIMA_NARANJA_LEVANTADA = 0.62
DISTANCIA_MINIMA_RETIRADA_SENSOR = 0.12
TOLERANCIA_X_VISION_SENSOR = 0.025
VENTANA_CAPTURA_VISION = 0.06

SEPARACION_DEDOS_PINZA_ABIERTA = 0.105
SEPARACION_DEDOS_PINZA_ABIERTA_MINIMA = 0.085
SEPARACION_DEDOS_PINZA_CERRADA = 0.058
FACTOR_CIERRE_SEGUN_DIAMETRO = 0.83
SEPARACION_MINIMA_AGARRE = 0.040
SEPARACION_MAXIMA_AGARRE = 0.075
TOLERANCIA_SEPARACION_PINZA = 0.001
TOLERANCIA_SEPARACION_AGARRE = 0.010
VELOCIDAD_APERTURA_PINZA = 0.150
VELOCIDAD_CIERRE_PINZA = -0.150
VELOCIDAD_MANTENER_AGARRE = -0.006
FUERZA_PINZA = 35
TIEMPO_MAXIMO_AJUSTE_PINZA = 1.3
TIEMPO_CIERRE_AGARRE_NARANJA = 0.25
PASOS_MOVIMIENTO_UR3 = 27
PAUSA_MOVIMIENTO_UR3 = 0.00125
PASOS_MOVIMIENTO_PRE_GIRO_RAPIDO = 4
PAUSA_MOVIMIENTO_PRE_GIRO_RAPIDO = 0.0
ITERACIONES_IK = 8
ALTURA_APROXIMACION_NARANJA = 0.78
ALTURA_RECOGIDA_NARANJA = 0.70
ALTURA_ELEVACION_NARANJA = 0.86
ALTURA_SEGURA_GIRO_UR3 = 0.95
ALTURA_CENTRO_DEDOS_APROXIMACION = 0.67
ALTURA_CENTRO_DEDOS_RECOGIDA = 0.55
GIRO_BASE_ZONA_DEPOSITO = 3.141592653589793
GIRO_BASE_ZONA_RECOGIDA = -3.141592653589793
AVANCE_X_TARGET_DEPOSITO = 0.05
AVANCE_X_TARGET_DEPOSITO_MESA = 0.15
AVANCE_X_TARGET_DEPOSITO_RECHAZO = 0.15
ALTURA_DEPOSITO_CAJA_AMARILLA = 0.76
Z_TARGET_PRE_APERTURA_CAJA_AMARILLA = 0.88

HSV_NARANJA_BAJO = np.array([5, 80, 60], dtype=np.uint8)
HSV_NARANJA_ALTO = np.array([25, 255, 255], dtype=np.uint8)
DIAMETRO_REAL_NARANJA_CM = 7.0
DIAMETRO_REFERENCIA_NARANJA_PX = 188.4
CARPETA_CAPTURAS_VISION = Path(__file__).with_name("capturas_vision_naranjas")
ARCHIVO_DIAMETROS = Path(__file__).with_name("diametros_naranjas.csv")

TIPO_NARANJA_MESA = "mesa"
TIPO_NARANJA_ZUMO = "zumo"
TIPO_NARANJA_RECHAZADA = "rechazada"
TIPO_NARANJA_DESCONOCIDA = "desconocida"

GIRO_BASE_CAJA_VERDE_MESA = math.radians(135)
GIRO_BASE_CAJA_AMARILLA_ZUMO = math.radians(180)
GIRO_BASE_RECHAZO = math.radians(225)

POSICIONES_INICIALES_NARANJAS = {
    1: [-1.839, -0.064, 0.840],
    2: [-1.770, -0.046, 0.810],
    3: [-1.702, -0.062, 0.843],
    4: [-1.838, 0.007, 0.847],
    5: [-1.770, 0.033, 0.797],
    6: [-1.693, 0.008, 0.851],
    7: [-1.812, 0.052, 0.899],
    8: [-1.743, 0.028, 0.900],
    9: [-1.839, -0.046, 0.909],
    10: [-1.699, -0.037, 0.918],
    11: [-1.867, 0.071, 0.935],
    12: [-1.672, 0.064, 0.931],
    13: [-1.820, 0.000, 0.976],
    14: [-1.700, 0.019, 0.988],
    15: [-1.770, 0.110, 0.996],
}


def conectar_coppeliasim():
    client = RemoteAPIClient()
    sim = client.require("sim")
    print("Conexion con CoppeliaSim establecida.")
    return sim


def ruta_psql():
    if POSTGRES_PSQL.exists():
        return str(POSTGRES_PSQL)

    return "psql"


def ejecutar_psql(base_datos, sql, devolver_salida=False):
    entorno = os.environ.copy()
    entorno["PGPASSWORD"] = POSTGRES_PASSWORD
    comando = [
        ruta_psql(),
        "-h",
        POSTGRES_HOST,
        "-p",
        POSTGRES_PORT,
        "-U",
        POSTGRES_USUARIO,
        "-d",
        base_datos,
        "-v",
        "ON_ERROR_STOP=1",
        "-c",
        sql,
    ]

    resultado = subprocess.run(
        comando,
        env=entorno,
        capture_output=True,
        text=True,
        check=False,
    )

    if resultado.returncode != 0:
        mensaje = resultado.stderr.strip() or resultado.stdout.strip()
        raise RuntimeError(f"Error ejecutando PostgreSQL: {mensaje}")

    if devolver_salida:
        return resultado.stdout.strip()

    return None


def consultar_psql_escalar(base_datos, sql):
    entorno = os.environ.copy()
    entorno["PGPASSWORD"] = POSTGRES_PASSWORD
    comando = [
        ruta_psql(),
        "-h",
        POSTGRES_HOST,
        "-p",
        POSTGRES_PORT,
        "-U",
        POSTGRES_USUARIO,
        "-d",
        base_datos,
        "-t",
        "-A",
        "-v",
        "ON_ERROR_STOP=1",
        "-c",
        sql,
    ]
    resultado = subprocess.run(
        comando,
        env=entorno,
        capture_output=True,
        text=True,
        check=False,
    )

    if resultado.returncode != 0:
        mensaje = resultado.stderr.strip() or resultado.stdout.strip()
        raise RuntimeError(f"Error consultando PostgreSQL: {mensaje}")

    return resultado.stdout.strip()


def inicializar_postgresql():
    print("Conectando con PostgreSQL 15.")
    consultar_psql_escalar(POSTGRES_BASE_MAESTRA, "SELECT version();")
    print("Conexion con PostgreSQL establecida correctamente.")

    existe_base = consultar_psql_escalar(
        POSTGRES_BASE_MAESTRA,
        (
            "SELECT 1 FROM pg_database "
            f"WHERE datname = '{POSTGRES_BASE_NARANJAS}';"
        ),
    )

    if existe_base != "1":
        ejecutar_psql(
            POSTGRES_BASE_MAESTRA,
            f"CREATE DATABASE {POSTGRES_BASE_NARANJAS};",
        )
        print(f"Base de datos {POSTGRES_BASE_NARANJAS} creada.")
    else:
        print(f"Base de datos {POSTGRES_BASE_NARANJAS} localizada.")

    ejecutar_psql(
        POSTGRES_BASE_NARANJAS,
        f"""
        CREATE TABLE IF NOT EXISTS {POSTGRES_TABLA_DATOS} (
            id_naranja INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            n_naranjas_procesadas INTEGER NOT NULL,
            n_naranjas_mesa INTEGER NOT NULL,
            n_naranjas_zumo INTEGER NOT NULL,
            n_naranjas_rechazo INTEGER NOT NULL,
            porcentaje_mesa NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
            porcentaje_zumo NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
            porcentaje_rechazo NUMERIC(5, 2) NOT NULL DEFAULT 0.00
        );

        ALTER TABLE {POSTGRES_TABLA_DATOS}
            ADD COLUMN IF NOT EXISTS porcentaje_mesa NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
            ADD COLUMN IF NOT EXISTS porcentaje_zumo NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
            ADD COLUMN IF NOT EXISTS porcentaje_rechazo NUMERIC(5, 2) NOT NULL DEFAULT 0.00;
        """,
    )
    print(f"Tabla {POSTGRES_TABLA_DATOS} preparada.")

    return {"base_datos": POSTGRES_BASE_NARANJAS, "tabla": POSTGRES_TABLA_DATOS}


def registrar_datos_naranja_postgresql(control_bd, tipo):
    if control_bd is None:
        return

    incremento_mesa = 1 if tipo == TIPO_NARANJA_MESA else 0
    incremento_zumo = 1 if tipo == TIPO_NARANJA_ZUMO else 0
    incremento_rechazo = 1 if tipo == TIPO_NARANJA_RECHAZADA else 0

    ejecutar_psql(
        control_bd["base_datos"],
        f"""
        WITH ultimo AS (
            SELECT
                n_naranjas_procesadas,
                n_naranjas_mesa,
                n_naranjas_zumo,
                n_naranjas_rechazo
            FROM {control_bd["tabla"]}
            ORDER BY id_naranja DESC
            LIMIT 1
        ),
        acumulado AS (
            SELECT
                COALESCE((SELECT n_naranjas_procesadas FROM ultimo), 0) AS procesadas,
                COALESCE((SELECT n_naranjas_mesa FROM ultimo), 0) AS mesa,
                COALESCE((SELECT n_naranjas_zumo FROM ultimo), 0) AS zumo,
                COALESCE((SELECT n_naranjas_rechazo FROM ultimo), 0) AS rechazo
        )
        INSERT INTO {control_bd["tabla"]} (
            n_naranjas_procesadas,
            n_naranjas_mesa,
            n_naranjas_zumo,
            n_naranjas_rechazo,
            porcentaje_mesa,
            porcentaje_zumo,
            porcentaje_rechazo
        )
        SELECT
            procesadas + 1,
            mesa + {incremento_mesa},
            zumo + {incremento_zumo},
            rechazo + {incremento_rechazo},
            ROUND(((mesa + {incremento_mesa}) * 100.0) / (procesadas + 1), 2),
            ROUND(((zumo + {incremento_zumo}) * 100.0) / (procesadas + 1), 2),
            ROUND(((rechazo + {incremento_rechazo}) * 100.0) / (procesadas + 1), 2)
        FROM acumulado;
        """,
    )
    print(f"PostgreSQL actualizado con naranja tipo {tipo}.")


def alias_de(sim, objeto):
    try:
        return sim.getObjectAlias(objeto, 1)
    except Exception:
        return str(objeto)


def obtener_objeto_opcional(sim, ruta):
    try:
        return sim.getObject(ruta)
    except Exception:
        return None


def buscar_por_alias(sim, alias_buscado, tipo=0):
    objetos = sim.getObjectsInTree(sim.handle_scene, tipo, 0)

    for objeto in objetos:
        if alias_de(sim, objeto) == alias_buscado:
            return objeto

    return None


def buscar_naranja(sim, indice):
    alias = f"/Orange_{indice:02d}"
    naranja = obtener_objeto_opcional(sim, alias)

    if naranja is not None:
        return naranja

    return buscar_por_alias(sim, alias, sim.sceneobject_shape)


def buscar_naranjas(sim):
    naranjas = []

    for indice in range(1, TOTAL_NARANJAS + 1):
        naranja = buscar_naranja(sim, indice)

        if naranja is None:
            print(f"No se ha localizado Orange_{indice:02d}.")
            continue

        posicion = sim.getObjectPosition(naranja, sim.handle_world)
        print(
            f"Orange_{indice:02d} localizada en "
            f"x={posicion[0]:.3f}, y={posicion[1]:.3f}, z={posicion[2]:.3f}."
        )
        naranjas.append((indice, naranja))

    if not naranjas:
        raise RuntimeError("No se ha localizado ninguna naranja en la escena.")

    print(f"Naranjas localizadas: {len(naranjas)} de {TOTAL_NARANJAS}.")
    return naranjas


def desactivar_script(sim, ruta_script):
    script = obtener_objeto_opcional(sim, ruta_script)

    if script is None:
        print(f"No se ha localizado {ruta_script}; continuo solo con Python.")
        return None

    desactivado = False

    try:
        sim.setScriptAttribute(script, sim.scriptattribute_enabled, 0)
        desactivado = True
    except Exception:
        pass

    try:
        sim.setScriptInt32Param(script, sim.scriptintparam_enabled, 0)
        desactivado = True
    except Exception:
        pass

    if desactivado:
        print(f"Script Lua {ruta_script} desactivado.")
    else:
        print(f"No se ha podido cambiar el estado de {ruta_script}.")

    return script


def preparar_naranja_para_python(sim, indice, naranja, grupo_naranjas):
    if grupo_naranjas is not None:
        try:
            sim.setObjectParent(naranja, grupo_naranjas, True)
        except Exception:
            pass

    posicion_inicial = POSICIONES_INICIALES_NARANJAS.get(indice)

    if posicion_inicial is not None:
        sim.setObjectPosition(naranja, sim.handle_world, posicion_inicial)

    sim.setObjectInt32Param(naranja, sim.shapeintparam_static, 1)
    sim.setObjectInt32Param(naranja, sim.shapeintparam_respondable, 0)

    try:
        sim.resetDynamicObject(naranja)
    except Exception:
        pass


def preparar_naranjas(sim, naranjas):
    grupo_naranjas = obtener_objeto_opcional(sim, RUTA_GRUPO_NARANJAS)

    for indice, naranja in naranjas:
        preparar_naranja_para_python(sim, indice, naranja, grupo_naranjas)

    print("Python ha restaurado y tomado el control inicial de las naranjas.")


def crear_control_vision(sim):
    vision_sensor = obtener_objeto(sim, RUTA_VISION_SENSOR, "visionSensor")
    posicion_sensor = sim.getObjectPosition(vision_sensor, sim.handle_world)

    print(
        "Control de vision preparado: "
        f"x={posicion_sensor[0]:.3f}, y={posicion_sensor[1]:.3f}, "
        f"z={posicion_sensor[2]:.3f}."
    )

    return {
        "sensor": vision_sensor,
        "x_sensor": posicion_sensor[0],
        "capturas_realizadas": set(),
        "diametros": {},
        "muestras": {},
        "control_bd": None,
    }


def obtener_imagen_vision(sim, control_vision):
    imagen, resolucion = sim.getVisionSensorImg(control_vision["sensor"])
    imagen = np.frombuffer(imagen, dtype=np.uint8)
    ancho, alto = resolucion

    if imagen.size != ancho * alto * 3:
        raise RuntimeError("Imagen recibida desde visionSensor con tamano inesperado.")

    imagen = imagen.reshape(alto, ancho, 3)
    imagen = cv2.flip(imagen, 0)
    return cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)


def medir_diametro_naranja(imagen_bgr):
    imagen_bgr = cv2.GaussianBlur(imagen_bgr, (5, 5), 0)
    imagen_hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(imagen_hsv, HSV_NARANJA_BAJO, HSV_NARANJA_ALTO)
    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    if not contornos:
        return None, mascara

    contorno = max(contornos, key=cv2.contourArea)
    area = cv2.contourArea(contorno)

    if area < 20:
        return None, mascara

    diametro_equivalente = (4 * area / math.pi) ** 0.5
    return diametro_equivalente, mascara


def px_a_cm(diametro_px):
    if diametro_px is None:
        return None

    escala_cm_por_px = DIAMETRO_REAL_NARANJA_CM / DIAMETRO_REFERENCIA_NARANJA_PX
    return diametro_px * escala_cm_por_px


def clasificar_naranja(diametro_cm):
    if diametro_cm is None:
        return TIPO_NARANJA_DESCONOCIDA

    if 6.5 <= diametro_cm <= 8.5:
        return TIPO_NARANJA_MESA

    if 5.0 <= diametro_cm <= 6.49:
        return TIPO_NARANJA_ZUMO

    if diametro_cm < 5.0:
        return TIPO_NARANJA_RECHAZADA

    return TIPO_NARANJA_DESCONOCIDA


def mostrar_resultado_vision(indice, imagen_bgr, mascara, diametro_px, diametro_cm, tipo):
    vista = imagen_bgr.copy()

    if diametro_cm is not None:
        cv2.putText(
            vista,
            f"Orange_{indice:02d} diametro: {diametro_cm:.2f} cm",
            (12, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2,
        )

    cv2.putText(
        vista,
        f"Tipo: {tipo}",
        (12, 58),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2,
    )

    mascara_bgr = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    panel = np.hstack((vista, mascara_bgr))
    cv2.imshow("VisionSensor - naranja y mascara", panel)
    cv2.waitKey(1)


def registrar_medida_vision(control_vision, indice, imagen, mascara, diametro_px):
    CARPETA_CAPTURAS_VISION.mkdir(exist_ok=True)
    diametro_cm = px_a_cm(diametro_px)
    tipo = clasificar_naranja(diametro_cm)
    control_vision["capturas_realizadas"].add(indice)
    control_vision["diametros"][indice] = {
        "px": diametro_px,
        "cm": diametro_cm,
        "tipo": tipo,
    }
    cv2.imwrite(str(CARPETA_CAPTURAS_VISION / f"Orange_{indice:02d}.png"), imagen)
    cv2.imwrite(str(CARPETA_CAPTURAS_VISION / f"Orange_{indice:02d}_mascara.png"), mascara)
    mostrar_resultado_vision(indice, imagen, mascara, diametro_px, diametro_cm, tipo)

    if diametro_cm is None:
        print(f"Orange_{indice:02d}: no se ha podido medir diametro.")
    else:
        print(
            f"Orange_{indice:02d}: diametro medido = "
            f"{diametro_cm:.2f} cm ({diametro_px:.1f} px). Tipo: {tipo}."
        )

    registrar_datos_naranja_postgresql(control_vision.get("control_bd"), tipo)


def guardar_diametros(control_vision):
    with ARCHIVO_DIAMETROS.open("w", encoding="utf-8") as archivo:
        archivo.write("naranja,diametro_px,diametro_cm,tipo\n")

        for indice in sorted(control_vision["diametros"]):
            medida = control_vision["diametros"][indice]
            diametro_px = medida["px"]
            diametro_cm = medida["cm"]
            tipo = medida["tipo"]
            valor_px = "" if diametro_px is None else f"{diametro_px:.3f}"
            valor_cm = "" if diametro_cm is None else f"{diametro_cm:.3f}"
            archivo.write(f"Orange_{indice:02d},{valor_px},{valor_cm},{tipo}\n")

    print(f"Diametros guardados en {ARCHIVO_DIAMETROS}.")


def actualizar_vision_en_transporte(sim, control_cinta, control_vision):
    if control_vision is None:
        return

    for _, datos in list(control_cinta["objetos_transportados"].items()):
        indice = datos["indice"]

        if indice in control_vision["capturas_realizadas"]:
            continue

        posicion_x = sim.getObjectPosition(datos["naranja"], sim.handle_world)[0]
        distancia_sensor = posicion_x - control_vision["x_sensor"]

        if abs(distancia_sensor) <= VENTANA_CAPTURA_VISION:
            imagen = obtener_imagen_vision(sim, control_vision)
            diametro_px, mascara = medir_diametro_naranja(imagen)
            muestra_actual = control_vision["muestras"].get(indice)

            if (
                muestra_actual is None
                or abs(distancia_sensor) < muestra_actual["distancia_abs"]
            ):
                control_vision["muestras"][indice] = {
                    "distancia_abs": abs(distancia_sensor),
                    "imagen": imagen,
                    "mascara": mascara,
                    "diametro_px": diametro_px,
                }

        if distancia_sensor > VENTANA_CAPTURA_VISION:
            muestra = control_vision["muestras"].pop(indice, None)

            if muestra is not None:
                registrar_medida_vision(
                    control_vision,
                    indice,
                    muestra["imagen"],
                    muestra["mascara"],
                    muestra["diametro_px"],
                )


def obtener_objeto(sim, ruta, descripcion):
    objeto = obtener_objeto_opcional(sim, ruta)

    if objeto is None:
        raise RuntimeError(f"No se ha podido localizar {descripcion}: {ruta}")

    return objeto


def crear_control_robot(sim):
    ur3 = obtener_objeto(sim, RUTA_UR3, "UR3")
    rg2 = obtener_objeto(sim, RUTA_RG2, "pinza RG2")
    attach_point = obtener_objeto(sim, RUTA_ATTACH_POINT_RG2, "attachPoint RG2")
    dedo_izquierdo = obtener_objeto(sim, RUTA_DEDO_IZQUIERDO_RG2, "dedo izquierdo RG2")
    dedo_derecho = obtener_objeto(sim, RUTA_DEDO_DERECHO_RG2, "dedo derecho RG2")
    target = obtener_objeto(sim, RUTA_TARGET_UR3, "UR3_target")
    tip = obtener_objeto(sim, RUTA_TIP_UR3, "UR3_tip")
    script_ik = obtener_objeto(sim, RUTA_SCRIPT_IK_UR3, "script IK del UR3")
    articulacion_base = obtener_objeto(sim, "/UR3/joint", "articulacion base UR3")

    articulaciones_rg2 = set(sim.getObjectsInTree(rg2, sim.object_joint_type, 0))
    articulaciones_ur3 = [
        articulacion
        for articulacion in sim.getObjectsInTree(ur3, sim.object_joint_type, 0)
        if articulacion not in articulaciones_rg2
    ]

    articulacion_apertura = None

    for articulacion in articulaciones_rg2:
        if alias_de(sim, articulacion).endswith("/openCloseJoint"):
            articulacion_apertura = articulacion
            break

    if articulacion_apertura is None:
        raise RuntimeError("No se ha localizado /openCloseJoint dentro de la RG2.")

    print("Control Python de UR3/RG2 preparado.")

    return {
        "ur3": ur3,
        "rg2": rg2,
        "articulacion_apertura": articulacion_apertura,
        "attach_point": attach_point,
        "dedo_izquierdo": dedo_izquierdo,
        "dedo_derecho": dedo_derecho,
        "target": target,
        "tip": tip,
        "script_ik": script_ik,
        "articulacion_base": articulacion_base,
        "articulaciones_ur3": articulaciones_ur3,
        "posiciones_articulaciones_iniciales": [
            sim.getJointPosition(articulacion)
            for articulacion in articulaciones_ur3
        ],
        "posicion_target_inicial": list(sim.getObjectPosition(target, sim.handle_world)),
        "orientacion_target_inicial": list(
            sim.getObjectOrientation(target, sim.handle_world)
        ),
        "posicion_tip_inicial": list(sim.getObjectPosition(tip, sim.handle_world)),
        "orientacion_tip_inicial": list(sim.getObjectOrientation(tip, sim.handle_world)),
        "posicion_base_inicial": sim.getJointPosition(articulacion_base),
    }


def calcular_distancia(posicion_a, posicion_b):
    return (
        (posicion_a[0] - posicion_b[0]) ** 2
        + (posicion_a[1] - posicion_b[1]) ** 2
        + (posicion_a[2] - posicion_b[2]) ** 2
    ) ** 0.5


def limitar(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def fijar_postura_inicial_ur3(sim, control_robot):
    print("Fijando UR3 en la postura inicial de referencia.")
    sim.setJointPosition(control_robot["articulacion_base"], POSICION_BASE_UR3_INICIAL)
    sim.setObjectPosition(
        control_robot["target"],
        sim.handle_world,
        POSICION_TARGET_UR3_INICIAL,
    )
    sim.setObjectOrientation(
        control_robot["target"],
        sim.handle_world,
        ORIENTACION_TARGET_UR3_INICIAL,
    )
    resolver_ik(sim, control_robot, ITERACIONES_IK * 3)

    control_robot["posiciones_articulaciones_iniciales"] = [
        sim.getJointPosition(articulacion)
        for articulacion in control_robot["articulaciones_ur3"]
    ]
    control_robot["posicion_target_inicial"] = list(
        sim.getObjectPosition(control_robot["target"], sim.handle_world)
    )
    control_robot["orientacion_target_inicial"] = list(
        sim.getObjectOrientation(control_robot["target"], sim.handle_world)
    )
    control_robot["posicion_tip_inicial"] = list(
        sim.getObjectPosition(control_robot["tip"], sim.handle_world)
    )
    control_robot["orientacion_tip_inicial"] = list(
        sim.getObjectOrientation(control_robot["tip"], sim.handle_world)
    )
    control_robot["posicion_base_inicial"] = sim.getJointPosition(
        control_robot["articulacion_base"]
    )


def medir_separacion_dedos(sim, control_robot):
    posicion_izquierda = sim.getObjectPosition(
        control_robot["dedo_izquierdo"],
        sim.handle_world,
    )
    posicion_derecha = sim.getObjectPosition(
        control_robot["dedo_derecho"],
        sim.handle_world,
    )

    return calcular_distancia(posicion_izquierda, posicion_derecha)


def fijar_separacion_pinza(sim, control_robot, separacion_objetivo, permitir_contacto=False):
    articulacion = control_robot["articulacion_apertura"]
    separacion_actual = medir_separacion_dedos(sim, control_robot)
    diferencia = separacion_objetivo - separacion_actual
    tolerancia = (
        TOLERANCIA_SEPARACION_AGARRE
        if permitir_contacto
        else TOLERANCIA_SEPARACION_PINZA
    )

    if abs(diferencia) <= tolerancia:
        sim.setJointTargetVelocity(articulacion, 0.0)
        return

    velocidad = VELOCIDAD_APERTURA_PINZA if diferencia > 0 else VELOCIDAD_CIERRE_PINZA
    sim.setJointForce(articulacion, FUERZA_PINZA)
    sim.setJointTargetVelocity(articulacion, velocidad)

    inicio = time.time()

    while time.time() - inicio < TIEMPO_MAXIMO_AJUSTE_PINZA:
        separacion_actual = medir_separacion_dedos(sim, control_robot)
        diferencia = separacion_objetivo - separacion_actual

        if abs(diferencia) <= tolerancia:
            velocidad_final = VELOCIDAD_MANTENER_AGARRE if permitir_contacto else 0.0
            sim.setJointTargetVelocity(articulacion, velocidad_final)
            return

        nueva_velocidad = VELOCIDAD_APERTURA_PINZA if diferencia > 0 else VELOCIDAD_CIERRE_PINZA

        if nueva_velocidad != velocidad:
            velocidad = nueva_velocidad
            sim.setJointTargetVelocity(articulacion, velocidad)

        time.sleep(sim.getSimulationTimeStep())

    if permitir_contacto:
        separacion_actual = medir_separacion_dedos(sim, control_robot)

        if separacion_actual <= separacion_objetivo + tolerancia:
            sim.setJointTargetVelocity(articulacion, VELOCIDAD_MANTENER_AGARRE)
            print(
                "La RG2 no alcanzo exactamente la separacion objetivo, "
                f"pero queda en agarre: {separacion_actual:.4f} m."
            )
            return

    sim.setJointTargetVelocity(articulacion, 0.0)
    raise RuntimeError("La RG2 no ha alcanzado la apertura solicitada.")


def abrir_pinza_totalmente(sim, control_robot):
    print("Abriendo completamente la RG2.")
    try:
        fijar_separacion_pinza(sim, control_robot, SEPARACION_DEDOS_PINZA_ABIERTA)
        return
    except RuntimeError:
        separacion = medir_separacion_dedos(sim, control_robot)

        if separacion >= SEPARACION_DEDOS_PINZA_ABIERTA_MINIMA:
            sim.setJointTargetVelocity(control_robot["articulacion_apertura"], 0.0)
            print(
                "La RG2 no alcanzo la apertura maxima exacta, "
                f"pero queda suficientemente abierta: {separacion:.4f} m."
            )
            return

        sim.setJointTargetVelocity(control_robot["articulacion_apertura"], 0.0)
        raise


def cerrar_pinza_para_naranja(sim, control_robot):
    print("Cerrando RG2 para sujetar la naranja.")
    cerrar_pinza_a_separacion(
        sim,
        control_robot,
        SEPARACION_DEDOS_PINZA_CERRADA,
    )


def cerrar_pinza_a_separacion(sim, control_robot, separacion_objetivo):
    print(f"Cerrando RG2 hasta {separacion_objetivo:.4f} m.")
    articulacion = control_robot["articulacion_apertura"]
    sim.setJointForce(articulacion, FUERZA_PINZA)
    sim.setJointTargetVelocity(articulacion, VELOCIDAD_CIERRE_PINZA)

    inicio = time.time()

    while time.time() - inicio < TIEMPO_CIERRE_AGARRE_NARANJA:
        separacion = medir_separacion_dedos(sim, control_robot)

        if separacion <= separacion_objetivo:
            break

        time.sleep(sim.getSimulationTimeStep())

    sim.setJointTargetVelocity(articulacion, VELOCIDAD_MANTENER_AGARRE)
    separacion = medir_separacion_dedos(sim, control_robot)
    print(f"RG2 en agarre de naranja. Separacion actual: {separacion:.4f} m.")


def calcular_centro_dedos_en_attach(sim, control_robot):
    attach_point = control_robot["attach_point"]
    posicion_izquierda = sim.getObjectPosition(
        control_robot["dedo_izquierdo"],
        attach_point,
    )
    posicion_derecha = sim.getObjectPosition(
        control_robot["dedo_derecho"],
        attach_point,
    )

    return [
        (posicion_izquierda[0] + posicion_derecha[0]) / 2,
        (posicion_izquierda[1] + posicion_derecha[1]) / 2,
        (posicion_izquierda[2] + posicion_derecha[2]) / 2,
    ]


def calcular_centro_dedos_en_mundo(sim, control_robot):
    posicion_izquierda = sim.getObjectPosition(
        control_robot["dedo_izquierdo"],
        sim.handle_world,
    )
    posicion_derecha = sim.getObjectPosition(
        control_robot["dedo_derecho"],
        sim.handle_world,
    )

    return [
        (posicion_izquierda[0] + posicion_derecha[0]) / 2,
        (posicion_izquierda[1] + posicion_derecha[1]) / 2,
        (posicion_izquierda[2] + posicion_derecha[2]) / 2,
    ]


def mover_centro_dedos_a_posicion(
    sim,
    control_robot,
    posicion_centro_objetivo,
    descripcion,
):
    target = control_robot["target"]
    posicion_target = sim.getObjectPosition(target, sim.handle_world)
    centro_dedos = calcular_centro_dedos_en_mundo(sim, control_robot)
    posicion_objetivo_target = [
        posicion_target[i] + posicion_centro_objetivo[i] - centro_dedos[i]
        for i in range(3)
    ]

    mover_target_ur3(sim, control_robot, posicion_objetivo_target, descripcion)


def separacion_agarre_desde_diametro(control_cinta, indice):
    control_vision = control_cinta.get("control_vision")
    diametro_cm = DIAMETRO_REAL_NARANJA_CM

    if control_vision is not None:
        medida = control_vision["diametros"].get(indice)

        if medida is not None and medida["cm"] is not None:
            diametro_cm = medida["cm"]

    diametro_m = diametro_cm / 100
    separacion = limitar(
        diametro_m * FACTOR_CIERRE_SEGUN_DIAMETRO,
        SEPARACION_MINIMA_AGARRE,
        SEPARACION_MAXIMA_AGARRE,
    )
    print(
        f"Orange_{indice:02d}: diametro usado para agarre "
        f"{diametro_cm:.2f} cm, separacion RG2 {separacion:.4f} m."
    )
    return separacion


def acoplar_naranja_a_pinza(sim, control_robot, naranja):
    sim.setObjectParent(naranja, control_robot["attach_point"], True)
    sim.setObjectInt32Param(naranja, sim.shapeintparam_static, 1)
    sim.setObjectInt32Param(naranja, sim.shapeintparam_respondable, 0)


def resolver_ik(sim, control_robot, iteraciones=ITERACIONES_IK):
    for _ in range(iteraciones):
        sim.callScriptFunction("handleIk", control_robot["script_ik"])


def actualizar_naranja_en_preparacion(sim, control_cinta, preparacion):
    if control_cinta is None or preparacion is None or preparacion.get("lista"):
        return

    aplicar_control_cinta(sim, control_cinta)
    llega, _, _ = naranja_llega_centrada_al_sensor(
        sim,
        control_cinta,
        preparacion["naranja"],
    )

    if sensor_final_detecta_naranja(sim, control_cinta, preparacion["naranja"]) or llega:
        detener_naranja_en_sensor(sim, control_cinta, preparacion["naranja"])
        preparacion["lista"] = True
        print(
            f"Orange_{preparacion['indice']:02d} queda preparada en sensor_final_cinta."
        )


def esperar_paso_simulacion(sim, control_cinta=None, preparacion=None):
    actualizar_naranja_en_preparacion(sim, control_cinta, preparacion)
    time.sleep(sim.getSimulationTimeStep())


def mover_target_ur3(
    sim,
    control_robot,
    posicion_objetivo,
    descripcion,
    control_cinta=None,
    preparacion=None,
):
    target = control_robot["target"]
    posicion_inicial = sim.getObjectPosition(target, sim.handle_world)

    print(f"Moviendo UR3_target a {descripcion}.")

    for paso in range(1, PASOS_MOVIMIENTO_UR3 + 1):
        progreso = paso / PASOS_MOVIMIENTO_UR3
        posicion = [
            posicion_inicial[i]
            + (posicion_objetivo[i] - posicion_inicial[i]) * progreso
            for i in range(3)
        ]

        sim.setObjectPosition(target, sim.handle_world, posicion)
        resolver_ik(sim, control_robot, 2)
        actualizar_naranja_en_preparacion(sim, control_cinta, preparacion)
        time.sleep(PAUSA_MOVIMIENTO_UR3)

    resolver_ik(sim, control_robot)


def mover_target_ur3_rapido(
    sim,
    control_robot,
    posicion_objetivo,
    descripcion,
    control_cinta=None,
    preparacion=None,
):
    target = control_robot["target"]
    posicion_inicial = sim.getObjectPosition(target, sim.handle_world)

    print(f"Moviendo UR3_target rapidamente a {descripcion}.")

    for paso in range(1, PASOS_MOVIMIENTO_PRE_GIRO_RAPIDO + 1):
        progreso = paso / PASOS_MOVIMIENTO_PRE_GIRO_RAPIDO
        posicion = [
            posicion_inicial[i]
            + (posicion_objetivo[i] - posicion_inicial[i]) * progreso
            for i in range(3)
        ]

        sim.setObjectPosition(target, sim.handle_world, posicion)
        resolver_ik(sim, control_robot, 3)
        actualizar_naranja_en_preparacion(sim, control_cinta, preparacion)

        if PAUSA_MOVIMIENTO_PRE_GIRO_RAPIDO > 0:
            time.sleep(PAUSA_MOVIMIENTO_PRE_GIRO_RAPIDO)

    resolver_ik(sim, control_robot)


def posicion_recogida_naranja(control_cinta, altura):
    return [
        control_cinta["x_sensor"],
        control_cinta["y_centro"],
        altura,
    ]


def rotar_posicion_sobre_eje_z(posicion, centro, angulo):
    dx = posicion[0] - centro[0]
    dy = posicion[1] - centro[1]
    coseno = math.cos(angulo)
    seno = math.sin(angulo)

    return [
        centro[0] + dx * coseno - dy * seno,
        centro[1] + dx * seno + dy * coseno,
        posicion[2],
    ]


def restaurar_target_inicial(sim, control_robot, control_cinta=None, preparacion=None):
    mover_target_ur3(
        sim,
        control_robot,
        control_robot["posicion_target_inicial"],
        "posicion inicial antes de girar",
        control_cinta,
        preparacion,
    )


def preparar_target_para_giro(sim, control_robot, control_cinta=None, preparacion=None):
    target = control_robot["target"]
    posicion_actual = sim.getObjectPosition(target, sim.handle_world)
    posicion_inicial = control_robot["posicion_target_inicial"]
    z_segura = max(
        ALTURA_SEGURA_GIRO_UR3,
        posicion_actual[2],
        posicion_inicial[2],
    )

    mover_target_ur3_rapido(
        sim,
        control_robot,
        [posicion_actual[0], posicion_actual[1], z_segura],
        "altura segura antes de girar",
        control_cinta,
        preparacion,
    )

    mover_target_ur3_rapido(
        sim,
        control_robot,
        [posicion_inicial[0], posicion_inicial[1], z_segura],
        "posicion inicial alta antes de girar sin bajar",
        control_cinta,
        preparacion,
    )


def restaurar_robot_inicio_ciclo(sim, control_robot):
    articulaciones = control_robot["articulaciones_ur3"]
    posiciones_iniciales = control_robot["posiciones_articulaciones_iniciales"]
    target = control_robot["target"]

    print("Restaurando UR3 a la posicion inicial exacta de ciclo.")

    for articulacion, posicion in zip(articulaciones, posiciones_iniciales):
        sim.setJointPosition(articulacion, posicion)
        sim.setJointTargetPosition(articulacion, posicion)

    sim.setObjectPosition(
        target,
        sim.handle_world,
        control_robot["posicion_target_inicial"],
    )
    sim.setObjectOrientation(
        target,
        sim.handle_world,
        control_robot["orientacion_target_inicial"],
    )
    resolver_ik(sim, control_robot, 20)

    posicion_tip = sim.getObjectPosition(control_robot["tip"], sim.handle_world)
    error_tip = calcular_distancia(posicion_tip, control_robot["posicion_tip_inicial"])

    print(f"UR3 restaurado. Error de tip respecto al inicio: {error_tip:.4f} m.")


def mover_robot_a_inicio_ciclo_suave(sim, control_robot):
    mover_target_ur3(
        sim,
        control_robot,
        control_robot["posicion_target_inicial"],
        "posicion inicial de recogida",
    )
    restaurar_robot_inicio_ciclo(sim, control_robot)


def girar_base_con_target(
    sim,
    control_robot,
    giro,
    descripcion,
    control_cinta=None,
    preparacion=None,
):
    articulacion_base = control_robot["articulacion_base"]
    target = control_robot["target"]
    posicion_base = sim.getObjectPosition(articulacion_base, sim.handle_world)
    posicion_base_inicial = sim.getJointPosition(articulacion_base)
    posicion_target_inicial = sim.getObjectPosition(target, sim.handle_world)
    z_giro = posicion_target_inicial[2]
    posicion_base_final = posicion_base_inicial + giro

    print(f"Girando base del UR3 hacia {descripcion} manteniendo z={z_giro:.3f} m.")

    for paso in range(1, PASOS_MOVIMIENTO_UR3 + 1):
        progreso = paso / PASOS_MOVIMIENTO_UR3
        giro_actual = giro * progreso
        posicion_articulacion = posicion_base_inicial + giro_actual
        posicion_target = rotar_posicion_sobre_eje_z(
            posicion_target_inicial,
            posicion_base,
            giro_actual,
        )
        posicion_target[2] = z_giro

        sim.setObjectPosition(target, sim.handle_world, posicion_target)
        sim.setJointPosition(articulacion_base, posicion_articulacion)
        sim.setJointTargetPosition(articulacion_base, posicion_articulacion)
        resolver_ik(sim, control_robot, 2)
        actualizar_naranja_en_preparacion(sim, control_cinta, preparacion)
        time.sleep(PAUSA_MOVIMIENTO_UR3)

    posicion_target_final = rotar_posicion_sobre_eje_z(
        posicion_target_inicial,
        posicion_base,
        giro,
    )
    posicion_target_final[2] = z_giro
    sim.setObjectPosition(target, sim.handle_world, posicion_target_final)
    sim.setJointPosition(articulacion_base, posicion_base_final)
    sim.setJointTargetPosition(articulacion_base, posicion_base_final)
    resolver_ik(sim, control_robot)


def avanzar_target_en_x(
    sim,
    control_robot,
    desplazamiento_x,
    descripcion,
    control_cinta=None,
    preparacion=None,
):
    posicion = sim.getObjectPosition(control_robot["target"], sim.handle_world)
    posicion_objetivo = [
        posicion[0] + desplazamiento_x,
        posicion[1],
        posicion[2],
    ]

    mover_target_ur3(
        sim,
        control_robot,
        posicion_objetivo,
        descripcion,
        control_cinta,
        preparacion,
    )


def depositar_naranja_en_caja_amarilla(
    sim,
    control_robot,
    indice,
    naranja,
    control_cinta=None,
    preparacion=None,
):
    posicion_alta = sim.getObjectPosition(control_robot["target"], sim.handle_world)
    posicion_deposito = [
        posicion_alta[0],
        posicion_alta[1],
        Z_TARGET_PRE_APERTURA_CAJA_AMARILLA,
    ]

    mover_target_ur3(
        sim,
        control_robot,
        posicion_deposito,
        f"deposito de Orange_{indice:02d} sobre caja amarilla",
        control_cinta,
        preparacion,
    )
    try:
        abrir_pinza_totalmente(sim, control_robot)
    except RuntimeError:
        separacion = medir_separacion_dedos(sim, control_robot)

        if separacion < SEPARACION_DEDOS_PINZA_CERRADA:
            raise

        print(
            "La RG2 no pudo abrir completamente durante el deposito, "
            f"pero queda abierta para soltar: {separacion:.4f} m."
        )

    sim.setObjectParent(naranja, sim.handle_world, True)
    sim.setObjectInt32Param(naranja, sim.shapeintparam_static, 0)
    sim.setObjectInt32Param(naranja, sim.shapeintparam_respondable, 1)

    try:
        sim.resetDynamicObject(naranja)
    except Exception:
        pass

    mover_target_ur3(
        sim,
        control_robot,
        posicion_alta,
        "subida tras deposito sobre caja amarilla",
        control_cinta,
        preparacion,
    )


def obtener_tipo_naranja(control_cinta, indice):
    control_vision = control_cinta.get("control_vision")

    if control_vision is None:
        return TIPO_NARANJA_DESCONOCIDA

    medida = control_vision["diametros"].get(indice)

    if medida is None:
        return TIPO_NARANJA_DESCONOCIDA

    return medida["tipo"]


def giro_deposito_por_tipo(tipo):
    if tipo == TIPO_NARANJA_MESA:
        return GIRO_BASE_CAJA_VERDE_MESA, "caja verde para naranja de mesa"

    if tipo == TIPO_NARANJA_ZUMO:
        return GIRO_BASE_CAJA_AMARILLA_ZUMO, "caja amarilla para naranja de zumo"

    if tipo == TIPO_NARANJA_RECHAZADA:
        return GIRO_BASE_RECHAZO, "zona de rechazo"

    return GIRO_BASE_CAJA_AMARILLA_ZUMO, "caja amarilla por clasificacion desconocida"


def avance_x_deposito_por_tipo(tipo):
    if tipo == TIPO_NARANJA_MESA:
        return AVANCE_X_TARGET_DEPOSITO_MESA

    if tipo == TIPO_NARANJA_RECHAZADA:
        return AVANCE_X_TARGET_DEPOSITO_RECHAZO

    return AVANCE_X_TARGET_DEPOSITO


def recoger_y_elevar_naranja_con_ur3(sim, control_robot, control_cinta, indice, naranja):
    posicion_naranja = sim.getObjectPosition(naranja, sim.handle_world)
    separacion_agarre = separacion_agarre_desde_diametro(control_cinta, indice)
    posicion_aproximacion = [
        posicion_naranja[0],
        posicion_naranja[1],
        ALTURA_CENTRO_DEDOS_APROXIMACION,
    ]
    posicion_recogida = [
        posicion_naranja[0],
        posicion_naranja[1],
        ALTURA_CENTRO_DEDOS_RECOGIDA,
    ]
    posicion_elevacion = [
        posicion_naranja[0],
        posicion_naranja[1],
        ALTURA_ELEVACION_NARANJA,
    ]

    mover_centro_dedos_a_posicion(
        sim,
        control_robot,
        posicion_aproximacion,
        f"aproximacion de dedos sobre Orange_{indice:02d}",
    )
    mover_centro_dedos_a_posicion(
        sim,
        control_robot,
        posicion_recogida,
        f"recogida de dedos de Orange_{indice:02d}",
    )
    cerrar_pinza_a_separacion(sim, control_robot, separacion_agarre)

    acoplar_naranja_a_pinza(sim, control_robot, naranja)

    mover_centro_dedos_a_posicion(
        sim,
        control_robot,
        posicion_elevacion,
        f"elevacion de dedos con Orange_{indice:02d}",
    )

    print(f"Orange_{indice:02d} recogida y elevada por el UR3.")


def depositar_y_volver_a_recogida(
    sim,
    control_robot,
    control_cinta,
    indice,
    naranja,
    preparacion=None,
):
    tipo = obtener_tipo_naranja(control_cinta, indice)
    giro_deposito, descripcion_deposito = giro_deposito_por_tipo(tipo)
    print(f"Orange_{indice:02d}: tipo {tipo}. Destino: {descripcion_deposito}.")
    preparar_target_para_giro(sim, control_robot, control_cinta, preparacion)
    girar_base_con_target(
        sim,
        control_robot,
        giro_deposito,
        descripcion_deposito,
        control_cinta,
        preparacion,
    )
    avance_x_deposito = avance_x_deposito_por_tipo(tipo)

    if tipo == TIPO_NARANJA_RECHAZADA:
        avanzar_target_en_x(
            sim,
            control_robot,
            avance_x_deposito,
            "avance directo hacia caja roja de rechazo",
            control_cinta,
            preparacion,
        )
        depositar_naranja_en_caja_amarilla(
            sim,
            control_robot,
            indice,
            naranja,
            control_cinta,
            preparacion,
        )
        avanzar_target_en_x(
            sim,
            control_robot,
            -avance_x_deposito,
            "retroceso desde caja roja de rechazo",
            control_cinta,
            preparacion,
        )
        girar_base_con_target(
            sim,
            control_robot,
            -giro_deposito,
            "posicion inicial",
            control_cinta,
            preparacion,
        )
        restaurar_robot_inicio_ciclo(sim, control_robot)
        print(f"Orange_{indice:02d} depositada y UR3 preparado para recogida.")
        return

    avanzar_target_en_x(
        sim,
        control_robot,
        avance_x_deposito,
        "avance hacia la caja de deposito",
        control_cinta,
        preparacion,
    )
    depositar_naranja_en_caja_amarilla(
        sim,
        control_robot,
        indice,
        naranja,
        control_cinta,
        preparacion,
    )
    avanzar_target_en_x(
        sim,
        control_robot,
        -avance_x_deposito,
        "retroceso desde la caja de deposito",
        control_cinta,
        preparacion,
    )
    girar_base_con_target(
        sim,
        control_robot,
        -giro_deposito,
        "posicion inicial",
        control_cinta,
        preparacion,
    )
    restaurar_robot_inicio_ciclo(sim, control_robot)

    print(f"Orange_{indice:02d} depositada y UR3 preparado para recogida.")


def crear_control_cinta(sim):
    cinta = obtener_objeto_opcional(sim, RUTA_CINTA)
    sensor_final = obtener_objeto_opcional(sim, RUTA_SENSOR_FINAL_CINTA)
    punto_caida = obtener_objeto_opcional(sim, RUTA_PUNTO_CAIDA)

    if cinta is None:
        raise RuntimeError(f"No se ha podido localizar la cinta: {RUTA_CINTA}")

    if sensor_final is None:
        raise RuntimeError(
            f"No se ha podido localizar el sensor final: {RUTA_SENSOR_FINAL_CINTA}"
        )

    objetos_propios = set(sim.getObjectsInTree(cinta, sim.handle_all, 0))
    posicion_sensor = sim.getObjectPosition(sensor_final, sim.handle_world)
    posicion_caida = (
        sim.getObjectPosition(punto_caida, sim.handle_world)
        if punto_caida is not None
        else [-1.77, Y_CAIDA_CINTA, Z_CAIDA_CINTA]
    )

    print(
        "Control Python de cinta preparado: "
        f"velocidad={VELOCIDAD_CINTA:.2f} m/s, "
        f"inicio x={posicion_caida[0]:.3f}, "
        f"sensor final x={posicion_sensor[0]:.3f}."
    )

    return {
        "cinta": cinta,
        "sensor_final": sensor_final,
        "objetos_propios": objetos_propios,
        "objetos_transportados": {},
        "control_vision": None,
        "x_inicio": posicion_caida[0],
        "y_centro": Y_CAIDA_CINTA,
        "z_contacto": Z_CAIDA_CINTA,
        "x_sensor": posicion_sensor[0],
    }


def aplicar_control_cinta(sim, control_cinta):
    tiempo_actual = sim.getSimulationTime()

    for shape, datos in list(control_cinta["objetos_transportados"].items()):
        tiempo_transporte = max(0.0, tiempo_actual - datos["tiempo_inicio"])
        x = datos["x_inicio"] + VELOCIDAD_CINTA * tiempo_transporte

        sim.setObjectPosition(
            shape,
            sim.handle_world,
            [x, control_cinta["y_centro"], control_cinta["z_contacto"]],
        )

    actualizar_vision_en_transporte(
        sim,
        control_cinta,
        control_cinta.get("control_vision"),
    )


def naranja_llega_centrada_al_sensor(sim, control_cinta, naranja):
    posicion_mundo = sim.getObjectPosition(naranja, sim.handle_world)
    posicion_local = sim.getObjectPosition(naranja, control_cinta["cinta"])
    llega_al_sensor = posicion_mundo[0] >= control_cinta["x_sensor"] - TOLERANCIA_X_SENSOR
    esta_centrada = abs(posicion_local[1]) <= TOLERANCIA_CENTRADO_SENSOR

    return llega_al_sensor and esta_centrada, posicion_mundo, posicion_local


def sensor_final_detecta_naranja(sim, control_cinta, naranja):
    try:
        lectura = sim.readProximitySensor(control_cinta["sensor_final"])
    except Exception:
        return False

    detectado = bool(lectura[0])
    objeto_detectado = lectura[3] if detectado and len(lectura) > 3 else -1

    return objeto_detectado == naranja


def detener_naranja_en_sensor(sim, control_cinta, naranja):
    control_cinta["objetos_transportados"].pop(naranja, None)
    sim.setObjectPosition(
        naranja,
        sim.handle_world,
        [
            control_cinta["x_sensor"],
            control_cinta["y_centro"],
            control_cinta["z_contacto"],
        ],
    )

    try:
        sim.setObjectInt32Param(naranja, sim.shapeintparam_static, 0)
        sim.setObjectInt32Param(naranja, sim.shapeintparam_respondable, 1)
        sim.resetDynamicObject(naranja)
    except Exception:
        pass


def esperar_naranja_en_sensor(sim, control_cinta, indice, naranja):
    print(f"Cinta en marcha: esperando Orange_{indice:02d} en sensor_final_cinta.")
    inicio = time.time()

    while time.time() - inicio < TIEMPO_MAXIMO_TRANSPORTE:
        aplicar_control_cinta(sim, control_cinta)
        llega, posicion_mundo, posicion_local = naranja_llega_centrada_al_sensor(
            sim,
            control_cinta,
            naranja,
        )

        if sensor_final_detecta_naranja(sim, control_cinta, naranja) or llega:
            detener_naranja_en_sensor(sim, control_cinta, naranja)
            print(
                f"Sensor final detecta Orange_{indice:02d}. "
                f"Cinta parada con naranja centrada: "
                f"x={control_cinta['x_sensor']:.3f}, "
                f"y={control_cinta['y_centro']:.3f}, "
                f"z={control_cinta['z_contacto']:.3f}."
            )
            return

        time.sleep(sim.getSimulationTimeStep())

    posicion = sim.getObjectPosition(naranja, sim.handle_world)
    raise RuntimeError(
        f"Orange_{indice:02d} no ha llegado al sensor final en "
        f"{TIEMPO_MAXIMO_TRANSPORTE:.1f} s. "
        f"Ultima posicion: x={posicion[0]:.3f}, "
        f"y={posicion[1]:.3f}, z={posicion[2]:.3f}."
    )


def naranja_retirada_por_robot(sim, control_cinta, naranja):
    posicion = sim.getObjectPosition(naranja, sim.handle_world)
    dx = posicion[0] - control_cinta["x_sensor"]
    dy = posicion[1] - control_cinta["y_centro"]
    distancia_horizontal = (dx * dx + dy * dy) ** 0.5

    return (
        posicion[2] >= ALTURA_MINIMA_NARANJA_LEVANTADA
        or distancia_horizontal >= DISTANCIA_MINIMA_RETIRADA_SENSOR
    )


def esperar_retirada_por_robot(sim, control_cinta, indice, naranja):
    print(
        f"Cinta y caida detenidas. "
        f"Esperando a que el UR3 levante Orange_{indice:02d}."
    )
    inicio = time.time()

    while time.time() - inicio < TIEMPO_MAXIMO_ESPERA_ROBOT:
        if naranja_retirada_por_robot(sim, control_cinta, naranja):
            posicion = sim.getObjectPosition(naranja, sim.handle_world)
            print(
                f"Orange_{indice:02d} retirada por el UR3: "
                f"x={posicion[0]:.3f}, y={posicion[1]:.3f}, z={posicion[2]:.3f}."
            )
            return

        time.sleep(sim.getSimulationTimeStep())

    raise RuntimeError(
        f"El UR3 no ha retirado Orange_{indice:02d} en "
        f"{TIEMPO_MAXIMO_ESPERA_ROBOT:.1f} s."
    )


def actualizar_llegadas_al_sensor(sim, control_cinta, pendientes_sensor):
    if not pendientes_sensor:
        return

    for indice, naranja in list(pendientes_sensor.items()):
        llega, posicion_mundo, posicion_local = naranja_llega_centrada_al_sensor(
            sim,
            control_cinta,
            naranja,
        )

        if not llega:
            continue

        print(
            f"Orange_{indice:02d} llega centrada al sensor final: "
            f"x={posicion_mundo[0]:.3f}, "
            f"y local cinta={posicion_local[1]:.3f}, "
            f"z={posicion_mundo[2]:.3f}."
        )
        del pendientes_sensor[indice]


def ejecutar_cinta_durante(sim, control_cinta, duracion, pendientes_sensor=None):
    inicio = time.time()

    while time.time() - inicio < duracion:
        aplicar_control_cinta(sim, control_cinta)
        actualizar_llegadas_al_sensor(sim, control_cinta, pendientes_sensor)
        time.sleep(sim.getSimulationTimeStep())


def esperar_llegada_pendientes_al_sensor(sim, control_cinta, pendientes_sensor):
    inicio = time.time()

    while pendientes_sensor and time.time() - inicio < TIEMPO_MAXIMO_TRANSPORTE:
        aplicar_control_cinta(sim, control_cinta)
        actualizar_llegadas_al_sensor(sim, control_cinta, pendientes_sensor)
        time.sleep(sim.getSimulationTimeStep())

    if pendientes_sensor:
        pendientes = ", ".join(f"Orange_{indice:02d}" for indice in pendientes_sensor)
        raise RuntimeError(
            "No todas las naranjas han llegado centradas al sensor final. "
            f"Pendientes: {pendientes}."
        )

    print("Todas las naranjas han llegado centradas al sensor final.")


def iniciar_simulacion_si_es_necesario(sim):
    if sim.getSimulationState() == sim.simulation_stopped:
        print("Iniciando simulacion...")
        sim.startSimulation()
        time.sleep(0.2)
    else:
        print("La simulacion ya estaba iniciada.")


def aproximar(valor_actual, valor_objetivo, paso):
    diferencia = valor_objetivo - valor_actual

    if abs(diferencia) <= paso:
        return valor_objetivo, True

    if diferencia > 0:
        return valor_actual + paso, False

    return valor_actual - paso, False


def mover_naranja_sobre_cinta(sim, naranja, control_cinta, pendientes_sensor):
    while True:
        aplicar_control_cinta(sim, control_cinta)
        actualizar_llegadas_al_sensor(sim, control_cinta, pendientes_sensor)
        posicion = sim.getObjectPosition(naranja, sim.handle_world)
        paso = VELOCIDAD_BAJADA * sim.getSimulationTimeStep()

        nueva_x, alcanza_x = aproximar(posicion[0], control_cinta["x_inicio"], paso)
        nueva_y, alcanza_y = aproximar(posicion[1], Y_CAIDA_CINTA, paso)
        nueva_z, alcanza_z = aproximar(posicion[2], Z_CAIDA_CINTA, paso)

        sim.setObjectPosition(
            naranja,
            sim.handle_world,
            [nueva_x, nueva_y, nueva_z],
        )

        if alcanza_x and alcanza_y and alcanza_z:
            return

        time.sleep(sim.getSimulationTimeStep())


def liberar_naranja(sim, indice, naranja, control_cinta):
    sim.setObjectParent(naranja, sim.handle_world, True)
    sim.setObjectPosition(
        naranja,
        sim.handle_world,
        [
            control_cinta["x_inicio"],
            control_cinta["y_centro"],
            control_cinta["z_contacto"],
        ],
    )

    sim.setObjectInt32Param(naranja, sim.shapeintparam_respondable, 1)
    sim.setObjectInt32Param(naranja, sim.shapeintparam_static, 0)

    try:
        sim.resetDynamicObject(naranja)
    except Exception:
        pass

    print(f"Orange_{indice:02d} liberada sobre la cinta.")


def registrar_naranja_en_cinta(sim, control_cinta, indice, naranja):
    try:
        sim.setObjectInt32Param(naranja, sim.shapeintparam_static, 1)
        sim.setObjectInt32Param(naranja, sim.shapeintparam_respondable, 0)
        sim.resetDynamicObject(naranja)
    except Exception:
        pass

    control_cinta["objetos_transportados"][naranja] = {
        "indice": indice,
        "naranja": naranja,
        "tiempo_inicio": sim.getSimulationTime(),
        "x_inicio": control_cinta["x_inicio"],
    }


def iniciar_andadura_naranja(sim, control_cinta, indice, naranja):
    print(f"Moviendo Orange_{indice:02d} hasta la zona de caida.")
    mover_naranja_sobre_cinta(sim, naranja, control_cinta, {})
    liberar_naranja(sim, indice, naranja, control_cinta)
    registrar_naranja_en_cinta(sim, control_cinta, indice, naranja)


def preparar_naranja_en_sensor(sim, control_cinta, indice, naranja):
    iniciar_andadura_naranja(sim, control_cinta, indice, naranja)
    ejecutar_cinta_durante(sim, control_cinta, TIEMPO_TRAS_LIBERACION)
    esperar_naranja_en_sensor(sim, control_cinta, indice, naranja)


def esperar_sensor_final_libre(sim, control_cinta, naranja):
    while sensor_final_detecta_naranja(sim, control_cinta, naranja):
        time.sleep(sim.getSimulationTimeStep())


def alimentar_cinta_con_naranjas(sim, naranjas, control_cinta, control_robot):
    print(f"Esperando {RETARDO_INICIAL:.1f} s antes de soltar la primera naranja.")
    time.sleep(RETARDO_INICIAL)
    naranjas_ciclo = naranjas[:NARANJAS_A_RECOGER_EN_ESTA_FASE]

    if not naranjas_ciclo:
        return

    restaurar_robot_inicio_ciclo(sim, control_robot)
    abrir_pinza_totalmente(sim, control_robot)
    primer_indice, primera_naranja = naranjas_ciclo[0]
    preparar_naranja_en_sensor(sim, control_cinta, primer_indice, primera_naranja)

    for posicion, (indice, naranja) in enumerate(naranjas_ciclo):
        print(f"Iniciando recogida de Orange_{indice:02d}.")
        recoger_y_elevar_naranja_con_ur3(
            sim,
            control_robot,
            control_cinta,
            indice,
            naranja,
        )
        esperar_sensor_final_libre(sim, control_cinta, naranja)

        preparacion_siguiente = None

        if posicion + 1 < len(naranjas_ciclo):
            siguiente_indice, siguiente_naranja = naranjas_ciclo[posicion + 1]
            print(
                f"Sensor libre: Orange_{siguiente_indice:02d} inicia su andadura."
            )
            iniciar_andadura_naranja(
                sim,
                control_cinta,
                siguiente_indice,
                siguiente_naranja,
            )
            preparacion_siguiente = {
                "indice": siguiente_indice,
                "naranja": siguiente_naranja,
                "lista": False,
            }

        depositar_y_volver_a_recogida(
            sim,
            control_robot,
            control_cinta,
            indice,
            naranja,
            preparacion_siguiente,
        )

        if preparacion_siguiente is not None:
            while not preparacion_siguiente["lista"]:
                actualizar_naranja_en_preparacion(
                    sim,
                    control_cinta,
                    preparacion_siguiente,
                )
                time.sleep(sim.getSimulationTimeStep())

            abrir_pinza_totalmente(sim, control_robot)

    print("Todas las naranjas han completado su ciclo de alimentacion y retirada.")


def analizar_escena(sim):
    objetos = sim.getObjectsInTree(sim.handle_scene, sim.handle_all, 0)
    print(f"Objetos totales en la escena: {len(objetos)}.")

    for ruta in [
        "/HOP_007_NARANJAS",
        RUTA_CINTA,
        RUTA_SCRIPT_CINTA,
        "/ORANGES",
        RUTA_SCRIPT_NARANJAS,
        "/Sensor_final_cinta",
        "/UR3",
        "/UR3/RG2",
        RUTA_SCRIPT_RG2,
        RUTA_TARGET_UR3,
        RUTA_TIP_UR3,
        RUTA_SCRIPT_IK_UR3,
        RUTA_VISION_SENSOR,
        "/ZONA_CLASIFICACION",
        "/vision_sensor",
    ]:
        objeto = obtener_objeto_opcional(sim, ruta)

        if objeto is None:
            print(f"No localizado: {ruta}.")
            continue

        posicion = sim.getObjectPosition(objeto, sim.handle_world)
        print(
            f"Localizado {ruta}: "
            f"x={posicion[0]:.3f}, y={posicion[1]:.3f}, z={posicion[2]:.3f}."
        )


def main():
    control_bd = inicializar_postgresql()
    sim = conectar_coppeliasim()

    try:
        analizar_escena(sim)
        desactivar_script(sim, RUTA_SCRIPT_NARANJAS)
        desactivar_script(sim, RUTA_SCRIPT_CINTA)
        desactivar_script(sim, RUTA_SCRIPT_RG2)
        naranjas = buscar_naranjas(sim)
        control_cinta = crear_control_cinta(sim)
        control_vision = crear_control_vision(sim)
        control_vision["control_bd"] = control_bd
        control_cinta["control_vision"] = control_vision
        control_robot = crear_control_robot(sim)
        fijar_postura_inicial_ur3(sim, control_robot)
        preparar_naranjas(sim, naranjas)
        iniciar_simulacion_si_es_necesario(sim)
        abrir_pinza_totalmente(sim, control_robot)
        alimentar_cinta_con_naranjas(sim, naranjas, control_cinta, control_robot)
        print("Diametros medidos por naranja:")

        for indice in sorted(control_vision["diametros"]):
            medida = control_vision["diametros"][indice]
            diametro_cm = medida["cm"]
            tipo = medida["tipo"]
            texto = "sin medida" if diametro_cm is None else f"{diametro_cm:.2f} cm"
            texto = f"{texto} - {tipo}"
            print(f"  Orange_{indice:02d}: {texto}")

        guardar_diametros(control_vision)

        print(
            "Proceso completo. "
            f"Esperando {TIEMPO_ESPERA_FINAL_SIMULACION:.1f} s antes de parar."
        )
        time.sleep(TIEMPO_ESPERA_FINAL_SIMULACION)
    finally:
        cv2.destroyAllWindows()

        if sim.getSimulationState() != sim.simulation_stopped:
            sim.stopSimulation()
            print("Simulacion parada.")


if __name__ == "__main__":
    main()

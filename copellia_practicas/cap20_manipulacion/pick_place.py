from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math
import msvcrt
import time


RUTAS_UR3 = ["/UR3"]
RUTAS_RG2 = ["/UR3/RG2", "/UR3/connection/RG2", "/RG2"]
RUTAS_TARGET = ["/UR3/UR3_target", "/UR3_target"]
RUTAS_TIP = ["/UR3/UR3_tip", "/UR3_tip"]
RUTAS_PIEZA = ["/pieza"]
RUTAS_ZONA_PLACE = ["/zona_place", "/zona place"]
RUTAS_DEDO_IZQUIERDO = ["/UR3/RG2/leftTouch"]
RUTAS_DEDO_DERECHO = ["/UR3/RG2/rightTouch"]
RUTAS_SCRIPT_DEMO_UR3 = ["/UR3/Script"]
RUTAS_SCRIPT_IK_UR3 = ["/UR3/IK"]
RUTAS_SCRIPT_RG2 = ["/UR3/RG2/Script", "/UR3/connection/RG2/Script", "/RG2/Script"]

SIGNAL_RG2 = "RG2_open"
VELOCIDAD_APERTURA = 0.36
VELOCIDAD_CIERRE = -0.36
VELOCIDAD_CIERRE_AGARRE = -0.08
FUERZA_PINZA = 20
POSICION_PINZA_ABIERTA = 0.045
POSICION_PINZA_CERRADA = -0.035
POSICION_PINZA_AGARRE_MINIMA = 0.010
POSICION_PINZA_AGARRE_MAXIMA = 0.025
MARGEN_CIERRE_SOBRE_CARA = 0.005
ANTICIPACION_CIERRE_LENTO = 0.012
TIEMPO_MAXIMO_APERTURA_PINZA = 0.5
TIEMPO_MAXIMO_CIERRE_PINZA = 0.5
TIEMPO_MAXIMO_AGARRE_PINZA = 0.25

PASOS_MOVIMIENTO = 35
PAUSA_MOVIMIENTO = 0.003
TOLERANCIA_ROBOT = 0.01
TIEMPO_MAXIMO_ESPERA_ROBOT = 5.0
ITERACIONES_IK_POR_PASO = 8
ITERACIONES_CENTRADO_PINZA = 2

ALTURA_APROXIMACION_SOBRE_PIEZA = 0.026
ALTURA_SEGURA_SOBRE_PIEZA = 0.22
FRACCION_ALTURA_AGARRE = 0.88
ELEVACION_SEGURA = 0.18
ALTURA_TRASLADO_SOBRE_PLACE = 0.22
ALTURA_APROX_DEPOSITO_SOBRE_PLACE = 0.070
ALTURA_DEPOSITO_SOBRE_PLACE = 0.001
RETIRADA_VERTICAL_PINZA = 0.05
ORIENTACION_PINZA_VERTICAL = [math.pi, math.pi / 2, 0.0]

# Offset medido en la escena con la RG2 apuntando verticalmente hacia la mesa.
# centro_puntas = UR3_target + OFFSET_TARGET_A_CENTRO_PUNTAS
OFFSET_TARGET_A_CENTRO_PUNTAS = [0.003, -0.095, 0.030]


class ParadaSolicitada(Exception):
    pass


def conectar_coppeliasim():
    client = RemoteAPIClient()
    sim = client.require("sim")
    print("Conexion con CoppeliaSim establecida.")
    return sim


def iniciar_simulacion_si_es_necesario(sim):
    if sim.getSimulationState() == sim.simulation_stopped:
        print("Iniciando simulacion...")
        sim.startSimulation()
        time.sleep(0.35)
    else:
        print("La simulacion ya esta iniciada.")


def obtener_objeto(sim, rutas, descripcion):
    for ruta in rutas:
        try:
            objeto = sim.getObject(ruta)
            print(f"{descripcion} localizado en {ruta}.")
            return objeto
        except Exception:
            pass

    raise RuntimeError(
        f"No se ha podido localizar {descripcion}. "
        f"Rutas comprobadas: {', '.join(rutas)}"
    )


def obtener_objeto_opcional(sim, rutas, descripcion):
    for ruta in rutas:
        try:
            objeto = sim.getObject(ruta)
            print(f"{descripcion} localizado en {ruta}.")
            return objeto
        except Exception:
            pass

    print(f"Aviso: no se ha localizado {descripcion}.")
    return None


def obtener_script_rg2(sim, rg2):
    script = obtener_objeto_opcional(sim, RUTAS_SCRIPT_RG2, "script de la RG2")
    if script is not None:
        return script

    try:
        script = sim.getScript(sim.scripttype_childscript, rg2)
        if script == -1:
            raise RuntimeError("getScript no devolvio un script valido")
        print("Script de la RG2 localizado mediante getScript.")
        return script
    except Exception:
        print("Aviso: no se ha podido controlar directamente el script de la RG2.")
        return None


def desactivar_script_demo_ur3(sim):
    for ruta in RUTAS_SCRIPT_DEMO_UR3:
        try:
            script = sim.getObject(ruta)
            sim.setScriptInt32Param(script, sim.scriptintparam_enabled, 0)
            print(f"Script de demostracion desactivado: {ruta}")
            return
        except Exception:
            pass


def activar_script(sim, script, activo):
    if script is None:
        return

    sim.setScriptInt32Param(script, sim.scriptintparam_enabled, 1 if activo else 0)


def tecla_q_pulsada():
    if not msvcrt.kbhit():
        return False

    tecla = msvcrt.getch().decode("utf-8", errors="ignore").lower()
    return tecla == "q"


def comprobar_parada_usuario():
    if tecla_q_pulsada():
        raise ParadaSolicitada


def resolver_ik(sim, script_ik, iteraciones=ITERACIONES_IK_POR_PASO):
    for _ in range(iteraciones):
        sim.callScriptFunction("handleIk", script_ik)


def obtener_articulaciones_ur3(sim, ur3, rg2):
    articulaciones_rg2 = set(sim.getObjectsInTree(rg2, sim.object_joint_type, 0))

    return [
        articulacion
        for articulacion in sim.getObjectsInTree(ur3, sim.object_joint_type, 0)
        if articulacion not in articulaciones_rg2
    ]


def obtener_articulaciones_rg2(sim, rg2):
    return sim.getObjectsInTree(rg2, sim.object_joint_type, 0)


def obtener_articulacion_apertura_rg2(sim, articulaciones_rg2):
    for articulacion in articulaciones_rg2:
        if sim.getObjectAlias(articulacion, 1).endswith("/openCloseJoint"):
            return articulacion

    raise RuntimeError("No se ha localizado /openCloseJoint dentro de la RG2.")


def calcular_centro_puntas(sim, dedo_izquierdo, dedo_derecho):
    posicion_izquierda = sim.getObjectPosition(dedo_izquierdo, -1)
    posicion_derecha = sim.getObjectPosition(dedo_derecho, -1)

    return [
        (posicion_izquierda[indice] + posicion_derecha[indice]) / 2
        for indice in range(3)
    ]


def obtener_dimensiones_pieza(sim, pieza):
    minimo_x = sim.getObjectFloatParam(pieza, sim.objfloatparam_objbbox_min_x)
    maximo_x = sim.getObjectFloatParam(pieza, sim.objfloatparam_objbbox_max_x)
    minimo_y = sim.getObjectFloatParam(pieza, sim.objfloatparam_objbbox_min_y)
    maximo_y = sim.getObjectFloatParam(pieza, sim.objfloatparam_objbbox_max_y)
    minimo_z = sim.getObjectFloatParam(pieza, sim.objfloatparam_objbbox_min_z)
    maximo_z = sim.getObjectFloatParam(pieza, sim.objfloatparam_objbbox_max_z)

    return [
        maximo_x - minimo_x,
        maximo_y - minimo_y,
        maximo_z - minimo_z,
    ]


def obtener_vertices_bbox_mundo(sim, objeto):
    minimo_x = sim.getObjectFloatParam(objeto, sim.objfloatparam_objbbox_min_x)
    maximo_x = sim.getObjectFloatParam(objeto, sim.objfloatparam_objbbox_max_x)
    minimo_y = sim.getObjectFloatParam(objeto, sim.objfloatparam_objbbox_min_y)
    maximo_y = sim.getObjectFloatParam(objeto, sim.objfloatparam_objbbox_max_y)
    minimo_z = sim.getObjectFloatParam(objeto, sim.objfloatparam_objbbox_min_z)
    maximo_z = sim.getObjectFloatParam(objeto, sim.objfloatparam_objbbox_max_z)
    matriz = sim.getObjectMatrix(objeto, -1)
    posicion = sim.getObjectPosition(objeto, -1)

    eje_x = [matriz[0], matriz[4], matriz[8]]
    eje_y = [matriz[1], matriz[5], matriz[9]]
    eje_z = [matriz[2], matriz[6], matriz[10]]
    vertices = []

    for x in (minimo_x, maximo_x):
        for y in (minimo_y, maximo_y):
            for z in (minimo_z, maximo_z):
                vertices.append([
                    posicion[indice]
                    + eje_x[indice] * x
                    + eje_y[indice] * y
                    + eje_z[indice] * z
                    for indice in range(3)
                ])

    return vertices


def limites_bbox_mundo(sim, objeto):
    vertices = obtener_vertices_bbox_mundo(sim, objeto)
    return {
        "min": [min(vertice[indice] for vertice in vertices) for indice in range(3)],
        "max": [max(vertice[indice] for vertice in vertices) for indice in range(3)],
    }


def calcular_posicion_target_sobre_pieza(sim, pieza, altura_sobre_pieza):
    posicion = sim.getObjectPosition(pieza, -1)
    dimensiones = obtener_dimensiones_pieza(sim, pieza)
    cara_superior = posicion[2] + dimensiones[2] / 2
    centro_puntas = calcular_centro_puntas_sobre_pieza(sim, pieza, altura_sobre_pieza)
    posicion_target = [
        centro_puntas[indice] - OFFSET_TARGET_A_CENTRO_PUNTAS[indice]
        for indice in range(3)
    ]

    print("Pieza:", [round(valor, 3) for valor in posicion])
    print("Dimensiones pieza:", [round(valor, 3) for valor in dimensiones])
    print("Centro deseado de puntas:", [round(valor, 3) for valor in centro_puntas])
    print("Posicion target:", [round(valor, 3) for valor in posicion_target])

    return posicion_target


def calcular_centro_puntas_sobre_pieza(sim, pieza, altura_sobre_pieza):
    posicion = sim.getObjectPosition(pieza, -1)
    dimensiones = obtener_dimensiones_pieza(sim, pieza)
    cara_superior = posicion[2] + dimensiones[2] / 2

    return [
        posicion[0],
        posicion[1],
        cara_superior + altura_sobre_pieza,
    ]


def calcular_recogida(sim, pieza):
    posicion = sim.getObjectPosition(pieza, -1)
    limites_pieza = limites_bbox_mundo(sim, pieza)
    base_pieza = limites_pieza["min"][2]
    altura_pieza = limites_pieza["max"][2] - limites_pieza["min"][2]
    centro_puntas = [
        posicion[0],
        posicion[1],
        base_pieza + altura_pieza * FRACCION_ALTURA_AGARRE,
    ]
    posicion_target = [
        centro_puntas[indice] - OFFSET_TARGET_A_CENTRO_PUNTAS[indice]
        for indice in range(3)
    ]

    print("RECOGIDA:", [round(valor, 3) for valor in posicion_target])
    print("Centro deseado de puntas en recogida:", [round(valor, 3) for valor in centro_puntas])

    return posicion_target


def calcular_traslado_place(sim, target, pieza, zona_place):
    posicion_pieza = sim.getObjectPosition(pieza, -1)
    posicion_zona = sim.getObjectPosition(zona_place, -1)
    limites_pieza = limites_bbox_mundo(sim, pieza)
    limites_zona = limites_bbox_mundo(sim, zona_place)
    altura_pieza = limites_pieza["max"][2] - limites_pieza["min"][2]
    cara_superior_zona = limites_zona["max"][2]
    centro_pieza_deseado = [
        posicion_zona[0],
        posicion_zona[1],
        cara_superior_zona + altura_pieza / 2 + ALTURA_TRASLADO_SOBRE_PLACE,
    ]
    desplazamiento = [
        centro_pieza_deseado[indice] - posicion_pieza[indice]
        for indice in range(3)
    ]
    posicion_target = sim.getObjectPosition(target, -1)

    print("Centro zona place:", [round(valor, 3) for valor in posicion_zona])
    print("Centro deseado de pieza sobre place:", [round(valor, 3) for valor in centro_pieza_deseado])

    return [
        posicion_target[indice] + desplazamiento[indice]
        for indice in range(3)
    ]


def calcular_deposito_place(sim, target, pieza, zona_place):
    posicion_pieza = sim.getObjectPosition(pieza, -1)
    posicion_zona = sim.getObjectPosition(zona_place, -1)
    limites_pieza = limites_bbox_mundo(sim, pieza)
    limites_zona = limites_bbox_mundo(sim, zona_place)
    desplazamiento_z = (
        limites_zona["max"][2]
        + ALTURA_APROX_DEPOSITO_SOBRE_PLACE
        - limites_pieza["min"][2]
    )
    centro_pieza_deseado = [
        posicion_zona[0],
        posicion_zona[1],
        posicion_pieza[2] + desplazamiento_z,
    ]
    desplazamiento = [
        centro_pieza_deseado[indice] - posicion_pieza[indice]
        for indice in range(3)
    ]
    posicion_target = sim.getObjectPosition(target, -1)

    print("DEPOSITO:", [round(valor, 3) for valor in centro_pieza_deseado])

    return [
        posicion_target[indice] + desplazamiento[indice]
        for indice in range(3)
    ]


def calcular_aprox_origen(sim, pieza):
    return calcular_posicion_target_sobre_pieza(
        sim,
        pieza,
        ALTURA_APROXIMACION_SOBRE_PIEZA,
    )


def mostrar_estado_aproximacion(sim, pieza, dedo_izquierdo, dedo_derecho):
    posicion_pieza = sim.getObjectPosition(pieza, -1)
    dimensiones = obtener_dimensiones_pieza(sim, pieza)
    cara_superior = posicion_pieza[2] + dimensiones[2] / 2
    centro_puntas = calcular_centro_puntas(sim, dedo_izquierdo, dedo_derecho)

    print("Centro puntas:", [round(valor, 3) for valor in centro_puntas])
    print(f"Altura puntas sobre pieza: {centro_puntas[2] - cara_superior:.3f} m")


def distancia(posicion_a, posicion_b):
    return (
        (posicion_a[0] - posicion_b[0]) ** 2
        + (posicion_a[1] - posicion_b[1]) ** 2
        + (posicion_a[2] - posicion_b[2]) ** 2
    ) ** 0.5


def interpolar_posicion(posicion_inicial, posicion_final, progreso):
    return [
        posicion_inicial[0] + (posicion_final[0] - posicion_inicial[0]) * progreso,
        posicion_inicial[1] + (posicion_final[1] - posicion_inicial[1]) * progreso,
        posicion_inicial[2] + (posicion_final[2] - posicion_inicial[2]) * progreso,
    ]


def cota_minima_pieza_sobre_zona(sim, pieza, zona_place):
    posicion_pieza = sim.getObjectPosition(pieza, -1)
    limites_pieza = limites_bbox_mundo(sim, pieza)
    limites_zona = limites_bbox_mundo(sim, zona_place)
    desplazamiento_z = limites_zona["max"][2] + ALTURA_DEPOSITO_SOBRE_PLACE - limites_pieza["min"][2]
    return posicion_pieza[2] + desplazamiento_z


def abrir_pinza(sim, articulacion_apertura, script_rg2=None):
    activar_script(sim, script_rg2, True)
    sim.setIntProperty(sim.handle_scene, f"signal.{SIGNAL_RG2}", 1)
    sim.setJointForce(articulacion_apertura, FUERZA_PINZA)
    sim.setJointTargetVelocity(articulacion_apertura, VELOCIDAD_APERTURA)
    print("Abriendo pinza.")


def cerrar_pinza(sim, articulacion_apertura):
    sim.setIntProperty(sim.handle_scene, f"signal.{SIGNAL_RG2}", 0)
    sim.setJointForce(articulacion_apertura, FUERZA_PINZA)
    sim.setJointTargetVelocity(articulacion_apertura, VELOCIDAD_CIERRE)
    print("Pinza cerrada.")


def detener_pinza(sim, articulacion_apertura):
    sim.setJointTargetVelocity(articulacion_apertura, 0)


def esperar_pinza_abierta(sim, articulacion_apertura):
    tiempo_inicio = time.time()

    while time.time() - tiempo_inicio < TIEMPO_MAXIMO_APERTURA_PINZA:
        comprobar_parada_usuario()

        if sim.getJointPosition(articulacion_apertura) >= POSICION_PINZA_ABIERTA:
            print("Pinza abierta.")
            return True

        time.sleep(0.006)

    print("Aviso: la pinza no ha alcanzado la apertura esperada.")
    return False


def esperar_pinza_cerrada(sim, articulacion_apertura):
    tiempo_inicio = time.time()

    while time.time() - tiempo_inicio < TIEMPO_MAXIMO_CIERRE_PINZA:
        comprobar_parada_usuario()

        if sim.getJointPosition(articulacion_apertura) <= POSICION_PINZA_CERRADA:
            print("Pinza cerrada.")
            return True

        time.sleep(0.006)

    print("Aviso: la pinza no ha alcanzado el cierre esperado.")
    return False


def calcular_posicion_pinza_agarre(sim, pieza):
    dimensiones = obtener_dimensiones_pieza(sim, pieza)
    ancho_pieza = min(dimensiones[0], dimensiones[1])
    posicion_objetivo = ancho_pieza / 2 - MARGEN_CIERRE_SOBRE_CARA

    return max(
        POSICION_PINZA_AGARRE_MINIMA,
        min(POSICION_PINZA_AGARRE_MAXIMA, posicion_objetivo),
    )


def cerrar_pinza_hasta_agarre(
    sim,
    articulacion_apertura,
    script_rg2,
    pieza,
    dedo_izquierdo,
    dedo_derecho,
):
    posicion_objetivo = calcular_posicion_pinza_agarre(sim, pieza)
    cierre_lento_activado = False
    activar_script(sim, script_rg2, True)
    sim.setIntProperty(sim.handle_scene, f"signal.{SIGNAL_RG2}", 0)
    sim.setJointForce(articulacion_apertura, FUERZA_PINZA)
    sim.setJointTargetVelocity(articulacion_apertura, VELOCIDAD_CIERRE)

    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < TIEMPO_MAXIMO_AGARRE_PINZA:
        comprobar_parada_usuario()
        posicion_actual = sim.getJointPosition(articulacion_apertura)

        if (
            not cierre_lento_activado
            and posicion_actual <= posicion_objetivo + ANTICIPACION_CIERRE_LENTO
        ):
            sim.setJointTargetVelocity(articulacion_apertura, VELOCIDAD_CIERRE_AGARRE)
            cierre_lento_activado = True

        if posicion_actual <= posicion_objetivo:
            detener_pinza(sim, articulacion_apertura)
            activar_script(sim, script_rg2, False)
            print(
                "Pinza cerrada hasta agarre visible. "
                f"Apertura RG2: {posicion_actual:.4f} m"
            )
            return True

        time.sleep(0.002)

    detener_pinza(sim, articulacion_apertura)
    activar_script(sim, script_rg2, False)
    print("Aviso: se ha detenido el cierre por tiempo para evitar atravesar la pieza.")
    return False


def mover_target(
    sim,
    target,
    posicion_final,
    script_ik,
    orientacion_final=None,
    pasos=PASOS_MOVIMIENTO,
    pausa=PAUSA_MOVIMIENTO,
):
    posicion_inicial = sim.getObjectPosition(target, -1)

    if orientacion_final is None:
        orientacion_final = sim.getObjectOrientation(target, -1)

    for paso in range(1, pasos + 1):
        comprobar_parada_usuario()
        progreso = paso / pasos
        nueva_posicion = interpolar_posicion(
            posicion_inicial,
            posicion_final,
            progreso,
        )

        sim.setObjectPosition(target, -1, nueva_posicion)
        sim.setObjectOrientation(target, -1, orientacion_final)
        resolver_ik(sim, script_ik)

        time.sleep(pausa)

    sim.setObjectOrientation(target, -1, orientacion_final)
    resolver_ik(sim, script_ik, 12)


def centrar_puntas_en_punto(
    sim,
    target,
    tip,
    script_ik,
    dedo_izquierdo,
    dedo_derecho,
    centro_deseado,
):
    for _ in range(ITERACIONES_CENTRADO_PINZA):
        centro_actual = calcular_centro_puntas(sim, dedo_izquierdo, dedo_derecho)
        correccion = [
            centro_deseado[indice] - centro_actual[indice]
            for indice in range(3)
        ]

        if distancia(centro_actual, centro_deseado) < 0.003:
            break

        posicion_target = sim.getObjectPosition(target, -1)
        posicion_corregida = [
            posicion_target[indice] + correccion[indice]
            for indice in range(3)
        ]
        mover_target(
            sim,
            target,
            posicion_corregida,
            script_ik,
            ORIENTACION_PINZA_VERTICAL,
            pasos=8,
            pausa=0.003,
        )
        esperar_robot(sim, tip, target)

    centro_actual = calcular_centro_puntas(sim, dedo_izquierdo, dedo_derecho)
    error = distancia(centro_actual, centro_deseado)
    print(f"Error centro puntas-pieza: {error:.4f} m")


def orientar_pinza_vertical(sim, target, tip, script_ik, rg2):
    sim.setObjectOrientation(target, -1, ORIENTACION_PINZA_VERTICAL)
    resolver_ik(sim, script_ik, 8)
    return True


def esperar_robot(sim, tip, target):
    tiempo_inicio = time.time()

    while time.time() - tiempo_inicio < TIEMPO_MAXIMO_ESPERA_ROBOT:
        comprobar_parada_usuario()
        posicion_tip = sim.getObjectPosition(tip, -1)
        posicion_target = sim.getObjectPosition(target, -1)

        if distancia(posicion_tip, posicion_target) <= TOLERANCIA_ROBOT:
            return True

        time.sleep(0.006)

    return False


def guardar_posicion_inicial_ur3(sim, tip):
    return {
        "pose": sim.getObjectPose(tip, -1),
        "posicion": sim.getObjectPosition(tip, -1),
        "orientacion": sim.getObjectOrientation(tip, -1),
    }


def volver_a_posicion_inicial(sim, target, tip, script_ik, posicion_inicial_ur3):
    print("Volviendo a la posicion inicial antes de parar...")
    sim.setObjectOrientation(target, -1, posicion_inicial_ur3["orientacion"])
    mover_target(sim, target, posicion_inicial_ur3["posicion"], script_ik)
    sim.setObjectPose(target, -1, posicion_inicial_ur3["pose"])
    resolver_ik(sim, script_ik, 8)
    esperar_robot(sim, tip, target)


def parar_simulacion(sim):
    if sim.getSimulationState() != sim.simulation_stopped:
        sim.stopSimulation()
        time.sleep(0.35)


def aproximar_a_pieza(
    sim,
    rg2,
    target,
    tip,
    script_ik,
    articulacion_apertura,
    script_rg2,
    pieza,
    dedo_izquierdo,
    dedo_derecho,
):
    time.sleep(0.02)
    aprox_origen = calcular_aprox_origen(sim, pieza)
    posicion_segura = calcular_posicion_target_sobre_pieza(
        sim,
        pieza,
        ALTURA_SEGURA_SOBRE_PIEZA,
    )

    abrir_pinza(sim, articulacion_apertura, script_rg2)
    esperar_pinza_abierta(sim, articulacion_apertura)

    sim.setObjectPose(target, -1, sim.getObjectPose(tip, -1))
    resolver_ik(sim, script_ik, 8)

    mover_target(
        sim,
        target,
        posicion_segura,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)

    aprox_origen = calcular_aprox_origen(sim, pieza)
    mover_target(
        sim,
        target,
        aprox_origen,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)
    orientar_pinza_vertical(sim, target, tip, script_ik, rg2)
    centrar_puntas_en_punto(
        sim,
        target,
        tip,
        script_ik,
        dedo_izquierdo,
        dedo_derecho,
        calcular_centro_puntas_sobre_pieza(
            sim,
            pieza,
            ALTURA_APROXIMACION_SOBRE_PIEZA,
        ),
    )

    abrir_pinza(sim, articulacion_apertura, script_rg2)
    esperar_pinza_abierta(sim, articulacion_apertura)
    mostrar_estado_aproximacion(sim, pieza, dedo_izquierdo, dedo_derecho)
    print("Robot situado en aproximacion de pick con la pinza abierta.")


def bajar_a_recogida(
    sim,
    rg2,
    target,
    tip,
    script_ik,
    pieza,
    dedo_izquierdo,
    dedo_derecho,
):
    recogida = calcular_recogida(sim, pieza)

    mover_target(
        sim,
        target,
        recogida,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)
    orientar_pinza_vertical(sim, target, tip, script_ik, rg2)
    posicion = sim.getObjectPosition(pieza, -1)
    limites_pieza = limites_bbox_mundo(sim, pieza)
    altura_pieza = limites_pieza["max"][2] - limites_pieza["min"][2]
    centro_recogida = [
        posicion[0],
        posicion[1],
        limites_pieza["min"][2] + altura_pieza * FRACCION_ALTURA_AGARRE,
    ]
    centrar_puntas_en_punto(
        sim,
        target,
        tip,
        script_ik,
        dedo_izquierdo,
        dedo_derecho,
        centro_recogida,
    )
    mostrar_estado_aproximacion(sim, pieza, dedo_izquierdo, dedo_derecho)
    print("Robot situado en punto de recogida.")


def fijar_pieza_a_pinza(sim, pieza):
    punto_agarre = obtener_objeto(
        sim,
        ["/UR3/RG2/attachPoint", "/UR3/connection/RG2/attachPoint"],
        "punto de agarre",
    )
    sim.setObjectInt32Param(pieza, sim.shapeintparam_static, 1)
    sim.setObjectInt32Param(pieza, sim.shapeintparam_respondable, 0)
    sim.setObjectParent(pieza, punto_agarre, True)
    print("Pieza fijada temporalmente a la pinza.")


def cerrar_y_elevar_pieza(
    sim,
    rg2,
    target,
    tip,
    script_ik,
    articulacion_apertura,
    script_rg2,
    pieza,
    dedo_izquierdo,
    dedo_derecho,
):
    cerrar_pinza_hasta_agarre(
        sim,
        articulacion_apertura,
        script_rg2,
        pieza,
        dedo_izquierdo,
        dedo_derecho,
    )
    fijar_pieza_a_pinza(sim, pieza)
    orientar_pinza_vertical(sim, target, tip, script_ik, rg2)

    posicion_actual = sim.getObjectPosition(target, -1)
    posicion_segura = [
        posicion_actual[0],
        posicion_actual[1],
        posicion_actual[2] + ELEVACION_SEGURA,
    ]

    mover_target(
        sim,
        target,
        posicion_segura,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)
    print("Pieza elevada a punto seguro.")


def trasladar_pieza_a_place(sim, rg2, target, tip, script_ik, pieza, zona_place):
    posicion_place = calcular_traslado_place(sim, target, pieza, zona_place)

    mover_target(
        sim,
        target,
        posicion_place,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)
    orientar_pinza_vertical(sim, target, tip, script_ik, rg2)
    print("Pieza situada verticalmente sobre el centro de zona place.")


def soltar_pieza_en_place(sim, pieza, zona_place):
    sim.setObjectParent(pieza, -1, True)
    sim.setObjectInt32Param(pieza, sim.shapeintparam_static, 1)
    sim.setObjectInt32Param(pieza, sim.shapeintparam_respondable, 0)
    print("Pieza depositada en zona_place.")


def depositar_y_retirar_pinza(
    sim,
    rg2,
    target,
    tip,
    script_ik,
    articulacion_apertura,
    script_rg2,
    pieza,
    zona_place,
    posicion_inicial_ur3,
):
    orientar_pinza_vertical(sim, target, tip, script_ik, rg2)
    deposito = calcular_deposito_place(sim, target, pieza, zona_place)

    mover_target(
        sim,
        target,
        deposito,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)
    orientar_pinza_vertical(sim, target, tip, script_ik, rg2)
    soltar_pieza_en_place(sim, pieza, zona_place)

    abrir_pinza(sim, articulacion_apertura, script_rg2)
    esperar_pinza_abierta(sim, articulacion_apertura)

    posicion_actual = sim.getObjectPosition(target, -1)
    posicion_retirada = [
        posicion_actual[0],
        posicion_actual[1],
        posicion_actual[2] + RETIRADA_VERTICAL_PINZA,
    ]
    mover_target(
        sim,
        target,
        posicion_retirada,
        script_ik,
        ORIENTACION_PINZA_VERTICAL,
    )
    esperar_robot(sim, tip, target)
    volver_a_posicion_inicial(sim, target, tip, script_ik, posicion_inicial_ur3)
    print("Ciclo pick and place finalizado.")


def pick_and_place():
    sim = conectar_coppeliasim()
    desactivar_script_demo_ur3(sim)
    iniciar_simulacion_si_es_necesario(sim)

    ur3 = obtener_objeto(sim, RUTAS_UR3, "UR3")
    rg2 = obtener_objeto(sim, RUTAS_RG2, "pinza RG2")
    target = obtener_objeto(sim, RUTAS_TARGET, "UR3_target")
    tip = obtener_objeto(sim, RUTAS_TIP, "UR3_tip")
    pieza = obtener_objeto(sim, RUTAS_PIEZA, "pieza")
    zona_place = obtener_objeto(sim, RUTAS_ZONA_PLACE, "zona place")
    dedo_izquierdo = obtener_objeto(sim, RUTAS_DEDO_IZQUIERDO, "dedo izquierdo")
    dedo_derecho = obtener_objeto(sim, RUTAS_DEDO_DERECHO, "dedo derecho")
    script_ik = obtener_objeto(sim, RUTAS_SCRIPT_IK_UR3, "script IK del UR3")
    script_rg2 = obtener_script_rg2(sim, rg2)

    articulaciones_rg2 = obtener_articulaciones_rg2(sim, rg2)
    articulacion_apertura = obtener_articulacion_apertura_rg2(sim, articulaciones_rg2)
    posicion_inicial_ur3 = guardar_posicion_inicial_ur3(sim, tip)

    try:
        aproximar_a_pieza(
            sim,
            rg2,
            target,
            tip,
            script_ik,
            articulacion_apertura,
            script_rg2,
            pieza,
            dedo_izquierdo,
            dedo_derecho,
        )
        bajar_a_recogida(
            sim,
            rg2,
            target,
            tip,
            script_ik,
            pieza,
            dedo_izquierdo,
            dedo_derecho,
        )
        cerrar_y_elevar_pieza(
            sim,
            rg2,
            target,
            tip,
            script_ik,
            articulacion_apertura,
            script_rg2,
            pieza,
            dedo_izquierdo,
            dedo_derecho,
        )
        trasladar_pieza_a_place(
            sim,
            rg2,
            target,
            tip,
            script_ik,
            pieza,
            zona_place,
        )
        depositar_y_retirar_pinza(
            sim,
            rg2,
            target,
            tip,
            script_ik,
            articulacion_apertura,
            script_rg2,
            pieza,
            zona_place,
            posicion_inicial_ur3,
        )
        print("Pulsa q para parar la simulacion.")

        while True:
            comprobar_parada_usuario()
            time.sleep(0.006)
    except ParadaSolicitada:
        detener_pinza(sim, articulacion_apertura)
        parar_simulacion(sim)


if __name__ == "__main__":
    pick_and_place()

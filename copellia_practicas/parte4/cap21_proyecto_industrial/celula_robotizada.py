from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math
import time


RUTAS_UR3 = ["/UR3"]
RUTAS_RG2 = ["/UR3/RG2", "/UR3/connection/RG2", "/RG2"]
RUTAS_CINTA = ["/cinta_transportadora"]
RUTAS_SCRIPT_CINTA = ["/cinta_transportadora/Script"]
RUTAS_SENSOR_FINAL_CINTA = ["/sensor_final_cinta"]
RUTAS_PIEZA = ["/pieza", "/pieza[0]"]
RUTAS_TARGET = ["/UR3/UR3_target", "/UR3_target"]
RUTAS_TIP = ["/UR3/UR3_tip", "/UR3_tip"]
RUTAS_BASE_UR3 = ["/UR3/joint", "/UR3/UR3_joint1", "/UR3/joint1"]
RUTAS_SCRIPT_IK_UR3 = ["/UR3/IK"]
RUTAS_SCRIPT_RG2 = ["/UR3/RG2/Script", "/UR3/connection/RG2/Script", "/RG2/Script"]
RUTAS_ATTACH_POINT_RG2 = ["/UR3/RG2/attachPoint", "/UR3/connection/RG2/attachPoint"]
RUTAS_DEDO_IZQUIERDO = ["/UR3/RG2/leftTouch"]
RUTAS_DEDO_DERECHO = ["/UR3/RG2/rightTouch"]

VELOCIDAD_CINTA = 0.03
VELOCIDAD_APERTURA_PINZA = 0.025
VELOCIDAD_CIERRE_PINZA = -0.025
VELOCIDAD_MANTENER_AGARRE = -0.003
FUERZA_PINZA = 20
FUERZA_AGARRE_PINZA = 35
SEPARACION_DEDOS_PINZA_ABIERTA = 0.105
SEPARACION_DEDOS_PINZA_AGARRE = 0.0340
SEPARACION_DEDOS_PINZA_SUELTA = 0.045
TOLERANCIA_SEPARACION_PINZA = 0.0005
TIEMPO_MAXIMO_AJUSTE_PINZA = 5.0
TIEMPO_ENTRE_LECTURAS_SENSOR = 0.002
TIEMPO_ORDEN_PARADA_CINTA = 0.25
TIEMPO_ESPERA_FINAL = 5.0
NUMERO_PIEZAS_CICLO = 4
Z_TARGET_BAJADA_PINZA = 0.62
Z_TARGET_SUBIDA_PINZA = 0.80023
Z_TARGET_BAJADA_ZONA_PLACE = 0.62
GIRO_BASE_HACIA_ZONA_PLACE = math.pi
GIRO_BASE_HACIA_CINTA = -math.pi
SEPARACION_X_ENTRE_PIEZAS_PLACE = 0.06
PASOS_GIRO_BASE = 60
PAUSA_GIRO_BASE = 0.01
PASOS_MOVIMIENTO_SUAVE_PLACE = 80
PAUSA_MOVIMIENTO_SUAVE_PLACE = 0.01
ITERACIONES_IK_TRAS_MOVIMIENTO = 20

def conectar_coppeliasim():
    client = RemoteAPIClient()
    sim = client.require("sim")
    print("Conexion con CoppeliaSim establecida.")
    return sim


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


def activar_script(sim, script, activo):
    valor = 1 if activo else 0

    try:
        sim.setScriptAttribute(script, sim.scriptattribute_enabled, valor)
    except Exception:
        pass

    try:
        sim.setScriptInt32Param(script, sim.scriptintparam_enabled, valor)
    except Exception:
        pass


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
            print("Articulacion de apertura RG2 localizada.")
            return articulacion

    raise RuntimeError("No se ha localizado /openCloseJoint dentro de la RG2.")


def listar_aliases(sim, objetos):
    return [sim.getObjectAlias(objeto, 1) for objeto in objetos]


def fijar_velocidad_cinta(sim, cinta, velocidad):
    sim.setBufferProperty(
        cinta,
        "customData.__ctrl__",
        sim.packTable({"vel": velocidad}),
    )


def iniciar_cinta(sim, cinta, script_cinta):
    activar_script(sim, script_cinta, True)
    fijar_velocidad_cinta(sim, cinta, VELOCIDAD_CINTA)
    print(f"Cinta transportadora en marcha a {VELOCIDAD_CINTA:.3f} m/s.")


def parar_cinta(sim, cinta):
    inicio = time.time()

    while time.time() - inicio < TIEMPO_ORDEN_PARADA_CINTA:
        fijar_velocidad_cinta(sim, cinta, 0.0)
        time.sleep(0.005)

    print("Cinta transportadora parada.")


def iniciar_simulacion_si_es_necesario(sim):
    if sim.getSimulationState() == sim.simulation_stopped:
        print("Iniciando simulacion...")
        sim.startSimulation()
        time.sleep(0.2)
    else:
        print("La simulacion ya estaba iniciada.")


def parar_simulacion_tras_espera(sim, tiempo_espera):
    print(f"Esperando {tiempo_espera:.1f} s antes de parar la simulacion.")
    time.sleep(tiempo_espera)
    sim.stopSimulation()
    print("Simulacion parada.")


def leer_sensor_proximidad(sim, sensor):
    lectura = sim.readProximitySensor(sensor)
    detectado = bool(lectura[0])
    distancia = lectura[1] if detectado and len(lectura) > 1 else None
    objeto_detectado = lectura[3] if detectado and len(lectura) > 3 else -1

    if not detectado or objeto_detectado == -1:
        return None, None

    return objeto_detectado, distancia


def esperar_pieza_y_parar_cinta(sim, cinta, sensor_final_cinta):
    print("Esperando deteccion en sensor_final_cinta...")

    while True:
        objeto_detectado, distancia = leer_sensor_proximidad(
            sim,
            sensor_final_cinta,
        )

        if objeto_detectado is not None:
            alias = sim.getObjectAlias(objeto_detectado, 1)
            print(
                f"Sensor activado por {alias}. "
                f"Distancia: {distancia:.4f} m."
            )
            parar_cinta(sim, cinta)
            return objeto_detectado

        time.sleep(TIEMPO_ENTRE_LECTURAS_SENSOR)


def resolver_ik(sim, script_ik, iteraciones=ITERACIONES_IK_TRAS_MOVIMIENTO):
    for _ in range(iteraciones):
        sim.callScriptFunction("handleIk", script_ik)


def detener_pinza(sim, articulacion_apertura):
    sim.setJointTargetVelocity(articulacion_apertura, 0.0)


def calcular_distancia(posicion_a, posicion_b):
    return (
        (posicion_a[0] - posicion_b[0]) ** 2
        + (posicion_a[1] - posicion_b[1]) ** 2
        + (posicion_a[2] - posicion_b[2]) ** 2
    ) ** 0.5


def medir_separacion_dedos(sim, dedo_izquierdo, dedo_derecho):
    posicion_izquierda = sim.getObjectPosition(dedo_izquierdo, -1)
    posicion_derecha = sim.getObjectPosition(dedo_derecho, -1)
    return calcular_distancia(posicion_izquierda, posicion_derecha)


def fijar_separacion_pinza(
    sim,
    articulacion_apertura,
    dedo_izquierdo,
    dedo_derecho,
    separacion_objetivo,
    script_rg2=None,
    mantener_presion=False,
):
    separacion_actual = medir_separacion_dedos(sim, dedo_izquierdo, dedo_derecho)
    diferencia = separacion_objetivo - separacion_actual

    activar_script(sim, script_rg2, False)

    if abs(diferencia) <= TOLERANCIA_SEPARACION_PINZA:
        if mantener_presion:
            sim.setJointForce(articulacion_apertura, FUERZA_AGARRE_PINZA)
            sim.setJointTargetVelocity(articulacion_apertura, VELOCIDAD_MANTENER_AGARRE)
        else:
            detener_pinza(sim, articulacion_apertura)
        print(f"Pinza ya situada a {separacion_actual:.4f} m entre dedos.")
        return

    velocidad = VELOCIDAD_APERTURA_PINZA if diferencia > 0 else VELOCIDAD_CIERRE_PINZA
    fuerza = FUERZA_AGARRE_PINZA if mantener_presion else FUERZA_PINZA
    sim.setJointForce(articulacion_apertura, fuerza)
    sim.setJointTargetVelocity(articulacion_apertura, velocidad)
    print(f"Ajustando separacion real de dedos hasta {separacion_objetivo:.3f} m.")

    inicio = time.time()
    while time.time() - inicio < TIEMPO_MAXIMO_AJUSTE_PINZA:
        separacion_actual = medir_separacion_dedos(sim, dedo_izquierdo, dedo_derecho)
        diferencia = separacion_objetivo - separacion_actual

        if abs(diferencia) <= TOLERANCIA_SEPARACION_PINZA:
            if mantener_presion:
                sim.setJointForce(articulacion_apertura, FUERZA_AGARRE_PINZA)
                sim.setJointTargetVelocity(articulacion_apertura, VELOCIDAD_MANTENER_AGARRE)
            else:
                detener_pinza(sim, articulacion_apertura)
            print(f"Separacion de dedos fijada en {separacion_actual:.4f} m.")
            return

        nueva_velocidad = VELOCIDAD_APERTURA_PINZA if diferencia > 0 else VELOCIDAD_CIERRE_PINZA
        if nueva_velocidad != velocidad:
            velocidad = nueva_velocidad
            sim.setJointTargetVelocity(articulacion_apertura, velocidad)

        time.sleep(0.002)

    detener_pinza(sim, articulacion_apertura)
    separacion_actual = medir_separacion_dedos(sim, dedo_izquierdo, dedo_derecho)
    raise RuntimeError(
        "La pinza no ha alcanzado la separacion objetivo. "
        f"Separacion actual entre dedos: {separacion_actual:.4f} m."
    )


def bajar_target_cambiando_solo_z(sim, target, script_ik, nueva_z):
    posicion = sim.getObjectPosition(target, -1)
    posicion_bajada = [posicion[0], posicion[1], nueva_z]

    sim.setObjectPosition(target, -1, posicion_bajada)
    resolver_ik(sim, script_ik)
    print(
        "UR3_target bajado cambiando solo z: "
        f"{posicion[2]:.3f} -> {nueva_z:.3f} m."
    )
    print("Nueva posicion UR3_target:", sim.getObjectPosition(target, -1))


def mover_target_z_suave(sim, target, script_ik, nueva_z):
    posicion_inicial = sim.getObjectPosition(target, -1)
    z_inicial = posicion_inicial[2]

    print(
        "Moviendo UR3_target suavemente solo en z: "
        f"{z_inicial:.3f} -> {nueva_z:.3f} m."
    )

    for paso in range(1, PASOS_MOVIMIENTO_SUAVE_PLACE + 1):
        progreso = paso / PASOS_MOVIMIENTO_SUAVE_PLACE
        z = z_inicial + (nueva_z - z_inicial) * progreso
        sim.setObjectPosition(
            target,
            -1,
            [posicion_inicial[0], posicion_inicial[1], z],
        )
        resolver_ik(sim, script_ik, 2)
        time.sleep(PAUSA_MOVIMIENTO_SUAVE_PLACE)

    resolver_ik(sim, script_ik)
    print("Nueva posicion UR3_target:", sim.getObjectPosition(target, -1))


def desplazar_target_cambiando_solo_x(sim, target, script_ik, desplazamiento_x):
    if desplazamiento_x == 0:
        return

    posicion = sim.getObjectPosition(target, -1)
    posicion_desplazada = [
        posicion[0] + desplazamiento_x,
        posicion[1],
        posicion[2],
    ]

    sim.setObjectPosition(target, -1, posicion_desplazada)
    resolver_ik(sim, script_ik)
    print(
        "UR3_target desplazado en x para separar piezas: "
        f"{desplazamiento_x:.3f} m."
    )
    print("Nueva posicion UR3_target:", sim.getObjectPosition(target, -1))


def colocar_target_en_posicion(sim, target, script_ik, posicion_objetivo):
    sim.setObjectPosition(target, -1, posicion_objetivo)
    resolver_ik(sim, script_ik)
    print("UR3_target restaurado:", sim.getObjectPosition(target, -1))


def rotar_posicion_sobre_eje_z(posicion, centro, angulo):
    desplazamiento_x = posicion[0] - centro[0]
    desplazamiento_y = posicion[1] - centro[1]
    coseno = math.cos(angulo)
    seno = math.sin(angulo)

    return [
        centro[0] + desplazamiento_x * coseno - desplazamiento_y * seno,
        centro[1] + desplazamiento_x * seno + desplazamiento_y * coseno,
        posicion[2],
    ]


def girar_base_ur3(sim, articulacion_base, target, script_ik, giro):
    posicion_inicial = sim.getJointPosition(articulacion_base)
    posicion_final = posicion_inicial + giro
    posicion_base = sim.getObjectPosition(articulacion_base, -1)
    posicion_inicial_target = sim.getObjectPosition(target, -1)
    alias = sim.getObjectAlias(articulacion_base, 1)

    print(
        f"Girando base del UR3 ({alias}): "
        f"{math.degrees(posicion_inicial):.1f} -> "
        f"{math.degrees(posicion_final):.1f} grados."
    )

    for paso in range(1, PASOS_GIRO_BASE + 1):
        progreso = paso / PASOS_GIRO_BASE
        posicion = posicion_inicial + (posicion_final - posicion_inicial) * progreso
        giro_actual = giro * progreso
        posicion_target = rotar_posicion_sobre_eje_z(
            posicion_inicial_target,
            posicion_base,
            giro_actual,
        )

        sim.setJointPosition(articulacion_base, posicion)
        sim.setJointTargetPosition(articulacion_base, posicion)
        sim.setObjectPosition(target, -1, posicion_target)
        resolver_ik(sim, script_ik, 2)
        time.sleep(PAUSA_GIRO_BASE)

    sim.setJointPosition(articulacion_base, posicion_final)
    sim.setJointTargetPosition(articulacion_base, posicion_final)
    sim.setObjectPosition(
        target,
        -1,
        rotar_posicion_sobre_eje_z(posicion_inicial_target, posicion_base, giro),
    )
    resolver_ik(sim, script_ik)
    print("Nueva posicion UR3_target:", sim.getObjectPosition(target, -1))
    print("Base del UR3 girada 180 grados.")


def main():
    sim = conectar_coppeliasim()

    ur3 = obtener_objeto(sim, RUTAS_UR3, "UR3")
    rg2 = obtener_objeto(sim, RUTAS_RG2, "pinza RG2")
    cinta = obtener_objeto(sim, RUTAS_CINTA, "cinta transportadora")
    script_cinta = obtener_objeto(sim, RUTAS_SCRIPT_CINTA, "script de la cinta")
    sensor_final_cinta = obtener_objeto(
        sim,
        RUTAS_SENSOR_FINAL_CINTA,
        "sensor final de cinta",
    )
    pieza = obtener_objeto(sim, RUTAS_PIEZA, "pieza")
    target = obtener_objeto(sim, RUTAS_TARGET, "UR3_target")
    tip = obtener_objeto(sim, RUTAS_TIP, "UR3_tip")
    articulacion_base_ur3 = obtener_objeto(sim, RUTAS_BASE_UR3, "articulacion de base UR3")
    script_ik = obtener_objeto(sim, RUTAS_SCRIPT_IK_UR3, "script IK del UR3")
    script_rg2 = obtener_objeto(sim, RUTAS_SCRIPT_RG2, "script de la RG2")
    attach_point = obtener_objeto(sim, RUTAS_ATTACH_POINT_RG2, "attachPoint RG2")
    dedo_izquierdo = obtener_objeto(sim, RUTAS_DEDO_IZQUIERDO, "dedo izquierdo RG2")
    dedo_derecho = obtener_objeto(sim, RUTAS_DEDO_DERECHO, "dedo derecho RG2")

    articulaciones_ur3 = obtener_articulaciones_ur3(sim, ur3, rg2)
    articulaciones_rg2 = obtener_articulaciones_rg2(sim, rg2)
    articulacion_apertura = obtener_articulacion_apertura_rg2(sim, articulaciones_rg2)
    partes_rg2 = [
        rg2,
        script_rg2,
        attach_point,
        dedo_izquierdo,
        dedo_derecho,
        *articulaciones_rg2,
    ]

    print("Articulaciones UR3:", listar_aliases(sim, articulaciones_ur3))
    print("Articulaciones RG2:", listar_aliases(sim, articulaciones_rg2))
    print("Partes RG2:", listar_aliases(sim, partes_rg2))
    print("UR3_target:", sim.getObjectPosition(target, -1))
    print("UR3_tip:", sim.getObjectPosition(tip, -1))
    print("Pieza inicial:", sim.getObjectPosition(pieza, -1))

    iniciar_simulacion_si_es_necesario(sim)
    posicion_target_ataque_cinta = list(sim.getObjectPosition(target, -1))

    for numero_pieza in range(1, NUMERO_PIEZAS_CICLO + 1):
        print(f"Iniciando ciclo de manipulacion de pieza {numero_pieza}.")
        colocar_target_en_posicion(
            sim,
            target,
            script_ik,
            posicion_target_ataque_cinta,
        )
        iniciar_cinta(sim, cinta, script_cinta)
        pieza_detectada = esperar_pieza_y_parar_cinta(
            sim,
            cinta,
            sensor_final_cinta,
        )

        print(
            "Pieza lista para el siguiente paso:",
            sim.getObjectAlias(pieza_detectada, 1),
            sim.getObjectPosition(pieza_detectada, -1),
        )

        fijar_separacion_pinza(
            sim,
            articulacion_apertura,
            dedo_izquierdo,
            dedo_derecho,
            SEPARACION_DEDOS_PINZA_ABIERTA,
            script_rg2,
        )
        bajar_target_cambiando_solo_z(
            sim,
            target,
            script_ik,
            Z_TARGET_BAJADA_PINZA,
        )
        fijar_separacion_pinza(
            sim,
            articulacion_apertura,
            dedo_izquierdo,
            dedo_derecho,
            SEPARACION_DEDOS_PINZA_AGARRE,
            script_rg2,
            mantener_presion=True,
        )
        bajar_target_cambiando_solo_z(
            sim,
            target,
            script_ik,
            Z_TARGET_SUBIDA_PINZA,
        )
        girar_base_ur3(
            sim,
            articulacion_base_ur3,
            target,
            script_ik,
            GIRO_BASE_HACIA_ZONA_PLACE,
        )
        desplazar_target_cambiando_solo_x(
            sim,
            target,
            script_ik,
            (numero_pieza - 1) * SEPARACION_X_ENTRE_PIEZAS_PLACE,
        )
        mover_target_z_suave(
            sim,
            target,
            script_ik,
            Z_TARGET_BAJADA_ZONA_PLACE,
        )
        fijar_separacion_pinza(
            sim,
            articulacion_apertura,
            dedo_izquierdo,
            dedo_derecho,
            SEPARACION_DEDOS_PINZA_SUELTA,
            script_rg2,
        )
        mover_target_z_suave(
            sim,
            target,
            script_ik,
            Z_TARGET_SUBIDA_PINZA,
        )
        fijar_separacion_pinza(
            sim,
            articulacion_apertura,
            dedo_izquierdo,
            dedo_derecho,
            SEPARACION_DEDOS_PINZA_ABIERTA,
            script_rg2,
        )
        girar_base_ur3(
            sim,
            articulacion_base_ur3,
            target,
            script_ik,
            GIRO_BASE_HACIA_CINTA,
        )

    print("Ciclo de manipulacion de las cuatro piezas completado.")
    parar_simulacion_tras_espera(sim, TIEMPO_ESPERA_FINAL)


if __name__ == "__main__":
    main()

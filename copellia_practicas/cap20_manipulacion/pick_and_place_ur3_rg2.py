from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time


SIGNAL_RG2 = "RG2_open"

TARGET_PATHS = [
    "/UR3/UR3_target",
    "/UR3_target",
]

RUTAS_RG2 = [
    "/RG2",
    "/UR3/connection/RG2",
    "/UR3/RG2",
]

RUTAS_ARTICULACION_PINZA = [
    "/RG2/openCloseJoint",
    "/UR3/connection/RG2/openCloseJoint",
    "/UR3/RG2/openCloseJoint",
    "/RG2/rightJoint[0]/rightLink/rightJoint/rightLink/openCloseJoint",
    "/UR3/connection/RG2/rightJoint[0]/rightLink/rightJoint/rightLink/openCloseJoint",
    "/UR3/RG2/rightJoint[0]/rightLink/rightJoint/rightLink/openCloseJoint",
    "/RG2/prismJoint",
    "/UR3/connection/RG2/prismJoint",
    "/UR3/RG2/prismJoint",
    "/RG2/leftJoint[0]",
    "/UR3/connection/RG2/leftJoint[0]",
    "/UR3/RG2/leftJoint[0]",
    "/RG2/rightJoint[0]",
    "/UR3/connection/RG2/rightJoint[0]",
    "/UR3/RG2/rightJoint[0]",
]

RUTAS_PIEZA = [
    "/pieza_pick",
    "/Pieza",
    "/Cuboid",
    "/cube",
]

RUTAS_PUNTO_AGARRE = [
    "/RG2/attachPoint",
    "/UR3/connection/RG2/attachPoint",
    "/UR3/RG2/attachPoint",
    "/UR3/UR3_tip",
    "/UR3/connection",
]

# Waypoints directos del UR3_target medidos en la escena limpia.
# Evitan saltos de configuracion de la IK y mantienen la RG2 vertical.
APROX_ORIGEN = [0.25, -0.20, 0.45]
RECOGIDA = [0.25, -0.20, 0.35]
APROX_DESTINO = [0.20, -0.30, 0.45]
DEPOSITO = [0.20, -0.30, 0.35]

POSICION_INICIAL_PIEZA = [0.123, -0.197, 0.281]
POSICION_FINAL_PIEZA = [0.113, -0.203, 0.281]
POSICION_INICIAL_TARGET = [0.25, -0.20, 0.45]
ORIENTACION_TARGET = [1.5708, 0.0, 1.5708]

PASOS_MOVIMIENTO = 60
PAUSA_ENTRE_PASOS = 0.03
PAUSA_PINZA = 1.0
VELOCIDAD_APERTURA = 0.04
VELOCIDAD_CIERRE = -0.04
FUERZA_PINZA = 20
PRECISION_AGARRE = 0.004
ITERACIONES_AJUSTE = 24
PAUSA_AJUSTE_IK = 0.12

# En True, la pieza se une a la RG2 cuando la pinza ya ha bajado hasta la pieza.
# No se mueve la pieza a mano durante la trayectoria: viaja como hija del attachPoint.
AGARRE_ASISTIDO = True


def obtener_objeto(sim, rutas, descripcion, obligatorio=True):
    for ruta in rutas:
        try:
            handle = sim.getObject(ruta)
            print(f"{descripcion} localizado en {ruta}.")
            return handle
        except Exception:
            pass

    if obligatorio:
        rutas_texto = ", ".join(rutas)
        raise RuntimeError(
            f"No se ha localizado {descripcion}. "
            f"Comprueba estas rutas en el arbol de la escena: {rutas_texto}"
        )

    print(f"No se ha localizado {descripcion}. Se continuara sin ese elemento.")
    return None


def iniciar_simulacion(sim):
    estado = sim.getSimulationState()

    if estado != sim.simulation_stopped:
        print("Reiniciando simulacion...")
        sim.stopSimulation()
        time.sleep(1.5)

    print("Iniciando simulacion...")
    sim.startSimulation()
    time.sleep(1.0)


def interpolar_posicion(inicio, fin, progreso):
    return [
        inicio[0] + (fin[0] - inicio[0]) * progreso,
        inicio[1] + (fin[1] - inicio[1]) * progreso,
        inicio[2] + (fin[2] - inicio[2]) * progreso,
    ]


def preparar_pieza(sim, pieza):
    if pieza is None:
        return

    sim.setObjectParent(pieza, -1, True)
    sim.setObjectInt32Param(pieza, sim.shapeintparam_static, 1)
    sim.setObjectInt32Param(pieza, sim.shapeintparam_respondable, 0)
    sim.setObjectPosition(pieza, -1, POSICION_INICIAL_PIEZA)
    sim.setObjectOrientation(pieza, -1, [0, 0, 0])


def preparar_target(sim, target):
    sim.setObjectPosition(target, -1, POSICION_INICIAL_TARGET)
    sim.setObjectOrientation(target, -1, ORIENTACION_TARGET)


def distancia(a, b):
    return (
        (a[0] - b[0]) ** 2
        + (a[1] - b[1]) ** 2
        + (a[2] - b[2]) ** 2
    ) ** 0.5


def mover_target(sim, target, posicion_final):
    posicion_inicial = sim.getObjectPosition(target, -1)

    for paso in range(1, PASOS_MOVIMIENTO + 1):
        progreso = paso / PASOS_MOVIMIENTO
        nueva_posicion = interpolar_posicion(posicion_inicial, posicion_final, progreso)
        sim.setObjectPosition(target, -1, nueva_posicion)
        sim.setObjectOrientation(target, -1, ORIENTACION_TARGET)
        time.sleep(PAUSA_ENTRE_PASOS)

    time.sleep(0.2)


def imprimir_punto_agarre(sim, punto_agarre, etiqueta):
    posicion = sim.getObjectPosition(punto_agarre, -1)
    print(f"{etiqueta}: {[round(valor, 3) for valor in posicion]}")


def mover_punto_agarre(sim, target, punto_agarre, posicion_final):
    for _ in range(ITERACIONES_AJUSTE):
        posicion_actual = sim.getObjectPosition(punto_agarre, -1)
        sim.setObjectOrientation(target, -1, ORIENTACION_TARGET)
        error = [
            posicion_final[0] - posicion_actual[0],
            posicion_final[1] - posicion_actual[1],
            posicion_final[2] - posicion_actual[2],
        ]

        if distancia(posicion_actual, posicion_final) <= PRECISION_AGARRE:
            break

        posicion_target = sim.getObjectPosition(target, -1)
        nueva_posicion_target = [
            posicion_target[0] + error[0] * 0.8,
            posicion_target[1] + error[1] * 0.8,
            posicion_target[2] + error[2] * 0.8,
        ]

        sim.setObjectPosition(target, -1, nueva_posicion_target)
        time.sleep(PAUSA_AJUSTE_IK)

    posicion_actual = sim.getObjectPosition(punto_agarre, -1)
    print(
        "Punto de agarre:",
        [round(valor, 3) for valor in posicion_actual],
        "objetivo:",
        posicion_final,
    )


def obtener_articulaciones_pinza(sim):
    articulaciones = []

    for ruta in RUTAS_ARTICULACION_PINZA:
        try:
            articulacion = sim.getObject(ruta)

            if articulacion not in articulaciones:
                articulaciones.append(articulacion)
        except Exception:
            pass

    if articulaciones:
        print(f"Articulaciones de la RG2 localizadas: {len(articulaciones)}")
    else:
        print("No se han localizado articulaciones internas de la RG2.")
        print("Se usara la senal RG2_open del script interno de la pinza.")

    return articulaciones


def aplicar_velocidad_pinza(sim, articulaciones, velocidad):
    for articulacion in articulaciones:
        try:
            sim.setJointForce(articulacion, FUERZA_PINZA)
        except Exception:
            pass

        try:
            sim.setJointTargetVelocity(articulacion, velocidad)
        except Exception:
            pass


def abrir_pinza(sim, articulaciones):
    sim.setIntegerSignal(SIGNAL_RG2, 1)
    aplicar_velocidad_pinza(sim, articulaciones, VELOCIDAD_APERTURA)
    print("Abriendo RG2...")
    time.sleep(PAUSA_PINZA)


def cerrar_pinza(sim, articulaciones):
    sim.setIntegerSignal(SIGNAL_RG2, 0)
    aplicar_velocidad_pinza(sim, articulaciones, VELOCIDAD_CIERRE)
    print("Cerrando RG2...")
    time.sleep(PAUSA_PINZA)


def fijar_pieza_a_pinza(sim, pieza, padre_pinza):
    if pieza is None or padre_pinza is None or not AGARRE_ASISTIDO:
        return

    try:
        sim.setObjectParent(pieza, padre_pinza, True)
    except Exception:
        pass

    print("Pieza fijada temporalmente a la pinza.")


def soltar_pieza(sim, pieza):
    if pieza is None or not AGARRE_ASISTIDO:
        return

    sim.setObjectParent(pieza, -1, True)
    sim.setObjectPosition(pieza, -1, POSICION_FINAL_PIEZA)
    sim.setObjectOrientation(pieza, -1, [0, 0, 0])
    print("Pieza liberada en el punto de deposito.")


def pick_and_place(sim, target, rg2, articulaciones_pinza, pieza, punto_agarre):
    preparar_target(sim, target)
    preparar_pieza(sim, pieza)

    abrir_pinza(sim, articulaciones_pinza)

    print("Aproximacion al origen")
    mover_target(sim, target, APROX_ORIGEN)
    imprimir_punto_agarre(sim, punto_agarre, "Punto de agarre en aproximacion")

    print("Descenso a recogida")
    mover_target(sim, target, RECOGIDA)
    imprimir_punto_agarre(sim, punto_agarre, "Punto de agarre en recogida")

    cerrar_pinza(sim, articulaciones_pinza)
    fijar_pieza_a_pinza(sim, pieza, rg2)

    print("Elevacion de la pieza")
    mover_target(sim, target, APROX_ORIGEN)
    imprimir_punto_agarre(sim, punto_agarre, "Punto de agarre elevado")

    print("Transporte al destino")
    mover_target(sim, target, APROX_DESTINO)
    imprimir_punto_agarre(sim, punto_agarre, "Punto de agarre en destino alto")

    print("Descenso a deposito")
    mover_target(sim, target, DEPOSITO)
    imprimir_punto_agarre(sim, punto_agarre, "Punto de agarre en deposito")

    soltar_pieza(sim, pieza)
    abrir_pinza(sim, articulaciones_pinza)

    print("Retirada a posicion segura")
    mover_target(sim, target, APROX_DESTINO)


def main():
    client = RemoteAPIClient()
    sim = client.require("sim")

    iniciar_simulacion(sim)

    target = obtener_objeto(sim, TARGET_PATHS, "UR3_target")
    rg2 = obtener_objeto(sim, RUTAS_RG2, "RG2")
    articulaciones_pinza = obtener_articulaciones_pinza(sim)
    pieza = obtener_objeto(sim, RUTAS_PIEZA, "pieza", obligatorio=False)
    punto_agarre = obtener_objeto(sim, RUTAS_PUNTO_AGARRE, "punto de agarre")

    print("Iniciando ciclo Pick and Place.")
    pick_and_place(sim, target, rg2, articulaciones_pinza, pieza, punto_agarre)
    print("Operacion Pick and Place finalizada.")


if __name__ == "__main__":
    main()

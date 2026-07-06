from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time


TARGET_PATHS = [
    "/UR3/UR3_target",
    "/UR3_target",
]

JOINT_PATHS = [
    "/UR3/joint",
    "/UR3/joint/link/joint",
    "/UR3/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint/link/joint/link/joint",
]

DESPLAZAMIENTO_X = 0.3
PASOS = 50
PAUSA_ENTRE_PASOS = 0.03


def obtener_objeto(sim, rutas):
    for ruta in rutas:
        try:
            handle = sim.getObject(ruta)
            print(f"Target encontrado: {ruta}")
            return handle
        except Exception:
            pass

    rutas_texto = ", ".join(rutas)
    raise RuntimeError(
        "No se ha encontrado el objeto UR3_target. "
        f"Comprueba estas rutas en el arbol de la escena: {rutas_texto}"
    )


def interpolar_posicion(posicion_inicial, posicion_final, progreso):
    return [
        posicion_inicial[0] + (posicion_final[0] - posicion_inicial[0]) * progreso,
        posicion_inicial[1] + (posicion_final[1] - posicion_inicial[1]) * progreso,
        posicion_inicial[2] + (posicion_final[2] - posicion_inicial[2]) * progreso,
    ]


def iniciar_simulacion(sim):
    estado = sim.getSimulationState()

    if estado == sim.simulation_stopped:
        print("La simulacion estaba parada. Iniciando simulacion...")
        sim.startSimulation()
        time.sleep(0.5)
    else:
        print("La simulacion ya esta en marcha.")


def obtener_articulaciones(sim):
    articulaciones = []

    for path in JOINT_PATHS:
        try:
            articulaciones.append(sim.getObject(path))
        except Exception:
            pass

    return articulaciones


def leer_posiciones_articulaciones(sim, articulaciones):
    return [sim.getJointPosition(articulacion) for articulacion in articulaciones]


def articulaciones_han_cambiado(posiciones_iniciales, posiciones_finales):
    if not posiciones_iniciales or not posiciones_finales:
        return False

    for inicial, final in zip(posiciones_iniciales, posiciones_finales):
        if abs(final - inicial) > 0.001:
            return True

    return False


def mover_target_suave(sim, target, posicion_final):
    posicion_inicial = sim.getObjectPosition(target, -1)

    for paso in range(1, PASOS + 1):
        progreso = paso / PASOS
        nueva_posicion = interpolar_posicion(
            posicion_inicial,
            posicion_final,
            progreso,
        )
        sim.setObjectPosition(target, -1, nueva_posicion)
        time.sleep(PAUSA_ENTRE_PASOS)


# Conectar con CoppeliaSim mediante la API remota ZMQ.
client = RemoteAPIClient()
sim = client.require("sim")

# La cinematica inversa se resuelve durante la simulacion.
iniciar_simulacion(sim)

# Obtener handle del Target usado por la configuracion de cinematica inversa.
target = obtener_objeto(sim, TARGET_PATHS)
articulaciones = obtener_articulaciones(sim)

# Leer posicion actual del Target en coordenadas del mundo.
posicion = sim.getObjectPosition(target, -1)
print("Posicion actual [X, Y, Z]:", posicion)

# Definir nueva posicion: desplazar 5 cm en el eje X.
nueva_posicion = [
    posicion[0] + DESPLAZAMIENTO_X,
    posicion[1],
    posicion[2],
]

print("Moviendo target hasta:", nueva_posicion)
posiciones_articulaciones_antes = leer_posiciones_articulaciones(sim, articulaciones)
mover_target_suave(sim, target, nueva_posicion)
time.sleep(0.5)
posiciones_articulaciones_despues = leer_posiciones_articulaciones(sim, articulaciones)

posicion_final = sim.getObjectPosition(target, -1)
print("Nueva posicion aplicada:", posicion_final)

if articulaciones_han_cambiado(posiciones_articulaciones_antes, posiciones_articulaciones_despues):
    print("Movimiento correcto: las articulaciones del UR3 han cambiado.")
else:
    print("El target se ha movido, pero las articulaciones no han cambiado.")
    print("Revisa en CoppeliaSim que la IK este activada y que UR3_tip y UR3_target formen el par tip-target.")

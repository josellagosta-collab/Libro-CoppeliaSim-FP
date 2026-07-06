from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math
import time


JOINT_PATHS = [
    "/UR3/joint",
    "/UR3/joint/link/joint",
    "/UR3/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint/link/joint/link/joint",
]

POSTURA_INICIAL = [0, 0, 0, 0, 0, 0]
POSTURA_TRABAJO = [150, -100, 120, -100, 90, 170]
PASOS_POR_ARTICULACION = 100
PAUSA_ENTRE_PASOS = 0.025
PAUSA_ENTRE_ARTICULACIONES = 0.4
TOLERANCIA_POSTURA_GRADOS = 1.0


def obtener_articulaciones_ur3(sim):
    articulaciones = []

    for numero, path in enumerate(JOINT_PATHS, start=1):
        handle = sim.getObject(path)
        articulaciones.append(handle)
        print(f"Eje {numero}: handle obtenido correctamente -> {handle}")

    return articulaciones


def mover_articulacion_lento(sim, articulacion, angulo_destino_grados):
    posicion_inicial = sim.getJointPosition(articulacion)
    posicion_final = math.radians(angulo_destino_grados)
    recorrido = posicion_final - posicion_inicial

    for paso in range(1, PASOS_POR_ARTICULACION + 1):
        progreso = paso / PASOS_POR_ARTICULACION
        nueva_posicion = posicion_inicial + recorrido * progreso
        sim.setJointPosition(articulacion, nueva_posicion)
        time.sleep(PAUSA_ENTRE_PASOS)


def mover_a_postura(sim, articulaciones, postura_grados):
    for numero, (articulacion, angulo) in enumerate(
        zip(articulaciones, postura_grados),
        start=1,
    ):
        print(f"Moviendo eje {numero} hasta {angulo} grados...")
        mover_articulacion_lento(sim, articulacion, angulo)
        time.sleep(PAUSA_ENTRE_ARTICULACIONES)


def esta_en_postura(sim, articulaciones, postura_grados):
    for articulacion, angulo_objetivo in zip(articulaciones, postura_grados):
        posicion_actual = math.degrees(sim.getJointPosition(articulacion))

        if abs(posicion_actual - angulo_objetivo) > TOLERANCIA_POSTURA_GRADOS:
            return False

    return True


def mostrar_posiciones(sim, articulaciones):
    print("\nPosicion actual de las articulaciones:")

    for numero, articulacion in enumerate(articulaciones, start=1):
        posicion_rad = sim.getJointPosition(articulacion)
        posicion_grados = math.degrees(posicion_rad)
        print(f"Eje {numero}: {posicion_grados:.1f} grados")


client = RemoteAPIClient()
sim = client.require("sim")

print("Obteniendo handles de las seis articulaciones del UR3...")
articulaciones = obtener_articulaciones_ur3(sim)

if len(articulaciones) != 6:
    raise RuntimeError("No se han obtenido las seis articulaciones del UR3.")

print("\nTodos los handles se han obtenido correctamente.")

if esta_en_postura(sim, articulaciones, POSTURA_INICIAL):
    print("\nEl UR3 ya esta en la postura inicial. Ejecutando movimientos...")
else:
    print("\nMoviendo a la postura inicial...")
    mover_a_postura(sim, articulaciones, POSTURA_INICIAL)

print("Moviendo a la segunda postura...")
mover_a_postura(sim, articulaciones, POSTURA_TRABAJO)

mostrar_posiciones(sim, articulaciones)

print("\nRegresando a la postura inicial...")
mover_a_postura(sim, articulaciones, POSTURA_INICIAL)

mostrar_posiciones(sim, articulaciones)

print("\nPractica finalizada.")

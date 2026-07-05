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
POSTURA_TRABAJO = [150, -110, 120, -100, 90, 170]


def obtener_articulaciones_ur3(sim):
    articulaciones = []

    for numero, path in enumerate(JOINT_PATHS, start=1):
        handle = sim.getObject(path)
        articulaciones.append(handle)
        print(f"Eje {numero}: handle obtenido correctamente -> {handle}")

    return articulaciones


def mover_a_postura(sim, articulaciones, postura_grados, pausa=2.5):
    for articulacion, angulo in zip(articulaciones, postura_grados):
        sim.setJointPosition(articulacion, math.radians(angulo))

    time.sleep(pausa)


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

print("\nMoviendo a la postura inicial...")
mover_a_postura(sim, articulaciones, POSTURA_INICIAL)

print("Moviendo a la segunda postura...")
mover_a_postura(sim, articulaciones, POSTURA_TRABAJO)

mostrar_posiciones(sim, articulaciones)

print("\nRegresando a la postura inicial...")
mover_a_postura(sim, articulaciones, POSTURA_INICIAL)

mostrar_posiciones(sim, articulaciones)

print("\nPractica finalizada.")

from pathlib import Path
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient


CARPETA = Path(__file__).resolve().parent
ESCENA_BASE = CARPETA / "cap20_abrir_cerrar_pinza.ttt"
ESCENA_SALIDA = CARPETA / "cap20_pick_and_place_ur3_rg2.ttt"

TARGET_PATHS = [
    "/UR3/UR3_target",
    "/UR3_target",
]

PIEZA_PATHS = [
    "/pieza_pick",
    "/Pieza",
    "/Cuboid",
]

ZONA_PATHS = [
    "/zona_deposito",
]

MESA_PATHS = [
    "/mesa_pick_place",
]

POS_TARGET_INICIAL = [0.25, -0.20, 0.45]
ORI_TARGET_INICIAL = [1.5708, 0.0, 1.5708]
POS_MESA = [0.118, -0.200, 0.241]
POS_PIEZA = [0.123, -0.197, 0.281]
POS_ZONA_DEPOSITO = [0.113, -0.203, 0.265]

TAM_PIEZA = [0.04, 0.04, 0.04]
TAM_MESA = [0.12, 0.10, 0.04]
TAM_ZONA_DEPOSITO = [0.05, 0.05, 0.008]


def obtener_objeto(sim, rutas):
    for ruta in rutas:
        try:
            return sim.getObject(ruta)
        except Exception:
            pass

    return None


def crear_o_colocar_cubo(sim, rutas, alias, tamanio, posicion, color):
    objeto = obtener_objeto(sim, rutas)

    if objeto is not None:
        sim.removeObjects([objeto])
        print(f"Eliminado objeto anterior: {alias}")

    objeto = sim.createPrimitiveShape(sim.primitiveshape_cuboid, tamanio, 2)
    sim.setObjectAlias(objeto, alias)
    print(f"Creado: {alias}")

    sim.setObjectPosition(objeto, -1, posicion)
    sim.setObjectOrientation(objeto, -1, [0, 0, 0])
    sim.setObjectInt32Param(objeto, sim.shapeintparam_static, 1)

    try:
        sim.setShapeColor(objeto, None, sim.colorcomponent_ambient_diffuse, color)
    except Exception:
        pass

    return objeto


def main():
    client = RemoteAPIClient()
    sim = client.require("sim")

    estado = sim.getSimulationState()
    if estado != sim.simulation_stopped:
        print("Deteniendo simulacion antes de modificar la escena...")
        sim.stopSimulation()
        time.sleep(1.0)

    sim.loadScene(str(ESCENA_BASE))
    time.sleep(0.5)
    print(f"Escena base cargada: {ESCENA_BASE}")

    target = obtener_objeto(sim, TARGET_PATHS)
    if target is None:
        raise RuntimeError(
            "No se ha encontrado UR3_target. Abre primero la escena base "
            "cap20_pick_and_place_ur3_rg2.ttt en CoppeliaSim."
        )

    sim.setObjectPosition(target, -1, POS_TARGET_INICIAL)
    sim.setObjectOrientation(target, -1, ORI_TARGET_INICIAL)
    print(f"UR3_target colocado en {POS_TARGET_INICIAL}")

    crear_o_colocar_cubo(
        sim,
        MESA_PATHS,
        "mesa_pick_place",
        TAM_MESA,
        POS_MESA,
        [0.55, 0.55, 0.50],
    )

    crear_o_colocar_cubo(
        sim,
        PIEZA_PATHS,
        "pieza_pick",
        TAM_PIEZA,
        POS_PIEZA,
        [0.9, 0.15, 0.10],
    )

    crear_o_colocar_cubo(
        sim,
        ZONA_PATHS,
        "zona_deposito",
        TAM_ZONA_DEPOSITO,
        POS_ZONA_DEPOSITO,
        [0.10, 0.45, 0.90],
    )

    sim.saveScene(str(ESCENA_SALIDA))
    print(f"Escena guardada en: {ESCENA_SALIDA}")


if __name__ == "__main__":
    main()

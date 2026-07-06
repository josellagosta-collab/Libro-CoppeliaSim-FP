from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time


SIGNAL_RG2 = "RG2_open"
TIEMPO_ABIERTA = 2.0
TIEMPO_CERRADA = 2.0
VELOCIDAD_APERTURA = 0.04
VELOCIDAD_CIERRE = -0.04
FUERZA_PINZA = 20

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


def iniciar_simulacion(sim):
    estado = sim.getSimulationState()

    if estado == sim.simulation_stopped:
        print("Iniciando simulacion...")
        sim.startSimulation()
        time.sleep(1.0)
    else:
        print("La simulacion ya esta en marcha.")


def comprobar_pinza(sim):
    for ruta in RUTAS_RG2:
        try:
            handle = sim.getObject(ruta)
            print(f"Pinza RG2 localizada en {ruta}. Handle: {handle}")
            return
        except Exception:
            pass

    print("No se ha localizado la RG2 por ruta, pero se intentara controlar con la senal.")
    print("Si no se mueve, revisa que la pinza se llame RG2 y conserve su script interno.")


def obtener_articulaciones_pinza(sim):
    articulaciones = []
    rutas_usadas = set()

    for ruta in RUTAS_ARTICULACION_PINZA:
        try:
            articulacion = sim.getObject(ruta)

            if articulacion not in articulaciones:
                articulaciones.append(articulacion)
                rutas_usadas.add(ruta)
        except Exception:
            pass

    if articulaciones:
        print("Articulaciones de la RG2 localizadas:")
        for ruta in sorted(rutas_usadas):
            print(f"  - {ruta}")
    else:
        print("No se han localizado articulaciones de la RG2 por ruta.")
        print("Se usara solamente la senal RG2_open.")

    return articulaciones


def aplicar_velocidad(sim, articulaciones, velocidad):
    for articulacion in articulaciones:
        try:
            sim.setJointForce(articulacion, FUERZA_PINZA)
        except Exception:
            pass

        try:
            sim.setJointTargetVelocity(articulacion, velocidad)
        except Exception:
            pass


def detener_articulaciones(sim, articulaciones):
    aplicar_velocidad(sim, articulaciones, 0)


def abrir_pinza(sim, articulaciones):
    sim.setIntegerSignal(SIGNAL_RG2, 1)
    aplicar_velocidad(sim, articulaciones, VELOCIDAD_APERTURA)
    print("Pinza abierta")


def cerrar_pinza(sim, articulaciones):
    sim.setIntegerSignal(SIGNAL_RG2, 0)
    aplicar_velocidad(sim, articulaciones, VELOCIDAD_CIERRE)
    print("Pinza cerrada")


client = RemoteAPIClient()
sim = client.require("sim")

iniciar_simulacion(sim)
comprobar_pinza(sim)
articulaciones_pinza = obtener_articulaciones_pinza(sim)

print("Controlando RG2 en bucle. Pulsa Ctrl+C para detener el programa.")

try:
    while True:
        abrir_pinza(sim, articulaciones_pinza)
        time.sleep(TIEMPO_ABIERTA)

        cerrar_pinza(sim, articulaciones_pinza)
        time.sleep(TIEMPO_CERRADA)
except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
    detener_articulaciones(sim, articulaciones_pinza)
    abrir_pinza(sim, articulaciones_pinza)

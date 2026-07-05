from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

# ----------------------------------------
# Conexión con CoppeliaSim
# Acuérdate de desactivar o borrar el scritpt interno del robot
# ----------------------------------------

client = RemoteAPIClient()
sim = client.require("sim")

robot = sim.getObject("/PioneerP3DX")
motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

# Control de seguridad opcional.
# El robot empieza donde lo coloques manualmente. Por eso, si activas estos
# limites, se miden respecto a esa posicion inicial, no respecto al origen.
CONTROLAR_LIMITES = False
DESPLAZAMIENTO_MAX_X = 1.5
DESPLAZAMIENTO_MAX_Y = 1.5

# Velocidades del recorrido programado original.
VELOCIDAD_AVANCE = 2.0
VELOCIDAD_GIRO_LENTA = 1.0
VELOCIDAD_GIRO_RAPIDA = 2.0

posicion_inicial = None


def detener_robot():
    sim.setJointTargetVelocity(motor_izquierdo, 0)
    sim.setJointTargetVelocity(motor_derecho, 0)


def imprimir_posicion(etiqueta):
    x, y, z = sim.getObjectPosition(robot, -1)
    print(f"{etiqueta}: x={x:.3f}, y={y:.3f}, z={z:.3f}")


def robot_dentro_del_suelo():
    if not CONTROLAR_LIMITES:
        return True

    x, y, _ = sim.getObjectPosition(robot, -1)
    x0, y0, _ = posicion_inicial
    return (
        abs(x - x0) < DESPLAZAMIENTO_MAX_X
        and abs(y - y0) < DESPLAZAMIENTO_MAX_Y
    )


def mover_durante(velocidad_izquierda, velocidad_derecha, duracion):
    sim.setJointTargetVelocity(motor_izquierdo, velocidad_izquierda)
    sim.setJointTargetVelocity(motor_derecho, velocidad_derecha)

    inicio = sim.getSimulationTime()

    while sim.getSimulationTime() - inicio < duracion:
        if not robot_dentro_del_suelo():
            detener_robot()
            print("Robot cerca del borde del suelo. Movimiento detenido.")
            return False

        time.sleep(0.01)

    detener_robot()
    time.sleep(0.2)
    return True


# ----------------------------------------
# Inicio de la simulación
# ----------------------------------------

sim.startSimulation()

time.sleep(0.5)

# El robot empieza en la posicion donde lo hayas colocado manualmente.
detener_robot()
posicion_inicial = sim.getObjectPosition(robot, -1)
imprimir_posicion("Posicion inicial")

time.sleep(1)

print("1. Avanzando")

imprimir_posicion("Antes del primer avance")

if not mover_durante(VELOCIDAD_AVANCE, VELOCIDAD_AVANCE, 3.0):
    raise SystemExit

imprimir_posicion("Despues del primer avance")

print("2. Girando a la izquierda")

if not mover_durante(VELOCIDAD_GIRO_LENTA, VELOCIDAD_GIRO_RAPIDA, 2.0):
    raise SystemExit

print("3. Avanzando")

if not mover_durante(VELOCIDAD_AVANCE, VELOCIDAD_AVANCE, 3.0):
    raise SystemExit

print("4. Girando a la derecha")

if not mover_durante(VELOCIDAD_GIRO_RAPIDA, VELOCIDAD_GIRO_LENTA, 2.0):
    raise SystemExit

print("5. Retrocediendo")

if not mover_durante(-VELOCIDAD_AVANCE, -VELOCIDAD_AVANCE, 3.0):
    raise SystemExit

print("6. Girando sobre el eje")

if not mover_durante(VELOCIDAD_AVANCE, -VELOCIDAD_AVANCE, 3.0):
    raise SystemExit

print("7. Deteniendo el robot")

detener_robot()

time.sleep(1)

sim.stopSimulation()

print("Programa finalizado")

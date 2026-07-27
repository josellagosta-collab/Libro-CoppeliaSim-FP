from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time


# ========================================
# Configuracion
# ========================================

VELOCIDAD_AVANCE = 1.6
VELOCIDAD_GIRO = 2.0
DISTANCIA_SEGURIDAD = 0.70
DURACION_GIRO = 0.8
DURACION_MAXIMA = 30
INTERVALO_CONTROL = 0.03
TIEMPO_ESPERA_INICIAL = 1

SENSORES_FRONTALES = [2, 3, 4, 5]


# ========================================
# Variables globales
# ========================================

client = None
sim = None

sensores_frontales = []
motor_izquierdo = None
motor_derecho = None


# ========================================
# Funciones
# ========================================

def conectar_con_coppeliasim():
    global client, sim

    client = RemoteAPIClient()
    sim = client.require("sim")


def obtener_objetos():
    global sensores_frontales, motor_izquierdo, motor_derecho

    sensores_frontales = []

    for numero_sensor in SENSORES_FRONTALES:
        nombre_sensor = f"/PioneerP3DX/ultrasonicSensor[{numero_sensor}]"
        sensor = sim.getObject(nombre_sensor)
        sensores_frontales.append((numero_sensor, sensor))

    motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
    motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")


def iniciar_simulacion():
    if sim.getSimulationState() == sim.simulation_stopped:
        sim.startSimulation()

    time.sleep(TIEMPO_ESPERA_INICIAL)


def detener_robot():
    sim.setJointTargetVelocity(motor_izquierdo, 0)
    sim.setJointTargetVelocity(motor_derecho, 0)


def avanzar():
    sim.setJointTargetVelocity(motor_izquierdo, VELOCIDAD_AVANCE)
    sim.setJointTargetVelocity(motor_derecho, VELOCIDAD_AVANCE)


def girar_sobre_si_mismo():
    detener_robot()
    time.sleep(0.2)

    sim.setJointTargetVelocity(motor_izquierdo, VELOCIDAD_GIRO)
    sim.setJointTargetVelocity(motor_derecho, -VELOCIDAD_GIRO)
    time.sleep(DURACION_GIRO)

    detener_robot()
    time.sleep(0.1)


def detectar_obstaculo():
    obstaculo_detectado = False
    distancia_mas_cercana = None
    sensor_mas_cercano = None

    for numero_sensor, sensor in sensores_frontales:
        detectado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

        if detectado and distancia <= DISTANCIA_SEGURIDAD:
            if distancia_mas_cercana is None or distancia < distancia_mas_cercana:
                obstaculo_detectado = True
                distancia_mas_cercana = distancia
                sensor_mas_cercano = numero_sensor

    return obstaculo_detectado, distancia_mas_cercana, sensor_mas_cercano


def ejecutar_algoritmo_reactivo():
    inicio = time.time()

    while time.time() - inicio < DURACION_MAXIMA:
        obstaculo_detectado, distancia, sensor = detectar_obstaculo()

        if obstaculo_detectado:
            print(f"Obstaculo detectado por el sensor {sensor} a {distancia:.3f} m")
            girar_sobre_si_mismo()
        else:
            avanzar()
            print("Camino libre")

        time.sleep(INTERVALO_CONTROL)


def finalizar_simulacion():
    detener_robot()
    time.sleep(0.5)
    sim.stopSimulation()


# ========================================
# Programa principal
# ========================================

def main():
    conectar_con_coppeliasim()
    obtener_objetos()

    try:
        iniciar_simulacion()
        ejecutar_algoritmo_reactivo()
    finally:
        finalizar_simulacion()


# ========================================
# Inicio de la aplicacion
# ========================================

if __name__ == "__main__":
    main()

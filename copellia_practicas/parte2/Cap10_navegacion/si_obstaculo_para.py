from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

sensores_frontales = [
    sim.getObject("/PioneerP3DX/ultrasonicSensor[3]"),
    sim.getObject("/PioneerP3DX/ultrasonicSensor[4]"),
]

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

VELOCIDAD_AVANCE = 2.0
DISTANCIA_PARADA = 0.50
DURACION_MAXIMA = 30

try:
    if sim.getSimulationState() == sim.simulation_stopped:
        sim.startSimulation()

    time.sleep(1)

    inicio = time.time()

    while time.time() - inicio < DURACION_MAXIMA:
        obstaculo_detectado = False
        distancia_obstaculo = None

        for sensor in sensores_frontales:
            detectado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

            if detectado and distancia <= DISTANCIA_PARADA:
                obstaculo_detectado = True
                distancia_obstaculo = distancia
                break

        if obstaculo_detectado:
            sim.setJointTargetVelocity(motor_izquierdo, 0)
            sim.setJointTargetVelocity(motor_derecho, 0)
            print(f"Obstaculo detectado a {distancia_obstaculo:.3f} m. Robot detenido.")
            break

        sim.setJointTargetVelocity(motor_izquierdo, VELOCIDAD_AVANCE)
        sim.setJointTargetVelocity(motor_derecho, VELOCIDAD_AVANCE)
        print("Camino libre")

        time.sleep(0.05)
    else:
        print("Tiempo maximo alcanzado.")

finally:
    sim.setJointTargetVelocity(motor_izquierdo, 0)
    sim.setJointTargetVelocity(motor_derecho, 0)
    time.sleep(0.5)

    print("Finalizando programa...")

    sim.stopSimulation()

    print("Programa finalizado.")

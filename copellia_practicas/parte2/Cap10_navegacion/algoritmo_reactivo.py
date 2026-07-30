from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

sensores_frontales = [
    (2, sim.getObject("/PioneerP3DX/ultrasonicSensor[2]")),
    (3, sim.getObject("/PioneerP3DX/ultrasonicSensor[3]")),
    (4, sim.getObject("/PioneerP3DX/ultrasonicSensor[4]")),
    (5, sim.getObject("/PioneerP3DX/ultrasonicSensor[5]")),
]

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

velocidad_avance = 1.6
velocidad_giro = 2.0
distancia_seguridad = 0.70
duracion_giro = 0.8
duracion_maxima = 30
intervalo_control = 0.03

try:
    if sim.getSimulationState() == sim.simulation_stopped:
        sim.startSimulation()

    time.sleep(1)

    inicio = time.time()

    while time.time() - inicio < duracion_maxima:
        obstaculo_detectado = False
        distancia_mas_cercana = None
        sensor_mas_cercano = None

        for numero_sensor, sensor in sensores_frontales:
            detectado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

            if detectado and distancia <= distancia_seguridad:
                if distancia_mas_cercana is None or distancia < distancia_mas_cercana:
                    obstaculo_detectado = True
                    distancia_mas_cercana = distancia
                    sensor_mas_cercano = numero_sensor

        if obstaculo_detectado:
            print(
                f"Obstaculo detectado por el sensor {sensor_mas_cercano} "
                f"a {distancia_mas_cercana:.3f} m"
            )

            sim.setJointTargetVelocity(motor_izquierdo, 0)
            sim.setJointTargetVelocity(motor_derecho, 0)
            time.sleep(0.2)

            sim.setJointTargetVelocity(motor_izquierdo, velocidad_giro)
            sim.setJointTargetVelocity(motor_derecho, -velocidad_giro)
            time.sleep(duracion_giro)

            sim.setJointTargetVelocity(motor_izquierdo, 0)
            sim.setJointTargetVelocity(motor_derecho, 0)
            time.sleep(0.1)

        else:
            sim.setJointTargetVelocity(motor_izquierdo, velocidad_avance)
            sim.setJointTargetVelocity(motor_derecho, velocidad_avance)
            print("Camino libre")

        time.sleep(intervalo_control)

finally:
    sim.setJointTargetVelocity(motor_izquierdo, 0)
    sim.setJointTargetVelocity(motor_derecho, 0)
    time.sleep(0.5)

    sim.stopSimulation()

from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

print("Inicio del programa")

client = RemoteAPIClient()
sim = client.require("sim")

print("Conectado con CoppeliaSim")

motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")
motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")

print("Motores localizados")

sim.startSimulation()
time.sleep(1)

velocidad = 2.0

print("Avanzando...")

sim.setJointTargetVelocity(motor_izquierdo, velocidad)
sim.setJointTargetVelocity(motor_derecho, velocidad)

time.sleep(3)

print("Deteniendo...")

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(1)

sim.stopSimulation()

print("Prueba finalizada")
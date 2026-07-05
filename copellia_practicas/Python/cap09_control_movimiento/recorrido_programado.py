from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

# ----------------------------------------
# Conexión con CoppeliaSim
# ----------------------------------------

client = RemoteAPIClient()
sim = client.require("sim")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

# ----------------------------------------
# Inicio de la simulación
# ----------------------------------------

sim.startSimulation()

time.sleep(1)

print("1. Avanzando")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)

time.sleep(3)

print("2. Girando a la izquierda")

sim.setJointTargetVelocity(motor_izquierdo, 1.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)

time.sleep(2)

print("3. Avanzando")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)

time.sleep(3)

print("4. Girando a la derecha")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 1.0)

time.sleep(2)

print("5. Retrocediendo")

sim.setJointTargetVelocity(motor_izquierdo, -2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)

time.sleep(3)

print("6. Girando sobre el eje")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)

time.sleep(3)

print("7. Deteniendo el robot")

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(1)

sim.stopSimulation()

print("Programa finalizado")
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

sim.startSimulation()

time.sleep(1)

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)

time.sleep(3)

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(1)

sim.stopSimulation()
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

print("Iniciando simulación...")

sim.startSimulation()

time.sleep(5)

sim.stopSimulation()

print("Simulación detenida.")
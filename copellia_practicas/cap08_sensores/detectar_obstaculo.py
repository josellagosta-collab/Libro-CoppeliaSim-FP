import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

if sim.getSimulationState() == sim.simulation_stopped:
    print("La simulacion estaba parada. Arrancando simulacion...")
    sim.startSimulation()
    time.sleep(0.5)

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor[4]")

detectado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

if detectado:
    print("Obstaculo detectado")
    print(f"Distancia: {distancia:.3f} m")
else:
    print("Camino libre")

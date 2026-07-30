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

distancia_seguridad = 0.50

if detectado and distancia < distancia_seguridad:
    print("Obstaculo demasiado cerca")
    print(f"Distancia: {distancia:.3f} m")
elif detectado:
    print("Obstaculo detectado, pero a distancia segura")
    print(f"Distancia: {distancia:.3f} m")
else:
    print("Camino libre")

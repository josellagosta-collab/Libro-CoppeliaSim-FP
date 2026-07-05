from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

for i in range(16):
    nombre = f"/PioneerP3DX/ultrasonicSensor[{i}]"
    sensor = sim.getObject(nombre)

    resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

    if resultado:
        print(f"{nombre} detecta a {distancia:.3f} m")
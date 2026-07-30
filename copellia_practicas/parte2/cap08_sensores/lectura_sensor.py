from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor[4]")

resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

print("===================================")
print(" SENSOR DE PROXIMIDAD")
print("===================================")

if resultado:
    print("Obstáculo detectado : True")
    print(f"Distancia           : {distancia:.3f} m")
else:
    print("Obstáculo detectado : False")
    print("Camino libre")
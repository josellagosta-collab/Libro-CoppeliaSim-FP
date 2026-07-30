from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

robot = sim.getObject('/PioneerP3DX')

posicion = sim.getObjectPosition(robot)

print(posicion)

orientacion = sim.getObjectOrientation(robot)

print(orientacion)
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

robot = sim.getObject("/PioneerP3DX")


posicion = sim.getObjectPosition(robot, sim.handle_world)

posicion[0] -= 0.50

sim.setObjectPosition(
    robot,
    sim.handle_world,
    posicion
)

orientacion = sim.getObjectOrientation(
    robot,
    sim.handle_world
)

print(orientacion)
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

robot = sim.getObject('/PioneerP3DX')

sim.setObjectPosition(robot, -1, [1.5, 0.0, 0.1388])
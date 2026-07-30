from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

robot = sim.getObject("/PioneerP3DX")

sim.setObjectPosition(
    robot,
    sim.handle_world,
    [1.0, 0.0, 0.138]
)
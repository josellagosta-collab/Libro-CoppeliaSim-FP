from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

visionSensor = sim.getObject('/visionSensor')

sim.startSimulation()

image, resolution = sim.getVisionSensorImg(visionSensor)

print("Resolución:", resolution)

sim.stopSimulation()
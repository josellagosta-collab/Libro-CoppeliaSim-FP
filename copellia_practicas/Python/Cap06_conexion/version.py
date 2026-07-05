from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

version = sim.getInt32Param(sim.intparam_program_version)

print(f"Versión de CoppeliaSim: {version}")
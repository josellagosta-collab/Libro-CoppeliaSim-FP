from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Crear el cliente
client = RemoteAPIClient()

# Obtener el objeto principal del simulador
sim = client.require('sim')

print("Conexión establecida correctamente.")
print(f"Tiempo actual de simulación: {sim.getSimulationTime():.3f} segundos")
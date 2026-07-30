from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math

# Conectar con CoppeliaSim
client = RemoteAPIClient()
sim = client.require('sim')

# Obtener la articulacion de la base del UR3
base_joint = sim.getObject('/UR3/joint')

# Cada ejecucion suma 45 grados a la posicion actual
incremento = math.radians(45)
posicion_actual = sim.getJointPosition(base_joint)
nueva_posicion = posicion_actual + incremento

# setJointPosition cambia el valor del joint directamente. Es mas fiable para
# ver el movimiento si el joint no esta configurado en modo motor/position.
sim.setJointPosition(base_joint, nueva_posicion)

print(
    "Base girada 45 grados: "
    f"{math.degrees(posicion_actual):.1f} -> {math.degrees(nueva_posicion):.1f} grados"
)

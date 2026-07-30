import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

NUM_SENSORES = 16
SENSORES_FRONTALES = {3, 4}
TIEMPO_LECTURA = 2.0
INTERVALO_LECTURA = 0.05

if sim.getSimulationState() == sim.simulation_stopped:
    print("La simulacion estaba parada. Arrancando simulacion...")
    sim.startSimulation()
    time.sleep(0.5)

sensores = []

for i in range(NUM_SENSORES):
    nombre = f"/PioneerP3DX/ultrasonicSensor[{i}]"
    sensores.append((i, nombre, sim.getObject(nombre)))

lecturas = {i: None for i in range(NUM_SENSORES)}
inicio = time.time()

while time.time() - inicio < TIEMPO_LECTURA:
    for i, nombre, sensor in sensores:
        resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

        if resultado and (lecturas[i] is None or distancia < lecturas[i]):
            lecturas[i] = distancia

    time.sleep(INTERVALO_LECTURA)

print("===================================")
print(" RECORRIDO DE SENSORES")
print("===================================")

hay_detecciones = False

for i, nombre, sensor in sensores:
    distancia = lecturas[i]
    marca = " frontal" if i in SENSORES_FRONTALES else ""

    if distancia is None:
        print(f"{nombre}{marca}: sin deteccion")
    else:
        hay_detecciones = True
        print(f"{nombre}{marca}: detecta a {distancia:.3f} m")

if not hay_detecciones:
    print()
    print("No se ha detectado ningun obstaculo.")
    print("Comprueba que el obstaculo este cerca, dentro del cono del sensor y que sea detectable.")

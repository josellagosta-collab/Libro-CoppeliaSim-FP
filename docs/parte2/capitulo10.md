::: chapter-cover
number: 10
title: Navegación autónoma mediante sensores
time: 6 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo

content:

Al finalizar este capítulo serás capaz de:

- Comprender el ciclo percepción → decisión → acción utilizado en robótica móvil.
- Integrar los sensores de proximidad y los motores del Pioneer P3DX en un mismo programa.
- Programar comportamientos reactivos sencillos.
- Detectar obstáculos y modificar automáticamente el movimiento del robot.
- Utilizar estructuras condicionales para controlar el comportamiento del Pioneer P3DX.
- Desarrollar tu primer robot autónomo utilizando Python y CoppeliaSim.

:::

# Capítulo 10 · Navegación autónoma mediante sensores

### Cuando un robot comienza a tomar decisiones

En los dos capítulos anteriores hemos aprendido dos capacidades fundamentales de cualquier robot móvil.

En primer lugar, descubrimos cómo utilizar los sensores de proximidad para conocer lo que ocurre alrededor del Pioneer P3DX.

Después aprendimos a controlar sus motores para desplazar el robot en cualquier dirección.

Hasta ahora ambas capacidades se han utilizado por separado.

Nuestros programas eran capaces de leer sensores o de mover el robot, pero nunca utilizaban la información obtenida para modificar su comportamiento.

En otras palabras, el Pioneer P3DX ejecutaba siempre la misma secuencia de movimientos independientemente de lo que encontrara a su alrededor.

Sin embargo, un robot autónomo funciona de una manera muy diferente.

Observa continuamente el entorno mediante sus sensores, interpreta la información recibida y decide cuál debe ser su siguiente acción.

Este proceso se repite una y otra vez mientras el robot permanece en funcionamiento.

Gracias a este mecanismo puede adaptarse a situaciones cambiantes sin necesidad de que una persona controle cada uno de sus movimientos.

En este capítulo construiremos nuestro primer robot reactivo.

Será capaz de desplazarse por la escena, detectar obstáculos y modificar automáticamente su trayectoria para evitar las colisiones.

Aunque el algoritmo que desarrollaremos será sencillo, reproduce el mismo principio de funcionamiento utilizado en robots móviles reales.

::: teacher
title: Consejo para el profesor

content:

Antes de comenzar este capítulo, pregunta al alumnado qué diferencia existe entre un coche teledirigido y un robot autónomo.

La discusión suele conducir de forma natural a la idea de que un robot no solo debe moverse, sino también interpretar el entorno y tomar decisiones.

Este es el concepto fundamental que se desarrollará a lo largo del capítulo.

:::

---

## 10.1 Del movimiento programado al comportamiento autónomo

Hasta ahora todos los movimientos del Pioneer P3DX estaban completamente definidos por el programa.

Si ejecutábamos el mismo código dos veces, el robot realizaba exactamente el mismo recorrido.

No importaba si delante del robot aparecía un obstáculo o si el camino estaba completamente despejado.

El comportamiento siempre era idéntico.

Esta forma de trabajar resulta muy útil para comprender el funcionamiento de los motores, pero presenta una limitación importante.

El robot no puede reaccionar ante los cambios que se producen en su entorno.

Para conseguir un comportamiento autónomo debemos combinar tres procesos que se ejecutan continuamente.

1. Percibir el entorno mediante los sensores.
2. Decidir cuál debe ser la siguiente acción.
3. Actuar modificando el movimiento del robot.

Cuando termina este ciclo, el proceso vuelve a comenzar.

De esta forma el Pioneer P3DX adapta continuamente su comportamiento a la información proporcionada por sus sensores.

::: info
title: El ciclo percepción → decisión → acción

content:

La mayoría de los robots móviles modernos funcionan siguiendo un ciclo continuo.

Primero obtienen información mediante sus sensores.

Después procesan esa información para decidir qué hacer.

Finalmente ejecutan la acción correspondiente actuando sobre los motores.

Al terminar, vuelven a comenzar el proceso.

Este ciclo puede repetirse decenas o incluso cientos de veces por segundo.

:::

---

### Del programa secuencial al bucle de control

Los programas desarrollados hasta ahora tenían una estructura muy sencilla.

Ejecutaban una serie de instrucciones y terminaban.

Por ejemplo:

```text
Iniciar simulación

Avanzar

Esperar tres segundos

Detener el robot

Finalizar simulación
```

En un robot autónomo esta estructura deja de ser válida.

El programa debe permanecer en ejecución mientras el robot esté funcionando.

Por ello utilizaremos un **bucle de control**, encargado de repetir continuamente las mismas operaciones.

Su funcionamiento puede resumirse de la siguiente forma.

```text
Mientras el robot esté funcionando

    Leer sensores

    Analizar la información

    Decidir el movimiento

    Controlar los motores

Repetir
```

Este esquema constituye la base de prácticamente todos los robots móviles, independientemente de su tamaño o complejidad.

---

### Nuestro primer comportamiento inteligente

El objetivo de este capítulo será desarrollar un algoritmo muy sencillo.

Mientras el Pioneer P3DX no detecte ningún obstáculo continuará avanzando.

En cuanto uno de los sensores detecte un objeto situado delante del robot, el programa modificará automáticamente el movimiento para evitar la colisión.

Aunque este comportamiento puede parecer simple, representa un cambio muy importante respecto a los capítulos anteriores.

Por primera vez el movimiento del robot dejará de estar completamente programado.

Será la información proporcionada por los sensores la que determine qué acción debe realizar en cada momento.

::: summary
title: Idea clave

content:

Un robot autónomo no ejecuta una secuencia fija de movimientos.

Observa continuamente el entorno, interpreta la información obtenida mediante sus sensores y modifica su comportamiento actuando sobre los motores.

Este ciclo de percepción, decisión y acción constituye la base del funcionamiento de cualquier robot móvil.

:::

---

## 10.2 Integrando sensores y motores

En el capítulo 8 aprendimos a leer la información proporcionada por los sensores de proximidad.

Posteriormente, en el capítulo 9, utilizamos los motores del Pioneer P3DX para controlar su movimiento.

Hasta ahora ambas capacidades se habían utilizado de forma independiente.

Ha llegado el momento de integrarlas en un único programa.

A partir de este momento el Pioneer P3DX será capaz de observar continuamente el entorno mientras se desplaza.

La información obtenida por los sensores servirá para decidir cómo deben actuar los motores en cada instante.

Este tipo de programación recibe el nombre de **control reactivo**, ya que el comportamiento del robot depende directamente de la información que recibe del entorno.

---

### Uniendo las dos partes del programa

Nuestro programa deberá realizar dos tareas de forma continua.

La primera consistirá en leer el sensor situado en la parte frontal del robot.

La segunda será controlar la velocidad de los motores en función del resultado obtenido.

De forma simplificada, el funcionamiento será el siguiente:

```text
Leer sensor frontal

¿Existe un obstáculo?

    Sí  → Cambiar el movimiento

    No  → Continuar avanzando
```

Este proceso se repetirá continuamente mientras el robot permanezca en funcionamiento.

---

### Obteniendo todas las referencias

Como ya vimos en los capítulos anteriores, lo primero será obtener las referencias a los objetos que vamos a utilizar.

Necesitaremos:

- el sensor frontal;
- el motor izquierdo;
- el motor derecho.

```python
sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor[3]")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")
```

A partir de ese momento podremos leer el sensor y controlar los motores tantas veces como sea necesario.

::: info
title: ¿Por qué obtenemos las referencias una sola vez?

content:

Las referencias a los objetos únicamente deben obtenerse al inicio del programa.

Una vez almacenadas en variables, pueden reutilizarse durante toda la ejecución.

Buscar continuamente los mismos objetos haría que el programa fuese menos eficiente.

:::

---

### Leyendo el sensor

Para comprobar si existe un obstáculo utilizaremos la función que ya conocemos.

```python
resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)
```

Recordemos que el primer valor indica si el sensor ha detectado un objeto.

```python
if resultado:
    print("Obstáculo detectado")
else:
    print("Camino libre")
```

En este capítulo únicamente utilizaremos el valor de `resultado`.

La distancia será útil más adelante, cuando desarrollemos comportamientos más avanzados.

---

### Controlando el movimiento

Una vez conocida la información del sensor podremos actuar sobre los motores.

Por ejemplo, si no existe ningún obstáculo:

```python
sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)
```

El Pioneer P3DX continuará avanzando.

Más adelante veremos cómo modificar estas velocidades cuando aparezca un obstáculo.

---

### Un único programa

Observa que ya no tenemos dos programas independientes.

Ahora el mismo programa es capaz de:

- leer el sensor;
- interpretar el resultado;
- controlar los motores.

Este es precisamente el principio de funcionamiento de cualquier robot móvil autónomo.

Aunque el comportamiento todavía es muy sencillo, la estructura general ya es la misma que utilizan aplicaciones mucho más complejas.

::: teacher
title: Consejo para el profesor

content:

Es importante que el alumnado comprenda que sensores y motores no son programas distintos.

Ambos forman parte del mismo sistema de control.

Una buena estrategia consiste en dibujar en la pizarra un esquema donde las flechas conecten los sensores con el programa y el programa con los motores.

Este diagrama facilitará la comprensión del algoritmo que desarrollaremos en el siguiente apartado.

:::

---

### Preparando el algoritmo de navegación

Ya disponemos de todos los elementos necesarios.

Sabemos cómo obtener información del entorno y cómo modificar el movimiento del Pioneer P3DX.

Solo falta una pieza.

Necesitamos un algoritmo que decida qué hacer cuando el sensor detecte un obstáculo.

Ese será precisamente el objetivo del siguiente apartado.

::: summary
title: Idea clave

content:

Un robot autónomo combina continuamente dos procesos:

- obtener información mediante los sensores;
- actuar sobre los motores.

La inteligencia del robot reside en el algoritmo que relaciona ambos procesos.

:::

---

## 10.3 Nuestro primer algoritmo reactivo

Ya sabemos cómo leer un sensor de proximidad y cómo controlar los motores del Pioneer P3DX.

Ahora vamos a combinar ambos conocimientos para desarrollar nuestro primer algoritmo reactivo.

Un algoritmo reactivo es aquel que modifica su comportamiento en función de la información que recibe del entorno.

En nuestro caso el comportamiento será muy sencillo.

- Si el camino está libre, el robot continuará avanzando.
- Si detecta un obstáculo, se detendrá.

Aunque pueda parecer un comportamiento muy simple, representa el primer paso hacia la navegación autónoma.

---

### Pensando como un robot

Antes de escribir una sola línea de código conviene imaginar cómo "piensa" el Pioneer P3DX.

Su razonamiento podría resumirse de la siguiente forma:

```text
Mientras la simulación esté funcionando

    Leer el sensor frontal

    Si existe un obstáculo

        Detener el robot

    En caso contrario

        Continuar avanzando

Volver a empezar
```

Este proceso se repetirá continuamente durante toda la ejecución del programa.

---

### El bucle de control

Para conseguir este comportamiento utilizaremos un bucle infinito.

```python
while True:

    resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

    if resultado:
        print("Obstáculo detectado")
    else:
        print("Camino libre")
```

Este programa todavía no mueve el robot.

Su única misión consiste en comprobar continuamente el estado del sensor.

Ejecútalo y acerca un cubo delante del Pioneer P3DX.

Deberías observar cómo el mensaje mostrado por la consola cambia automáticamente.

::: info
title: ¿Por qué utilizamos un bucle infinito?

content:

Un robot no deja de observar el entorno después de realizar una única lectura.

Mientras permanezca funcionando debe seguir comprobando continuamente la información proporcionada por sus sensores.

Por este motivo utilizamos un bucle que repite el mismo proceso una y otra vez.

:::

---

### Añadiendo el movimiento

Una vez comprobado que el sensor funciona correctamente, podemos incorporar el control de los motores.

```python
if resultado:

    sim.setJointTargetVelocity(motor_izquierdo, 0)
    sim.setJointTargetVelocity(motor_derecho, 0)

else:

    sim.setJointTargetVelocity(motor_izquierdo, 2.0)
    sim.setJointTargetVelocity(motor_derecho, 2.0)
```

Ahora el comportamiento cambia completamente.

Mientras no exista ningún obstáculo el Pioneer P3DX avanzará.

En cuanto el sensor detecte un objeto, ambos motores se detendrán inmediatamente.

---

### El primer comportamiento autónomo

Aunque el algoritmo únicamente dispone de dos acciones posibles, ya podemos afirmar que el robot presenta un comportamiento autónomo.

Su movimiento deja de estar completamente programado.

Ahora depende de la información recibida por el sensor.

Si colocamos un obstáculo delante del Pioneer, el robot actuará de una manera.

Si retiramos el obstáculo, actuará de otra completamente distinta.

La decisión ya no la toma el programador.

La toma el propio algoritmo durante la ejecución.

---

### Programa completo

El siguiente programa reúne todos los elementos estudiados hasta ahora.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor[3]")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

sim.startSimulation()

time.sleep(1)

while True:

    resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

    if resultado:

        sim.setJointTargetVelocity(motor_izquierdo, 0)
        sim.setJointTargetVelocity(motor_derecho, 0)

        print("Obstáculo detectado")

    else:

        sim.setJointTargetVelocity(motor_izquierdo, 2.0)
        sim.setJointTargetVelocity(motor_derecho, 2.0)

        print("Camino libre")

    time.sleep(0.05)
```

Observa que el programa ya no termina automáticamente.

Permanece ejecutándose mientras el usuario no lo interrumpa.

Este comportamiento es completamente normal en aplicaciones de robótica.

---

::: common-error
title: El programa muestra demasiados mensajes

content:

El bucle de control puede ejecutarse decenas de veces por segundo.

Si no incorporamos una pequeña pausa mediante `time.sleep()`, la consola se llenará rápidamente de mensajes y el programa consumirá más recursos de los necesarios.

En este ejemplo utilizamos una espera de 50 milisegundos para limitar la frecuencia de ejecución.

:::

---

::: teacher
title: Consejo para el profesor

content:

Este es un buen momento para insistir en la diferencia entre un programa secuencial y un sistema reactivo.

El alumnado debe comprender que el robot ya no ejecuta una lista fija de movimientos.

Ahora observa continuamente el entorno y modifica su comportamiento en tiempo real.

:::

---

::: summary
title: Idea clave

content:

El primer comportamiento autónomo del Pioneer P3DX consiste en relacionar directamente la información del sensor con el movimiento de los motores.

Cuando el sensor detecta un obstáculo, el robot se detiene.

Cuando el camino vuelve a estar libre, continúa avanzando automáticamente.

Este sencillo algoritmo constituye la base de los sistemas de navegación reactiva.

:::

---

## 10.4 Construyendo un bucle de control seguro

En el apartado anterior hemos desarrollado nuestro primer algoritmo reactivo.

El Pioneer P3DX era capaz de avanzar cuando el camino estaba libre y detenerse al detectar un obstáculo.

Sin embargo, nuestro programa presentaba una limitación importante.

El bucle de control se ejecutaba indefinidamente.

```python
while True:
```

Para finalizar el programa era necesario interrumpir manualmente su ejecución mediante **Ctrl+C**.

Aunque este comportamiento puede resultar aceptable durante las primeras pruebas, no constituye una buena práctica de programación.

Siempre que sea posible, un robot debe finalizar su ejecución dejando el sistema en un estado seguro.

En nuestro caso eso significa:

- detener los motores;
- finalizar la simulación;
- cerrar correctamente el programa.

---

### Una ejecución controlada

Durante las primeras prácticas no necesitamos que el robot funcione indefinidamente.

Podemos limitar la duración de la simulación.

Por ejemplo, durante treinta segundos.

```python
inicio = time.time()

while time.time() - inicio < 30:

    ...
```

De esta forma el programa finalizará automáticamente cuando transcurra el tiempo establecido.

---

### Finalizando correctamente

Cuando el bucle termina debemos asegurarnos de dejar el robot completamente detenido.

```python
sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(0.5)

sim.stopSimulation()
```

Con estas instrucciones garantizamos que el Pioneer P3DX no continúa moviéndose después de finalizar el programa.

---

### Programa completo

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor[3]")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

sim.startSimulation()

time.sleep(1)

inicio = time.time()

while time.time() - inicio < 30:

    resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

    if resultado:

        sim.setJointTargetVelocity(motor_izquierdo, 0)
        sim.setJointTargetVelocity(motor_derecho, 0)

        print("Obstáculo detectado")

    else:

        sim.setJointTargetVelocity(motor_izquierdo, 2.0)
        sim.setJointTargetVelocity(motor_derecho, 2.0)

        print("Camino libre")

    time.sleep(0.05)

print("Finalizando programa...")

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(0.5)

sim.stopSimulation()

print("Programa finalizado.")
```

---

### Un comportamiento todavía mejor

Nuestro robot ya es capaz de reaccionar ante un obstáculo.

Sin embargo, todavía presenta una limitación.

Cuando detecta un objeto simplemente se detiene.

Si el obstáculo permanece delante del Pioneer P3DX, el robot permanecerá inmóvil para siempre.

No intenta rodearlo ni buscar un camino alternativo.

En otras palabras, todavía no evita los obstáculos.

Únicamente deja de avanzar.

Esta diferencia es importante.

Detenerse no significa navegar.

Para que el robot pueda desplazarse de forma autónoma necesitaremos añadir una nueva decisión.

En lugar de detenerse cuando detecte un obstáculo, hará lo siguiente:

1. Detenerse brevemente.
2. Girar sobre su propio eje.
3. Comprobar nuevamente el sensor.
4. Continuar avanzando cuando el camino vuelva a estar libre.

Este sencillo comportamiento permitirá al Pioneer P3DX esquivar obstáculos de forma completamente automática.

Será el algoritmo que desarrollaremos en el siguiente apartado.

::: info
title: De un robot reactivo a un robot autónomo

content:

Todos los robots autónomos son reactivos, pero no todos los robots reactivos son realmente autónomos.

Un robot que únicamente se detiene cuando detecta un obstáculo sigue sin resolver el problema.

La autonomía aparece cuando el robot es capaz de modificar su comportamiento para continuar realizando su tarea.

En nuestro caso, buscará una nueva dirección antes de seguir avanzando.

:::

---

::: summary
title: Idea clave

content:

Un programa de robótica no solo debe controlar correctamente sensores y motores.

También debe comenzar y finalizar su ejecución de forma segura.

Además, un verdadero robot autónomo no se limita a detenerse ante un obstáculo: intenta encontrar una forma de continuar su recorrido.

:::

---

## 10.5 Construyendo un robot que evita obstáculos

Hasta ahora nuestro Pioneer P3DX era capaz de detectar un obstáculo y detenerse.

Aunque este comportamiento ya puede considerarse reactivo, presenta una limitación evidente.

Si el obstáculo permanece delante del robot, este nunca volverá a moverse.

Para conseguir una verdadera navegación autónoma necesitamos añadir una nueva estrategia.

Cuando el sensor detecte un obstáculo, el robot deberá buscar una nueva dirección antes de continuar avanzando.

Nuestro algoritmo será muy sencillo.

1. Avanzar mientras el camino esté libre.
2. Si aparece un obstáculo, detenerse.
3. Girar sobre su propio eje durante un breve intervalo de tiempo.
4. Volver a comprobar el sensor.
5. Continuar avanzando cuando el camino vuelva a estar despejado.

Aunque el comportamiento es simple, el resultado es sorprendente.

El Pioneer P3DX será capaz de desplazarse por la escena evitando los obstáculos que encuentre a su paso.

---

### Diseñando el algoritmo

Antes de escribir el programa conviene representar el comportamiento mediante un algoritmo.

```text
Mientras la simulación esté funcionando

    Leer sensor frontal

    ¿Hay obstáculo?

        Sí

            Detener el robot

            Girar sobre el eje

        No

            Avanzar

Repetir
```

Observa que el algoritmo continúa ejecutándose indefinidamente.

Cada decisión depende exclusivamente de la información obtenida por el sensor.

---

### Programa completo

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor[3]")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

sim.startSimulation()

time.sleep(1)

inicio = time.time()

while time.time() - inicio < 30:

    resultado, distancia, punto, objeto, normal = sim.readProximitySensor(sensor)

    if resultado:

        print("Obstáculo detectado")

        sim.setJointTargetVelocity(motor_izquierdo, 0)
        sim.setJointTargetVelocity(motor_derecho, 0)

        time.sleep(0.2)

        sim.setJointTargetVelocity(motor_izquierdo, 2.0)
        sim.setJointTargetVelocity(motor_derecho, -2.0)

        time.sleep(0.8)

    else:

        sim.setJointTargetVelocity(motor_izquierdo, 2.0)
        sim.setJointTargetVelocity(motor_derecho, 2.0)

    time.sleep(0.05)

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(0.5)

sim.stopSimulation()
```

---

### Analizando el comportamiento

Mientras el sensor no detecta ningún obstáculo, ambos motores giran a la misma velocidad.

El Pioneer P3DX avanza en línea recta.

Cuando aparece un obstáculo delante del robot ocurre una secuencia de acciones muy rápida.

Primero ambos motores se detienen.

Después las ruedas giran en sentidos opuestos.

Como consecuencia, el Pioneer P3DX rota sobre su propio eje.

Tras unos instantes vuelve a comenzar el ciclo de control.

Si el sensor ya no detecta el obstáculo, el robot continúa avanzando en la nueva dirección.

Este comportamiento produce la sensación de que el robot está "pensando", cuando en realidad únicamente está ejecutando un algoritmo muy sencillo.

---

::: info
title: ¿Por qué giramos siempre hacia el mismo lado?

content:

En este ejemplo el Pioneer P3DX gira siempre hacia la derecha.

Se trata de una simplificación que facilita la comprensión del algoritmo.

Más adelante podríamos introducir estrategias más elaboradas, como elegir aleatoriamente el sentido del giro o utilizar varios sensores para decidir cuál es la mejor dirección.

:::

---

### Limitaciones del algoritmo

Nuestro robot ya evita obstáculos sencillos.

Sin embargo, todavía presenta algunas limitaciones.

- Siempre gira en el mismo sentido.
- Solo utiliza un sensor frontal.
- No planifica la trayectoria.
- Puede quedar atrapado en determinadas configuraciones de obstáculos.

Estas limitaciones son completamente normales.

Los algoritmos utilizados en robots industriales y vehículos autónomos son mucho más complejos.

No obstante, todos ellos parten del mismo principio que acabamos de estudiar: utilizar la información de los sensores para decidir cómo deben actuar los motores.

---

::: practice
title: Práctica guiada · Mejorando el algoritmo

difficulty: Media

time: 30 minutos

content:

Modifica el programa para experimentar con diferentes comportamientos.

Prueba, por ejemplo:

- aumentar o disminuir el tiempo de giro;
- modificar la velocidad de los motores;
- hacer que el robot retroceda antes de girar;
- cambiar el sentido del giro.

Observa cómo pequeñas modificaciones producen comportamientos muy diferentes.

Intenta conseguir que el Pioneer P3DX recorra la mayor distancia posible sin chocar con los obstáculos.

:::

---

::: challenge
title: Reto · Un comportamiento más inteligente

difficulty: Alta

content:

Diseña una nueva versión del programa que alterne el sentido del giro cada vez que detecte un obstáculo.

Para ello puedes utilizar una variable que recuerde el último giro realizado.

Compara el comportamiento obtenido con el algoritmo original y analiza cuál de los dos consigue desplazarse con mayor eficacia.

:::

---

::: summary
title: Idea clave

content:

La navegación autónoma surge al combinar sensores, algoritmos de decisión y motores.

Aunque el comportamiento desarrollado en este capítulo es muy sencillo, reproduce el mismo principio utilizado por sistemas de navegación mucho más avanzados.

Hemos construido nuestro primer robot capaz de reaccionar automáticamente ante el entorno.

:::

---

# Conceptos clave

Al finalizar este capítulo deberías recordar las siguientes ideas fundamentales.

- Un robot autónomo combina continuamente percepción, decisión y acción.
- Los sensores proporcionan información sobre el entorno.
- Los motores permiten modificar el movimiento del robot.
- Un algoritmo reactivo adapta el comportamiento del robot según la información recibida por los sensores.
- La estructura básica de un robot autónomo se implementa mediante un bucle de control.
- La sentencia `if` permite seleccionar diferentes acciones dependiendo del resultado de la lectura de un sensor.
- Un robot puede modificar su trayectoria sin intervención humana reaccionando automáticamente ante los obstáculos.
- La navegación autónoma más sencilla consiste en detectar un obstáculo, cambiar la orientación del robot y continuar avanzando.
- Todos los sistemas de navegación móvil parten del ciclo percepción → decisión → acción.

---

# Autoevaluación

Responde a las siguientes preguntas antes de continuar con el siguiente capítulo.

1. ¿Qué diferencia existe entre un movimiento programado y un comportamiento autónomo?

2. ¿Qué función desempeñan los sensores dentro de un robot móvil?

3. ¿Por qué un robot autónomo necesita un bucle de control?

4. ¿Qué ocurre cuando el sensor detecta un obstáculo en el algoritmo desarrollado durante este capítulo?

5. ¿Por qué utilizamos una estructura `if` en el programa?

6. ¿Qué ventajas presenta un comportamiento reactivo frente a una secuencia fija de movimientos?

7. ¿Qué limitaciones presenta el algoritmo de evasión de obstáculos implementado?

8. ¿Cómo podría mejorarse este algoritmo utilizando varios sensores?

---

::: practice
title: Práctica guiada · Diseñando un algoritmo reactivo

difficulty: Media

time: 45 minutos

content:

Construye una escena con varios cubos distribuidos aleatoriamente.

Ejecuta el programa desarrollado durante este capítulo y observa cómo reacciona el Pioneer P3DX.

A continuación realiza las siguientes modificaciones:

- cambia la velocidad de avance;
- modifica el tiempo de giro;
- añade un pequeño retroceso antes del giro;
- prueba diferentes posiciones para los obstáculos.

Anota qué configuración consigue que el robot recorra una mayor distancia sin quedar bloqueado.

:::

---

::: challenge
title: Reto · Mejorando la navegación autónoma

difficulty: Alta

content:

Desarrolla una versión más avanzada del algoritmo incorporando alguna de las siguientes mejoras:

- alternar automáticamente el sentido del giro;
- seleccionar el giro de forma aleatoria;
- utilizar varios sensores frontales en lugar de uno solo;
- reducir la velocidad cuando el obstáculo se encuentre muy próximo.

Compara el comportamiento obtenido con el algoritmo original e identifica las ventajas e inconvenientes de cada estrategia.

:::

---

::: teacher
title: Orientaciones para el profesorado

content:

Este capítulo constituye un excelente punto de partida para introducir conceptos de Inteligencia Artificial y Robótica Autónoma.

Es recomendable dedicar parte de la sesión a que el alumnado proponga diferentes estrategias para evitar obstáculos antes de implementarlas.

La comparación entre algoritmos suele generar debates muy interesantes sobre eficiencia, robustez y comportamiento emergente.

También resulta aconsejable organizar una pequeña competición entre grupos para comprobar qué algoritmo consigue recorrer una escena con obstáculos durante más tiempo sin quedar bloqueado.

:::

---

# Resumen

En este capítulo hemos construido el primer robot autónomo del libro.

Hemos integrado los sensores de proximidad con el control de los motores para desarrollar un algoritmo capaz de reaccionar automáticamente ante los obstáculos presentes en la escena.

Aunque el comportamiento implementado es sencillo, reproduce el mismo principio utilizado por robots móviles reales: observar continuamente el entorno, interpretar la información obtenida y actuar en consecuencia.

También hemos aprendido la importancia del bucle de control, que permite repetir continuamente el ciclo percepción → decisión → acción mientras el robot permanece en funcionamiento.

Este modelo constituye la base sobre la que se desarrollan sistemas de navegación mucho más avanzados.

En los próximos capítulos ampliaremos este comportamiento incorporando nuevos sensores, estrategias de navegación más sofisticadas y técnicas de programación que permitirán construir robots cada vez más inteligentes.

---

::: chapter-end
next: "Capítulo 11 · Programación avanzada del Pioneer P3DX"
previous: "Capítulo 9 · Control del movimiento del Pioneer P3DX"
:::
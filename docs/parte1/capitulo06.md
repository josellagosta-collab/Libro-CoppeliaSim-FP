# Capítulo 6 · Primera conexión entre Python y CoppeliaSim

::: chapter-cover
number: 6
title: Primera conexión entre Python y CoppeliaSim
time: 4 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo se comunica Python con CoppeliaSim.
- Instalar la API remota basada en ZeroMQ.
- Crear un entorno virtual para el proyecto.
- Escribir tu primer programa en Python.
- Establecer la primera conexión con CoppeliaSim.
- Ejecutar un programa que interactúe con el simulador.

:::

## ¿Por qué utilizar Python?

Hasta ahora todas las acciones realizadas sobre el robot han sido manuales.

Sin embargo, un robot industrial no espera a que un operador pulse botones continuamente.

Los robots ejecutan programas.

Python será el lenguaje que utilizaremos para crear esos programas.

Su sintaxis sencilla, la enorme cantidad de bibliotecas disponibles y su amplia implantación en robótica lo convierten en una excelente elección tanto para el aprendizaje como para proyectos profesionales.

Además, CoppeliaSim incorpora una interfaz que permite controlar prácticamente cualquier elemento del simulador desde programas escritos en Python.

A partir de este capítulo comenzaremos a utilizar esa interfaz.

::: teacher
content:

Aunque algunos estudiantes no hayan programado nunca en Python, este capítulo puede seguirse sin dificultad.

Los ejemplos serán muy sencillos y se explicarán paso a paso.

:::

---

## 6.1 ¿Cómo se comunican Python y CoppeliaSim?

Python y CoppeliaSim son dos programas independientes.

Para que puedan intercambiar información necesitan un mecanismo de comunicación.

En este libro utilizaremos la **API remota basada en ZeroMQ (ZMQ Remote API)**.

Esta API permite:

- iniciar y detener simulaciones;
- leer sensores;
- mover robots;
- modificar objetos;
- acceder prácticamente a todas las funciones del simulador.

La comunicación se realiza mediante mensajes enviados entre Python y CoppeliaSim.

Podemos imaginarla como una conversación.

1. Python envía una petición.
2. CoppeliaSim la recibe.
3. Ejecuta la acción solicitada.
4. Devuelve el resultado a Python.

Este proceso ocurre en unas pocas milésimas de segundo.

::: figure
image: ../assets/cap06/python_coppeliasim_comunicacion.svg
caption: Comunicación entre Python y CoppeliaSim mediante la API remota ZeroMQ.
:::

---

## 6.2 Preparando el entorno de trabajo

Antes de escribir nuestro primer programa prepararemos un entorno de trabajo específico para Python.

Dentro de la carpeta principal del curso crea el siguiente directorio:

```text
CoppeliaSim-FP/

└── Python/

    ├── practica01/

    ├── practica02/

    └── practica03/
```

Cada práctica tendrá su propia carpeta.

Esto facilitará la organización del código conforme avancemos en el libro.

---

## 6.3 Creando un entorno virtual

Para evitar conflictos entre diferentes proyectos utilizaremos un entorno virtual de Python.

Abre un terminal en la carpeta del proyecto y ejecuta:

```bash
python -m venv .venv
```

Una vez creado el entorno virtual, actívalo.

En Windows:

```powershell
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Cuando el entorno esté activo, el terminal mostrará su nombre al principio de la línea de comandos.

A partir de ese momento todas las bibliotecas que instalemos quedarán aisladas dentro del proyecto.

::: common-error
content:

Si el entorno virtual no está activado, las bibliotecas se instalarán en la instalación global de Python.

Esto puede provocar conflictos entre distintos proyectos.

:::

## 6.4 Instalando la API remota de CoppeliaSim

La comunicación entre Python y CoppeliaSim se realiza mediante una biblioteca denominada **ZMQ Remote API Client**.

Esta biblioteca implementa el protocolo de comunicación necesario para que ambos programas puedan intercambiar información.

Con el entorno virtual activado, instala la biblioteca ejecutando el siguiente comando:

```bash
pip install coppeliasim-zmqremoteapi-client
```

Una vez finalizada la instalación, puedes comprobar que todo ha ido correctamente ejecutando:

```bash
pip show coppeliasim-zmqremoteapi-client
```

El terminal mostrará información similar a la siguiente:

```text
Name: coppeliasim-zmqremoteapi-client
Version: ...
Location: ...
```

Si aparece esta información, la biblioteca está correctamente instalada y lista para utilizarse.

::: teacher
content:

Antes de continuar, verifica que todos los alumnos han instalado correctamente la biblioteca.

Resolver este tipo de incidencias ahora evitará muchos problemas durante las prácticas posteriores.

:::

---

## 6.5 Creando nuestro primer programa

Vamos a crear nuestro primer programa en Python.

Dentro de la carpeta **practica01** crea un archivo llamado:

```text
conexion.py
```

Por el momento únicamente comprobaremos que Python puede establecer comunicación con CoppeliaSim.

Escribe el siguiente código:

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()

sim = client.require('sim')

print("Conexión establecida correctamente.")
```

Aunque el programa es muy corto, realiza varias operaciones importantes.

1. Importa la biblioteca de comunicación.
2. Crea un cliente que se conectará con CoppeliaSim.
3. Solicita acceso al módulo principal del simulador.
4. Muestra un mensaje indicando que la conexión se ha realizado correctamente.

En los próximos apartados analizaremos cada una de estas instrucciones con detalle.

---

## 6.6 Analizando el código

La primera línea importa la clase responsable de establecer la comunicación.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
```

La siguiente instrucción crea un cliente.

```python
client = RemoteAPIClient()
```

Este objeto será el encargado de enviar todas las peticiones al simulador.

Después solicitamos acceso al módulo principal de CoppeliaSim.

```python
sim = client.require('sim')
```

A partir de este momento podremos utilizar las funciones disponibles en la API.

Finalmente mostramos un mensaje informativo.

```python
print("Conexión establecida correctamente.")
```

Aunque todavía no estamos controlando ningún robot, ya disponemos de un canal de comunicación completamente funcional.

---

## 6.7 Ejecutando el programa

Antes de ejecutar el programa asegúrate de que CoppeliaSim está abierto.

No es necesario que exista ninguna escena cargada.

Abre un terminal dentro de la carpeta del proyecto y ejecuta:

```bash
python conexion.py
```

Si todo funciona correctamente, aparecerá el siguiente mensaje:

```text
Conexión establecida correctamente.
```

Este sencillo mensaje confirma que Python ha conseguido comunicarse con el simulador.

Es un paso muy importante, ya que a partir de ahora todas las órdenes que enviemos seguirán exactamente el mismo mecanismo.

::: common-error
content:

Si aparece un mensaje indicando que no es posible conectar con CoppeliaSim, comprueba que el simulador está abierto antes de ejecutar el programa.

También verifica que la biblioteca **coppeliasim-zmqremoteapi-client** está instalada en el entorno virtual activo.

:::

---

## 6.8 Nuestra primera llamada a la API

Una vez establecida la comunicación podemos solicitar información al simulador.

Por ejemplo, podemos obtener la versión de CoppeliaSim mediante el siguiente programa:

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

version = sim.getInt32Param(sim.intparam_program_version)

print(f"Versión de CoppeliaSim: {version}")
```

La función utilizada puede parecer compleja, pero no es necesario comprender todavía todos sus detalles.

Lo importante es observar que ya somos capaces de solicitar información al simulador y recibir una respuesta.

Este mecanismo será la base de todas las aplicaciones que desarrollaremos en los capítulos siguientes.

::: summary
title: Idea clave

content:

Una vez establecida la conexión, Python puede acceder a las funciones de CoppeliaSim como si fueran funciones propias.

La API remota actúa como un puente entre ambos programas.
:::

## 6.9 Controlando la simulación desde Python

Hasta este momento hemos utilizado los botones **Play**, **Pause** y **Stop** de la interfaz de CoppeliaSim.

Sin embargo, una de las principales ventajas de la API remota consiste en que estas mismas acciones pueden realizarse desde un programa en Python.

Esto permitirá automatizar completamente nuestras simulaciones.

Comenzaremos iniciando la simulación mediante código.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

print("Iniciando simulación...")

sim.startSimulation()

print("La simulación está en marcha.")
```

Ejecuta el programa con CoppeliaSim abierto.

Observa que el botón **Play** cambia automáticamente de estado y la simulación comienza exactamente igual que si hubieras pulsado el botón con el ratón.

Acabas de controlar CoppeliaSim desde Python por primera vez.

---

## 6.10 Deteniendo la simulación

Del mismo modo que podemos iniciarla, también podemos detenerla.

Añade las siguientes líneas al programa anterior:

```python
import time

time.sleep(5)

sim.stopSimulation()

print("Simulación detenida.")
```

El programa completo quedará así:

```python
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

print("Iniciando simulación...")

sim.startSimulation()

time.sleep(5)

sim.stopSimulation()

print("Simulación detenida.")
```

Al ejecutarlo observarás el siguiente comportamiento:

1. Python establece la conexión.
2. La simulación comienza automáticamente.
3. El programa espera cinco segundos.
4. La simulación se detiene.

Este ejemplo demuestra que Python puede controlar completamente el ciclo de ejecución de CoppeliaSim.

::: common-error
content:

Si ejecutas varias veces el programa de forma consecutiva, espera unos segundos entre una ejecución y la siguiente para asegurarte de que la simulación anterior se ha detenido completamente.

:::

---

## 6.11 Localizando un objeto de la escena

Hasta ahora hemos trabajado con la simulación en general.

El siguiente paso consiste en acceder a un objeto concreto.

Para ello utilizaremos su nombre.

Supongamos que en la escena existe un robot llamado:

```text
PioneerP3DX
```

Podemos obtener una referencia al robot mediante:

```python
robot = sim.getObject("/PioneerP3DX")
```

A partir de ese momento la variable **robot** contendrá un identificador interno que permitirá acceder a todas sus propiedades.

No se trata del robot en sí, sino de una referencia que CoppeliaSim utiliza para localizarlo dentro de la escena.

---

## 6.12 Comprobando que el objeto existe

Antes de modificar un objeto conviene asegurarse de que la referencia se ha obtenido correctamente.

Podemos comprobarlo mostrando su identificador:

```python
robot = sim.getObject("/PioneerP3DX")

print(robot)
```

La salida será un número entero similar al siguiente:

```text
37
```

Este valor puede variar entre diferentes escenas.

Lo importante es comprobar que Python ha localizado correctamente el robot.

Si el objeto no existe o su nombre no coincide exactamente con el utilizado en la escena, CoppeliaSim mostrará un mensaje de error.

::: teacher
content:

Insiste en la importancia de asignar nombres claros a los objetos.

Una nomenclatura coherente facilitará enormemente la programación y evitará errores difíciles de localizar.

:::

---

## 6.13 Nuestra primera interacción con un objeto

Aunque todavía no modificaremos ninguna propiedad, ya somos capaces de localizar objetos dentro de la escena.

Este sencillo paso supone un cambio muy importante.

Hasta ahora Python únicamente controlaba la simulación.

A partir de este momento comenzará a controlar también los elementos que forman parte de ella.

En los próximos capítulos aprenderemos a:

- leer la posición de un robot;
- modificar sus coordenadas;
- cambiar su orientación;
- acceder a sensores;
- controlar motores.

Todo ello utilizando exactamente el mismo mecanismo que acabamos de aprender.

::: summary
title: Idea clave

content:

La API remota trabaja siempre con referencias a objetos.

Antes de mover un robot, leer un sensor o modificar una cámara, es necesario obtener una referencia al objeto correspondiente mediante su nombre.
:::

## 6.14 Leyendo la posición de un robot

En el apartado anterior aprendimos a obtener una referencia a un objeto de la escena.

El siguiente paso consiste en consultar una de sus propiedades más importantes: **su posición**.

La API de CoppeliaSim proporciona una función específica para ello.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

robot = sim.getObject("/PioneerP3DX")

posicion = sim.getObjectPosition(robot, sim.handle_world)

print(posicion)
```

Si todo funciona correctamente, Python mostrará una lista similar a la siguiente:

```text
[0.0, 0.0, 0.138]
```

Los valores corresponden a las coordenadas del robot respecto al sistema de referencia global.

- El primer valor representa la coordenada **X**.
- El segundo valor representa la coordenada **Y**.
- El tercero representa la coordenada **Z**.

Cada escena puede devolver valores diferentes dependiendo de la posición del robot.

---

## 6.15 Interpretando las coordenadas

Supongamos que el programa devuelve el siguiente resultado:

```text
[1.20, -0.50, 0.138]
```

Esto significa que:

- el robot está situado a **1,20 metros** sobre el eje X;
- se encuentra a **0,50 metros** en sentido negativo del eje Y;
- su altura respecto al origen es **0,138 metros**.

En un robot móvil normalmente la coordenada Z apenas cambia, ya que permanece apoyado sobre el suelo.

Lo realmente importante serán las coordenadas X e Y.

::: figure
image: ../assets/cap06/coordenadas_robot.png
caption: Interpretación de la posición de un robot en el sistema de coordenadas global.
:::

---

## 6.16 Modificando la posición del robot

Además de consultar la posición de un objeto, también podemos modificarla.

El siguiente programa desplaza el robot un metro hacia el eje X.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

robot = sim.getObject("/PioneerP3DX")

sim.setObjectPosition(
    robot,
    sim.handle_world,
    [1.0, 0.0, 0.138]
)
```

Al ejecutar el programa observarás que el robot cambia inmediatamente de posición.

No ha sido necesario utilizar el ratón.

Toda la operación ha sido realizada mediante Python.

Este es uno de los aspectos más potentes de la API remota.

---

## 6.17 Desplazamientos relativos

Hasta ahora hemos asignado una posición concreta.

Sin embargo, en muchas ocasiones resulta más útil desplazar el robot respecto a su posición actual.

Podemos hacerlo leyendo primero las coordenadas y modificándolas después.

```python
posicion = sim.getObjectPosition(robot, sim.handle_world)

posicion[0] += 0.50

sim.setObjectPosition(
    robot,
    sim.handle_world,
    posicion
)
```

Este programa añade medio metro a la coordenada X.

Si se ejecuta varias veces, el robot avanzará medio metro en cada ejecución.

Este tipo de desplazamientos será muy habitual cuando comencemos a desarrollar algoritmos de navegación.

---

## 6.18 Leyendo la orientación

La orientación de un objeto también puede consultarse desde Python.

La función utilizada es muy similar a la empleada para obtener la posición.

```python
orientacion = sim.getObjectOrientation(
    robot,
    sim.handle_world
)

print(orientacion)
```

La salida será una lista formada por tres valores.

```text
[0.0, 0.0, 1.5708]
```

Estos valores representan la orientación del objeto respecto a los ejes X, Y y Z.

Observa que el tercer valor corresponde aproximadamente a **1,57 radianes**, es decir, **90 grados**.

En capítulos posteriores aprenderemos a trabajar tanto con radianes como con grados.

::: common-error
content:

La API de CoppeliaSim utiliza radianes para representar los ángulos.

Muchos errores aparecen al introducir grados directamente sin realizar la conversión correspondiente.

:::

---

## 6.19 Primera modificación completa

Combina ahora las funciones estudiadas en este capítulo para realizar una pequeña prueba.

1. Obtén la referencia al robot.
2. Lee su posición.
3. Muévelo un metro sobre el eje X.
4. Lee nuevamente la posición.
5. Muestra ambas posiciones por pantalla.

El resultado permitirá comprobar que Python ha modificado correctamente las coordenadas del robot.

Este sencillo ejercicio resume el funcionamiento básico de la API remota.

::: summary
title: Idea clave

content:

La comunicación entre Python y CoppeliaSim se basa en tres operaciones fundamentales:

- obtener una referencia al objeto;
- leer una propiedad;
- modificar esa propiedad.

La mayoría de los programas que desarrollaremos durante el resto del libro seguirán exactamente esta secuencia.
:::

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| API remota | Conjunto de funciones que permiten controlar CoppeliaSim desde un programa externo. |
| ZeroMQ (ZMQ) | Tecnología de comunicación utilizada por la API remota de CoppeliaSim. |
| Cliente | Objeto encargado de establecer la comunicación entre Python y CoppeliaSim. |
| Referencia | Identificador interno que permite acceder a un objeto de la escena. |
| Entorno virtual | Entorno aislado de Python utilizado para instalar bibliotecas específicas de un proyecto. |
| Posición | Coordenadas que indican la ubicación de un objeto en la escena. |
| Orientación | Ángulos que indican hacia dónde está orientado un objeto. |
| Sistema de referencia | Marco utilizado para expresar posiciones y orientaciones. |
| Radianes | Unidad utilizada por la API para representar los ángulos de rotación. |
| Propiedad | Característica de un objeto que puede consultarse o modificarse mediante programación. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender cómo se comunican Python y CoppeliaSim.
- ✅ Crear un entorno virtual para un proyecto.
- ✅ Instalar la API remota basada en ZeroMQ.
- ✅ Establecer una conexión con el simulador.
- ✅ Obtener referencias a los objetos de una escena.
- ✅ Leer la posición y la orientación de un robot.
- ✅ Modificar la posición de un objeto mediante Python.

A partir de este momento ya dispones de todos los conocimientos necesarios para comenzar a desarrollar programas que controlen robots virtuales.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué función desempeña la API remota de CoppeliaSim?
2. ¿Por qué utilizamos un entorno virtual en Python?
3. ¿Qué hace la instrucción `RemoteAPIClient()`?
4. ¿Qué devuelve la función `sim.getObject()`?
5. ¿Qué diferencia existe entre leer y modificar la posición de un objeto?
6. ¿Por qué la API utiliza radianes para representar los ángulos?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a programar el movimiento del robot.

---

## Práctica guiada

::: practice
title: Primera comunicación con CoppeliaSim

difficulty: Media

time: 50 minutos

content:

Realiza la siguiente práctica paso a paso.

1. Activa el entorno virtual del proyecto.
2. Comprueba que la biblioteca **coppeliasim-zmqremoteapi-client** está instalada.
3. Abre CoppeliaSim.
4. Ejecuta un programa que establezca la conexión con el simulador.
5. Obtén la referencia al robot Pioneer P3DX.
6. Muestra por pantalla su posición.
7. Desplaza el robot medio metro sobre el eje X.
8. Lee nuevamente la posición y verifica que el cambio se ha realizado correctamente.
9. Guarda el programa con el nombre **practica01.py**.

Al finalizar habrás controlado por primera vez un robot virtual mediante Python.
:::

---

## Reto

::: challenge
title: Explorando la escena mediante programación

content:

Modifica el programa desarrollado en este capítulo para realizar las siguientes acciones:

- Mostrar la posición inicial del robot.
- Desplazarlo un metro sobre el eje Y.
- Mostrar la nueva posición.
- Devolverlo posteriormente a su posición original.

¿Serías capaz de realizar todo el proceso utilizando una única variable para almacenar las coordenadas?

Este reto te ayudará a comprender cómo manipular listas y cómo reutilizar la información obtenida desde la API.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Configurar correctamente el entorno de programación.
- Verificar la comunicación entre Python y CoppeliaSim.
- Introducir el uso de la API remota.
- Leer y modificar propiedades básicas de un robot.

**Material necesario**

- Ordenadores con Python instalado.
- Entorno virtual configurado.
- Biblioteca `coppeliasim-zmqremoteapi-client`.
- CoppeliaSim EDU 4.10 en ejecución.

**Sugerencias metodológicas**

Dedica tiempo a comprobar que todos los estudiantes consiguen establecer la conexión antes de avanzar.

Una vez superado este punto, la mayoría de los ejemplos posteriores funcionarán sin modificaciones importantes.

Anima al alumnado a experimentar modificando las coordenadas del robot y observando el resultado directamente en la simulación.
:::

---

## Próximo capítulo

Hasta ahora hemos aprendido a comunicarnos con CoppeliaSim y a consultar las propiedades de un robot.

En el siguiente capítulo comenzaremos a programar sus primeros movimientos.

Aprenderás a desplazar el robot mediante Python, crear pequeñas trayectorias y comprender cómo transformar una secuencia de instrucciones en un comportamiento observable dentro de la simulación.

Será el primer capítulo en el que desarrollarás una aplicación completa de control robótico utilizando Python.
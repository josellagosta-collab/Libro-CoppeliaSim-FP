::: chapter-cover
number: 9
title: Control del movimiento del Pioneer P3DX
time: 5 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo

content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo se desplaza un robot móvil con tracción diferencial.
- Identificar los motores que controlan el movimiento del Pioneer P3DX.
- Controlar la velocidad de las ruedas mediante Python.
- Desplazar el robot hacia delante, hacia atrás y detenerlo.
- Realizar giros sobre su propio eje.
- Comprender la relación entre la velocidad de las ruedas y la trayectoria del robot.
:::

# Capítulo 9 · Control del movimiento del Pioneer P3DX

### De percibir el entorno a comenzar a moverse

En el capítulo anterior aprendimos a utilizar los sensores de proximidad del Pioneer P3DX para detectar obstáculos.

Nuestro programa ya era capaz de obtener información del entorno e interpretar si existía o no un objeto delante del robot.

Sin embargo, detectar un obstáculo no sirve de mucho si el robot no puede reaccionar ante esa información.

Ha llegado el momento de dar un paso más.

En este capítulo aprenderemos a controlar el movimiento del Pioneer P3DX utilizando sus motores.

Dejaremos de modificar directamente la posición del robot dentro de la simulación y comenzaremos a utilizar el mismo sistema de control que emplearía un robot real.

A partir de ahora los desplazamientos serán consecuencia del giro de sus ruedas.

Este cambio supone una diferencia muy importante.

Cuando un robot se mueve mediante sus motores, aparecen conceptos como la velocidad, la aceleración, el radio de giro o la trayectoria recorrida.

Estos conceptos son fundamentales para comprender el funcionamiento de cualquier robot móvil.

Al finalizar el capítulo serás capaz de controlar completamente el movimiento del Pioneer P3DX desde Python.

En el siguiente capítulo utilizaremos ese movimiento junto con los sensores para desarrollar nuestro primer algoritmo de navegación autónoma.

::: teacher
title: Consejo para el profesor

content:

Antes de comenzar la programación, pregunta al alumnado cómo creen que gira un robot móvil.

Muchos responderán que dispone de un volante, como un automóvil.

Esta actividad resulta muy útil para introducir el concepto de **tracción diferencial**, que constituye la base del movimiento del Pioneer P3DX.
:::

---

## 9.1 ¿Cómo se mueve un robot móvil?

Cuando observamos un robot desplazándose por una sala resulta fácil pensar que simplemente "avanza" o "gira".

Sin embargo, detrás de esos movimientos existe un mecanismo muy sencillo y al mismo tiempo extremadamente eficaz.

El Pioneer P3DX pertenece a la familia de los robots de **tracción diferencial**.

Esto significa que su movimiento depende exclusivamente de la velocidad de giro de sus dos ruedas motrices.

No necesita un volante para cambiar de dirección.

Tampoco utiliza un mecanismo de dirección como el de un automóvil.

Toda su maniobrabilidad se consigue controlando de forma independiente la velocidad de la rueda izquierda y la rueda derecha.

Esta solución mecánica presenta numerosas ventajas.

Es sencilla, robusta y permite realizar giros muy precisos incluso en espacios reducidos.

Por este motivo es uno de los sistemas de locomoción más utilizados en robots móviles educativos, industriales y de investigación.

::: info
title: Tracción diferencial

content:

En un robot de tracción diferencial cada rueda motriz dispone de su propio motor.

Modificando la velocidad de cada una de ellas es posible avanzar, retroceder, girar o describir trayectorias curvas sin necesidad de utilizar ningún sistema de dirección adicional.
:::

---

### Los tres elementos fundamentales

Aunque el Pioneer P3DX incorpora numerosos sensores y componentes electrónicos, su desplazamiento depende únicamente de tres elementos mecánicos.

- Una rueda motriz izquierda.
- Una rueda motriz derecha.
- Una rueda de apoyo libre situada en la parte posterior.

Las dos ruedas motrices son las responsables de impulsar el robot.

La rueda de apoyo únicamente mantiene la estabilidad del conjunto y permite que el robot se desplace con suavidad.

No interviene en la propulsión ni en el cambio de dirección.

---

### Movimiento rectilíneo

Cuando ambas ruedas giran exactamente a la misma velocidad y en el mismo sentido, el Pioneer P3DX se desplaza en línea recta.

Si ambas giran hacia delante, el robot avanza.

Si ambas giran hacia atrás, el robot retrocede.

En ambos casos la trayectoria será prácticamente rectilínea.

Este será el primer movimiento que aprenderemos a programar.

---

### Cambiando de dirección

La situación cambia cuando las ruedas giran a velocidades diferentes.

Si una rueda gira más deprisa que la otra, el robot comenzará a describir una curva.

Cuanto mayor sea la diferencia entre ambas velocidades, más cerrado será el giro.

En el caso extremo, cuando una rueda gira hacia delante y la otra hacia atrás con la misma velocidad, el Pioneer P3DX gira prácticamente sobre su propio eje.

Este comportamiento constituye una de las principales ventajas de la tracción diferencial.

Permite realizar maniobras muy precisas incluso en espacios reducidos.

::: summary
title: Idea clave

content:

El Pioneer P3DX no utiliza ningún sistema de dirección como el de un automóvil.

Todos sus movimientos se consiguen controlando de forma independiente la velocidad de las dos ruedas motrices.

Comprender este principio resulta esencial para programar correctamente cualquier robot móvil de tracción diferencial.
:::

::: figure
image: ../assets/cap09/png/traccion_diferencial_pioneer.png
caption: Esquema del sistema de tracción diferencial del robot Pioneer P3DX."
:::

Para interpretar correctamente los movimientos del robot es útil identificar su sistema de referencia: el eje delantero, el eje lateral y el sentido positivo de giro.

::: figure
image: ../assets/cap09/png/marcos_referencia_pioneer.png
caption: Marcos de referencia del robot Pioneer P3DX utilizados para interpretar su movimiento."
:::

---

## 9.2 Los motores del Pioneer P3DX

En el apartado anterior hemos visto que el movimiento del Pioneer P3DX depende exclusivamente de sus dos ruedas motrices.

Ahora vamos a conocer los elementos responsables de hacerlas girar.

Cada una de las ruedas está unida a un motor independiente.

Esto significa que podemos controlar la velocidad de la rueda izquierda y la rueda derecha por separado.

Gracias a ello el robot puede desplazarse en línea recta, describir curvas o girar sobre su propio eje sin necesidad de ningún mecanismo de dirección.

En CoppeliaSim estos motores ya forman parte del modelo del Pioneer P3DX.

No es necesario añadirlos ni configurarlos.

Únicamente tendremos que obtener una referencia a cada uno de ellos desde Python para poder enviarles órdenes de movimiento.

---

### Los dos motores principales

Si desplegamos el Pioneer P3DX en el árbol de la escena encontraremos dos articulaciones que controlan el movimiento del robot.

Habitualmente aparecen con los nombres:

- `leftMotor`
- `rightMotor`

Estos dos objetos representan los motores que accionan las ruedas izquierda y derecha, respectivamente.

Desde el punto de vista de CoppeliaSim, ambos motores son articulaciones (*joints*) cuya velocidad puede controlarse mediante la API remota.

::: info
title: Motores y articulaciones

content:

En CoppeliaSim los motores de un robot suelen representarse mediante articulaciones (*joints*).

Aunque físicamente hablamos de motores, desde Python interactuaremos con ellos utilizando las funciones destinadas al control de articulaciones.

:::

---

### Una rueda, un motor

Cada motor actúa únicamente sobre una de las ruedas motrices.

No existe ningún mecanismo que sincronice automáticamente ambas ruedas.

Será nuestro programa quien decida en cada instante la velocidad de cada motor.

Esta filosofía proporciona una gran flexibilidad.

Podremos hacer que ambas ruedas giren a la misma velocidad o asignar velocidades completamente diferentes para obtener distintos tipos de movimiento.

Más adelante veremos que este principio también se utiliza en numerosos robots móviles reales.

---

### El árbol de la escena

Si observamos el árbol de la escena del Pioneer P3DX veremos que los motores forman parte de la jerarquía del robot.

Esto resulta muy útil porque podremos acceder a ellos igual que hicimos con los sensores.

Bastará con obtener una referencia mediante la función `getObject()`.

No es necesario memorizar todavía el nombre exacto de cada motor.

En el siguiente apartado aprenderemos a obtener su referencia desde Python.

::: figure
image: ../assets/cap09/png/escena_pioneer_p3dx.png
caption: "Escena básica del Pioneer P3DX en CoppeliaSim mostrando la jerarquía de objetos del robot."
:::

::: teacher
title: Consejo para el profesor

content:

Antes de comenzar a programar los motores, pide al alumnado que localice `leftMotor` y `rightMotor` dentro del árbol de la escena.

Esta sencilla actividad ayuda a comprender que un robot no es un único objeto, sino un conjunto jerárquico de componentes que pueden controlarse de manera independiente.

:::

---

### ¿Qué controla realmente un motor?

Cuando enviamos una orden a un motor no estamos indicando una posición concreta del robot.

Lo que realmente hacemos es establecer la velocidad de giro de una rueda.

Será el simulador quien calcule automáticamente el desplazamiento resultante teniendo en cuenta la dinámica del robot.

Este enfoque reproduce el comportamiento de un robot físico.

En un robot real no ordenamos que avance exactamente un metro modificando su posición.

Lo que hacemos es controlar los motores durante un determinado tiempo.

El movimiento aparece como consecuencia del giro de las ruedas.

Este mismo principio será el que utilizaremos a partir de ahora.

::: summary
title: Idea clave

content:

El Pioneer P3DX dispone de dos motores independientes, uno para cada rueda motriz.

Controlando la velocidad de ambos motores podremos generar todos los movimientos del robot.

En CoppeliaSim estos motores se representan como articulaciones (*joints*) y se controlan mediante la API remota.

:::

::: figure
image: ../assets/cap09/png/jerarquia_objetos_pioneer.png
caption: "Jerarquía de objetos del Pioneer P3DX en CoppeliaSim y componentes principales."
:::

---

## 9.3 Controlando la velocidad de los motores desde Python

Ya conocemos los dos motores responsables del movimiento del Pioneer P3DX.

Ha llegado el momento de aprender a controlarlos desde Python.

El procedimiento será muy similar al utilizado para acceder a los sensores.

Primero obtendremos una referencia a cada motor.

Después utilizaremos la API remota para establecer su velocidad de giro.

A partir de ese momento el robot comenzará a desplazarse de forma completamente realista dentro de la simulación.

---

### Obteniendo la referencia de los motores

Como cualquier otro objeto de la escena, los motores pueden obtenerse mediante la función `getObject()`.

Necesitaremos una referencia para la rueda izquierda y otra para la rueda derecha.

```python
motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")
```

A partir de este momento podremos enviar órdenes de movimiento a cada uno de ellos de forma independiente.

::: info
title: Comprueba el nombre de los motores

content:

Aunque los modelos oficiales del Pioneer P3DX utilizan habitualmente los nombres `leftMotor` y `rightMotor`, siempre es recomendable comprobar el nombre exacto en el árbol de la escena.

En caso de duda, despliega el modelo del robot y verifica cómo aparecen identificados los motores en tu versión de CoppeliaSim.
:::

::: figure
image: ../assets/cap09/png/control_motores_python.png
caption: "Esquema del flujo de control de los motores del Pioneer P3DX desde Python."
:::

---

### La función `setJointTargetVelocity()`

La API remota proporciona la función `setJointTargetVelocity()` para establecer la velocidad objetivo de una articulación.

Su sintaxis es muy sencilla.

```python
sim.setJointTargetVelocity(motor_izquierdo, velocidad)
```

El primer parámetro indica qué motor queremos controlar.

El segundo especifica la velocidad angular deseada.

Esta velocidad se expresa en **radianes por segundo (rad/s)**.

---

### Velocidad positiva y velocidad negativa

El signo de la velocidad determina el sentido de giro.

- Un valor positivo hace girar la rueda hacia delante.
- Un valor negativo invierte el sentido de giro.
- El valor cero detiene completamente el motor.

Por ejemplo:

```python
sim.setJointTargetVelocity(motor_izquierdo, 2.0)
```

hará que la rueda izquierda comience a girar hacia delante.

En cambio:

```python
sim.setJointTargetVelocity(motor_izquierdo, -2.0)
```

producirá el giro en sentido contrario.

---

### Controlando ambos motores

Lo habitual será enviar órdenes a los dos motores al mismo tiempo.

Por ejemplo:

```python
sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)
```

En este caso ambas ruedas giran a la misma velocidad.

Como consecuencia, el Pioneer P3DX avanzará en línea recta.

Más adelante modificaremos la velocidad de cada rueda para obtener otros tipos de movimiento.

::: teacher
title: Consejo para el profesor

content:

Antes de explicar trayectorias complejas, permite que el alumnado experimente modificando únicamente el valor de la velocidad.

Observar cómo cambia el comportamiento del robot ayuda a comprender rápidamente la relación entre la programación y el movimiento físico.
:::

---

### Unidades utilizadas

Es importante recordar que la función `setJointTargetVelocity()` no utiliza kilómetros por hora ni metros por segundo.

La velocidad se expresa en **radianes por segundo**, ya que controla directamente la velocidad de giro de cada motor.

No es necesario conocer todavía la relación exacta entre esta velocidad angular y la velocidad lineal del robot.

Durante las primeras prácticas bastará con experimentar utilizando valores sencillos como:

- `1.0`
- `2.0`
- `3.0`

Con la experiencia aprenderemos qué velocidad resulta más adecuada para cada aplicación.

::: common-error
title: El robot no se mueve

content:

Si los motores reciben una velocidad distinta de cero y el robot permanece inmóvil, comprueba los siguientes puntos:

- La simulación está en ejecución.
- Has obtenido correctamente la referencia de ambos motores.
- Los nombres `leftMotor` y `rightMotor` coinciden con los de tu escena.
- No existe ningún script que esté controlando simultáneamente los motores.

En caso de duda, verifica los nombres directamente en el árbol de la escena.
:::

---

### Preparando el primer movimiento

Ya sabemos cómo controlar la velocidad de cada rueda.

En el siguiente apartado utilizaremos estos conocimientos para realizar los primeros movimientos del Pioneer P3DX.

Comenzaremos con el caso más sencillo: avanzar, detenerse y retroceder.

A partir de ahí construiremos movimientos cada vez más complejos.

::: summary
title: Idea clave

content:

La función `setJointTargetVelocity()` permite controlar la velocidad de giro de cada rueda del Pioneer P3DX.

Combinando la velocidad del motor izquierdo y del derecho podremos generar cualquier movimiento del robot.

:::

---

## 9.4 Primer movimiento del robot

Ya hemos comprobado que Python puede localizar los motores del Pioneer P3DX y enviarles órdenes de velocidad.

Ahora vamos a construir nuestro primer programa completo de movimiento.

El objetivo será muy sencillo:

1. iniciar la simulación;
2. hacer avanzar el robot durante unos segundos;
3. detenerlo;
4. finalizar la simulación.

Aunque el programa es breve, representa un paso muy importante.

A partir de este momento ya no estamos modificando directamente la posición del robot.

Estamos controlando sus motores.

---

### Programa completo

Crea un archivo llamado:

```text
movimiento_prueba.py
```

Escribe el siguiente código:

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

print("Inicio del programa")

client = RemoteAPIClient()
sim = client.require("sim")

print("Conectado con CoppeliaSim")

motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")
motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")

print("Motores localizados")

sim.startSimulation()
time.sleep(1)

velocidad = 2.0

print("Avanzando...")

sim.setJointTargetVelocity(motor_izquierdo, velocidad)
sim.setJointTargetVelocity(motor_derecho, velocidad)

time.sleep(3)

print("Deteniendo...")

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(1)

sim.stopSimulation()

print("Prueba finalizada")
```

---

### ¿Qué hace el programa?

El programa comienza estableciendo la conexión con CoppeliaSim.

Después obtiene la referencia de los dos motores principales del Pioneer P3DX.

```python
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")
motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
```

A continuación inicia la simulación desde Python.

```python
sim.startSimulation()
```

Esto significa que no es necesario pulsar manualmente el botón **Play**.

Es el propio programa quien pone en marcha la simulación.

---

### Avanzar

Para que el robot avance basta con enviar la misma velocidad a ambos motores.

```python
velocidad = 2.0

sim.setJointTargetVelocity(motor_izquierdo, velocidad)
sim.setJointTargetVelocity(motor_derecho, velocidad)
```

Como las dos ruedas giran a la misma velocidad y en el mismo sentido, el Pioneer P3DX se desplaza en línea recta.

El valor `2.0` representa una velocidad angular expresada en **radianes por segundo (rad/s)**.

No indica la velocidad lineal del robot, sino la velocidad de giro de cada motor.

---

### Mantener el movimiento

La instrucción:

```python
time.sleep(3)
```

hace que el programa espere tres segundos antes de continuar.

Durante ese tiempo los motores mantienen la velocidad establecida y el robot sigue avanzando.

Si aumentas este tiempo, recorrerá una mayor distancia.

Si lo reduces, el recorrido será más corto.

---

### Detener el robot

Para detener el Pioneer P3DX basta con establecer la velocidad de ambos motores a cero.

```python
sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)
```

Es importante distinguir entre detener el robot y detener la simulación.

Las instrucciones anteriores únicamente paran el movimiento del Pioneer.

La simulación continúa ejecutándose hasta que llamamos a:

```python
sim.stopSimulation()
```

---

::: common-error
title: El robot se mueve solo al iniciar la simulación

content:

Algunos modelos del Pioneer P3DX incorporan scripts internos que controlan automáticamente los motores.

Si el robot comienza a desplazarse nada más iniciar la simulación, desactiva ese script o trabaja sobre una copia del modelo preparada para control externo.

Para todas las prácticas de este libro el Pioneer P3DX debe permanecer completamente inmóvil hasta que Python envíe las órdenes de movimiento.

:::

---

### Comprobando el resultado

Ejecuta el programa desde la terminal:

```powershell
python movimiento_prueba.py
```

La salida debería ser similar a la siguiente:

```text
Inicio del programa
Conectado con CoppeliaSim
Motores localizados
Avanzando...
Deteniendo...
Prueba finalizada
```

En CoppeliaSim observarás que el Pioneer P3DX avanza durante tres segundos, se detiene y finalmente la simulación finaliza automáticamente.

Si el robot se desplaza hacia atrás en lugar de hacia delante, basta con invertir el signo de la velocidad.

```python
velocidad = -2.0
```

El sentido positivo o negativo puede variar ligeramente dependiendo de la configuración del modelo utilizado.

::: summary
title: Idea clave

content:

Para mover el Pioneer P3DX no modificamos directamente su posición.

Controlamos la velocidad de sus motores mediante `setJointTargetVelocity()` y dejamos que el motor físico de CoppeliaSim calcule el movimiento resultante.

:::

---

## 9.5 Girando sobre su propio eje

En el apartado anterior hemos visto que el Pioneer P3DX avanza cuando las dos ruedas giran a la misma velocidad y en el mismo sentido.

Ahora vamos a modificar esa situación.

¿Qué ocurre si una rueda gira más deprisa que la otra?

¿Y si una gira hacia delante mientras la otra gira hacia atrás?

La respuesta es sencilla: el robot cambia de dirección.

Gracias a la tracción diferencial podemos controlar completamente la trayectoria del Pioneer P3DX modificando únicamente la velocidad de cada rueda.

---

### Girar hacia la izquierda

El primer experimento consiste en hacer que la rueda derecha gire más deprisa que la izquierda.

```python
sim.setJointTargetVelocity(motor_izquierdo, 1.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)
```

Como la rueda derecha recorre más distancia durante el mismo intervalo de tiempo, el robot comienza a describir una curva hacia la izquierda.

Cuanto mayor sea la diferencia entre ambas velocidades, más cerrada será la trayectoria.

---

### Girar hacia la derecha

El efecto contrario se consigue aumentando la velocidad de la rueda izquierda.

```python
sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 1.0)
```

Ahora será la rueda izquierda la que avance más rápidamente y el Pioneer describirá una curva hacia la derecha.

Observa que no hemos añadido ningún mecanismo de dirección.

Todo el cambio de trayectoria se produce únicamente variando la velocidad de las ruedas.

::: info
title: Curvas suaves

content:

No es necesario detener una rueda para cambiar de dirección.

En la mayoría de aplicaciones ambos motores permanecen en movimiento.

La trayectoria dependerá únicamente de la diferencia de velocidad entre ellos.

:::

---

### Girar sobre el propio eje

Existe un caso especialmente interesante.

Si una rueda gira hacia delante y la otra exactamente a la misma velocidad pero en sentido contrario, el Pioneer P3DX gira prácticamente sobre sí mismo.

```python
sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)
```

El robot apenas avanza.

En lugar de desplazarse, rota alrededor de su centro.

Este movimiento resulta muy útil cuando el robot necesita cambiar rápidamente de orientación antes de continuar avanzando.

---

### Programa de ejemplo

El siguiente programa realiza una rotación sobre el propio eje durante tres segundos.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

sim.startSimulation()

time.sleep(1)

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)

time.sleep(3)

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(1)

sim.stopSimulation()
```

Ejecuta el programa y observa cómo el robot gira sobre sí mismo sin desplazarse apenas.

---

### Experimenta

Modifica los valores de velocidad y observa cómo cambia la trayectoria.

Prueba, por ejemplo, las siguientes combinaciones.

| Motor izquierdo | Motor derecho | Resultado esperado |
|----------------:|--------------:|--------------------|
| 2.0 | 2.0 | Avanza en línea recta |
| 2.0 | 1.0 | Curva hacia la derecha |
| 1.0 | 2.0 | Curva hacia la izquierda |
| 2.0 | -2.0 | Giro sobre el propio eje |
| -2.0 | -2.0 | Retrocede en línea recta |

::: figure
image: ../assets/cap09/png/movimientos_pioneer_velocidad_ruedas.png
caption: "Movimientos del Pioneer P3DX en función de la velocidad de las ruedas motrices."
:::

Dedica unos minutos a experimentar.

Comprender la relación entre la velocidad de las ruedas y la trayectoria es mucho más sencillo cuando se observa directamente en la simulación.

::: practice
title: Práctica guiada · Explorando el movimiento diferencial

difficulty: Baja

time: 20 minutos

content:

Realiza las cinco combinaciones de velocidades propuestas en la tabla anterior.

En cada caso:

- ejecuta el programa;
- observa la trayectoria seguida por el robot;
- anota el comportamiento obtenido;
- intenta predecir el resultado antes de ejecutar cada prueba.

Al finalizar deberías ser capaz de anticipar el movimiento del Pioneer P3DX únicamente observando la velocidad asignada a cada rueda.

:::

::: summary
title: Idea clave

content:

En un robot con tracción diferencial la trayectoria depende exclusivamente de la velocidad relativa de las dos ruedas motrices.

No existe ningún volante ni mecanismo de dirección.

Controlando de forma independiente ambos motores es posible generar cualquier movimiento del robot.

:::

---

## 9.6 Combinando movimientos

Hasta ahora hemos aprendido a realizar movimientos básicos de forma independiente.

Hemos visto cómo avanzar, retroceder y girar modificando la velocidad de las ruedas.

Sin embargo, un robot raramente ejecuta un único movimiento.

Lo habitual es combinar varios desplazamientos consecutivos para recorrer una trayectoria determinada.

En este apartado construiremos nuestro primer programa completo de movimiento.

El Pioneer P3DX realizará la siguiente secuencia:

1. Iniciar la simulación.
2. Avanzar.
3. Girar a la izquierda.
4. Avanzar nuevamente.
5. Girar a la derecha.
6. Retroceder.
7. Girar sobre su propio eje.
8. Detenerse.
9. Finalizar la simulación.

Aunque la trayectoria es muy sencilla, representa el primer programa capaz de controlar completamente el movimiento del robot.

---

### Programa completo

Guarda el siguiente código como:

```text
recorrido_programado.py
```

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

# ----------------------------------------
# Conexión con CoppeliaSim
# ----------------------------------------

client = RemoteAPIClient()
sim = client.require("sim")

motor_izquierdo = sim.getObject("/PioneerP3DX/leftMotor")
motor_derecho = sim.getObject("/PioneerP3DX/rightMotor")

# ----------------------------------------
# Inicio de la simulación
# ----------------------------------------

sim.startSimulation()

time.sleep(1)

print("1. Avanzando")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)

time.sleep(3)

print("2. Girando a la izquierda")

sim.setJointTargetVelocity(motor_izquierdo, 1.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)

time.sleep(2)

print("3. Avanzando")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 2.0)

time.sleep(3)

print("4. Girando a la derecha")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, 1.0)

time.sleep(2)

print("5. Retrocediendo")

sim.setJointTargetVelocity(motor_izquierdo, -2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)

time.sleep(3)

print("6. Girando sobre el eje")

sim.setJointTargetVelocity(motor_izquierdo, 2.0)
sim.setJointTargetVelocity(motor_derecho, -2.0)

time.sleep(3)

print("7. Deteniendo el robot")

sim.setJointTargetVelocity(motor_izquierdo, 0)
sim.setJointTargetVelocity(motor_derecho, 0)

time.sleep(1)

sim.stopSimulation()

print("Programa finalizado")
```

---

### Analizando el programa

Observa que el programa no contiene ninguna instrucción complicada.

Todo el comportamiento del robot se consigue combinando únicamente dos funciones:

```python
sim.setJointTargetVelocity()
```

y

```python
time.sleep()
```

La primera establece la velocidad de cada rueda.

La segunda mantiene ese movimiento durante un determinado intervalo de tiempo.

Cada tramo del recorrido no es más que una combinación distinta de velocidades aplicada durante unos segundos.

::: figure
image: ../assets/cap09/png/recorrido_programado.png
caption: "Ejecución del programa `recorrido_programado.py`: secuencia de movimientos y trayectoria resultante del Pioneer P3DX."
:::

---

### La importancia de las velocidades

Fíjate en que nunca indicamos al robot una posición concreta.

En ningún momento aparece una instrucción como:

```python
ir_a(2.5, 1.8)
```

En robótica móvil esto no suele hacerse así.

El robot se desplaza porque sus ruedas giran.

La posición es una consecuencia del movimiento, no una orden directa.

Este modo de trabajar reproduce fielmente el funcionamiento de un robot físico.

---

::: info
title: ¿Por qué utilizamos time.sleep()?

content:

En este capítulo utilizamos `time.sleep()` para mantener cada movimiento durante un tiempo determinado.

Es una forma sencilla de comprender cómo responde el robot a las órdenes enviadas desde Python.

En aplicaciones reales suele utilizarse un control basado en sensores o en temporizadores internos, evitando detener completamente la ejecución del programa.

En el próximo capítulo sustituiremos estas esperas por decisiones tomadas a partir de la información proporcionada por los sensores
:::

---

### Experimenta

Ahora es tu turno.

Intenta modificar el programa realizando algunos cambios sencillos.

Por ejemplo:

- aumenta la velocidad de avance;
- reduce el tiempo de cada movimiento;
- realiza dos giros consecutivos;
- elimina el retroceso;
- añade un nuevo tramo rectilíneo.

Observa cómo pequeños cambios producen trayectorias completamente diferentes.

Esta es una de las grandes ventajas de la simulación: puedes experimentar tantas veces como quieras sin riesgo para el robot.

::: figure
image: ../assets/cap09/png/experimento_velocidades_pioneer.png
caption: "Experimentos propuestos para observar el efecto de diferentes velocidades de las ruedas sobre el movimiento del Pioneer P3DX."
:::

---

::: practice
title: Práctica guiada · Diseñando tu propio recorrido

difficulty: Media

time: 30 minutos

content:

Modifica el programa anterior para que el Pioneer P3DX describa una trayectoria con forma de cuadrado.

Para conseguirlo deberás combinar movimientos rectilíneos y giros de noventa grados.

No importa que las dimensiones no sean exactas.

El objetivo consiste en comprender cómo influye la velocidad de cada rueda en la trayectoria seguida por el robot.
:::

---

::: challenge
title: Reto

difficulty: Media

content:

Diseña un programa capaz de escribir la inicial de tu nombre utilizando únicamente movimientos rectilíneos y giros.

Antes de comenzar a programar, dibuja sobre un papel la trayectoria que deberá seguir el Pioneer P3DX.

Después intenta reproducirla en CoppeliaSim modificando únicamente las velocidades de los motores y la duración de cada movimiento.
:::

---

::: summary
title: Idea clave

content:

Todos los movimientos del Pioneer P3DX pueden construirse combinando diferentes velocidades para la rueda izquierda y la rueda derecha.

Esta forma de controlar el robot constituye la base de la navegación de cualquier plataforma con tracción diferencial y será el punto de partida del próximo capítulo, donde el movimiento dejará de estar predefinido para responder automáticamente a la información proporcionada por los sensores.
:::

---

# Conceptos clave

Al finalizar este capítulo deberías ser capaz de recordar las siguientes ideas.

- El Pioneer P3DX utiliza un sistema de **tracción diferencial**.
- Cada rueda motriz dispone de un motor independiente.
- Los motores aparecen en el árbol de la escena como `leftMotor` y `rightMotor`.
- La función `getObject()` permite obtener una referencia a cada motor.
- La función `setJointTargetVelocity()` establece la velocidad angular de una rueda.
- Una velocidad positiva hace girar la rueda hacia delante.
- Una velocidad negativa invierte el sentido de giro.
- Cuando ambas ruedas giran a la misma velocidad, el robot se desplaza en línea recta.
- Si las ruedas giran a velocidades diferentes, el robot describe una trayectoria curva.
- Si las ruedas giran en sentidos opuestos, el Pioneer P3DX gira prácticamente sobre su propio eje.
- El movimiento del robot es consecuencia del giro de sus ruedas y no de modificar directamente su posición.

---

# Autoevaluación

Responde a las siguientes preguntas antes de continuar con el siguiente capítulo.

1. ¿Qué significa que un robot tenga tracción diferencial?

2. ¿Qué función de la API remota permite modificar la velocidad de un motor?

3. ¿Qué ocurre cuando ambas ruedas giran exactamente a la misma velocidad?

4. ¿Cómo conseguirías que el Pioneer P3DX describiera una curva hacia la izquierda?

5. ¿Qué combinación de velocidades permite que el robot gire sobre su propio eje?

6. ¿Qué diferencia existe entre detener los motores y detener la simulación?

7. ¿Por qué la velocidad de los motores se expresa en radianes por segundo?

---

::: practice
title: Práctica guiada · Dibujando un recorrido

difficulty: Media

time: 40 minutos

content:

Diseña un programa capaz de realizar el siguiente recorrido:

1. Avanza durante tres segundos.
2. Gira noventa grados a la izquierda.
3. Avanza dos segundos.
4. Gira noventa grados a la derecha.
5. Retrocede tres segundos.
6. Detente.

Una vez conseguido, modifica las velocidades y los tiempos para obtener una trayectoria diferente.

Intenta predecir el recorrido antes de ejecutar el programa y comprueba después si coincide con el resultado obtenido.
:::

---

::: challenge
title: Reto · Recorriendo un circuito

difficulty: Alta

content:

Diseña un pequeño circuito utilizando varios cubos como obstáculos.

Programa el Pioneer P3DX para recorrer dicho circuito utilizando únicamente movimientos temporizados.

No utilices todavía sensores.

El objetivo consiste en comprobar hasta qué punto es posible controlar la trayectoria del robot actuando únicamente sobre la velocidad de las ruedas.

Compara posteriormente la trayectoria obtenida con la trayectoria prevista e identifica las posibles diferencias.
:::

---

::: teacher
title: Orientaciones para el profesorado

content:

Antes de comenzar el siguiente capítulo es recomendable que el alumnado experimente libremente con distintas combinaciones de velocidades.

No es necesario que memoricen valores concretos.

Lo importante es que comprendan la relación existente entre la velocidad de cada rueda y la trayectoria seguida por el robot.

Una buena actividad consiste en pedir a cada grupo que diseñe un pequeño recorrido y que el resto de compañeros intente reproducirlo únicamente observando el programa.

Este tipo de ejercicios favorece el razonamiento espacial y ayuda a consolidar el concepto de tracción diferencial.
:::

---

# Resumen

En este capítulo hemos aprendido a controlar el movimiento del Pioneer P3DX utilizando Python y la API remota de CoppeliaSim.

Hemos comprobado que el robot dispone de dos motores independientes y que modificando la velocidad de cada uno de ellos podemos generar cualquier tipo de trayectoria.

También hemos construido nuestro primer programa completo de movimiento y hemos experimentado con desplazamientos rectilíneos, curvas, giros sobre el propio eje y recorridos compuestos.

Estos conocimientos constituyen la base de la programación de robots móviles.

Sin embargo, los movimientos que hemos realizado hasta ahora estaban completamente predefinidos.

El robot ejecutaba siempre la misma secuencia de acciones independientemente de lo que ocurriese a su alrededor.

En el siguiente capítulo incorporaremos un nuevo elemento: **la toma de decisiones**.

El Pioneer P3DX utilizará la información proporcionada por sus sensores para modificar automáticamente su comportamiento y reaccionar ante los obstáculos presentes en la escena.

---

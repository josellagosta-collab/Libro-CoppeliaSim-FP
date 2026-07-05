::: chapter-cover
number: 18
title: Control de articulaciones
time: 5 horas
level: ★★★☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo se controla un robot industrial mediante sus articulaciones.
- Obtener desde Python los identificadores (*handles*) de las articulaciones del UR3.
- Leer la posición de cada eje.
- Modificar la posición de una articulación.
- Controlar simultáneamente varias articulaciones.
- Realizar los primeros movimientos programados del robot.

:::

# Capítulo 18 · Control de articulaciones

### Ha llegado el momento de mover el UR3

En el capítulo anterior conocimos la estructura del **Universal Robots UR3**, identificamos sus seis articulaciones y aprendimos a incorporarlo a una escena de CoppeliaSim.

Ahora comenzaremos a controlarlo mediante programas escritos en Python.

Hasta este momento habíamos movido algunas articulaciones manualmente utilizando las herramientas del simulador.

Aunque este procedimiento resulta muy útil para comprender el funcionamiento del robot, en un entorno industrial todos los movimientos son realizados por programas.

Nuestro objetivo será aprender a escribir esos programas.

A diferencia del **Pioneer P3DX**, que se desplazaba modificando la velocidad de sus ruedas, un robot industrial obtiene su movimiento actuando sobre cada una de sus articulaciones.

Cada eje dispone de un motor independiente que puede posicionarse con gran precisión.

Controlando adecuadamente estos seis motores podremos situar el efector final prácticamente en cualquier punto de su espacio de trabajo.

::: figure
image: ../assets/cap18/fig18_1.png
caption: Cada articulación del UR3 puede controlarse de forma independiente desde Python.
:::

::: teacher
content:

Antes de comenzar la programación es recomendable recordar al alumnado la estructura del árbol de la escena estudiada en el capítulo anterior.

Comprender dónde se encuentran las articulaciones facilitará mucho la obtención de sus identificadores desde Python.

:::

---

## 18.1 Las articulaciones como objetos de CoppeliaSim

En CoppeliaSim cada una de las articulaciones del UR3 se representa mediante un objeto independiente.

Esto significa que podemos acceder a ellas desde nuestros programas exactamente igual que hacemos con un sensor, una cámara o cualquier otro elemento de la escena.

Para poder controlar una articulación, el primer paso consiste en obtener su **identificador**, conocido en CoppeliaSim como **handle**.

Un *handle* puede entenderse como una referencia interna que permite al programa localizar un objeto concreto dentro de la escena.

Sin él, Python no sabría sobre qué articulación debe actuar.

En el caso del UR3 necesitaremos obtener los identificadores correspondientes a sus seis ejes.

Una vez dispongamos de ellos podremos:

- consultar su posición;
- modificar su ángulo;
- establecer velocidades;
- sincronizar varios movimientos;
- crear secuencias de trabajo.

A partir de este capítulo utilizaremos continuamente estos identificadores, por lo que es importante comprender su función desde el principio.

::: figure
image: ../assets/cap18/fig18_2.png
caption: Relación entre el árbol de la escena, las articulaciones del UR3 y sus correspondientes *handles* en Python.
:::

---

### ¿Qué es un *handle*?

Podemos imaginar un *handle* como el número de teléfono de un objeto.

Para hablar con una persona necesitamos conocer su número.

De la misma forma, para que Python pueda comunicarse con una articulación necesita conocer su identificador.

Una vez obtenido ese *handle*, podremos utilizarlo tantas veces como sea necesario durante la ejecución del programa.

En los siguientes apartados aprenderemos a obtener estos identificadores utilizando la API de CoppeliaSim y realizaremos nuestros primeros movimientos programados del UR3.

---

## 18.2 Obteniendo los *handles* de las articulaciones

En el apartado anterior aprendimos que cada articulación del **UR3** es un objeto independiente dentro de CoppeliaSim.

Para poder controlarla desde Python necesitamos obtener su identificador o *handle*.

Este será siempre el primer paso antes de realizar cualquier movimiento.

Una vez obtenido el *handle*, podremos utilizarlo para:

- leer la posición de la articulación;
- modificar su ángulo;
- controlar su velocidad;
- sincronizar varios ejes;
- crear secuencias automáticas de movimiento.

---

### El nombre de las articulaciones

Cada articulación del UR3 posee un nombre dentro del árbol de la escena.

En la versión de CoppeliaSim utilizada en estas prácticas, las articulaciones del modelo no aparecen con nombres numerados. En el árbol se llaman simplemente `joint` y están encadenadas dentro de objetos llamados `link`.

Por tanto, no debemos buscar seis objetos con nombres numerados. Debemos respetar la jerarquía real del robot:

```text
UR3
├── Script
├── link1_visible
└── joint
    └── link
        ├── link2_visible
        └── joint
            └── link
                ├── link3_visible
                └── joint
                    └── link
                        ├── link4_visible
                        └── joint
                            └── link
                                ├── link5_visible
                                └── joint
                                    └── link
                                        ├── link6_visible
                                        └── joint
                                            └── link
                                                ├── connection
                                                └── link7_visible
```

Cada línea llamada `joint` corresponde a uno de los seis ejes del robot. Como varias articulaciones tienen el mismo nombre, para obtenerlas desde Python utilizaremos su ruta completa dentro del árbol.

::: figure
image: ../assets/cap18/fig18_3.png
caption: Identificación de las seis articulaciones del UR3 en el árbol de la escena.
:::

---

## Obteniendo el primer *handle*

La API remota de CoppeliaSim proporciona la función `sim.getObject()` para localizar cualquier objeto de la escena a partir de su nombre.

El siguiente ejemplo obtiene el identificador de la primera articulación del robot, que es el `joint` situado directamente bajo `UR3`.

```python
eje_1 = sim.getObject("/UR3/joint")
```

A partir de este momento, la variable `eje_1` contendrá una referencia directa a la primera articulación del robot.

Podremos utilizarla tantas veces como sea necesario durante la ejecución del programa.

---

## Obteniendo todas las articulaciones

Lo habitual será obtener los seis *handles* al comenzar el programa.

En este modelo, las rutas completas de las articulaciones son:

```python
eje_1 = sim.getObject("/UR3/joint")
eje_2 = sim.getObject("/UR3/joint/link/joint")
eje_3 = sim.getObject("/UR3/joint/link/joint/link/joint")
eje_4 = sim.getObject("/UR3/joint/link/joint/link/joint/link/joint")
eje_5 = sim.getObject("/UR3/joint/link/joint/link/joint/link/joint/link/joint")
eje_6 = sim.getObject("/UR3/joint/link/joint/link/joint/link/joint/link/joint/link/joint")
```

De esta forma tendremos acceso inmediato a todas las articulaciones del robot.

::: common-error
content:

No escribas los nombres de memoria.

Comprueba siempre el árbol de la escena.

Si el nombre utilizado en el programa no coincide exactamente con el del objeto existente en CoppeliaSim, la función no podrá localizar la articulación.

En este UR3 concreto, las articulaciones no tienen nombres únicos visibles en el árbol. La primera articulación es `/UR3/joint`, y las siguientes se encuentran bajando por la cadena `joint/link/joint`.

:::

---

## Guardando los *handles* en una lista

Cuando un robot dispone de varias articulaciones resulta más cómodo almacenarlas en una lista.

Así podremos recorrerlas mediante un bucle sin repetir continuamente el mismo código.

```python
joint_paths = [
    "/UR3/joint",
    "/UR3/joint/link/joint",
    "/UR3/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint/link/joint",
    "/UR3/joint/link/joint/link/joint/link/joint/link/joint/link/joint",
]

joints = []

for path in joint_paths:
    joints.append(sim.getObject(path))
```

Esta técnica simplificará mucho los programas de los próximos capítulos.

Además, permitirá escribir funciones reutilizables para mover varias articulaciones simultáneamente.

También podemos dejar esta parte preparada en una función:

```python
def obtener_articulaciones_ur3(sim):
    joint_paths = [
        "/UR3/joint",
        "/UR3/joint/link/joint",
        "/UR3/joint/link/joint/link/joint",
        "/UR3/joint/link/joint/link/joint/link/joint",
        "/UR3/joint/link/joint/link/joint/link/joint/link/joint",
        "/UR3/joint/link/joint/link/joint/link/joint/link/joint/link/joint",
    ]

    return [sim.getObject(path) for path in joint_paths]
```

::: figure
image: ../assets/cap18/fig18_4.png
caption: Obtención de los seis *handles* del UR3 y almacenamiento en una lista para facilitar su utilización desde Python.
:::

---

### ¿Por qué utilizar una lista?

Supongamos que queremos mostrar por pantalla la posición de todas las articulaciones.

Si utilizáramos variables independientes tendríamos que escribir seis instrucciones diferentes.

En cambio, utilizando una lista bastará con recorrerla mediante un bucle.

Este enfoque hace que nuestros programas sean más cortos, más claros y mucho más fáciles de mantener.

A partir de este momento trabajaremos siempre utilizando esta estructura de datos.

---

## 18.3 Moviendo la primera articulación

Ya disponemos de los *handles* de las seis articulaciones del UR3.

Ha llegado el momento de realizar nuestro primer movimiento desde Python.

Comenzaremos utilizando únicamente la primera articulación del robot.

Este enfoque presenta dos ventajas importantes.

Por un lado, resulta mucho más sencillo comprender el funcionamiento de la API.

Por otro, podremos comprobar inmediatamente el efecto que produce una orden enviada desde nuestro programa.

---

### Estableciendo una posición

La función `sim.setJointTargetPosition()` permite indicar la posición objetivo de una articulación.

Su sintaxis es muy sencilla:

```python
sim.setJointTargetPosition(joints[0], math.radians(45))
```

En este ejemplo estamos indicando que la primera articulación debe girar hasta **45 grados**.

Observa que utilizamos la función `math.radians()`.

Esto es necesario porque CoppeliaSim trabaja internamente utilizando **radianes**, mientras que para las personas resulta mucho más intuitivo trabajar con grados.

::: teacher
content:

Es recomendable insistir desde el primer momento en la diferencia entre grados y radianes.

Muchos errores posteriores se deben simplemente a olvidar esta conversión.

:::

---

## Nuestro primer programa

El siguiente ejemplo realiza una conexión con CoppeliaSim, obtiene el *handle* de la primera articulación y ordena un giro de 45°.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import math


def obtener_articulaciones_ur3(sim):
    joint_paths = [
        "/UR3/joint",
        "/UR3/joint/link/joint",
        "/UR3/joint/link/joint/link/joint",
        "/UR3/joint/link/joint/link/joint/link/joint",
        "/UR3/joint/link/joint/link/joint/link/joint/link/joint",
        "/UR3/joint/link/joint/link/joint/link/joint/link/joint/link/joint",
    ]

    return [sim.getObject(path) for path in joint_paths]


client = RemoteAPIClient()
sim = client.require('sim')

joints = obtener_articulaciones_ur3(sim)

sim.setJointTargetPosition(joints[0], math.radians(45))
```

Al ejecutar este programa observarás cómo la base del robot gira suavemente hasta alcanzar la nueva posición.

::: figure
image: ../assets/cap18/fig18_5.png
caption: Movimiento de la primera articulación del UR3 tras ejecutar el programa en Python.
:::

---

### Probando diferentes posiciones

Una vez comprobado el funcionamiento del programa, modifica el valor del ángulo y observa el resultado.

Puedes probar, por ejemplo:

| Ángulo | Resultado esperado |
|---------|--------------------|
| 0° | Posición inicial del robot. |
| 30° | Giro suave hacia la izquierda. |
| 45° | Giro intermedio. |
| 90° | Giro amplio de la base. |
| -45° | Giro en sentido contrario. |

Realizar pequeñas modificaciones en el código es una excelente forma de comprender cómo responde el robot.

::: common-error
content:

No introduzcas valores excesivamente grandes.

Aunque una articulación pueda girar varios cientos de grados en la simulación, cada eje del UR3 posee límites mecánicos que conviene respetar.

Más adelante aprenderemos a consultar esos límites automáticamente.

:::

---

## Leyendo la posición de una articulación

Además de enviar órdenes al robot, también podemos consultar la posición actual de cualquiera de sus articulaciones.

La función `sim.getJointPosition()` devuelve el ángulo actual del eje en **radianes**.

```python
angulo = sim.getJointPosition(joints[0])

print(math.degrees(angulo))
```

En este caso convertimos el resultado nuevamente a grados para mostrar una información más comprensible al usuario.

Esta técnica será muy útil cuando necesitemos verificar que el robot ha alcanzado realmente la posición solicitada.

::: figure
image: ../assets/cap18/fig18_6.png
caption: Lectura de la posición de una articulación y conversión del resultado a grados.
:::

---

### Posición objetivo y posición real

Es importante distinguir dos conceptos.

Cuando utilizamos `setJointTargetPosition()` estamos indicando al robot **dónde queremos que llegue**.

Sin embargo, durante el movimiento puede transcurrir un pequeño intervalo de tiempo hasta que la articulación alcance realmente esa posición.

Por este motivo, en muchas aplicaciones industriales resulta habitual comprobar la posición real mediante `getJointPosition()` antes de continuar con la siguiente operación.

En los próximos apartados aprenderemos a mover varias articulaciones de forma coordinada para conseguir movimientos mucho más naturales.

---

## 18.4 Coordinando varias articulaciones

Mover una única articulación resulta útil para comprender el funcionamiento del robot.

Sin embargo, un robot industrial rara vez trabaja de esta forma.

En una aplicación real, varias articulaciones se desplazan de manera coordinada para que el efector final siga una trayectoria suave y precisa.

En este apartado aprenderemos a controlar varias articulaciones del UR3 dentro del mismo programa.

---

### Estableciendo varias posiciones objetivo

Una vez obtenidos los *handles*, podemos enviar órdenes a todas las articulaciones de forma consecutiva.

```python
sim.setJointTargetPosition(joints[0], math.radians(30))
sim.setJointTargetPosition(joints[1], math.radians(-40))
sim.setJointTargetPosition(joints[2], math.radians(60))
sim.setJointTargetPosition(joints[3], math.radians(20))
sim.setJointTargetPosition(joints[4], math.radians(-15))
sim.setJointTargetPosition(joints[5], math.radians(90))
```

Aunque las instrucciones se ejecutan una detrás de otra, el robot comenzará a mover todos los ejes de forma prácticamente simultánea.

El resultado será un movimiento mucho más natural que el obtenido actuando sobre una sola articulación.

::: figure
image: ../assets/cap18/fig18_7.png
caption: Movimiento coordinado de las seis articulaciones del UR3 hasta alcanzar una nueva configuración.
:::

---

### Utilizando una lista de articulaciones

En el apartado anterior almacenamos los *handles* en una lista.

Gracias a ello podemos recorrer todas las articulaciones mediante un único bucle.

```python
objetivos = [30, -40, 60, 20, -15, 90]

for joint, angulo in zip(joints, objetivos):
    sim.setJointTargetPosition(joint, math.radians(angulo))
```

Este enfoque presenta numerosas ventajas.

- El código resulta más corto.
- Es mucho más fácil modificar las posiciones.
- Permite reutilizar funciones en diferentes programas.

Además, será la técnica que utilizaremos durante el resto de la Parte IV.

::: teacher
content:

Acostumbra al alumnado a trabajar con listas desde el principio.

En robots con seis o más articulaciones esta forma de programar reduce considerablemente los errores y mejora la legibilidad del código.

:::

---

## Creando una postura del robot

Una **postura** es un conjunto de posiciones para todas las articulaciones del robot.

Cada postura representa una configuración concreta del UR3.

Por ejemplo:

| Postura | Eje 1 | Eje 2 | Eje 3 | Eje 4 | Eje 5 | Eje 6 |
|----------|--------|--------|--------|--------|--------|--------|
| Inicio | 0° | 0° | 0° | 0° | 0° | 0° |
| Recogida | 20° | -50° | 75° | 10° | -25° | 0° |
| Transporte | 45° | -20° | 45° | 30° | 0° | 90° |

En lugar de calcular continuamente nuevos ángulos, muchas aplicaciones industriales trabajan desplazando el robot entre distintas posturas previamente definidas.

---

### Ventajas de trabajar con posturas

Este método ofrece importantes beneficios.

- Facilita la programación.
- Permite reutilizar posiciones.
- Hace que el código sea más fácil de entender.
- Reduce los errores durante el desarrollo.

En los siguientes capítulos ampliaremos este concepto para construir secuencias completas de manipulación.

::: common-error
content:

No confundas una postura con una trayectoria.

Una postura describe únicamente una configuración concreta del robot.

La trayectoria es el movimiento que realiza el UR3 para pasar de una postura a otra.

:::

::: figure
image: ../assets/cap18/fig18_8.png
caption: Ejemplo de tres posturas diferentes del UR3 utilizadas durante una secuencia de trabajo.
:::

---

## 18.5 Controlando la velocidad del movimiento

Hasta ahora hemos indicado al robot la posición que debe alcanzar.

Sin embargo, en una aplicación industrial también resulta importante controlar **la velocidad** con la que se realiza el movimiento.

No es lo mismo desplazar una herramienta de soldadura que transportar una pieza de vidrio o manipular un componente electrónico de precisión.

Cada tarea requiere una velocidad diferente.

En CoppeliaSim podemos ajustar este comportamiento para conseguir movimientos más suaves y realistas.

::: figure
image: ../assets/cap18/fig18_9.png
caption: La velocidad de las articulaciones influye directamente en el comportamiento del robot durante la ejecución de una tarea.
:::

---

### ¿Por qué controlar la velocidad?

Modificar la velocidad de las articulaciones permite:

- aumentar la precisión durante operaciones delicadas;
- reducir el tiempo de ciclo de una aplicación;
- evitar movimientos bruscos;
- mejorar la seguridad cuando el robot trabaja cerca de personas.

En los robots colaborativos, como el **UR3**, el control de la velocidad resulta especialmente importante para garantizar un funcionamiento seguro.

---

## Creando movimientos suaves

Observa la diferencia entre estos dos ejemplos.

En el primero, el robot se desplaza a la máxima velocidad permitida.

En el segundo, el movimiento es mucho más progresivo.

Aunque ambos alcanzan exactamente la misma posición final, la sensación visual es completamente distinta.

Durante las prácticas de este libro procuraremos utilizar velocidades moderadas para facilitar la observación de los movimientos.

::: teacher
content:

Durante las primeras prácticas utiliza velocidades reducidas.

El alumnado comprenderá mucho mejor cómo interviene cada articulación y será más sencillo detectar posibles errores de programación.

:::

---

## Ejecutando una secuencia de posturas

Ya conocemos los elementos fundamentales necesarios para mover el robot:

- los *handles*;
- las posiciones objetivo;
- las velocidades de movimiento.

Con ellos podemos crear una pequeña secuencia de trabajo.

Por ejemplo:

1. Llevar el robot a la postura inicial.
2. Desplazarlo hasta una postura de aproximación.
3. Regresar nuevamente a la posición inicial.

El siguiente ejemplo ilustra esta idea.

```python
def mover_robot(joints, postura):
    for joint, angulo in zip(joints, postura):
        sim.setJointTargetPosition(joint, math.radians(angulo))


postura_inicio = [0, 0, 0, 0, 0, 0]
postura_aproximacion = [25, -35, 60, 15, -20, 0]

mover_robot(joints, postura_inicio)
time.sleep(2)

mover_robot(joints, postura_aproximacion)
time.sleep(2)

mover_robot(joints, postura_inicio)
```

En los próximos capítulos ampliaremos esta función para construir secuencias mucho más complejas.

::: figure
image: ../assets/cap18/fig18_10.png
caption: Secuencia de movimiento del UR3 entre distintas posturas programadas desde Python.
:::

---

### Preparados para el siguiente paso

Hasta este momento hemos trabajado directamente con las articulaciones del robot.

Cada movimiento se ha definido indicando el ángulo de cada uno de los seis ejes.

Aunque este método resulta muy útil para comprender el funcionamiento del UR3, presenta una limitación importante.

Imagina que deseas mover la pinza exactamente hasta las coordenadas:

- **X = 300 mm**
- **Y = -150 mm**
- **Z = 200 mm**

¿Qué ángulo debería adoptar cada una de las seis articulaciones?

Responder a esta pregunta manualmente resulta muy complicado.

Afortunadamente, los robots industriales disponen de herramientas que realizan estos cálculos automáticamente.

Ese será precisamente el objetivo del próximo capítulo.

Aprenderemos qué es la **cinemática directa** y la **cinemática inversa**, y descubriremos cómo CoppeliaSim permite mover el efector final del UR3 indicando únicamente la posición que queremos alcanzar.

---

## 18.6 Práctica guiada: Controlando el UR3 desde Python

Ha llegado el momento de poner en práctica todo lo aprendido durante este capítulo.

El objetivo consiste en desarrollar un pequeño programa capaz de controlar las seis articulaciones del robot y ejecutar una sencilla secuencia de movimientos.

::: practice
title: Primer programa de control del UR3

difficulty: Media

time: 45 minutos

content:

Realiza las siguientes tareas:

1. Abre la escena base del UR3 utilizada durante la Parte IV.
2. Establece la conexión entre Python y CoppeliaSim.
3. Obtén los *handles* de las seis articulaciones.
4. Comprueba que todos los *handles* se obtienen correctamente.
5. Lleva el robot a la postura inicial.
6. Programa una segunda postura modificando al menos cuatro articulaciones.
7. Regresa nuevamente a la postura inicial.
8. Lee la posición de todas las articulaciones y muéstrala por pantalla en grados.
9. Repite la secuencia varias veces modificando las velocidades de movimiento.
10. Observa el comportamiento del robot e identifica las diferencias entre movimientos rápidos y lentos.

Al finalizar la práctica deberás ser capaz de controlar completamente las articulaciones del UR3 desde Python.

:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Articulación | Eje motorizado que proporciona movimiento al robot. |
| Handle | Identificador que permite acceder a un objeto de CoppeliaSim desde Python. |
| Posición objetivo | Ángulo que deseamos que alcance una articulación. |
| Posición real | Ángulo que posee realmente la articulación en un instante determinado. |
| Radianes | Unidad angular utilizada internamente por CoppeliaSim. |
| Grados | Unidad más intuitiva para representar ángulos. |
| Postura | Conjunto de posiciones de todas las articulaciones del robot. |
| Movimiento coordinado | Desplazamiento simultáneo de varias articulaciones. |
| Velocidad articular | Rapidez con la que una articulación alcanza la posición objetivo. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Obtener los *handles* de las articulaciones del UR3.
- ✅ Controlar individualmente cada eje del robot.
- ✅ Leer la posición de las articulaciones.
- ✅ Convertir ángulos entre grados y radianes.
- ✅ Programar movimientos coordinados.
- ✅ Definir y reutilizar posturas.
- ✅ Crear pequeñas secuencias de movimiento.
- ✅ Comprender la influencia de la velocidad en el comportamiento del robot.

A partir de este momento ya puedes controlar completamente las articulaciones del UR3 mediante programas escritos en Python.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué es un *handle* y por qué resulta imprescindible para controlar el robot?
2. ¿Por qué CoppeliaSim trabaja internamente en radianes?
3. ¿Qué diferencia existe entre una posición objetivo y una posición real?
4. ¿Qué ventajas ofrece almacenar las articulaciones en una lista?
5. ¿Qué entendemos por una postura del robot?
6. ¿Por qué resulta importante controlar la velocidad de movimiento?
7. ¿Qué diferencia existe entre mover una articulación y coordinar varias simultáneamente?

Si puedes responder correctamente a todas ellas, estás preparado para estudiar la cinemática del robot.

---

## Reto

::: challenge
title: Diseñando una secuencia de inspección

content:

Programa una secuencia formada por cuatro posturas diferentes del UR3.

El robot deberá:

- partir de la postura inicial;
- desplazarse hasta una primera posición de inspección;
- continuar hacia una segunda posición;
- regresar finalmente al punto de partida.

Intenta que los movimientos sean suaves y naturales.

Como ampliación, modifica las velocidades para comprobar cómo cambia el comportamiento del robot.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Consolidar el control de articulaciones mediante Python.
- Familiarizar al alumnado con la obtención de *handles*.
- Comprender el concepto de postura.
- Introducir la programación estructurada de movimientos.

**Material necesario**

- Ordenadores con CoppeliaSim y Python configurados.
- Escena base del UR3.
- Proyector para realizar demostraciones.

**Consejos metodológicos**

Es recomendable que todos los estudiantes trabajen siempre sobre la misma escena del UR3.

Evita que modifiquen la estructura del robot durante las prácticas.

Esto facilitará enormemente el desarrollo de los capítulos posteriores, donde comenzarán a trabajar con cinemática y manipulación de objetos.

:::

---

## Próximo capítulo

Hasta ahora hemos controlado el robot indicando directamente el ángulo de cada una de sus articulaciones.

Aunque este método resulta muy útil para comprender el funcionamiento del UR3, presenta una limitación evidente: obliga a calcular manualmente la posición de todos los ejes.

En el próximo capítulo aprenderás a trabajar de una forma mucho más intuitiva.

Descubrirás qué son la **cinemática directa** y la **cinemática inversa**, comprenderás el papel de los sistemas de referencia y aprenderás a mover el efector final del robot indicando únicamente el punto del espacio que deseas alcanzar.

Será uno de los capítulos más importantes de todo el libro y la base de las aplicaciones de manipulación que desarrollaremos posteriormente.

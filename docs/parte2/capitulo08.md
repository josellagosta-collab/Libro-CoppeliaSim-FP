::: chapter-cover
number: 8
title: Sensores en robots móviles
time: 5 horas
level: ⭐⭐☆☆☆ (Inicial)
:::

::: objectives
title: Objetivos del capítulo

content:

Al finalizar este capítulo serás capaz de:

- Comprender la importancia de los sensores en un robot móvil.
- Identificar los principales sensores del Pioneer P3DX.
- Explicar el funcionamiento básico de los sensores de proximidad.
- Leer la información proporcionada por un sensor desde Python.
- Interpretar correctamente los datos obtenidos durante una simulación.
- Desarrollar un primer programa capaz de detectar obstáculos.
:::

# Capítulo 8 · Sensores en robots móviles

### ¿Cómo sabe un robot lo que ocurre a su alrededor?

Hasta ahora hemos aprendido a controlar un robot móvil desde Python.

Podemos conocer su posición, modificar sus coordenadas e interactuar con la simulación mediante la API remota de CoppeliaSim.

Sin embargo, todavía existe una gran diferencia entre nuestro robot y un robot verdaderamente autónomo.

Hasta este momento el Pioneer P3DX es completamente "ciego".

Puede moverse, pero es incapaz de saber si delante de él existe una pared, otro robot o cualquier obstáculo.

Para que un robot pueda tomar decisiones necesita recibir información del entorno.

Esa información la proporcionan los sensores.

En este capítulo aprenderemos cómo funcionan los sensores de proximidad del Pioneer P3DX, cómo acceder a ellos desde Python y cómo interpretar correctamente los datos que devuelven.

Estos conceptos serán la base para desarrollar, en los siguientes capítulos, robots capaces de desplazarse de forma autónoma evitando obstáculos.

::: teacher
title: Consejo para el profesor

content:

Antes de comenzar con la programación, pregunta al alumnado cómo creen que un robot "ve" el mundo que le rodea.

La mayoría responderá que mediante cámaras.

Esta actividad resulta muy útil para introducir la idea de que existen numerosos tipos de sensores y que, en muchas aplicaciones industriales, una cámara ni siquiera es necesaria.
:::

---

## 8.1 La importancia de la percepción

Cuando observamos el comportamiento de un robot solemos fijarnos únicamente en sus movimientos.

Sin embargo, ningún robot puede desplazarse de forma inteligente si antes no es capaz de obtener información del entorno.

En robótica existe una idea fundamental:

> **Un robot primero percibe, después decide y finalmente actúa.**

::: figure
image: ../assets/cap08/png/svgciclo_percepcion_decision_accion.png
caption: Ciclo percepción → decisión → acción utilizado por un robot móvil autónomo.
:::

Este ciclo se repite continuamente mientras el robot está funcionando.

En cada instante los sensores recopilan información del entorno.

El sistema de control analiza esos datos y decide cuál debe ser la siguiente acción.

Finalmente, los motores ejecutan el movimiento correspondiente.

Este proceso ocurre cientos o incluso miles de veces por segundo en muchos robots industriales.

---

### ¿Qué significa percibir?

Percibir consiste en obtener información del entorno utilizando sensores.

Del mismo modo que las personas utilizamos los ojos, los oídos o el tacto para conocer lo que ocurre a nuestro alrededor, los robots emplean diferentes dispositivos electrónicos para recopilar información.

Dependiendo del tipo de robot y de la tarea que deba realizar, será necesario utilizar unos sensores u otros.

Algunos permiten medir distancias.

Otros detectan colores.

Existen sensores capaces de medir temperatura, presión, aceleración, velocidad, fuerza o incluso la posición exacta de una pieza dentro de una línea de producción.

En todos los casos, el objetivo es el mismo: proporcionar al robot la información necesaria para tomar decisiones.

::: info
title: Percibir no significa comprender

content:

Los sensores únicamente proporcionan datos.

Interpretar correctamente esos datos y decidir cómo actuar corresponde al programa de control del robot.

Dos robots pueden recibir exactamente la misma información y reaccionar de forma completamente diferente dependiendo del algoritmo que ejecuten.
:::

---

### Sensores y actuadores

En robótica es habitual distinguir entre dos grandes tipos de componentes.

Por un lado se encuentran los **sensores**, encargados de obtener información.

Por otro lado encontramos los **actuadores**, responsables de ejecutar acciones físicas.

En el Pioneer P3DX, los sensores de proximidad detectan obstáculos mientras que los motores de las ruedas permiten desplazar el robot.

Ambos tipos de dispositivos trabajan continuamente de forma coordinada.

Los sensores informan.

Los actuadores actúan.

El programa de control conecta ambos mundos.

Sin sensores, el robot se movería sin conocer el entorno.

Sin actuadores, conocería perfectamente el entorno, pero sería incapaz de reaccionar.

---

### El ciclo percepción → decisión → acción

Todo robot autónomo sigue, de una forma u otra, un ciclo de funcionamiento muy similar.

1. Los sensores recopilan información.
2. El programa analiza los datos recibidos.
3. Se toma una decisión.
4. Los actuadores ejecutan la acción correspondiente.
5. El proceso vuelve a comenzar.

Este ciclo se repite constantemente mientras el robot permanece activo.

En los próximos apartados veremos cómo implementar las dos primeras fases utilizando Python y CoppeliaSim.

Más adelante incorporaremos la fase de decisión y, finalmente, desarrollaremos robots capaces de reaccionar automáticamente ante la presencia de obstáculos.

::: summary
title: Idea clave

content:

La autonomía de un robot no depende únicamente de su capacidad para moverse.

Lo realmente importante es su capacidad para percibir el entorno, interpretar la información recibida y actuar en consecuencia.

Los sensores constituyen el primer paso de todo ese proceso.
:::

---

## 8.2 Los sensores del Pioneer P3DX

El Pioneer P3DX incorpora diferentes dispositivos capaces de obtener información del entorno.

Gracias a ellos el robot puede detectar obstáculos, medir distancias y conocer lo que ocurre a su alrededor sin necesidad de intervención humana.

En este libro centraremos nuestra atención en los **sensores de proximidad**, ya que constituyen la base de la navegación autónoma.

Aunque el Pioneer puede equiparse con otros tipos de sensores, los de proximidad son suficientes para desarrollar un gran número de aplicaciones educativas y profesionales.

Antes de aprender a utilizarlos desde Python conviene conocer cómo están distribuidos y cuál es su funcionamiento.

---

### Un anillo de sensores

Si observamos el Pioneer P3DX desde la parte superior veremos que los sensores se encuentran distribuidos alrededor de todo el perímetro del robot.

::: figure
image: ../assets/cap07/annotated/sensores_pioneer_p3dx.png
caption: Distribución aproximada de los sensores ultrasónicos del Pioneer P3DX.
:::

Esta disposición permite detectar obstáculos prácticamente en cualquier dirección.

No todos los sensores apuntan hacia el frente.

Algunos vigilan los laterales y otros controlan la parte trasera.

De esta forma el robot dispone de una visión casi completa de su entorno inmediato.

En CoppeliaSim estos sensores ya vienen incorporados al modelo del Pioneer P3DX.

No es necesario añadirlos manualmente ni realizar ninguna configuración especial.

Basta con acceder a ellos desde nuestro programa Python.

::: info
title: ¿Por qué tantos sensores?

content:

Un único sensor frontal únicamente permitiría detectar obstáculos situados justo delante del robot.

Distribuir varios sensores alrededor del chasis proporciona una percepción mucho más completa del entorno y facilita la navegación en espacios complejos.
:::

---

### Sensores delanteros

Los sensores situados en la parte frontal son los más utilizados durante las primeras prácticas.

Su misión consiste en detectar cualquier obstáculo que aparezca delante del robot.

Gracias a ellos el Pioneer puede:

- detenerse antes de una colisión;
- reducir su velocidad;
- cambiar de dirección;
- buscar un camino alternativo.

En los siguientes ejemplos trabajaremos principalmente con estos sensores para simplificar la programación.

Más adelante aprenderemos a utilizar simultáneamente todos los sensores del robot.

---

### Sensores laterales

Además de controlar la zona frontal, el Pioneer incorpora sensores orientados hacia ambos laterales.

Estos dispositivos permiten detectar paredes u objetos cercanos mientras el robot se desplaza.

Su utilización resulta especialmente útil en algoritmos como:

- seguimiento de paredes;
- navegación por pasillos;
- mantenimiento de una distancia constante respecto a un obstáculo.

Aunque inicialmente apenas los utilizaremos, desempeñarán un papel fundamental en capítulos posteriores.

---

### Sensores traseros

En la parte posterior también encontramos varios sensores de proximidad.

Su función principal consiste en supervisar la zona situada detrás del robot.

Gracias a ellos es posible realizar maniobras de retroceso con mayor seguridad.

En robots industriales reales este tipo de sensores resulta muy habitual cuando el vehículo debe desplazarse tanto hacia delante como hacia atrás dentro de espacios reducidos.

---

### ¿Todos los sensores trabajan al mismo tiempo?

Sí.

Durante la simulación todos los sensores permanecen activos de forma simultánea.

Cada uno realiza continuamente medidas sobre la zona del espacio que tiene asignada.

Nuestro programa Python puede consultar cualquiera de ellos cuando lo necesite.

No existe ninguna obligación de leer todos los sensores en cada instante.

En ocasiones bastará con consultar únicamente los sensores frontales.

En otras aplicaciones será necesario analizar la información proporcionada por todo el conjunto.

La elección dependerá del algoritmo que estemos desarrollando.

::: teacher
title: Consejo para el profesor

content:

Muchos estudiantes imaginan que el robot "mira" el entorno como si tuviera una cámara.

Aprovecha este apartado para insistir en que cada sensor únicamente obtiene información de una pequeña región del espacio.

La percepción completa del entorno se consigue combinando la información procedente de todos ellos.
:::

---

### Un primer vistazo al árbol de la escena

Si desplegamos el Pioneer P3DX en el árbol de la escena podremos localizar fácilmente los sensores.

::: figure
image: ../assets/cap08/annotated/arbol_sensores.png
caption: Sensores del Pioneer P3DX en el árbol de la escena.
:::

Cada uno aparece como un objeto independiente dentro de la jerarquía del robot.

Esto resulta especialmente útil porque podremos acceder a ellos individualmente desde Python utilizando su nombre.

No es necesario memorizar todavía todos los identificadores.

En el próximo apartado aprenderemos a obtener automáticamente la referencia de cualquier sensor mediante la API remota.

::: summary
title: Idea clave

content:

El Pioneer P3DX incorpora varios sensores de proximidad distribuidos alrededor de todo el robot.

Cada sensor supervisa una pequeña zona del entorno y todos trabajan simultáneamente para proporcionar una percepción mucho más completa que la que ofrecería un único sensor frontal.
:::

---

## 8.3 ¿Cómo funcionan los sensores de proximidad?

Hasta ahora sabemos que el Pioneer P3DX incorpora varios sensores distribuidos alrededor de su estructura.

Pero... ¿cómo consiguen detectar un obstáculo?

Aunque en un robot real existen diferentes tecnologías de detección, en CoppeliaSim todos los sensores de proximidad siguen un principio de funcionamiento muy similar.

Cada sensor proyecta una región de detección delante de él.

Cuando un objeto entra dentro de esa región, el sensor informa al simulador de que ha detectado un obstáculo.

Nuestro programa Python únicamente tendrá que consultar esa información.

---

### El volumen de detección

Un sensor de proximidad no "ve" todo lo que ocurre a su alrededor.

Su campo de visión está limitado a una determinada zona del espacio.

Podemos imaginar este volumen como un cono que parte desde la parte frontal del sensor.

::: figure
image: ../assets/cap08/svg/volumen_deteccion_sensor.svg
caption: Volumen de detección de un sensor de proximidad.
:::

Mientras no exista ningún objeto dentro de ese cono, el sensor no detectará nada.

Cuando un objeto penetra en la zona de detección, el sensor genera una respuesta positiva.

::: figure
image: ../assets/cap08/png/deteccion_correcta_incorrecta.png
caption: Comparación entre un objeto detectado y un objeto situado fuera del volumen de detección.
:::

Este comportamiento resulta muy parecido al funcionamiento de una linterna.

La luz únicamente ilumina aquello que se encuentra dentro de su haz.

Todo lo que queda fuera permanece invisible.

::: figure
image: ../assets/cap08/png/analogia_linterna_sensor.png
caption: Analogía entre el haz de una linterna y el volumen de detección de un sensor de proximidad.
:::


::: info
content:

Un sensor no es una cámara.

Los sensores de proximidad no generan imágenes.

Su única misión consiste en indicar si existe o no un objeto dentro de su volumen de detección y, en muchos casos, proporcionar la distancia hasta dicho objeto.
:::

---

### Alcance máximo

Todo sensor posee una distancia máxima de funcionamiento.

Si un obstáculo se encuentra demasiado lejos, el sensor simplemente no podrá detectarlo.

En CoppeliaSim este alcance depende de la configuración del propio sensor.

En la mayoría de las prácticas utilizaremos la configuración predeterminada incluida en el modelo del Pioneer P3DX.

No será necesario modificar ningún parámetro.

Más adelante aprenderemos que es posible cambiar el alcance de un sensor para adaptarlo a diferentes situaciones.

---

### Ángulo de detección

Además del alcance, otro parámetro importante es el ángulo de apertura.

Un sensor muy estrecho resulta muy preciso, pero únicamente detecta objetos situados justo delante de él.

Por el contrario, un sensor con un ángulo muy amplio cubre una zona mayor, aunque normalmente pierde precisión.

Por este motivo el Pioneer utiliza varios sensores orientados en distintas direcciones.

Cada uno supervisa una pequeña región del espacio.

La combinación de todos ellos proporciona una percepción mucho más completa del entorno.

---

### ¿Qué ocurre cuando un objeto es detectado?

Cuando un obstáculo entra en el volumen de detección ocurren varias cosas de forma prácticamente instantánea.

El sensor:

- detecta la presencia del objeto;
- calcula el punto donde se ha producido la detección;
- determina la distancia hasta dicho punto;
- comunica esa información a CoppeliaSim.

Nuestro programa Python podrá consultar posteriormente estos datos mediante la API remota.

Es importante comprender que el sensor no toma ninguna decisión.

Únicamente proporciona información.

Será nuestro programa quien decida cómo reaccionar.

::: teacher
title: Consejo para el profesor

content:

Este es un buen momento para insistir en la diferencia entre detectar y decidir.

Muchos estudiantes creen que el sensor "evita" automáticamente los obstáculos.

En realidad, el sensor únicamente proporciona datos.

Toda la inteligencia reside en el programa que interpreta esa información.
:::

---

### Objetos detectables

No todos los objetos de una escena tienen por qué ser detectados.

En CoppeliaSim cada objeto puede configurarse para responder o no a los sensores de proximidad.

Esta característica resulta muy útil cuando queremos que determinados elementos formen parte de la escena sin interferir en la navegación del robot.

Durante las prácticas de este libro utilizaremos los valores predeterminados del simulador.

De este modo todos los obstáculos preparados para las actividades responderán correctamente a los sensores del Pioneer.

---

### Preparando la programación

Ahora ya conocemos el funcionamiento general de los sensores.

En el siguiente apartado aprenderemos a acceder a ellos desde Python.

Obtendremos la referencia de un sensor concreto, leeremos su estado y analizaremos la información que devuelve la API remota.

Será nuestro primer paso hacia la construcción de robots capaces de reaccionar automáticamente ante la presencia de obstáculos.

::: summary
title: Idea clave

content:

Un sensor de proximidad únicamente detecta objetos situados dentro de su volumen de detección.

Cuando encuentra un obstáculo, proporciona información al programa de control, pero nunca toma decisiones por sí mismo.

La inteligencia del robot depende del software que interpreta esos datos.
:::

---

## 8.4 Leyendo sensores desde Python

Ya sabemos cómo funcionan los sensores de proximidad y qué información son capaces de obtener.

Ha llegado el momento de acceder a ellos desde Python.

El procedimiento será muy parecido al que utilizamos para controlar el Pioneer P3DX.

Primero obtendremos la referencia del sensor.

Después consultaremos la información que proporciona durante la simulación.

A partir de ese momento podremos utilizar esos datos para que el robot tome decisiones.

---

### Obteniendo la referencia de un sensor

Los sensores forman parte de la jerarquía del Pioneer P3DX.

Por tanto, igual que hicimos con el robot, primero debemos obtener una referencia al sensor que queremos utilizar.

Supongamos que queremos acceder al primer sensor frontal.

Podemos hacerlo mediante la función `getObject()`.

```python
sensor = sim.getObject('/PioneerP3DX/ultrasonicSensor1')
```

A partir de ese momento la variable `sensor` almacenará el identificador interno del dispositivo.

Ese identificador será el que utilizaremos en todas las lecturas posteriores.

::: info
title: Los nombres de los sensores

content:

Los sensores aparecen identificados dentro del árbol de la escena con nombres como `ultrasonicSensor1`, `ultrasonicSensor2`, etc.

No es necesario memorizar todos estos nombres.

Basta con localizarlos una vez dentro de CoppeliaSim y utilizarlos posteriormente desde Python.
:::

---

### Leyendo un sensor

La API remota proporciona la función `readProximitySensor()` para consultar el estado de un sensor de proximidad.

Su utilización es muy sencilla.

```python
detectado, distancia, objeto, normal = sim.readProximitySensor(sensor)
```

Aunque la función devuelve varios valores, durante las primeras prácticas únicamente utilizaremos los dos primeros.

- `detectado` indica si existe o no un obstáculo.
- `distancia` contiene la distancia medida por el sensor.

Más adelante utilizaremos también el resto de la información.

---

### Interpretando el resultado

Cuando el sensor no detecta ningún obstáculo, la variable `detectado` contiene el valor:

```python
False
```

En ese caso no existe ningún objeto dentro del volumen de detección.

Si aparece un obstáculo delante del sensor, el resultado será:

```python
True
```

Además, la variable `distancia` contendrá la separación entre el sensor y el punto detectado.

::: figure
image: ../assets/cap08/png/distancia_objeto_mas_cercano.png
caption: El sensor de proximidad devuelve la distancia al objeto más cercano situado dentro de su volumen de detección.
:::

Nuestro programa podrá utilizar esa información para decidir cómo debe actuar el robot.

---

### Mostrando la información por pantalla

Podemos comprobar fácilmente el funcionamiento del sensor mostrando los datos obtenidos.

```python
detectado, distancia, objeto, normal = sim.readProximitySensor(sensor)

print("Detectado:", detectado)
print("Distancia:", distancia)
```

Ejecuta el programa varias veces.

A continuación coloca un obstáculo delante del Pioneer P3DX y vuelve a ejecutarlo.

Observarás que los valores cambian automáticamente.

Este sencillo experimento demuestra que Python está recibiendo información procedente de la simulación en tiempo real.

::: teacher
title: Consejo para el profesor

content:

Anima al alumnado a mover manualmente un cubo delante del robot mientras ejecuta repetidamente el programa.

Ver cómo cambia la distancia medida ayuda a comprender el funcionamiento del sensor mucho mejor que una explicación teórica.
:::

---

### Utilizando una estructura condicional

Una vez sabemos interpretar la lectura del sensor podemos comenzar a tomar decisiones.

Por ejemplo, podemos mostrar un mensaje únicamente cuando exista un obstáculo.

```python
detectado, distancia, objeto, normal = sim.readProximitySensor(sensor)

if detectado:
    print("Obstáculo detectado")
else:
    print("Camino libre")
```

Este es el primer ejemplo de un robot que adapta su comportamiento en función de la información recibida por sus sensores.

Aunque todavía no mueve las ruedas, ya es capaz de distinguir entre una situación segura y otra que requiere atención.

---

### El primer paso hacia la autonomía

Puede parecer un programa muy sencillo.

Sin embargo, representa uno de los conceptos más importantes de toda la robótica.

Por primera vez el comportamiento del robot depende de lo que ocurre en el entorno.

Ya no estamos ejecutando una secuencia fija de instrucciones.

Ahora el programa observa, interpreta la información y responde de forma diferente según la situación.

A partir de este momento todos los algoritmos que desarrollaremos seguirán esta misma filosofía.

::: summary
title: Idea clave

content:

La función `readProximitySensor()` permite consultar el estado de un sensor desde Python.

Gracias a ella nuestros programas pueden obtener información del entorno y comenzar a tomar decisiones basadas en los datos recibidos.
:::

---

## 8.5 Nuestro primer detector de obstáculos

Ya sabemos leer el estado de un sensor de proximidad desde Python.

Ahora construiremos un pequeño programa capaz de detectar si existe un obstáculo delante del Pioneer P3DX.

El objetivo todavía no será mover el robot de forma autónoma.

Por ahora únicamente queremos comprobar que el sensor informa correctamente de la presencia de un objeto.

---

### Preparando la escena

Crea una escena sencilla con los siguientes elementos:

1. El robot **Pioneer P3DX** situado sobre el plano de trabajo.
2. Un cubo colocado delante del robot.
3. Espacio suficiente alrededor para poder mover el cubo y repetir la prueba.

El cubo actuará como obstáculo.

No es necesario que tenga un tamaño concreto.

Basta con que se encuentre dentro del volumen de detección del sensor frontal.

::: common-error
content:

Si el sensor no detecta el cubo, comprueba que el obstáculo está situado justo delante del sensor utilizado.

También verifica que el cubo no queda demasiado lejos o fuera del ángulo de detección.
:::

---

### Programa completo

Crea un archivo llamado:

```text
detectar_obstaculo.py
```

Escribe el siguiente código:

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor1")

detectado, distancia, objeto, normal = sim.readProximitySensor(sensor)

if detectado:
    print("Obstáculo detectado")
    print("Distancia:", distancia)
else:
    print("Camino libre")
```

Este programa realiza cuatro operaciones fundamentales.

1. Establece la conexión con CoppeliaSim.
2. Obtiene la referencia del sensor.
3. Lee el estado del sensor.
4. Muestra un mensaje diferente según exista o no un obstáculo.

---

### Probando el programa

Ejecuta primero el programa con el cubo delante del robot.

Deberías obtener una salida similar a:

```text
Obstáculo detectado
Distancia: 0.42
```

A continuación, aleja el cubo o colócalo fuera del campo de detección del sensor.

Vuelve a ejecutar el programa.

Ahora deberías ver:

```text
Camino libre
```

Este cambio confirma que el programa está interpretando correctamente la información del sensor.

---

### Interpretando la distancia

El valor de distancia representa la separación entre el sensor y el punto detectado.

CoppeliaSim devuelve esta medida en metros.

Por ejemplo:

```text
Distancia: 0.42
```

significa que el obstáculo se encuentra aproximadamente a 42 centímetros del sensor.

Esta información será muy útil en los próximos capítulos.

Gracias a ella podremos tomar decisiones más precisas.

Por ejemplo:

- detener el robot si el obstáculo está muy cerca;
- reducir la velocidad si se aproxima a una pared;
- girar cuando la distancia sea inferior a un umbral;
- mantener una separación constante respecto a un objeto.

---

### Añadiendo un umbral de seguridad

En robótica es habitual definir una distancia mínima de seguridad.

Si el obstáculo se encuentra por debajo de ese valor, el robot debe reaccionar.

Podemos representar esta distancia mediante una variable.

```python
distancia_seguridad = 0.50
```

Ahora podemos modificar el programa para comprobar si el obstáculo está demasiado cerca.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require("sim")

sensor = sim.getObject("/PioneerP3DX/ultrasonicSensor1")

detectado, distancia, objeto, normal = sim.readProximitySensor(sensor)

distancia_seguridad = 0.50

if detectado and distancia < distancia_seguridad:
    print("Obstáculo demasiado cerca")
elif detectado:
    print("Obstáculo detectado, pero a distancia segura")
else:
    print("Camino libre")
```

Este programa ya no se limita a detectar un objeto.

Ahora interpreta la distancia y clasifica la situación.

Se trata de un primer paso hacia comportamientos robóticos más inteligentes.

::: summary
title: Idea clave

content:

Detectar un obstáculo no siempre significa que el robot deba detenerse inmediatamente.

El programa debe interpretar también la distancia y decidir si la situación requiere una respuesta.

:::

---

### Hacia la toma de decisiones

El programa que acabamos de escribir sigue siendo muy sencillo, pero introduce una idea fundamental.

El robot ya no responde igual en todas las situaciones.

Ahora diferencia entre:

- camino libre;
- obstáculo detectado;
- obstáculo demasiado cercano.

En los próximos capítulos utilizaremos esta misma lógica para controlar el movimiento del Pioneer P3DX.

Cuando el robot detecte un obstáculo cercano, podrá detenerse, girar o buscar una trayectoria alternativa.

Por ahora basta con comprender que los sensores proporcionan datos y que nuestro programa debe convertir esos datos en decisiones.

---

## 8.6 Preparando la navegación autónoma

En este capítulo hemos dado un paso muy importante.

El Pioneer P3DX ya no es únicamente un robot que podemos mover desde Python.

Ahora también es un robot capaz de obtener información del entorno.

Hemos aprendido a consultar un sensor de proximidad, interpretar si existe un obstáculo y utilizar una distancia de seguridad para clasificar la situación.

Aunque todavía no estamos moviendo el robot de forma autónoma, ya tenemos una parte esencial del problema resuelta.

---

### De detectar a reaccionar

Detectar un obstáculo es solo el primer paso.

El siguiente será decidir qué debe hacer el robot cuando aparece ese obstáculo.

Por ejemplo:

- detenerse;
- girar hacia la izquierda;
- girar hacia la derecha;
- retroceder;
- buscar una trayectoria alternativa.

Todas estas acciones requieren combinar dos capacidades:

1. leer sensores;
2. controlar motores.

En este capítulo hemos trabajado la primera.

En los próximos capítulos comenzaremos a trabajar la segunda.

---

### Sensores como entrada del programa

Podemos imaginar los sensores como las entradas de nuestro programa.

Cada lectura proporciona información sobre el estado del entorno.

El programa analiza esa información y genera una respuesta.

Esa respuesta se traducirá posteriormente en órdenes para los motores.

Este esquema será fundamental durante toda la parte dedicada a robótica móvil.

```text
Sensores → Programa de control → Motores
```

---

### El papel de Python

Python actuará como el cerebro externo del robot.

Desde nuestros programas podremos:

- leer sensores;
- consultar posiciones;
- calcular decisiones;
- enviar órdenes de movimiento;
- registrar datos;
- mostrar información por pantalla.

CoppeliaSim, por su parte, se encargará de simular el comportamiento físico del robot y del entorno.

La combinación de ambos nos permitirá construir aplicaciones cada vez más completas.

::: summary
title: Idea clave

content:

Un robot autónomo necesita combinar percepción y acción.

Los sensores proporcionan información del entorno, pero será el programa de control quien decida cómo debe responder el robot ante cada situación.

:::

---

### Lo que viene a continuación

En el próximo capítulo empezaremos a controlar el movimiento del Pioneer P3DX utilizando sus ruedas.

Dejaremos de modificar directamente la posición del robot y comenzaremos a enviar órdenes a sus motores.

Ese cambio será muy importante.

A partir de entonces el robot se desplazará de forma mucho más realista, igual que lo haría una plataforma móvil física.

Cuando combinemos ese movimiento con los sensores estudiados en este capítulo, estaremos preparados para construir nuestro primer comportamiento autónomo de evitación de obstáculos.

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Sensor | Dispositivo capaz de obtener información del entorno del robot. |
| Sensor de proximidad | Sensor que detecta la presencia de objetos cercanos sin necesidad de contacto físico. |
| Percepción | Proceso mediante el cual un robot obtiene información del entorno. |
| Actuador | Elemento encargado de producir una acción física, como el movimiento de las ruedas. |
| Volumen de detección | Región del espacio donde un sensor es capaz de detectar objetos. |
| Alcance | Distancia máxima a la que un sensor puede detectar un objeto. |
| Ángulo de detección | Apertura del volumen de detección de un sensor. |
| `readProximitySensor()` | Función de la API remota utilizada para leer un sensor de proximidad. |
| Detección | Resultado que indica si existe un objeto dentro del volumen de detección. |
| Distancia de seguridad | Distancia mínima establecida para reaccionar ante un obstáculo. |
| Toma de decisiones | Proceso mediante el cual el programa decide cómo actuar utilizando la información de los sensores. |
| Navegación autónoma | Capacidad de un robot para desplazarse reaccionando ante el entorno. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender la importancia de los sensores en robótica móvil.
- ✅ Diferenciar entre sensores y actuadores.
- ✅ Explicar el funcionamiento básico de un sensor de proximidad.
- ✅ Identificar los sensores del Pioneer P3DX.
- ✅ Obtener la referencia de un sensor mediante la API remota.
- ✅ Leer un sensor utilizando `readProximitySensor()`.
- ✅ Interpretar correctamente los datos devueltos por el sensor.
- ✅ Detectar obstáculos desde un programa Python.
- ✅ Utilizar una distancia de seguridad para clasificar diferentes situaciones.

A partir de este momento el Pioneer P3DX ya no es un robot "ciego".

Ahora dispone de información suficiente para comenzar a tomar decisiones.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Cuál es la diferencia entre un sensor y un actuador?
2. ¿Qué información proporciona un sensor de proximidad?
3. ¿Qué significa que un objeto esté fuera del volumen de detección?
4. ¿Para qué sirve la función `readProximitySensor()`?
5. ¿Qué información devuelve esta función?
6. ¿Por qué resulta útil definir una distancia de seguridad?
7. ¿Qué diferencia existe entre detectar un obstáculo y reaccionar ante él?
8. ¿Por qué un sensor, por sí solo, no puede tomar decisiones?

Si puedes responder correctamente a todas ellas, estás preparado para continuar.

---

## Práctica guiada

::: practice
title: Detectando obstáculos con el Pioneer P3DX

difficulty: Baja

time: 50 minutos

content:

Realiza las siguientes actividades.

1. Crea una escena nueva.
2. Inserta un Pioneer P3DX.
3. Coloca varios cubos delante del robot a diferentes distancias.
4. Obtén la referencia del sensor frontal.
5. Lee el estado del sensor utilizando `readProximitySensor()`.
6. Muestra por pantalla si existe o no un obstáculo.
7. Muestra también la distancia detectada.
8. Define una distancia de seguridad de 50 centímetros.
9. Modifica el programa para distinguir entre:
   - Camino libre.
   - Obstáculo lejano.
   - Obstáculo cercano.
10. Repite el experimento modificando la posición de los cubos.

Comprueba cómo cambian las lecturas del sensor al variar la distancia entre el robot y el obstáculo.

:::

---

## Reto

::: challenge
title: ¿Qué sensor detecta primero?

content:

Coloca un obstáculo delante del Pioneer P3DX.

Ahora desplázalo lentamente desde el lado izquierdo hacia el lado derecho del robot.

Observa qué sensores comienzan a detectar el obstáculo durante el recorrido.

Intenta responder:

- ¿Qué sensor detecta primero el objeto?
- ¿En qué momento dejan de detectarlo los sensores frontales?
- ¿Qué sensores continúan detectándolo cuando el obstáculo se desplaza hacia un lateral?

Este ejercicio te ayudará a comprender cómo colaboran varios sensores para construir una percepción completa del entorno.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender el funcionamiento de los sensores de proximidad.
- Introducir la lectura de sensores mediante la API remota.
- Interpretar correctamente las medidas obtenidas.
- Relacionar la percepción del entorno con la toma de decisiones.

**Material necesario**

- CoppeliaSim.
- Python con la API remota ZeroMQ configurada.
- Pioneer P3DX.
- Cubos u otros obstáculos sencillos.

**Consejos metodológicos**

Insiste en que los sensores únicamente proporcionan información.

La inteligencia del robot no reside en los sensores, sino en el programa que interpreta sus lecturas.

Es recomendable que el alumnado experimente modificando la posición de los obstáculos y observando cómo cambian las medidas obtenidas.

Evita introducir todavía algoritmos de navegación.

El objetivo de este capítulo consiste únicamente en comprender el proceso de percepción.

:::

---

## Próximo capítulo

Ya sabemos cómo obtener información del entorno utilizando los sensores del Pioneer P3DX.

Ha llegado el momento de utilizar esa información para controlar el movimiento del robot.

En el siguiente capítulo aprenderemos a manejar los motores del Pioneer P3DX, controlar la velocidad de cada rueda y desarrollar nuestro primer algoritmo de evitación de obstáculos.

Será el momento en el que percepción y movimiento comiencen a trabajar conjuntamente para construir un robot verdaderamente autónomo.

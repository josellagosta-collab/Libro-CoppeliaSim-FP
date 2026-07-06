::: chapter-cover
number: 21
title: Proyecto industrial completo con el UR3
time: 8 horas
level: ★★★★★ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Diseñar una célula robotizada utilizando CoppeliaSim.
- Integrar un UR3 con sensores y una cinta transportadora.
- Coordinar el movimiento del robot con la llegada de piezas.
- Desarrollar un ciclo automático completo de manipulación.
- Organizar una aplicación industrial mediante programación modular en Python.
- Comprender la estructura general de una célula robotizada similar a las utilizadas en la industria.

:::

# Capítulo 21 · Proyecto industrial completo con el UR3

## Del robot aislado a la célula robotizada

En el capítulo anterior aprendimos a controlar el **UR3** para realizar operaciones de **pick & place**.

El robot era capaz de recoger una pieza, transportarla y depositarla en otra posición.

Sin embargo, en una fábrica real el robot rara vez trabaja de forma aislada.

Habitualmente forma parte de una instalación mucho más amplia en la que intervienen otros elementos, como cintas transportadoras, sensores, cámaras de visión artificial y sistemas de control.

Todos estos dispositivos colaboran para realizar un proceso automático de forma coordinada.

En este capítulo construiremos una célula robotizada inspirada en una instalación industrial real, integrando el **UR3** con otros componentes para desarrollar un proceso completo de manipulación.

::: figure
image: ../assets/cap21/fig21_1.png
caption: Célula robotizada formada por un UR3, una cinta transportadora y un puesto de depósito.
:::

::: teacher
content:

Antes de comenzar el proyecto, muestra al alumnado fotografías o vídeos de células robotizadas reales.

El objetivo es que identifiquen los distintos elementos que las componen y comprendan que el robot constituye únicamente una parte del sistema de automatización.

:::

---

## 21.1 Arquitectura de la célula robotizada

La aplicación que desarrollaremos durante este capítulo estará formada por cuatro elementos principales.

- Un **UR3**, encargado de manipular las piezas.
- Una **cinta transportadora**, que suministrará los objetos.
- Un **sensor de presencia**, que detectará la llegada de cada pieza.
- Una **zona de depósito**, donde el robot dejará los objetos una vez manipulados.

Aunque se trata de una célula simplificada, reproduce la estructura utilizada en numerosas aplicaciones industriales de clasificación, empaquetado y alimentación de máquinas.

::: figure
image: ../assets/cap21/fig21_2.png
caption: Componentes principales de la célula robotizada desarrollada en este capítulo.
:::

---

### El flujo de trabajo

La secuencia general de funcionamiento será la siguiente:

1. La cinta transportadora desplaza una pieza hasta la zona de trabajo.
2. El sensor detecta la presencia del objeto.
3. El UR3 espera la confirmación del sensor.
4. El robot recoge la pieza mediante la pinza.
5. La transporta hasta la zona de depósito.
6. El ciclo vuelve a comenzar con la siguiente pieza.

Este comportamiento reproduce el funcionamiento de muchas células robotizadas utilizadas en procesos de producción automatizados.

---

### Un proyecto integrador

Este capítulo no introduce únicamente nuevos componentes.

Su principal objetivo consiste en integrar todos los conocimientos adquiridos durante la Parte IV.

A lo largo del proyecto utilizaremos:

A lo largo del proyecto utilizaremos:

- control de articulaciones;
- cinemática inversa;
- coordenadas cartesianas;
- los objetos auxiliares `UR3_tip` y `UR3_target`, creados y configurados en el capítulo anterior;
- control de la pinza **RG2**;
- trayectorias seguras;
- programación modular;
- ciclos automáticos.

Partiremos de la escena obtenida al finalizar el capítulo 20. Si tu modelo de **UR3** no incorpora de forma predeterminada los objetos `UR3_tip` y `UR3_target`, recuerda crearlos y configurarlos mediante el sistema de cinemática inversa, tal como se explicó en dicho capítulo.

Al finalizar el capítulo habrás construido una aplicación muy próxima a las que pueden encontrarse en un entorno industrial real.

::: common-error
content:

Antes de comenzar a programar, asegúrate de que todos los elementos de la célula están correctamente posicionados.

Una mala ubicación de la cinta transportadora o de la zona de depósito puede impedir que el UR3 alcance las piezas o provocar colisiones durante la manipulación.

:::

::: common-error
content:

Antes de comenzar este proyecto, verifica que la pinza **RG2** está correctamente ensamblada con el robot mediante la herramienta **Assemble / Disassemble**.

Comprueba también que la simulación se encuentra en ejecución antes de intentar controlar la pinza desde Python.

Si la pinza no está ensamblada correctamente o la simulación está detenida, el programa puede ejecutarse sin errores aparentes, pero la pinza no responderá como se espera.

:::

---

## 21.2 Construyendo la célula robotizada

Antes de comenzar a programar debemos preparar la escena que utilizaremos durante todo el proyecto.

En una instalación industrial real, la programación siempre comienza con el diseño de la célula y la correcta ubicación de todos sus componentes.

En CoppeliaSim seguiremos exactamente el mismo procedimiento.

Nuestro objetivo será construir una escena sencilla, pero suficientemente completa para desarrollar una aplicación de automatización industrial.

---

### Elementos necesarios

La célula robotizada estará formada por los siguientes componentes:

- Un robot **UR3**.
- Una cinta transportadora.
- Un sensor de presencia.
- Varias piezas para manipular.
- Una mesa o bandeja de depósito.
- El suelo de la instalación.

Cada uno de estos elementos desempeñará una función concreta dentro del proceso automático.

::: figure
image: ../assets/cap21/fig21_3.png
caption: Elementos principales que componen la escena del proyecto industrial.
:::

---

## Distribución de la escena

Una buena distribución facilita enormemente la programación posterior.

Para este proyecto utilizaremos la siguiente organización:

- La cinta transportadora se situará a la izquierda del robot.
- El UR3 ocupará la zona central de la célula.
- La bandeja de depósito se colocará a la derecha.
- El sensor de presencia se instalará junto al final de la cinta transportadora.
- Las piezas llegarán desde la izquierda hacia la zona de recogida.

Esta disposición permitirá que el robot alcance todas las posiciones sin aproximarse a los límites de su espacio de trabajo.

::: figure
image: ../assets/cap21/fig21_4.png
caption: Distribución recomendada de los elementos dentro de la célula robotizada.
:::

---

### Organizando el árbol de la escena

A medida que aumenta el número de objetos, el árbol de la escena comienza a crecer rápidamente.

Por este motivo resulta recomendable asignar nombres descriptivos desde el principio.

Una posible organización podría ser la siguiente:

```text
CelulaRobotizada
│
├── UR3
│   ├── Script
│   ├── joint
│   └── ...
│
├── RG2
│   ├── openCloseJoint
│   └── ...
│
├── UR3_tip
├── UR3_target
│
├── Conveyor
├── PresenceSensor
├── DepositTray
│
├── Piece_01
├── Piece_02
└── Piece_03

```

Esta organización reproduce la escena utilizada a lo largo del libro.

El robot mantiene su estructura interna, mientras que la pinza **RG2** aparece ensamblada con el UR3. Los objetos auxiliares `UR3_tip` y `UR3_target` permiten controlar la cinemática inversa desde Python.

Recuerda que los nombres de los objetos pueden variar ligeramente según la escena utilizada. Si has empleado nombres diferentes, deberás utilizarlos también en tu programa.

---

### Preparando las piezas

Para simplificar el proyecto utilizaremos inicialmente piezas cúbicas idénticas.

Más adelante podremos sustituirlas por piezas de diferentes tamaños, colores o formas para desarrollar aplicaciones de clasificación.

Todas las piezas deberán situarse sobre la cinta transportadora respetando una separación suficiente para que el UR3 pueda manipularlas individualmente.

---

### Buenas prácticas de diseño

Antes de empezar a programar conviene revisar algunos aspectos importantes.

- Comprueba que el UR3 puede alcanzar cómodamente la posición de recogida.
- Evita colocar la cinta demasiado cerca de la base del robot.
- Mantén despejada la zona situada sobre la bandeja de depósito.
- Deja espacio suficiente entre las piezas.
- Utiliza nombres descriptivos para todos los objetos de la escena.

Una escena correctamente organizada simplificará considerablemente el desarrollo del proyecto.

::: teacher
content:

Dedica unos minutos a revisar la escena creada por el alumnado antes de comenzar la programación.

La mayoría de los problemas posteriores suelen deberse a una mala colocación de los elementos o a una organización deficiente del árbol de la escena.

:::

---

## Preparando la programación

Con la escena completamente construida ya disponemos de todos los elementos necesarios para comenzar a desarrollar la aplicación.

En el siguiente apartado aprenderemos a conectar Python con cada uno de los componentes de la célula robotizada, obteniendo los *handles* del robot, la cinta transportadora y el sensor de presencia para construir el primer ciclo automático completo.

---

## 21.3 Conectando Python con la célula robotizada

Una vez construida la escena, el siguiente paso consiste en establecer la comunicación entre Python y los diferentes elementos de la célula.

Hasta ahora habíamos trabajado principalmente con el **UR3** y el objeto auxiliar `UR3_target`.

En este proyecto necesitaremos controlar varios dispositivos de forma coordinada.

Nuestro programa deberá interactuar con:

- el robot UR3;
- la pinza;
- la cinta transportadora;
- el sensor de presencia.

El primer paso será obtener el *handle* de cada uno de estos objetos.

---

### Obteniendo los identificadores

Como ya vimos en capítulos anteriores, todos los objetos de CoppeliaSim disponen de un identificador único.

Estos identificadores permiten acceder a cada elemento desde Python.

```python
ur3 = sim.getObject('/UR3')
target = sim.getObject('/UR3_target')
rg2 = sim.getObject('/RG2')
conveyor = sim.getObject('/Conveyor')
sensor = sim.getObject('/PresenceSensor')
```

En este libro utilizaremos los nombres empleados en nuestra escena de trabajo (`UR3`, `UR3_target`, `RG2`, `Conveyor` y `PresenceSensor`).

Si en tu escena alguno de estos objetos tiene un nombre diferente, deberás utilizar ese mismo nombre en las llamadas a `sim.getObject()`.

Una vez almacenados estos *handles*, el programa podrá controlar cada componente de forma independiente.

::: figure
image: ../assets/cap21/fig21_5.png
caption: Obtención de los *handles* de los principales elementos de la célula robotizada.
:::

---

## Inicializando la aplicación

Una buena práctica consiste en realizar toda la inicialización al comienzo del programa.

En esta fase se obtienen los identificadores y se comprueba que todos los componentes están disponibles.

Si alguno de ellos no existe o ha sido renombrado, el error aparecerá inmediatamente, facilitando su localización.

```python
def inicializar():

    global ur3
    global target
    global rg2
    global conveyor
    global sensor

    ur3 = sim.getObject('/UR3')
    target = sim.getObject('/UR3_target')
    rg2 = sim.getObject('/RG2') 
    conveyor = sim.getObject('/Conveyor')
    sensor = sim.getObject('/PresenceSensor')
```

Organizar el código de esta forma facilitará enormemente el mantenimiento del proyecto.

Los nombres utilizados corresponden a la escena desarrollada en este libro. Si has utilizado nombres diferentes para la pinza, la cinta transportadora o cualquier otro objeto, recuerda actualizar también las llamadas a `sim.getObject()`.

---

## Dividiendo el programa en funciones

En una aplicación sencilla podríamos escribir todas las instrucciones seguidas.

Sin embargo, conforme aumenta la complejidad de la célula, esta estrategia deja de ser práctica.

Por ello organizaremos el programa en pequeñas funciones, cada una encargada de una tarea concreta.

Por ejemplo:

- iniciar la aplicación;
- mover el robot;
- controlar la apertura y cierre de la pinza RG2;
- leer el sensor;
- controlar la cinta;
- ejecutar un ciclo completo.

Esta organización hace que el código resulte mucho más claro y reutilizable.

::: figure
image: ../assets/cap21/fig21_6.png
caption: Organización modular del programa que controla la célula robotizada.
:::

---

### Un programa más fácil de mantener

La programación modular ofrece numerosas ventajas.

- Cada función realiza una única tarea.
- Los errores son más fáciles de localizar.
- Es posible reutilizar funciones en otros proyectos.
- El código resulta más legible.
- La ampliación del programa es mucho más sencilla.

Este enfoque es el mismo que emplean los integradores de sistemas cuando desarrollan aplicaciones para robots industriales.

::: teacher
content:

Pide al alumnado que compruebe los nombres de todos los objetos en el árbol de la escena antes de ejecutar el programa.

Un nombre incorrecto suele ser la causa más frecuente de errores al utilizar `sim.getObject()`.

:::

---

## Preparando el primer ciclo automático

Antes de integrar todos los elementos en un único programa es recomendable comprobar de forma independiente que:

- el UR3 responde correctamente a los movimientos;
- la pinza RG2 abre y cierra sin problemas;
- la cinta transportadora funciona correctamente;
- el sensor detecta el paso de las piezas.

Una vez verificados todos los subsistemas será mucho más sencillo localizar posibles errores durante la integración.

Ya disponemos de todos los elementos necesarios para controlar la célula robotizada desde Python.

En el siguiente apartado integraremos la cinta transportadora, el sensor de presencia y el UR3 para desarrollar el primer ciclo completamente automático, en el que el robot esperará la llegada de una pieza antes de recogerla y depositarla en la bandeja de salida.

---

## 21.4 Coordinando la cinta transportadora y el UR3

Hasta ahora todos los movimientos del robot comenzaban en un instante determinado por nuestro programa.

Sin embargo, en una instalación industrial real el robot no decide cuándo debe iniciar una operación.

Normalmente permanece esperando hasta que una nueva pieza llega a la zona de trabajo.

En nuestra célula robotizada ese momento será detectado mediante un **sensor de presencia** situado al final de la cinta transportadora.

A partir de ese instante comenzará automáticamente el ciclo de manipulación.

---

### El funcionamiento de la célula

La secuencia completa será la siguiente:

1. La cinta transportadora desplaza una pieza.
2. El sensor detecta su llegada.
3. La cinta se detiene.
4. El UR3 recoge la pieza.
5. El robot la deposita en la bandeja de salida.
6. La cinta vuelve a ponerse en marcha para transportar la siguiente pieza.

Esta forma de trabajar permite sincronizar todos los elementos de la instalación sin intervención del operador.

::: figure
image: ../assets/cap21/fig21_7.png
caption: Secuencia de coordinación entre la cinta transportadora, el sensor de presencia y el UR3.
:::

---

## Detectando la llegada de una pieza

El sensor de presencia supervisa continuamente la zona situada al final de la cinta transportadora.

Cuando una pieza entra en su área de detección, el sensor cambia de estado.

Nuestro programa comprobará periódicamente este estado para decidir cuándo debe comenzar el ciclo de manipulación.

En pseudocódigo, el comportamiento sería el siguiente:

```text
Mientras la simulación esté activa

    Si el sensor detecta una pieza

        detener la cinta

        ejecutar pick_and_place()

        volver a arrancar la cinta
```

Esta lógica constituye el núcleo de numerosas aplicaciones de automatización industrial.

---

## Esperando un evento

Hasta ahora nuestros programas ejecutaban instrucciones de forma secuencial.

En esta aplicación, el robot pasa gran parte del tiempo **esperando**.

Solo actuará cuando el sensor indique que existe una pieza disponible.

Este tipo de programación, basada en eventos, resulta muy habitual en sistemas automáticos.

Permite reducir movimientos innecesarios y coordinar distintos equipos de manera eficiente.

::: figure
image: ../assets/cap21/fig21_8.png
caption: El UR3 permanece en espera hasta que el sensor detecta una nueva pieza.
:::

---

### Ventajas de este enfoque

Coordinar el robot mediante sensores ofrece numerosas ventajas.

- El robot solo trabaja cuando es necesario.
- Se evita recoger piezas inexistentes.
- El consumo energético disminuye.
- El movimiento resulta más seguro.
- La célula puede ampliarse fácilmente incorporando nuevos sensores.

Este mismo principio se utiliza en líneas de montaje, sistemas de empaquetado y estaciones automáticas de clasificación.

---

### Preparando la clasificación automática

Hasta este momento todas las piezas eran idénticas.

En la siguiente entrega incorporaremos una **cámara de visión artificial** para distinguir entre distintos tipos de piezas.

El UR3 dejará de recoger simplemente cualquier objeto que llegue por la cinta y comenzará a tomar decisiones en función de la información proporcionada por el sistema de visión.

De este modo, nuestra célula robotizada se aproximará todavía más al funcionamiento de una instalación industrial moderna.

::: teacher
content:

Antes de introducir la cámara de visión artificial, comprueba que el alumnado comprende perfectamente el funcionamiento del ciclo basado en el sensor de presencia.

Es importante que identifiquen claramente qué elemento inicia cada acción de la célula, ya que este concepto será la base para integrar posteriormente sistemas de visión y clasificación automática.

:::

---

## 21.5 Incorporando visión artificial a la célula robotizada

Hasta este momento el **UR3** recogía cualquier pieza que llegaba al final de la cinta transportadora.

Sin embargo, en una instalación industrial real no todas las piezas reciben el mismo tratamiento.

Antes de manipularlas suele ser necesario identificar sus características para decidir qué hacer con cada una de ellas.

Para ello incorporaremos una **cámara de visión artificial** situada sobre la cinta transportadora.

Su misión consistirá en inspeccionar cada pieza antes de que llegue a la zona de recogida.

::: figure
image: ../assets/cap21/fig21_9.png
caption: Cámara de visión artificial supervisando las piezas que circulan por la cinta transportadora.
:::

---

## ¿Qué información puede obtener la cámara?

La cámara instalada sobre la cinta puede proporcionar numerosos datos sobre cada pieza.

Entre los más habituales encontramos:

- color;
- forma;
- tamaño;
- posición;
- orientación;
- dimensiones.

En este proyecto utilizaremos inicialmente únicamente el **color** de la pieza para decidir su destino.

Posteriormente este mismo sistema podría ampliarse para reconocer diferentes modelos, medir dimensiones o detectar defectos de fabricación.

---

### Clasificando las piezas

Supongamos que la cámara distingue tres colores diferentes.

Nuestro sistema aplicará las siguientes reglas:

| Color detectado | Destino |
|-----------------|---------|
| Rojo | Bandeja A |
| Verde | Bandeja B |
| Azul | Bandeja C |

El UR3 modificará automáticamente la posición de depósito según la información recibida por la cámara.

De este modo, el robot dejará de repetir siempre el mismo movimiento y comenzará a tomar decisiones.

::: figure
image: ../assets/cap21/fig21_10.png
caption: Clasificación automática de piezas según el color detectado por la cámara.
:::

---

## Integrando la visión con el robot

El flujo completo de trabajo será el siguiente:

1. La pieza avanza por la cinta transportadora.
2. La cámara captura una imagen.
3. Python procesa la imagen mediante OpenCV.
4. Se identifica el color de la pieza.
5. El sensor confirma la llegada del objeto.
6. El UR3 recoge la pieza.
7. El robot la deposita en la bandeja correspondiente.

Observa que la cámara y el sensor desempeñan funciones diferentes.

La cámara proporciona información sobre la **pieza**, mientras que el sensor indica **cuándo** debe comenzar la manipulación.

---

### Ventajas de combinar visión artificial y robótica

La integración de una cámara con un robot industrial aporta numerosas ventajas.

- Permite adaptar el comportamiento del robot a cada pieza.
- Reduce la necesidad de posicionamientos extremadamente precisos.
- Facilita la clasificación automática.
- Mejora la flexibilidad de la instalación.
- Permite detectar errores antes de iniciar la manipulación.

Este tipo de soluciones es habitual en líneas de montaje, sistemas logísticos y procesos de control de calidad.

::: teacher
content:

Recuerda al alumnado que la cámara no sustituye al sensor de presencia.

Ambos dispositivos colaboran durante el proceso: la cámara identifica la pieza y el sensor determina el instante adecuado para que el UR3 inicie el ciclo de manipulación.

Esta diferenciación ayudará a comprender mejor la arquitectura de las células robotizadas utilizadas en la industria.

:::

---

## Un proyecto muy próximo a la industria

Con la incorporación de la visión artificial, nuestra célula robotizada ya integra los principales elementos presentes en muchas instalaciones industriales modernas:

- un robot colaborativo **UR3**;
- una pinza de manipulación;
- una cinta transportadora;
- un sensor de presencia;
- una cámara de visión artificial;
- un programa de control desarrollado en Python.

Observa que esta aplicación reutiliza todos los conocimientos desarrollados en los capítulos anteriores.

Primero aprendimos a controlar las articulaciones del UR3, después utilizamos la cinemática inversa mediante `UR3_target`, posteriormente integramos la pinza RG2 y, finalmente, incorporamos sensores, cintas transportadoras y visión artificial para construir una célula robotizada completa.

El proyecto desarrollado a lo largo de este capítulo constituye una excelente aproximación a una célula de automatización real y demuestra cómo integrar percepción, decisión y manipulación dentro de una única aplicación.

En la siguiente y última entrega del capítulo realizaremos una práctica guiada completa, repasaremos los conceptos fundamentales y propondremos un reto final que servirá como cierre de la Parte IV del libro.

---

## 21.6 Práctica guiada: Desarrollo de una célula robotizada completa

En esta práctica integrarás todos los conocimientos adquiridos durante la Parte IV para construir una célula robotizada completa utilizando **CoppeliaSim**, **Python** y el robot **UR3**.

El objetivo será desarrollar una aplicación capaz de detectar, clasificar y manipular automáticamente diferentes piezas.

::: practice
title: Proyecto final de robótica industrial

difficulty: Alta

time: 120 minutos

content:

Realiza las siguientes actividades:

1. Crea una nueva escena en CoppeliaSim.
2. Inserta el robot UR3 y verifica su funcionamiento.
3. Añade una cinta transportadora.
4. Coloca un sensor de presencia al final de la cinta.
5. Incorpora una cámara de visión artificial sobre la zona de inspección.
6. Sitúa varias piezas de distintos colores sobre la cinta.
7. Obtén desde Python los *handles* de todos los elementos de la célula.
8. Comprueba que la pinza RG2 abre y cierra correctamente antes de iniciar el ciclo automático.
9. Programa el movimiento del UR3 mediante posiciones de aproximación y recogida.
10. Procesa la imagen capturada por la cámara para identificar el color de cada pieza.
11. Deposita automáticamente cada pieza en la bandeja correspondiente.

Una vez finalizada la práctica, el robot deberá ejecutar de forma completamente automática un ciclo continuo de clasificación de piezas.

:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición |
|-----------|------------|
| Célula robotizada | Conjunto de dispositivos que trabajan coordinadamente para automatizar un proceso. |
| Cinta transportadora | Sistema encargado de suministrar piezas al robot. |
| Sensor de presencia | Detecta la llegada de una pieza a la zona de trabajo. |
| Cámara de visión artificial | Captura imágenes para identificar características de las piezas. |
| Clasificación automática | Proceso de separación de objetos según determinados criterios. |
| Pick & Place | Operación de recogida y depósito realizada por el robot. |
| Programación modular | Organización del programa en funciones reutilizables. |
| Ciclo automático | Secuencia repetitiva que permite el funcionamiento continuo de la instalación. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Diseñar una célula robotizada completa utilizando CoppeliaSim.
- ✅ Integrar un robot UR3 con una cinta transportadora.
- ✅ Utilizar sensores para iniciar automáticamente un proceso.
- ✅ Incorporar una cámara de visión artificial al sistema.
- ✅ Clasificar piezas utilizando Python y OpenCV.
- ✅ Coordinar todos los elementos mediante programación modular.
- ✅ Desarrollar un proyecto de automatización inspirado en una aplicación industrial real.

Con este capítulo concluye la **Parte IV** del libro, dedicada a la robótica industrial y la manipulación.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Cuál es la función de una cinta transportadora dentro de una célula robotizada?
2. ¿Qué diferencia existe entre un sensor de presencia y una cámara de visión artificial?
3. ¿Por qué es recomendable utilizar posiciones de aproximación durante la manipulación?
4. ¿Qué ventajas aporta organizar el programa en funciones?
5. ¿Cómo decide el UR3 en qué bandeja debe depositar cada pieza?
6. ¿Qué ocurriría si el sensor detectara una pieza antes de que el robot hubiera finalizado el ciclo anterior?
7. ¿Qué modificaciones realizarías para clasificar las piezas por tamaño en lugar de por color?

Si puedes responder correctamente a todas ellas, estás preparado para abordar proyectos de integración robótica más complejos.

---

## Reto

::: challenge
title: Clasificación multicriterio

content:

Amplía la célula robotizada para clasificar las piezas utilizando **dos criterios simultáneamente**.

Por ejemplo:

- color;
- tamaño.

El UR3 deberá decidir automáticamente la bandeja de destino en función de ambas características.

Como ampliación, incorpora un contador de piezas clasificadas y muestra el resultado en la consola de Python al finalizar cada ciclo.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Tres sesiones de 55 minutos.

**Objetivos**

- Integrar todos los conocimientos adquiridos durante la Parte IV.
- Desarrollar una aplicación robotizada inspirada en una instalación industrial real.
- Consolidar la programación modular y la coordinación entre robot, sensores y visión artificial.

**Material necesario**

- CoppeliaSim.
- Python.
- OpenCV.
- Escena del UR3 utilizada durante el capítulo.

**Consejos metodológicos**

Antes de comenzar la programación completa, verifica que cada subsistema funciona de forma independiente:

- movimiento del UR3;
- control de la pinza;
- funcionamiento de la cinta;
- lectura del sensor;
- captura de imágenes con la cámara.

Una vez comprobados todos los elementos, procede a integrarlos progresivamente hasta obtener una célula robotizada completamente funcional.

:::

---

## Cierre de la Parte IV

Durante esta parte del libro hemos recorrido el mismo camino que sigue un técnico de automatización cuando comienza a trabajar con robots industriales.

Primero conocimos la estructura del **UR3** y aprendimos a controlar sus articulaciones.

Después estudiamos la cinemática, comprendimos cómo mover el efector final mediante coordenadas cartesianas y desarrollamos nuestras primeras operaciones de **pick & place**.

Finalmente, integramos todos estos conocimientos en una célula robotizada completa, combinando robot, pinza, sensores, cinta transportadora y visión artificial para resolver un problema de automatización similar a los que pueden encontrarse en una fábrica moderna.

Esta progresión demuestra que la robótica industrial no consiste únicamente en mover un brazo robótico, sino en coordinar múltiples dispositivos para construir sistemas automáticos capaces de percibir, decidir y actuar sobre su entorno.

---

## Próxima parte

En la **Parte V · Integración de sistemas robóticos**, el siguiente paso será conectar CoppeliaSim con aplicaciones externas y tecnologías utilizadas en la Industria 4.0.

Aprenderás a intercambiar información con programas desarrollados en Python, utilizar protocolos de comunicación industrial, introducir **ROS 2**, trabajar con **OPC UA**, **MQTT** y desarrollar auténticos **gemelos digitales**, llevando los proyectos realizados hasta ahora a un entorno profesional completamente conectado.

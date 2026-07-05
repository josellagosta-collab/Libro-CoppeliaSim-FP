::: chapter-cover
number: 27
title: Diseño de una célula robotizada
time: 4 horas
level: ⭐⭐⭐⭐☆ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué es una célula robotizada.
- Analizar un problema industrial antes de construir la simulación.
- Seleccionar los elementos principales de una célula robótica.
- Diseñar una escena inicial en CoppeliaSim.
- Distribuir robots, sensores, cintas y zonas de trabajo.
- Identificar criterios básicos de seguridad en una célula automatizada.
- Preparar un proyecto completo que integre contenidos de capítulos anteriores.
:::

# Capítulo 27 · Diseño de una célula robotizada

### ¿Por qué diseñar una célula robotizada completa?

Hasta este punto del libro hemos aprendido a utilizar CoppeliaSim de forma progresiva.

Primero conocimos el entorno de simulación.

Después trabajamos con robots móviles, sensores, visión artificial, brazos industriales, manipulación de objetos y comunicación con sistemas externos.

Ahora damos un paso más.

En esta última parte del libro no vamos a estudiar conceptos aislados.

Vamos a integrarlos en proyectos completos.

Una célula robotizada representa muy bien esta idea, porque combina en un mismo espacio:

- un robot;
- una tarea industrial;
- objetos que deben manipularse;
- sensores;
- zonas de entrada y salida;
- elementos de seguridad;
- lógica de control;
- comunicación con otros sistemas.

El objetivo de este capítulo no es empezar colocando objetos al azar en una escena.

Antes de construir nada en CoppeliaSim debemos aprender a pensar como se haría en un proyecto real.

Primero analizamos el problema.

Después decidimos qué elementos necesitamos.

Finalmente diseñamos la célula de forma ordenada.

::: teacher
content:

Este capítulo debe plantearse como el inicio de un proyecto completo.

Conviene insistir en que una buena simulación no empieza abriendo CoppeliaSim, sino definiendo correctamente qué problema queremos resolver.

El alumnado debe acostumbrarse a justificar cada elemento que incorpora a la escena.
:::

---

## 27.1 Qué es una célula robotizada

Una **célula robotizada** es un espacio de trabajo en el que uno o varios robots realizan una tarea automática dentro de un entorno controlado.

Puede tratarse de una célula muy sencilla, formada únicamente por un robot y una mesa de trabajo, o de una instalación mucho más compleja con cintas transportadoras, sensores, cámaras, pinzas, PLC, bases de datos y sistemas de supervisión.

En la industria encontramos células robotizadas dedicadas a tareas como:

- recoger y colocar piezas;
- clasificar productos;
- alimentar máquinas;
- paletizar cajas;
- inspeccionar objetos mediante visión artificial;
- separar piezas defectuosas;
- preparar pedidos;
- colaborar con otros sistemas de automatización.

Aunque cada aplicación es diferente, todas comparten una misma idea: el robot no trabaja aislado.

El robot forma parte de un sistema.

Por eso, al diseñar una célula robotizada debemos pensar en el conjunto completo y no únicamente en el brazo robótico.

::: figure
image: ../assets/cap27/fig27_1.png
caption: Elementos principales de una célula robotizada industrial.
:::

Una célula bien diseñada debe permitir que el flujo de trabajo sea claro.

Los objetos entran por una zona determinada, son detectados por sensores, el robot actúa sobre ellos y finalmente salen por otra zona o quedan almacenados en una posición concreta.

Este recorrido debe poder explicarse de forma sencilla.

Si no podemos explicar cómo circulan los objetos dentro de la célula, probablemente el diseño todavía no está suficientemente maduro.

---

## 27.2 Antes de abrir CoppeliaSim: analizar el problema

Un error frecuente cuando se empieza a trabajar con simuladores consiste en abrir el programa y comenzar a colocar elementos sin una planificación previa.

Esto puede parecer rápido al principio, pero suele provocar escenas desordenadas, difíciles de modificar y poco realistas.

En un proyecto robótico conviene responder primero a varias preguntas.

::: table
caption: Preguntas iniciales para diseñar una célula robotizada.
content:

| Pregunta | Finalidad |
|----------|-----------|
| ¿Qué tarea debe realizar el robot? | Define el objetivo principal del proyecto. |
| ¿Qué objetos va a manipular o detectar? | Permite decidir tamaños, formas, materiales y posiciones. |
| ¿Desde dónde entran los objetos? | Ayuda a diseñar la zona de alimentación. |
| ¿Dónde deben terminar los objetos? | Permite definir zonas de salida, clasificación o almacenamiento. |
| ¿Qué sensores son necesarios? | Determina cómo sabrá el sistema lo que ocurre. |
| ¿Qué robot o mecanismo resulta adecuado? | Relaciona la tarea con el alcance y las capacidades del robot. |
| ¿Qué riesgos pueden aparecer? | Introduce criterios básicos de seguridad. |
:::

Estas preguntas nos obligan a pensar antes de construir.

En este capítulo diseñaremos una célula sencilla, pero suficientemente completa para integrar muchos de los contenidos trabajados en capítulos anteriores.

La idea general será crear una célula en la que varios objetos lleguen a una zona de trabajo, sean detectados y posteriormente manipulados por un robot.

Más adelante podremos ampliar este diseño incorporando visión artificial, comunicación con Python, registro de datos o integración con sistemas industriales.

::: figure
image: ../assets/cap27/fig27_2.png
caption: Análisis previo del flujo de trabajo antes de construir la célula en CoppeliaSim.
:::

Antes de pasar a la construcción de la escena, debemos tener claro el recorrido básico de los objetos.

En nuestro caso trabajaremos con una estructura inicial formada por:

- una zona de entrada;
- una zona de detección;
- una zona de trabajo del robot;
- una zona de salida o clasificación;
- sensores que informen del estado del proceso;
- un robot encargado de realizar la manipulación.

Esta planificación inicial será la base sobre la que construiremos la célula robotizada en CoppeliaSim durante las siguientes entregas.

---

## 27.3 Selección de los elementos de la célula robotizada

Una vez definido el objetivo del proyecto, el siguiente paso consiste en decidir qué elementos formarán parte de la célula robotizada.

En una instalación industrial real esta selección depende de numerosos factores, como el tipo de pieza, el peso, el tiempo de ciclo, el espacio disponible o el presupuesto. En nuestro caso, al tratarse de una simulación didáctica, escogeremos únicamente aquellos componentes necesarios para comprender el funcionamiento global del sistema.

La célula que construiremos a lo largo de este capítulo estará formada por los siguientes elementos:

- un brazo robótico industrial;
- una cinta transportadora para el movimiento de las piezas;
- sensores fotoeléctricos para detectar la presencia de objetos;
- una cámara de visión artificial (que incorporaremos en capítulos posteriores del proyecto);
- un panel de control industrial;
- un vallado de seguridad;
- cajas de entrada y salida de piezas.

Esta configuración reproduce una arquitectura muy habitual en las líneas de producción automatizadas y servirá como base para los proyectos que desarrollaremos durante el resto de la Parte VI.

::: figure
image: ../assets/cap27/fig27_3.png
caption: Componentes que formarán la célula robotizada desarrollada durante el proyecto.
:::

No es necesario que todos estos elementos sean operativos desde el primer momento.

Durante las siguientes entregas iremos incorporándolos progresivamente, comprobando cómo interactúan entre sí hasta construir una instalación completamente funcional.

---

## 27.4 Distribución del espacio de trabajo

Tan importante como seleccionar los componentes es decidir dónde se colocará cada uno de ellos.

Una distribución adecuada mejora la eficiencia del proceso, reduce movimientos innecesarios y facilita las tareas de mantenimiento y supervisión.

En robótica industrial suele seguirse un flujo de trabajo lineal.

Las piezas llegan por una zona de entrada, avanzan hasta la posición de trabajo, el robot realiza la operación correspondiente y, finalmente, las deposita en una zona de salida o clasificación.

En nuestro proyecto seguiremos esta misma filosofía.

La disposición general será la siguiente:

::: table
caption: Distribución inicial de la célula robotizada.
content:

| Zona | Elementos principales | Función |
|------|-----------------------|---------|
| Entrada | Caja de alimentación y cinta transportadora | Introducir las piezas en la instalación. |
| Detección | Sensor fotoeléctrico | Detectar la llegada de cada pieza. |
| Manipulación | Robot industrial | Recoger y colocar las piezas. |
| Clasificación | Bandejas de destino | Depositar los objetos según el criterio establecido. |
| Control | Panel industrial | Supervisar el funcionamiento de la célula. |

:::

Una vez definida esta distribución resulta mucho más sencillo construir la escena en CoppeliaSim, ya que cada elemento tiene una ubicación claramente justificada.

Además, una buena organización facilita futuras ampliaciones del proyecto, como la incorporación de cámaras de visión artificial, sistemas de comunicación mediante OPC UA o cuadros de mando para monitorizar la producción.

::: figure
image: ../assets/cap27/fig27_4.png
caption: Distribución propuesta de los distintos elementos dentro de la célula robotizada.
:::

---

## 27.5 Construcción de la escena en CoppeliaSim

Una vez planificada la distribución de la célula robotizada, llega el momento de trasladar ese diseño al simulador.

Aunque CoppeliaSim permite construir una escena de muchas formas diferentes, resulta recomendable seguir siempre un método de trabajo ordenado. De esta manera evitaremos tener que reorganizar continuamente los objetos conforme el proyecto vaya creciendo.

La primera tarea consiste en crear una escena completamente nueva.

A continuación incorporaremos únicamente aquellos elementos que constituyen la estructura básica de la instalación, dejando para más adelante la configuración de sensores, cámaras, scripts y comunicaciones.

Un posible orden de construcción sería el siguiente:

1. Crear una escena vacía.
2. Insertar el suelo de trabajo.
3. Incorporar el brazo robótico.
4. Añadir la cinta transportadora.
5. Colocar las cajas de entrada y salida.
6. Situar el panel de control.
7. Instalar el vallado de seguridad.

Trabajar siguiendo este orden facilita comprobar continuamente que todos los elementos mantienen una distribución coherente.

::: figure
image: ../assets/cap27/fig27_5.png
caption: Construcción progresiva de la célula robotizada dentro de CoppeliaSim.
:::

Es recomendable guardar versiones sucesivas del proyecto conforme se incorporan nuevos componentes.

Así, si durante el desarrollo aparece algún problema, siempre podremos regresar a una versión anterior sin necesidad de reconstruir toda la escena.

::: teacher
content:

Acostumbra al alumnado a guardar una copia del proyecto al finalizar cada sesión de trabajo.

En proyectos complejos es preferible disponer de varias versiones numeradas que sobrescribir continuamente el mismo archivo.
:::

---

## 27.6 Organización de la escena

A medida que una simulación aumenta de tamaño, también lo hace el número de objetos presentes en el árbol de la escena.

Si todos los elementos permanecen al mismo nivel jerárquico, localizar un objeto concreto puede convertirse rápidamente en una tarea complicada.

Por este motivo resulta recomendable organizar la escena utilizando grupos lógicos.

Una posible estructura para nuestro proyecto podría ser la siguiente:

```text
CeldaRobotizada
│
├── Robot
│   ├── Base
│   ├── Articulaciones
│   └── Pinza
│
├── Transporte
│   ├── CintaEntrada
│   └── CintaSalida
│
├── Sensores
│   ├── SensorEntrada
│   ├── SensorZonaRobot
│   └── SensorSalida
│
├── Seguridad
│   ├── Vallado
│   └── TorreLuminosa
│
└── Control
    ├── PanelIndustrial
    └── Scripts
```

Esta organización aporta numerosas ventajas:

- facilita localizar cualquier objeto;
- simplifica la programación posterior;
- mejora el mantenimiento de la escena;
- hace más comprensible el proyecto para otros usuarios.

En proyectos industriales reales es habitual que una misma escena contenga varios cientos de objetos. Una buena organización desde el principio evita errores y reduce considerablemente el tiempo de desarrollo.

::: figure
image: ../assets/cap27/fig27_6.png
caption: Organización jerárquica recomendada para una célula robotizada en CoppeliaSim.
:::

---

## 27.7 Incorporación del robot industrial

Con la estructura general de la célula robotizada ya definida, el siguiente paso consiste en incorporar el elemento principal de la instalación: el robot industrial.

En CoppeliaSim disponemos de una amplia biblioteca de manipuladores desarrollados por distintos fabricantes. Entre ellos encontramos robots articulados de seis grados de libertad, robots SCARA, robots cartesianos y robots colaborativos.

Para este proyecto utilizaremos un robot articulado de seis ejes, ya que es la configuración más habitual en aplicaciones de manipulación industrial y ofrece la flexibilidad necesaria para realizar operaciones de recogida, transporte y colocación de piezas.

Antes de situar el robot en la escena conviene analizar cuidadosamente su ubicación.

Una posición incorrecta puede limitar el espacio de trabajo, dificultar el acceso a determinados puntos o provocar colisiones con otros elementos de la instalación.

Por este motivo, normalmente el robot se instala en una posición central que le permita alcanzar tanto la zona de entrada como la de salida con el menor número posible de movimientos.

::: figure
image: ../assets/cap27/fig27_7.png
caption: Posicionamiento inicial del robot dentro de la célula robotizada.
:::

Además de la posición, también es importante definir correctamente la orientación de la base.

Una orientación adecuada permite simplificar las trayectorias del robot y aprovechar al máximo su volumen de trabajo.

Durante esta fase todavía no realizaremos ningún movimiento automático.

Nuestro objetivo consiste únicamente en integrar correctamente el manipulador dentro de la escena y comprobar que dispone del espacio suficiente para desarrollar su trabajo.

---

## 27.8 Incorporación de sensores y elementos de seguridad

Una célula robotizada no está formada únicamente por un brazo robótico.

Para que la instalación pueda funcionar de forma autónoma resulta necesario incorporar distintos dispositivos capaces de informar del estado del proceso.

Los primeros elementos que añadiremos serán los sensores fotoeléctricos.

Estos sensores permiten detectar la presencia de piezas sobre la cinta transportadora y constituyen uno de los dispositivos más utilizados en automatización industrial.

En nuestro proyecto instalaremos sensores en tres posiciones estratégicas:

- entrada de piezas;
- zona de trabajo del robot;
- salida de la instalación.

Gracias a ellos el sistema podrá conocer en todo momento la posición aproximada de cada objeto y coordinar correctamente las diferentes operaciones.

Junto con los sensores incorporaremos también algunos elementos destinados a mejorar la seguridad de la instalación.

Entre ellos destacan:

- vallado perimetral;
- puertas de acceso;
- torre luminosa de señalización;
- panel de control con parada de emergencia.

Aunque en una simulación estos elementos no son estrictamente necesarios, incluirlos desde el principio permite representar una instalación mucho más próxima a la realidad industrial.

::: figure
image: ../assets/cap27/fig27_8.png
caption: Integración de sensores fotoeléctricos y elementos básicos de seguridad en la célula robotizada.
:::

Una vez incorporados todos estos componentes, la escena comienza a reproducir la estructura de una célula robotizada real, preparada para iniciar las primeras pruebas de funcionamiento.

---

## 27.9 Validación del diseño de la célula robotizada

Antes de comenzar a programar el comportamiento del robot resulta recomendable verificar que la célula robotizada ha sido diseñada correctamente.

En un proyecto industrial, una revisión inicial permite detectar errores de distribución, interferencias entre equipos o problemas de accesibilidad antes de invertir tiempo en el desarrollo del software de control.

En nuestro proyecto realizaremos una validación visual de todos los componentes incorporados a la escena.

Los principales aspectos que debemos comprobar son los siguientes:

- el robot dispone de espacio suficiente para realizar todos sus movimientos;
- las cintas transportadoras no interfieren con el vallado de seguridad;
- los sensores se encuentran correctamente orientados hacia la zona de detección;
- las cajas de entrada y salida permiten el acceso del robot;
- el panel de control es accesible desde el exterior de la célula;
- ningún elemento invade el volumen de trabajo del manipulador.

Una vez realizada esta comprobación, la escena estará preparada para comenzar las primeras pruebas dinámicas.

::: figure
image: ../assets/cap27/fig27_9.png
caption: Validación de la distribución y accesibilidad de los elementos de la célula robotizada.
:::

Además de la inspección visual, resulta aconsejable recorrer toda la escena desde diferentes puntos de vista utilizando la cámara de CoppeliaSim.

Esta sencilla operación permite descubrir pequeños problemas de alineación que pueden pasar desapercibidos cuando la escena se observa únicamente desde una perspectiva.

---

## 27.10 Preparación del proyecto para las siguientes fases

Con la célula robotizada completamente diseñada ya disponemos de una base sólida sobre la que desarrollar el resto del proyecto.

Aunque hasta este momento todavía no hemos programado ningún movimiento automático, sí hemos realizado una parte fundamental del trabajo: definir correctamente la arquitectura de la instalación.

Durante este proceso hemos aprendido a:

- analizar un problema industrial antes de comenzar la simulación;
- seleccionar los componentes adecuados para la aplicación;
- distribuir correctamente los diferentes elementos de la célula;
- organizar la escena siguiendo una estructura jerárquica;
- incorporar el robot, los sensores y los elementos de seguridad;
- verificar que toda la instalación presenta una distribución coherente.

Este modo de trabajar reproduce el procedimiento habitual utilizado por los ingenieros de automatización antes de iniciar la programación de una célula robotizada real.

A partir de una buena planificación resulta mucho más sencillo desarrollar posteriormente la lógica de control, los movimientos del robot y la integración con aplicaciones externas.

::: figure
image: ../assets/cap27/fig27_10.png
caption: Célula robotizada completamente preparada para comenzar su programación y puesta en marcha.
:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Célula robotizada | Espacio de trabajo donde uno o varios robots realizan tareas automatizadas junto con otros dispositivos industriales. |
| Flujo de trabajo | Secuencia ordenada de operaciones que siguen las piezas dentro de la instalación. |
| Distribución de planta (Layout) | Organización física de todos los elementos que forman la célula robotizada. |
| Robot industrial | Manipulador encargado de ejecutar las operaciones de recogida, transporte o manipulación de piezas. |
| Sensor fotoeléctrico | Dispositivo capaz de detectar la presencia de objetos mediante un haz luminoso. |
| Panel de control | Equipo utilizado para supervisar y controlar el funcionamiento de la instalación. |
| Vallado de seguridad | Protección física que delimita el área de trabajo del robot y evita accesos no autorizados. |
| Volumen de trabajo | Espacio tridimensional que el robot puede alcanzar con su efector final. |
| Organización jerárquica | Estructura lógica utilizada para ordenar los objetos dentro de la escena de CoppeliaSim. |
| Validación de la célula | Proceso de comprobación previo a la programación para verificar que la instalación está correctamente diseñada. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Analizar una aplicación antes de comenzar una simulación.
- ✅ Diseñar la distribución general de una célula robotizada.
- ✅ Seleccionar los principales componentes de una instalación industrial.
- ✅ Organizar correctamente una escena de CoppeliaSim.
- ✅ Incorporar un robot industrial dentro del proyecto.
- ✅ Distribuir sensores y elementos de seguridad.
- ✅ Validar el diseño antes de iniciar la programación.

Ya dispones de una célula robotizada completamente preparada para comenzar a desarrollar aplicaciones de manipulación industrial.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué ventajas aporta planificar una célula robotizada antes de construirla en CoppeliaSim?
2. ¿Qué criterios deben tenerse en cuenta para seleccionar el robot de una aplicación?
3. ¿Por qué es importante organizar correctamente el árbol de la escena?
4. ¿Qué función desempeñan los sensores fotoeléctricos dentro de una célula robotizada?
5. ¿Qué elementos básicos de seguridad deberían incorporarse a una instalación industrial?
6. ¿Qué aspectos conviene validar antes de comenzar la programación del robot?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a programar el comportamiento de la célula robotizada.

---

## Práctica guiada

::: practice
title: Diseño completo de una célula robotizada

difficulty: Media

time: 60 minutos

content:

Diseña una célula robotizada siguiendo la metodología presentada en este capítulo.

1. Crea una escena nueva en CoppeliaSim.
2. Inserta un brazo robótico industrial.
3. Añade una cinta transportadora.
4. Incorpora cajas de entrada y salida.
5. Sitúa tres sensores fotoeléctricos.
6. Añade un panel de control.
7. Delimita la instalación mediante un vallado de seguridad.
8. Organiza todos los objetos utilizando una estructura jerárquica.
9. Comprueba que el robot puede alcanzar todas las zonas de trabajo.
10. Guarda el proyecto para utilizarlo en los siguientes capítulos.

El objetivo de esta práctica consiste en obtener una célula robotizada correctamente organizada y preparada para comenzar su programación.
:::

---

## Reto

::: challenge
title: Diseñando una célula industrial realista

content:

Imagina que una empresa te solicita automatizar una línea de clasificación de piezas.

Diseña una propuesta indicando:

- el robot que utilizarías;
- la posición de las cintas transportadoras;
- la ubicación de los sensores;
- la disposición del vallado de seguridad;
- la posición del panel de control;
- posibles ampliaciones futuras, como cámaras de visión artificial, lectores de códigos o comunicación con un PLC.

Realiza un pequeño croquis justificando todas tus decisiones de diseño.

Compara posteriormente tu propuesta con la de otros compañeros y analiza las ventajas e inconvenientes de cada solución.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender el proceso de diseño de una célula robotizada.
- Aplicar criterios de distribución industrial.
- Familiarizar al alumnado con la planificación previa al desarrollo de una simulación.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Biblioteca de modelos de robots industriales.
- Ratón con rueda de desplazamiento.

**Consejos metodológicos**

Insista en que el objetivo principal del capítulo no consiste en programar el robot, sino en aprender a planificar correctamente una instalación industrial.

Anime al alumnado a justificar cada decisión de diseño y a debatir diferentes distribuciones de la célula robotizada.

Es recomendable comparar varias propuestas para que los estudiantes comprendan que un mismo problema puede admitir distintas soluciones correctamente diseñadas.
:::

---

## Próximo capítulo

La célula robotizada ya está completamente diseñada y preparada para comenzar a trabajar.

En el siguiente capítulo desarrollaremos un **sistema automático de clasificación**, donde integraremos el robot industrial, la cinta transportadora, los sensores y la lógica de control para construir una aplicación muy similar a las utilizadas actualmente en la industria.

Será el primer proyecto completo de manipulación automática del libro y servirá como base para los desarrollos más avanzados de los capítulos posteriores.
::: chapter-cover
number: 28
title: Sistema automático de clasificación
time: 5 horas
level: ⭐⭐⭐⭐☆ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender el funcionamiento de un sistema automático de clasificación.
- Identificar los elementos que intervienen en una célula de clasificación industrial.
- Analizar el flujo completo de una pieza dentro de la instalación.
- Diseñar la arquitectura funcional de un sistema de clasificación utilizando CoppeliaSim.
- Preparar la simulación para incorporar posteriormente la lógica de control y la programación del robot.
:::

# Capítulo 28 · Sistema automático de clasificación

### ¿Por qué construir un sistema de clasificación?

La clasificación automática de productos constituye una de las aplicaciones más habituales de la robótica industrial.

Cada día miles de instalaciones automatizadas clasifican paquetes, alimentos, componentes electrónicos o piezas mecánicas utilizando robots, sensores y sistemas de visión artificial.

Aunque desde el exterior estas instalaciones parecen muy complejas, todas comparten un mismo principio de funcionamiento: identificar cada objeto y decidir cuál debe ser su destino.

En este capítulo construiremos una célula robotizada inspirada en una aplicación industrial real.

El proyecto integrará gran parte de los conocimientos adquiridos a lo largo del libro y servirá como punto de partida para desarrollar aplicaciones de automatización mucho más completas.

::: teacher
content:

Este capítulo marca el comienzo de los proyectos integradores del libro.

Es recomendable recordar al alumnado que ya dispone de todas las herramientas necesarias para abordar una aplicación industrial completa.

El profesor puede relacionar este proyecto con ejemplos reales presentes en centros logísticos, líneas de fabricación o sistemas de clasificación automática.
:::

---

## 28.1 Funcionamiento general de un sistema de clasificación

Un sistema automático de clasificación tiene como objetivo separar los objetos que circulan por una instalación según uno o varios criterios previamente definidos.

Estos criterios pueden estar relacionados con:

- el color;
- el tamaño;
- la forma;
- el peso;
- el material;
- la presencia de defectos;
- un código de barras o un código QR.

En una instalación industrial, esta decisión suele tomarse a partir de la información proporcionada por distintos sensores o cámaras de visión artificial.

Una vez identificado el objeto, el sistema determina cuál debe ser su destino y coordina todos los dispositivos necesarios para completar la operación.

En nuestro proyecto utilizaremos una arquitectura simplificada formada por una cinta transportadora, varios sensores y un robot industrial encargado de trasladar cada pieza hasta la zona correspondiente.

::: figure
image: ../assets/cap28/fig28_1.png
caption: Funcionamiento general de un sistema automático de clasificación mediante robot industrial.
:::

Aunque inicialmente todas las piezas recorrerán el mismo camino, más adelante incorporaremos diferentes criterios de clasificación que permitirán enviarlas automáticamente a distintos destinos.

---

## 28.2 Arquitectura del proyecto

Antes de comenzar la construcción de la simulación resulta conveniente analizar cómo interactúan los diferentes elementos que formarán parte de la instalación.

Nuestro sistema estará compuesto por cinco bloques principales:

1. Alimentación de piezas.
2. Detección e identificación.
3. Manipulación mediante robot industrial.
4. Clasificación.
5. Almacenamiento de las piezas.

Cada uno de estos bloques desempeña una función concreta dentro del proceso y todos ellos deben trabajar de forma coordinada para conseguir una clasificación correcta.

La información generada por los sensores permitirá conocer el estado de cada pieza en todo momento, mientras que el robot ejecutará las acciones necesarias para completar el proceso.

Esta arquitectura modular facilitará futuras ampliaciones del proyecto, como la incorporación de cámaras de visión artificial, sistemas de comunicación industrial o bases de datos para registrar la producción.

::: figure
image: ../assets/cap28/fig28_2.png
caption: Arquitectura funcional del sistema automático de clasificación desarrollado en este capítulo.
:::

---

## 28.3 Diseño de la línea de clasificación

Una vez definida la arquitectura general del sistema, el siguiente paso consiste en diseñar la línea de clasificación dentro de CoppeliaSim.

En una instalación industrial, la distribución física de los equipos influye directamente en la productividad, la seguridad y la facilidad de mantenimiento. Por ello, antes de colocar cualquier componente resulta conveniente definir el recorrido que seguirán las piezas desde que entran en la célula hasta que abandonan la instalación.

En nuestro proyecto utilizaremos un flujo lineal, compuesto por las siguientes etapas:

1. Alimentación de las piezas.
2. Transporte mediante cinta.
3. Detección e identificación.
4. Manipulación mediante robot.
5. Clasificación.
6. Almacenamiento.

Este recorrido permitirá seguir fácilmente el estado de cada pieza durante toda la simulación y facilitará la incorporación de nuevas funcionalidades en capítulos posteriores.

::: figure
image: ../assets/cap28/fig28_3.png
caption: Distribución física de la línea de clasificación dentro de la célula robotizada.
:::

Al igual que en una instalación real, todos los elementos deberán colocarse de forma que el robot pueda acceder cómodamente a cada zona de trabajo, evitando recorridos innecesarios y posibles interferencias.

---

## 28.4 Selección de los criterios de clasificación

Una característica fundamental de cualquier sistema automático de clasificación consiste en decidir qué criterio utilizar para separar los diferentes objetos.

Dependiendo de la aplicación industrial, esta decisión puede basarse en distintas propiedades de las piezas.

Entre las más habituales encontramos:

- color;
- forma;
- tamaño;
- peso;
- material;
- código de identificación;
- presencia de defectos.

En esta primera versión del proyecto utilizaremos un criterio sencillo que nos permita concentrarnos en la lógica general del sistema sin aumentar innecesariamente su complejidad.

Más adelante incorporaremos técnicas de visión artificial y procesamiento de imágenes que permitirán realizar clasificaciones mucho más avanzadas.

La lógica general del sistema será la siguiente:

::: table
caption: Criterios básicos de clasificación utilizados en el proyecto.
content:

| Pieza detectada | Destino |
|-----------------|---------|
| Tipo A | Bandeja 1 |
| Tipo B | Bandeja 2 |
| Tipo C | Bandeja 3 |
| No identificada | Zona de rechazo |
:::

Este esquema reproduce el funcionamiento habitual de numerosas líneas de producción, donde cada producto es enviado automáticamente a una ubicación diferente en función de la información obtenida durante el proceso de inspección.

::: figure
image: ../assets/cap28/fig28_4.png
caption: Ejemplo del proceso de decisión utilizado para clasificar automáticamente las piezas.
:::

---

## 28.5 Integración del robot con el sistema de clasificación

Con la línea de clasificación completamente definida, llega el momento de integrar el robot industrial dentro del proceso.

Aunque el robot constituye el elemento más visible de la instalación, su función es únicamente ejecutar las órdenes que recibe del sistema de control. La verdadera inteligencia del proceso reside en la coordinación entre sensores, lógica de decisión y movimientos del manipulador.

Cada vez que una pieza alcanza la zona de trabajo, el sistema debe seguir una secuencia perfectamente sincronizada.

En primer lugar, los sensores detectan la llegada del objeto.

A continuación, el sistema identifica el tipo de pieza y determina cuál debe ser su destino.

Finalmente, el robot recoge el objeto y lo deposita en la bandeja correspondiente.

Esta secuencia debe repetirse continuamente para cada una de las piezas que circulan por la instalación.

::: figure
image: ../assets/cap28/fig28_5.png
caption: Secuencia completa de manipulación realizada por el robot durante el proceso de clasificación.
:::

Para conseguir un funcionamiento fluido es importante minimizar los desplazamientos innecesarios del robot.

Cuanto menor sea la distancia recorrida entre la posición de recogida y la de depósito, menor será el tiempo de ciclo y mayor la productividad de la instalación.

Por este motivo, durante el diseño de la célula resulta recomendable situar las bandejas de clasificación dentro del volumen óptimo de trabajo del manipulador.

---

## 28.6 Flujo de información del sistema

Además del movimiento físico de las piezas, en una célula robotizada circula continuamente información entre los distintos dispositivos.

Cada componente genera datos que permiten al sistema conocer el estado de la instalación en tiempo real.

El flujo básico de información sigue el siguiente recorrido:

1. El sensor detecta la presencia de una pieza.
2. La información llega al sistema de control.
3. Se determina el tipo de objeto.
4. Se calcula el destino correspondiente.
5. Se envía la orden al robot.
6. El robot ejecuta el movimiento.
7. El sistema confirma que la operación ha finalizado correctamente.

Este intercambio continuo de información constituye la base de cualquier sistema automatizado moderno.

En aplicaciones industriales reales, este flujo suele gestionarse mediante PLC, ordenadores industriales o aplicaciones desarrolladas en Python que coordinan todos los dispositivos de la instalación.

::: figure
image: ../assets/cap28/fig28_6.png
caption: Flujo de información entre sensores, sistema de control y robot industrial.
:::

Separar claramente el flujo de materiales del flujo de información facilita enormemente el diseño, el mantenimiento y la ampliación futura de la instalación.

Esta filosofía será la que utilizaremos durante el resto de proyectos desarrollados en este libro.

---

## 28.7 Optimización del tiempo de ciclo

Una vez que el sistema de clasificación funciona correctamente, el siguiente objetivo consiste en mejorar su rendimiento.

En una instalación industrial no basta con que el robot complete correctamente todas las operaciones; además, debe hacerlo en el menor tiempo posible sin comprometer la seguridad ni la precisión del proceso.

El tiempo empleado por una pieza desde que entra en la célula hasta que es depositada en su destino recibe el nombre de **tiempo de ciclo**.

Reducir este tiempo supone aumentar directamente la productividad de la instalación.

Para conseguirlo pueden aplicarse distintas estrategias:

- reducir la distancia recorrida por el robot;
- minimizar los movimientos innecesarios;
- optimizar la posición de las bandejas de clasificación;
- sincronizar correctamente la llegada de las piezas;
- evitar tiempos de espera entre operaciones.

En nuestro proyecto analizaremos el recorrido completo del robot para identificar aquellos movimientos que puedan simplificarse.

::: figure
image: ../assets/cap28/fig28_7.png
caption: Optimización del recorrido del robot para reducir el tiempo de ciclo.
:::

Una buena distribución de los elementos puede reducir considerablemente el tiempo de funcionamiento de la instalación sin necesidad de modificar la programación del robot.

Por este motivo, el diseño mecánico y la programación siempre deben desarrollarse de forma coordinada.

---

## 28.8 Supervisión del proceso de clasificación

Durante el funcionamiento de una célula robotizada resulta imprescindible conocer en todo momento el estado del proceso.

Para ello se utilizan diferentes indicadores que permiten comprobar si la instalación está trabajando correctamente.

Entre los datos más habituales encontramos:

- número de piezas procesadas;
- piezas clasificadas correctamente;
- piezas rechazadas;
- tiempo medio de ciclo;
- estado del robot;
- estado de los sensores;
- alarmas activas.

Toda esta información puede mostrarse mediante un panel de supervisión o **dashboard**, facilitando el seguimiento de la producción y la detección de posibles incidencias.

En aplicaciones reales estos datos suelen almacenarse en bases de datos industriales y visualizarse mediante sistemas SCADA o aplicaciones web.

En CoppeliaSim también es posible representar esta información para validar el comportamiento del sistema durante la simulación.

::: figure
image: ../assets/cap28/fig28_8.png
caption: Panel de supervisión del sistema automático de clasificación durante la simulación.
:::

La incorporación de herramientas de supervisión permite comprobar rápidamente si el sistema mantiene un funcionamiento estable y facilita enormemente las tareas de depuración cuando aparecen incidencias durante el desarrollo del proyecto.

---

## 28.9 Validación del sistema automático de clasificación

Una vez completada la construcción de la célula robotizada y configurados todos sus componentes, es necesario comprobar que el sistema funciona de forma correcta antes de ponerlo en producción.

En un entorno industrial esta fase recibe el nombre de **puesta en marcha** o **comisionado** (*commissioning*). Su objetivo consiste en verificar que todos los dispositivos trabajan de forma coordinada y que el proceso responde exactamente a las especificaciones definidas durante el diseño.

Durante la validación deben comprobarse, entre otros, los siguientes aspectos:

- Las piezas recorren correctamente la cinta transportadora.
- Los sensores detectan todos los objetos sin pérdidas.
- El robot recoge únicamente una pieza en cada ciclo.
- Cada objeto se deposita en la bandeja correspondiente.
- No existen colisiones entre el robot y el resto de elementos de la instalación.
- El sistema recupera correctamente su estado inicial al finalizar cada operación.

Una forma muy eficaz de realizar esta comprobación consiste en ejecutar varios ciclos consecutivos observando detenidamente el comportamiento de toda la instalación.

::: figure
image: ../assets/cap28/fig28_9.png
caption: Validación funcional del sistema automático de clasificación antes de su puesta en marcha.
:::

Si durante estas pruebas se detecta cualquier anomalía, resulta recomendable corregirla antes de continuar incorporando nuevas funcionalidades.

La simulación permite localizar estos problemas sin riesgo para las personas ni para los equipos, reduciendo considerablemente el tiempo y el coste de desarrollo.

---

## 28.10 Preparación para la integración con sistemas inteligentes

El sistema desarrollado hasta este momento reproduce el funcionamiento básico de una célula automática de clasificación.

Sin embargo, las instalaciones industriales actuales incorporan habitualmente funciones mucho más avanzadas.

Entre ellas destacan:

- visión artificial para identificar automáticamente las piezas;
- bases de datos para registrar toda la producción;
- comunicación con PLC y sistemas SCADA;
- monitorización mediante cuadros de mando;
- algoritmos de optimización;
- inteligencia artificial para mejorar la toma de decisiones.

Gracias a la estructura modular diseñada durante este capítulo, todas estas funcionalidades podrán añadirse sin necesidad de modificar la arquitectura principal de la instalación.

Nuestro sistema se encuentra preparado para evolucionar desde una simple célula robotizada hacia una solución propia de la Industria 4.0.

::: figure
image: ../assets/cap28/fig28_10.png
caption: Sistema automático de clasificación preparado para su integración con tecnologías de Industria 4.0.
:::

La utilización de CoppeliaSim durante esta fase permite experimentar con nuevas ideas, validar mejoras y comprobar su comportamiento antes de trasladarlas a una instalación física, reduciendo tanto el tiempo de desarrollo como los costes de implantación.

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Sistema automático de clasificación | Instalación capaz de identificar y separar objetos de forma automática según uno o varios criterios. |
| Línea de clasificación | Conjunto de equipos que permiten transportar, inspeccionar, manipular y almacenar las piezas. |
| Criterio de clasificación | Propiedad utilizada para decidir el destino de cada objeto, como el color, tamaño, forma o peso. |
| Flujo de materiales | Recorrido físico que siguen las piezas dentro de la instalación. |
| Flujo de información | Intercambio de señales y datos entre sensores, sistema de control y robot. |
| Tiempo de ciclo | Tiempo necesario para completar el procesamiento de una pieza desde la entrada hasta la salida. |
| Productividad | Número de piezas procesadas correctamente durante un determinado intervalo de tiempo. |
| Supervisión | Seguimiento en tiempo real del estado y funcionamiento de la instalación. |
| Dashboard | Panel gráfico que muestra indicadores de funcionamiento y producción. |
| Industria 4.0 | Modelo industrial basado en la integración de robots, comunicaciones, análisis de datos e inteligencia artificial. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender el funcionamiento de un sistema automático de clasificación.
- ✅ Diseñar una línea de clasificación robotizada.
- ✅ Definir criterios de clasificación para diferentes tipos de piezas.
- ✅ Integrar el robot dentro del flujo de producción.
- ✅ Diferenciar el flujo de materiales del flujo de información.
- ✅ Optimizar el tiempo de ciclo de una instalación robotizada.
- ✅ Supervisar el funcionamiento mediante indicadores de producción.
- ✅ Preparar la célula para su integración con tecnologías de Industria 4.0.

Ya dispones de una instalación completamente diseñada y preparada para comenzar a incorporar sistemas inteligentes de automatización.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Cuál es la función principal de un sistema automático de clasificación?
2. ¿Qué diferencias existen entre el flujo de materiales y el flujo de información?
3. ¿Qué factores influyen directamente en el tiempo de ciclo de una instalación robotizada?
4. ¿Qué ventajas aporta optimizar los movimientos del robot?
5. ¿Qué información suele mostrar un panel de supervisión industrial?
6. ¿Qué tecnologías de Industria 4.0 podrían incorporarse a esta célula robotizada?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a desarrollar aplicaciones robotizadas más inteligentes e integradas.

---

## Práctica guiada

::: practice
title: Construcción de un sistema robotizado de clasificación

difficulty: Media

time: 75 minutos

content:

Construye una célula robotizada similar a la desarrollada durante este capítulo.

1. Crea una escena nueva en CoppeliaSim.
2. Inserta una cinta transportadora para alimentar las piezas.
3. Incorpora un robot industrial de seis ejes.
4. Añade sensores de detección en la línea.
5. Diseña tres zonas de clasificación y una zona de rechazo.
6. Organiza todos los elementos mediante una estructura jerárquica.
7. Comprueba el recorrido completo de las piezas.
8. Analiza si el robot puede acceder correctamente a todas las posiciones.
9. Optimiza la distribución para reducir el tiempo de ciclo.
10. Guarda el proyecto para utilizarlo en los siguientes capítulos.

El objetivo consiste en obtener una célula completamente preparada para comenzar su programación automática.

:::

---

## Reto

::: challenge
title: Diseña tu propia línea de clasificación inteligente

content:

Una empresa necesita automatizar la clasificación de paquetes antes de su expedición.

Diseña una propuesta indicando:

- el recorrido que seguirán los paquetes;
- el número de sensores necesarios;
- la ubicación del robot;
- el criterio de clasificación utilizado;
- las zonas de almacenamiento;
- los indicadores que mostraría el panel de supervisión;
- qué tecnologías de Industria 4.0 incorporarías para mejorar el rendimiento.

Realiza un esquema justificando todas las decisiones adoptadas y compáralo posteriormente con otras posibles soluciones.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender la arquitectura de un sistema robotizado de clasificación.
- Analizar el flujo de materiales y de información.
- Introducir conceptos de optimización y supervisión industrial.
- Relacionar la simulación con aplicaciones reales de Industria 4.0.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Biblioteca de robots industriales.
- Modelos de cintas transportadoras y sensores.

**Consejos metodológicos**

Anime al alumnado a comparar distintas distribuciones de la línea de clasificación y a justificar cuál ofrece un menor tiempo de ciclo.

Es recomendable debatir cómo evolucionaría este proyecto si se incorporaran cámaras de visión artificial, PLC industriales, bases de datos o algoritmos de inteligencia artificial, preparando así el contexto de los siguientes capítulos.

:::

---

## Próximo capítulo

Hasta este momento el sistema ha funcionado siguiendo una lógica de clasificación previamente definida.

En el siguiente capítulo incorporaremos **visión artificial** para que el propio sistema sea capaz de identificar automáticamente las piezas antes de clasificarlas.

El robot dejará de depender exclusivamente de sensores de presencia y comenzará a tomar decisiones a partir de la información obtenida por una cámara, acercándonos todavía más al funcionamiento de una instalación industrial moderna basada en tecnologías de Industria 4.0.
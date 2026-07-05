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
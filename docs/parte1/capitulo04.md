# Capítulo 4 · Creando nuestra primera simulación

::: chapter-cover
number: 4
title: Creando nuestra primera simulación
time: 3 horas
level: ⭐☆☆☆☆ (Inicial)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Crear una escena nueva.
- Insertar un robot desde la biblioteca de modelos.
- Mover y posicionar objetos dentro de la escena.
- Guardar correctamente una simulación.
- Comprender la estructura básica de una escena de CoppeliaSim.
- Preparar el proyecto para comenzar a programar en Python.
:::

## ¿Ha llegado el momento de crear nuestro primer robot?

Después de tres capítulos ya conoces qué es la simulación, has instalado CoppeliaSim y sabes desenvolverte por su interfaz.

Ha llegado el momento de comenzar a construir.

A partir de este capítulo todas las prácticas tendrán un objetivo muy claro: desarrollar paso a paso una simulación funcional.

No utilizaremos escenas complejas descargadas de Internet.

Construiremos nuestras propias simulaciones desde cero.

Ese será uno de los aspectos diferenciadores de este libro.

Cuando finalices todas las prácticas no solo sabrás utilizar CoppeliaSim, sino que comprenderás cómo está construido internamente un proyecto de robótica.

::: teacher
content:

Este capítulo marca el cambio entre la parte introductoria y la parte práctica del libro.

Es recomendable que todos los alumnos realicen simultáneamente cada paso, verificando el resultado antes de continuar.

:::

---

## 4.1 Crear una escena nueva

Cada proyecto comienza con una escena vacía.

Una escena es el espacio tridimensional donde colocaremos todos los elementos de la simulación.

Para crear una nueva escena:

1. Abre CoppeliaSim.
2. Selecciona **File → New Scene**.
3. Comprueba que aparece una escena vacía.
4. Guarda inmediatamente la escena.

Aunque todavía no hayamos añadido ningún objeto, es una buena práctica guardar el proyecto desde el primer momento.

Utiliza el siguiente nombre:

```text
Practica01_PrimerRobot.ttt
```

Guárdalo dentro de la carpeta:

```text
CoppeliaSim-FP/

└── Practicas/

    └── Practica01/
```

::: common-error
content:

Muchos usuarios comienzan a trabajar sin guardar previamente la escena.

Si el programa se cierra inesperadamente, todo el trabajo realizado se perderá.

Acostúmbrate a guardar el proyecto desde el primer minuto.

:::

---

## 4.2 La escena vacía

Una escena recién creada puede parecer poco interesante.

Sin embargo, ya contiene algunos elementos importantes que permiten que la simulación funcione correctamente.

En la vista tridimensional observarás un plano de referencia y un sistema de ejes.

Estos elementos nos ayudan a orientarnos y a colocar correctamente los objetos.

::: figure
image: ../assets/cap04/escena_vacia.png
caption: Escena vacía al crear un nuevo proyecto en CoppeliaSim.
:::

Durante las siguientes prácticas iremos incorporando nuevos elementos hasta construir una simulación completa.

---

## 4.3 El sistema de coordenadas

Como cualquier programa de diseño tridimensional, CoppeliaSim utiliza un sistema de coordenadas cartesianas para definir la posición de todos los objetos.

Los tres ejes principales son:

- **X**
- **Y**
- **Z**

Cada objeto posee una posición expresada mediante estas tres coordenadas.

Comprender este sistema resultará fundamental cuando comencemos a programar movimientos mediante Python.

::: figure
image: ../assets/cap04/ejes_xyz.png
caption: Sistema de coordenadas utilizado por CoppeliaSim.
:::

No es necesario memorizar todavía el significado exacto de cada eje.

Lo aprenderemos de forma práctica durante los próximos capítulos.

---

## 4.4 Primer recorrido por una escena

Antes de añadir ningún robot, dedica unos minutos a explorar la escena.

Practica los movimientos aprendidos en el capítulo anterior.

- Gira la cámara.
- Acércate utilizando el zoom.
- Desplázate lateralmente.
- Cambia el punto de vista.

El objetivo consiste en sentirte completamente cómodo antes de comenzar a trabajar con objetos.

## 4.5 Insertando nuestro primer robot

Ha llegado el momento que muchos estábamos esperando.

Vamos a incorporar nuestro primer robot a la simulación.

No vamos a construirlo pieza a pieza. Aprovecharemos uno de los modelos incluidos en la biblioteca de CoppeliaSim.

De esta forma podremos centrarnos en aprender cómo funciona un robot antes de estudiar su construcción interna.

::: figure
image: ../assets/cap04/model_browser_robot.png
caption: Selección de un robot desde la biblioteca de modelos.
:::

Para insertar el robot sigue estos pasos:

1. Abre la **Model Browser**.
2. Busca la categoría **Mobile Robots**.
3. Localiza el modelo **Pioneer P3DX**.
4. Arrastra el modelo hasta la vista tridimensional.
5. Suelta el robot sobre el plano de trabajo.

Si todo ha ido correctamente, el robot aparecerá inmediatamente en la escena.

Además, observarás que también se ha añadido una nueva entrada en el árbol de la escena.

---

### ¿Por qué utilizaremos el Pioneer P3DX?

Durante este libro trabajaremos principalmente con el robot móvil **Pioneer P3DX**.

Se trata de uno de los robots más utilizados en docencia e investigación debido a su sencillez y versatilidad.

Entre sus principales características destacan:

- Dos ruedas motrices.
- Movimiento diferencial.
- Sensores ultrasónicos.
- Facilidad para integrar algoritmos de navegación.
- Compatibilidad con numerosos ejemplos de CoppeliaSim.

::: robot
id: PioneerP3DX
:::

Más adelante conoceremos cada uno de sus componentes con detalle.

Por el momento basta con saber que será nuestro robot de referencia durante buena parte del libro.

---

## 4.6 Observando el robot

Antes de poner el robot en movimiento, dedica unos minutos a explorarlo.

Gira la cámara alrededor del modelo y observa su estructura.

Intenta identificar:

- las ruedas;
- el cuerpo principal;
- los sensores;
- los elementos de fijación.

No te preocupes si algunos componentes todavía resultan desconocidos.

Los iremos estudiando progresivamente.

::: teacher
content:

Pide al alumnado que describa con sus propias palabras las distintas partes del robot.

Este pequeño ejercicio favorece la observación y ayuda a familiarizarse con el modelo antes de comenzar a programarlo.
:::

---

## 4.7 Seleccionando objetos

En CoppeliaSim existen dos formas principales de seleccionar un objeto.

La primera consiste en hacer clic directamente sobre él en la vista tridimensional.

La segunda consiste en seleccionarlo desde el árbol de la escena.

Ambos métodos producen el mismo resultado.

Cuando un objeto está seleccionado aparece resaltado tanto en la escena como en el árbol jerárquico.

Esto facilita enormemente el trabajo cuando una simulación contiene muchos elementos.

---

### Cambiar el nombre del robot

Es recomendable utilizar nombres descriptivos.

Aunque CoppeliaSim asigna automáticamente un nombre al modelo, podemos modificarlo para que resulte más sencillo identificarlo.

Por ejemplo:

```text
Pioneer_Principal
```

o

```text
Robot_Explorador
```

Una buena nomenclatura evitará confusiones cuando trabajemos con varios robots simultáneamente.

::: common-error
content:

Evita utilizar nombres como **Robot1**, **Robot2** o **NuevoRobot**.

Cuando un proyecto crece resulta muy difícil recordar qué representa cada objeto.
:::

---

## 4.8 Guardando la simulación

Una vez insertado el robot debemos guardar nuevamente la escena.

Selecciona:

**File → Save**

o utiliza el botón correspondiente de la barra de herramientas.

Acostúmbrate a guardar el trabajo con frecuencia.

Aunque CoppeliaSim es una aplicación muy estable, cualquier proyecto de ingeniería debe incorporar el hábito de realizar guardados periódicos.

Una buena práctica consiste en guardar la escena después de completar cada paso importante.

---

## 4.9 ¿Qué contiene realmente una escena?

Desde el punto de vista del usuario, una escena parece simplemente un conjunto de objetos colocados sobre un plano.

Sin embargo, internamente contiene mucha más información.

Una escena almacena, entre otros elementos:

- la posición de todos los objetos;
- su orientación;
- sus propiedades físicas;
- los sensores asociados;
- los scripts incorporados;
- las cámaras;
- las luces;
- las relaciones jerárquicas entre objetos.

Todo ello queda almacenado en un único archivo con extensión **.ttt**.

Gracias a ello podremos cerrar CoppeliaSim y continuar nuestro trabajo exactamente donde lo dejamos.

::: summary
title: Idea importante

content:

Una escena no es únicamente un dibujo en tres dimensiones.

Es un proyecto completo que contiene toda la información necesaria para reproducir una simulación.
:::

## 4.10 Ejecutando la primera simulación

Hasta este momento hemos preparado la escena, insertado un robot y aprendido a movernos por el entorno de trabajo.

Ha llegado el momento de ejecutar nuestra primera simulación.

No esperamos que el robot realice ninguna tarea especial. El objetivo consiste simplemente en comprender cómo funciona el ciclo de ejecución de CoppeliaSim.

Pulsa el botón **Play** situado en la barra de herramientas.

Observa atentamente lo que ocurre.

Aunque el robot permanezca inmóvil, internamente el simulador ha comenzado a ejecutar todos los procesos asociados a la escena.

Entre otras tareas:

- se inicia el motor físico;
- se activan los sensores;
- comienzan a ejecutarse los scripts;
- se calculan continuamente las colisiones;
- se actualiza la posición de todos los objetos.

En una escena sencilla apenas percibiremos cambios, pero en simulaciones complejas este proceso controla cientos de elementos simultáneamente.

::: figure
image: ../assets/cap04/play_stop.png
caption: Inicio y detención de una simulación mediante los controles principales.
:::

---

### Pausar la simulación

Pulsa ahora el botón **Pause**.

La simulación se detendrá temporalmente.

Todos los objetos permanecerán exactamente en el mismo estado en el que se encontraban.

Esta función resulta muy útil para inspeccionar una simulación mientras está en funcionamiento.

Pulsa nuevamente **Play** para continuar.

---

### Finalizar la simulación

Pulsa finalmente el botón **Stop**.

La simulación finalizará y todos los objetos recuperarán automáticamente su posición inicial.

Este comportamiento resulta especialmente útil durante el aprendizaje, ya que permite repetir una práctica tantas veces como sea necesario.

::: common-error
content:

Muchos alumnos creen que el botón **Stop** únicamente detiene el movimiento.

En realidad restaura completamente el estado inicial de la escena.

Por este motivo cualquier cambio realizado durante la simulación desaparecerá al detenerla.
:::

---

## 4.11 Explorando las propiedades del robot

Selecciona el robot en la escena.

A continuación abre el panel de propiedades.

En él podrás observar que cada objeto dispone de una gran cantidad de información.

Por ejemplo:

- nombre;
- posición;
- orientación;
- dimensiones;
- propiedades físicas;
- relaciones jerárquicas;
- scripts asociados.

No es necesario comprender todavía todos estos parámetros.

El objetivo consiste únicamente en descubrir la enorme cantidad de información que almacena cada objeto.

En capítulos posteriores modificaremos muchas de estas propiedades desde la propia interfaz y también mediante Python.

---

## 4.12 Guardando versiones del proyecto

Una buena práctica consiste en guardar diferentes versiones del proyecto conforme avanza el desarrollo.

Por ejemplo:

```text
Practica01_v1.ttt

Practica01_v2.ttt

Practica01_v3.ttt
```

De esta forma podremos volver fácilmente a una versión anterior si cometemos algún error importante.

En proyectos profesionales esta técnica resulta muy habitual.

Además del control de versiones mediante Git, conservar diferentes escenas puede ahorrar mucho tiempo durante el desarrollo de una simulación.

::: teacher
content:

Anima al alumnado a guardar versiones sucesivas de las prácticas.

Cuando comiencen a experimentar con escenas más complejas agradecerán disponer de copias anteriores.
:::

---

## 4.13 Buenas prácticas de trabajo

Antes de finalizar este capítulo conviene adquirir algunos hábitos que utilizaremos durante todo el libro.

- Guarda la escena con frecuencia.
- Utiliza nombres descriptivos para todos los objetos.
- Mantén organizada la estructura de carpetas.
- Realiza pequeñas modificaciones y comprueba el resultado antes de continuar.
- Experimenta sin miedo. Siempre podrás volver a cargar la última versión guardada.

Estos hábitos pueden parecer poco importantes al principio, pero marcarán una gran diferencia cuando los proyectos aumenten de tamaño.

---

## 4.14 Preparando el siguiente capítulo

Ya disponemos de una escena funcional.

Contiene un robot correctamente colocado y sabemos iniciar y detener la simulación.

En el siguiente capítulo comenzaremos a interactuar realmente con el robot.

Aprenderemos a:

- moverlo manualmente;
- modificar su posición;
- cambiar su orientación;
- comprender cómo se representan los movimientos en el espacio tridimensional.

Estos conceptos serán imprescindibles antes de comenzar a programar utilizando Python.

::: summary
title: Idea clave

content:

Durante este capítulo has creado tu primera simulación desde cero.

Aunque todavía no hemos escrito una sola línea de código, ya has aprendido el flujo de trabajo básico que seguirás durante todo el libro:

1. Crear una escena.
2. Añadir objetos.
3. Configurar la simulación.
4. Ejecutarla.
5. Analizar el resultado.
6. Guardar el proyecto.
:::

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Escena | Espacio de trabajo donde se desarrolla la simulación. |
| Robot móvil | Robot capaz de desplazarse por el entorno mediante ruedas u otros sistemas de locomoción. |
| Modelo | Conjunto de objetos reutilizables que representan un elemento completo de la simulación. |
| Biblioteca de modelos | Catálogo de robots, sensores y objetos disponibles en CoppeliaSim. |
| Sistema de coordenadas | Referencia espacial basada en los ejes X, Y y Z. |
| Simulación | Ejecución del modelo virtual utilizando el motor físico de CoppeliaSim. |
| Motor físico | Sistema encargado de calcular movimientos, colisiones y fuerzas. |
| Posición | Localización de un objeto dentro de la escena. |
| Orientación | Dirección hacia la que está orientado un objeto. |
| Proyecto | Conjunto formado por la escena, los modelos y los recursos asociados. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Crear una escena nueva.
- ✅ Guardar correctamente un proyecto.
- ✅ Comprender el sistema de coordenadas.
- ✅ Insertar un robot desde la biblioteca de modelos.
- ✅ Seleccionar y organizar objetos dentro de la escena.
- ✅ Ejecutar, pausar y detener una simulación.
- ✅ Comprender qué información almacena una escena de CoppeliaSim.

Ya has construido tu primera simulación.

Aunque todavía no has programado el robot, ya conoces el flujo básico de trabajo que utilizarás durante todo el libro.

---

## Autoevaluación

Responde a las siguientes preguntas.

1. ¿Qué diferencia existe entre una escena y un modelo?
2. ¿Por qué resulta recomendable guardar la escena desde el principio?
3. ¿Qué representa el sistema de coordenadas XYZ?
4. ¿Qué ocurre cuando pulsamos el botón **Play**?
5. ¿Qué diferencia existe entre **Pause** y **Stop**?
6. ¿Por qué es conveniente utilizar nombres descriptivos para los objetos?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a manipular el robot.

---

## Práctica guiada

::: practice
title: Mi primera simulación

difficulty: Baja

time: 35 minutos

content:

Realiza la siguiente práctica de forma individual.

1. Crea una escena nueva.
2. Guarda el proyecto con el nombre **Practica01_PrimerRobot.ttt**.
3. Inserta un robot Pioneer P3DX desde la biblioteca de modelos.
4. Explora el robot utilizando la vista tridimensional.
5. Comprueba que aparece correctamente en el árbol de la escena.
6. Ejecuta la simulación durante unos segundos.
7. Pausa la simulación y observa el estado del robot.
8. Detén la simulación.
9. Guarda nuevamente el proyecto.

Al finalizar habrás creado tu primera simulación completamente funcional.
:::

---

## Reto

::: challenge
title: Explora la biblioteca de modelos

content:

Además del Pioneer P3DX, CoppeliaSim incorpora numerosos robots de diferentes tipos.

Explora la biblioteca e identifica:

- Un brazo robótico.
- Un robot móvil diferente.
- Un dron.
- Un sensor de visión.
- Una cinta transportadora.

Anota para cada uno:

- Su nombre.
- El tipo de aplicación para el que ha sido diseñado.
- En qué capítulo de este libro crees que podría utilizarse.

Este ejercicio te ayudará a descubrir el enorme potencial de la biblioteca de modelos.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Crear la primera simulación del curso.
- Familiarizar al alumnado con la inserción de modelos.
- Comprender el ciclo de ejecución de una simulación.

**Material necesario**

- CoppeliaSim EDU 4.10 instalado.
- Ratón con rueda.
- Carpeta de trabajo creada en el capítulo anterior.

**Sugerencias metodológicas**

Permite que los alumnos exploren libremente la biblioteca de modelos durante unos minutos.

La curiosidad inicial suele aumentar notablemente la motivación.

Evita explicar todavía el funcionamiento interno del robot.

Ese contenido se desarrollará en los próximos capítulos.
:::

---

## Próximo capítulo

Hasta ahora hemos aprendido a construir una escena y a insertar un robot.

En el siguiente capítulo comenzaremos a interactuar realmente con él.

Aprenderás a mover objetos con precisión, modificar su posición y orientación, comprender los sistemas de referencia y preparar el robot para ser controlado mediante Python.

Será el primer paso hacia la programación de robots virtuales.
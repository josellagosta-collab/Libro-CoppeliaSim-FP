::: chapter-cover
number: 3
title: Conociendo la interfaz de CoppeliaSim
time: 3 horas
level: ⭐☆☆☆☆ (Inicial)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Identificar todas las zonas de trabajo de CoppeliaSim.
- Navegar correctamente por el espacio tridimensional.
- Utilizar el árbol de la escena.
- Abrir y cerrar escenas.
- Localizar modelos en la biblioteca.
- Iniciar, pausar y detener una simulación.
- Configurar las vistas principales del entorno de trabajo.
:::

# Capítulo 3 · Conociendo la interfaz de CoppeliaSim

### ¿Por qué es importante conocer la interfaz?

Cuando aprendemos a utilizar un programa nuevo es habitual querer comenzar a trabajar inmediatamente.

Sin embargo, dedicar unos minutos a conocer la interfaz de usuario supone una enorme ventaja.

Si sabemos dónde se encuentran las herramientas más importantes, podremos concentrarnos en resolver problemas de robótica en lugar de perder tiempo buscando opciones entre los menús.

En este capítulo no construiremos ningún robot.

Nuestro objetivo será aprender a movernos con soltura por el simulador.

Piensa en este capítulo como una visita guiada a un laboratorio que utilizarás durante todo el libro.

::: teacher
content:

Evita explicar todos los menús durante la primera sesión.

Es mucho más eficaz presentar únicamente aquellas herramientas que el alumnado utilizará en las primeras prácticas.

Las opciones más avanzadas irán apareciendo de forma natural en capítulos posteriores.
:::

---

## 3.1 La ventana principal

La primera vez que abrimos CoppeliaSim encontramos una interfaz que puede parecer compleja.

A simple vista aparecen numerosas barras de herramientas, paneles, ventanas y botones.

No te preocupes.

En realidad, durante las primeras prácticas utilizaremos únicamente una pequeña parte de ellos.

La figura siguiente muestra la distribución general de la interfaz.

::: figure
image: ../assets/cap03/annotated/interfaz_general.png
caption: Interfaz principal de CoppeliaSim EDU 4.10.0.
:::

A lo largo de este capítulo aprenderemos qué función desempeña cada una de estas zonas y cuándo utilizarlas.

## 3.2 La barra de menús

La barra de menús constituye el punto de acceso a prácticamente todas las funciones de CoppeliaSim.

Aunque durante las primeras prácticas utilizaremos principalmente los botones de la barra de herramientas, conocer la organización de los menús facilitará enormemente el trabajo cuando nuestros proyectos comiencen a crecer.

La barra de menús se encuentra en la parte superior de la ventana principal y agrupa las funciones del programa por categorías.

::: figure
image: ../assets/cap03/barra_menus_anotada.png
caption: Barra de menús de CoppeliaSim EDU 4.10.0.
:::

No es necesario memorizar todas las opciones desde el principio.

A lo largo del libro iremos utilizando cada menú cuando resulte necesario.

---

### Menú File

El menú **File** reúne todas las operaciones relacionadas con la gestión de archivos.

Desde este menú podremos:

- crear una escena nueva;
- abrir una escena existente;
- guardar nuestro trabajo;
- importar y exportar modelos;
- acceder a escenas recientes;
- cerrar la aplicación.

Durante las primeras prácticas utilizaremos principalmente las opciones:

- **New Scene**
- **Open Scene**
- **Save Scene**
- **Save Scene As...**

::: common-error
content:

Muchos estudiantes utilizan siempre **Save**.

Cuando vayas a modificar una escena descargada o proporcionada por el profesor, utiliza primero **Save Scene As...** y trabaja sobre una copia.

Así conservarás siempre el archivo original.
:::

---

### Menú Edit

El menú **Edit** contiene las herramientas necesarias para modificar los elementos de una escena.

Entre las operaciones más habituales encontramos:

- copiar;
- pegar;
- duplicar;
- eliminar;
- deshacer;
- rehacer.

Aunque parecen funciones sencillas, las utilizaremos constantemente cuando comencemos a construir nuestras propias simulaciones.

---

### Menú Add

El menú **Add** permite incorporar nuevos elementos a la escena.

Desde aquí podremos crear, entre otros:

- formas geométricas;
- cámaras;
- luces;
- sensores;
- trayectorias;
- scripts;
- puntos de referencia.

En los primeros capítulos utilizaremos principalmente modelos ya existentes, pero más adelante aprenderemos a construir nuestros propios objetos desde cero.

---

### Menú Simulation

Este menú controla el comportamiento general de la simulación.

Desde él podremos:

- iniciar la simulación;
- pausarla;
- detenerla;
- configurar diferentes parámetros relacionados con la ejecución.

Aunque estas funciones también están disponibles mediante botones en la barra de herramientas, conocer su ubicación dentro del menú resulta muy útil.

---

### Menú Tools

El menú **Tools** reúne diferentes utilidades de configuración y análisis.

Conforme avancemos en el libro utilizaremos algunas de ellas para:

- inspeccionar objetos;
- visualizar información de depuración;
- configurar determinados parámetros del entorno.

No es necesario explorar todavía todas sus opciones.

---

### Menú Modules

CoppeliaSim permite ampliar sus funcionalidades mediante módulos y complementos.

Gracias a esta arquitectura es posible integrar el simulador con numerosas herramientas externas.

Durante este libro utilizaremos algunos de estos módulos para conectar CoppeliaSim con Python y desarrollar aplicaciones cada vez más completas.

---

### Menú Help

Siempre que tengas dudas sobre una opción del simulador, este será el primer lugar donde buscar información.

Desde el menú **Help** podrás acceder a:

- documentación;
- información sobre la versión instalada;
- recursos de ayuda.

Aunque este libro pretende servir como guía completa, es recomendable acostumbrarse a consultar también la documentación oficial.

---

## 3.3 La barra de herramientas

Justo debajo de la barra de menús encontramos la barra de herramientas principal.

Su objetivo consiste en proporcionar acceso rápido a las funciones que utilizaremos con mayor frecuencia.

::: figure
image: ../assets/cap03/barra_herramientas_anotada.png
caption: Barra de herramientas principal de CoppeliaSim.
:::

Los botones más importantes durante las primeras prácticas son los siguientes.

::: table
caption: Botones principales de la barra de herramientas.
content:

| Botón | Función |
|--------|---------|
| Nuevo | Crea una escena vacía. |
| Abrir | Abre una escena existente. |
| Guardar | Guarda la escena actual. |
| Play | Inicia la simulación. |
| Pause | Pausa la simulación. |
| Stop | Detiene la simulación. |
| Model Browser | Muestra la biblioteca de modelos. |
| Scene Hierarchy | Activa el árbol de la escena. |
:::

No intentes memorizar todos los iconos.

En muy pocas prácticas terminarás identificándolos de forma natural.

::: teacher
content:

Durante la explicación inicial evita describir botón por botón.

Es mucho más eficaz presentar únicamente aquellos que los alumnos utilizarán en la práctica del día.

El resto podrán descubrirse progresivamente conforme aumente la complejidad de los proyectos.
:::

---

## 3.4 Primer recorrido por la interfaz

Antes de continuar, dedica unos minutos a explorar libremente el simulador.

No tengas miedo de pulsar botones o abrir diferentes ventanas.

La mayoría de las acciones pueden deshacerse fácilmente y, en caso de duda, siempre podrás cerrar la escena sin guardar los cambios.

El objetivo de esta primera toma de contacto no consiste en dominar todas las funciones del programa, sino en comenzar a familiarizarte con su entorno de trabajo.

En el siguiente apartado aprenderemos a utilizar la zona más importante de todo el simulador: **la vista tridimensional**, donde construiremos y controlaremos nuestros robots virtuales.

## 3.5 La vista tridimensional

La **vista tridimensional (3D View)** es el corazón de CoppeliaSim.

Es el área donde se representan todos los elementos de la simulación y donde pasaremos la mayor parte del tiempo mientras trabajemos con el programa.

Cada robot, sensor, cámara, objeto o mecanismo que creemos aparecerá dentro de esta ventana.

::: figure
image: ../assets/cap03/vista3d_anotada.png
caption: Vista tridimensional de CoppeliaSim.
:::

Al principio puede resultar extraño trabajar en un espacio tridimensional utilizando únicamente el ratón. Sin embargo, tras unos minutos de práctica descubrirás que el manejo resulta muy intuitivo.

Antes de comenzar a construir robots es imprescindible aprender a desplazarse correctamente por la escena.

---

### El punto de vista

Cuando observamos una simulación debemos imaginar que estamos manejando una cámara virtual.

Mover la cámara **no desplaza los robots**, únicamente cambia nuestra forma de observar la escena.

Esta diferencia es importante.

Muchos estudiantes creen inicialmente que están moviendo el robot cuando, en realidad, únicamente están cambiando el punto de vista desde el que lo observan.

---

### Rotar la cámara

La operación que utilizarás con mayor frecuencia será la rotación de la vista.

Al rotar la cámara podremos observar un mismo objeto desde diferentes ángulos.

Esto resulta especialmente útil para:

- comprobar la posición de un robot;
- inspeccionar sensores;
- localizar posibles colisiones;
- observar mecanismos complejos.

Dedica unos minutos a girar la vista alrededor de la escena hasta sentirte cómodo con el movimiento.

---

### Desplazar la vista

Además de girar la cámara, también podemos desplazarla horizontal o verticalmente.

Este movimiento recibe el nombre de **panorámica** o **desplazamiento lateral**.

Permite centrar rápidamente cualquier zona de la escena sin modificar el ángulo de observación.

Utilízalo para colocar el objeto de interés en el centro de la ventana.

---

### Acercar y alejar el zoom

El zoom permite modificar la distancia entre la cámara y la escena.

No debe confundirse con el desplazamiento.

Cuando acercamos el zoom obtenemos una visión más detallada de un objeto.

Cuando lo alejamos conseguimos una perspectiva más amplia del conjunto.

Durante el desarrollo de proyectos complejos alternaremos continuamente entre ambas vistas.

---

### Restablecer la vista

Es habitual perder la orientación durante las primeras prácticas.

No te preocupes.

Nos ocurre a todos.

Cuando esto suceda, utiliza las herramientas de centrado de la cámara para volver a visualizar correctamente la escena.

Con la práctica aprenderás a recuperar rápidamente cualquier punto de vista.

::: teacher
content:

Durante los primeros minutos de clase no propongas ejercicios de programación.

Pide simplemente al alumnado que explore la escena utilizando los distintos movimientos de cámara.

Cinco minutos de práctica aquí evitarán muchas dificultades en capítulos posteriores.
:::

---

## 3.6 El árbol de la escena

A la izquierda de la interfaz encontramos uno de los paneles más importantes de CoppeliaSim: el **árbol de la escena** (*Scene Hierarchy*).

Este panel muestra todos los objetos que forman parte de la simulación.

::: figure
image: ../assets/cap03/arbol_escena_anotado.png
caption: Árbol de la escena con varios objetos organizados jerárquicamente.
:::

Cada línea del árbol representa un objeto distinto.

Por ejemplo:

- un robot;
- una cámara;
- una luz;
- un sensor;
- una cinta transportadora;
- una forma geométrica.

Cuando una escena contiene únicamente dos o tres objetos resulta sencillo localizarlos directamente en la vista 3D.

Sin embargo, en proyectos reales pueden existir cientos de elementos.

En esas situaciones el árbol de la escena se convierte en una herramienta imprescindible.

---

### Relaciones jerárquicas

Los objetos pueden organizarse formando una estructura jerárquica.

Esto significa que un objeto puede contener otros objetos.

Por ejemplo:

```text
Robot

├── Base

├── Brazo

│   ├── Articulación 1

│   ├── Articulación 2

│   └── Pinza

└── Cámara
```

Esta organización facilita enormemente el manejo de robots complejos.

Mover el objeto principal implica desplazar automáticamente todos los elementos que dependen de él.

Más adelante aprenderemos a crear nuestras propias jerarquías.

---

### Seleccionar objetos

Una de las formas más cómodas de seleccionar un objeto consiste en hacerlo directamente desde el árbol.

Al hacerlo, el objeto correspondiente quedará resaltado también en la vista tridimensional.

Esta sincronización entre ambos paneles facilita mucho el trabajo.

---

### Renombrar objetos

Asignar nombres descriptivos a los objetos constituye un hábito muy recomendable.

Compara estos dos ejemplos.

Incorrecto:

```text
Shape0

Shape1

Shape2
```

Correcto:

```text
Robot

Mesa

CajaEntrada

SensorColor

CamaraSuperior
```

Cuando una escena crezca agradecerás enormemente haber dedicado unos segundos a nombrar correctamente cada elemento.

::: common-error
content:

Evita dejar los nombres que CoppeliaSim asigna automáticamente a los objetos.

Con el tiempo resulta muy difícil recordar qué representa cada uno de ellos.
:::

---

## 3.7 Primera exploración

Ha llegado el momento de explorar el simulador por tu cuenta.

No intentes comprender todavía todas las opciones disponibles.

Simplemente familiarízate con:

- la vista 3D;
- el árbol de la escena;
- la barra de herramientas;
- la barra de menús.

En el próximo apartado aprenderemos a utilizar la **biblioteca de modelos**, una de las características más potentes de CoppeliaSim y el lugar desde el que incorporaremos nuestros primeros robots virtuales.

## 3.8 La biblioteca de modelos

Uno de los aspectos que distingue a CoppeliaSim de otros simuladores es la enorme cantidad de modelos listos para utilizar que incorpora.

En lugar de construir todos los objetos desde cero, podemos reutilizar robots, sensores, mecanismos y escenarios completos ya preparados.

Esta colección recibe el nombre de **Model Browser**.

::: figure
image: ../assets/cap03/model_browser_anotado.png
caption: Biblioteca de modelos de CoppeliaSim.
:::

La biblioteca está organizada por categorías, lo que facilita localizar rápidamente el elemento que necesitamos.

Encontraremos, entre otros:

- Robots móviles.
- Brazos robóticos.
- Sensores.
- Cámaras.
- Vehículos.
- Mobiliario.
- Cintas transportadoras.
- Objetos geométricos.
- Escenarios completos.

A lo largo del libro utilizaremos con frecuencia esta biblioteca para incorporar nuevos elementos a nuestras simulaciones.

---

### ¿Qué es un modelo?

Un **modelo** es un conjunto de objetos que se comportan como una única unidad.

Por ejemplo, un robot móvil no está formado por una sola pieza.

Internamente incluye:

- el chasis;
- las ruedas;
- los motores;
- los sensores;
- los scripts de control;
- las propiedades físicas.

Todo este conjunto se almacena como un único modelo que puede reutilizarse tantas veces como sea necesario.

Gracias a ello, crear una simulación resulta mucho más rápido.

---

### Insertar un modelo en una escena

Añadir un modelo a una escena es muy sencillo.

El procedimiento general es el siguiente:

1. Abrir la biblioteca de modelos.
2. Localizar el modelo deseado.
3. Arrastrarlo con el ratón hasta la vista 3D.
4. Soltarlo en la posición deseada.

Automáticamente el nuevo elemento pasará a formar parte de la escena y aparecerá también en el árbol de la jerarquía.

::: teacher
content:

Durante la primera práctica permite que el alumnado explore libremente la biblioteca.

Es una excelente forma de despertar su curiosidad y descubrir las posibilidades del simulador.
:::

---

### Nuestro primer robot

Durante buena parte de este libro utilizaremos un robot móvil diferencial.

Este tipo de robot resulta ideal para aprender:

- desplazamiento.
- orientación.
- navegación.
- uso de sensores.
- programación.

En los próximos capítulos insertaremos este robot en una escena completamente vacía y aprenderemos a controlarlo.

No es necesario conocer todavía todos sus componentes.

Iremos descubriéndolos poco a poco.

---

## 3.9 Los controles de simulación

Una vez creada una escena necesitamos ponerla en funcionamiento.

Para ello utilizaremos los controles de simulación.

::: figure
image: ../assets/cap03/controles_simulacion_anotados.png
caption: Controles principales de la simulación.
:::

Estos botones permiten controlar la ejecución de la escena.

Los tres más importantes son:

::: table
caption: Controles básicos de la simulación.
content:

| Botón | Función |
|--------|---------|
| ▶ Play | Inicia la simulación. |
| ⏸ Pause | Pausa temporalmente la simulación. |
| ■ Stop | Finaliza la simulación y devuelve todos los objetos a su estado inicial. |
:::

Estos controles estarán presentes en prácticamente todas las prácticas del libro.

---

### Iniciar una simulación

Cuando pulsamos el botón **Play**, CoppeliaSim comienza a ejecutar todos los cálculos necesarios para reproducir el comportamiento de la escena.

En ese momento:

- comienza el movimiento de los robots;
- se activan los sensores;
- se ejecutan los scripts;
- el motor físico calcula continuamente las interacciones entre los distintos objetos.

Aunque visualmente parezca una simple animación, internamente el simulador está realizando cientos de cálculos cada segundo.

---

### Pausar la simulación

En ocasiones resulta útil detener temporalmente la ejecución para observar con detalle lo que está ocurriendo.

La opción **Pause** permite hacerlo sin perder el estado actual de la escena.

Podremos reanudar posteriormente la simulación exactamente desde el mismo punto.

---

### Detener la simulación

El botón **Stop** finaliza completamente la ejecución.

Cuando una simulación se detiene, todos los objetos recuperan la posición que tenían antes de iniciarse.

Este comportamiento resulta especialmente útil durante el aprendizaje, ya que permite repetir una práctica tantas veces como sea necesario.

::: common-error
content:

Muchos estudiantes esperan que el robot permanezca en la última posición alcanzada tras pulsar **Stop**.

Sin embargo, CoppeliaSim restaura automáticamente el estado inicial de la escena.

Este comportamiento es completamente normal y facilita repetir las simulaciones.
:::

---

## 3.10 Personalizando el entorno de trabajo

Cada usuario tiene una forma diferente de trabajar.

Por este motivo, CoppeliaSim permite adaptar la interfaz a las preferencias de cada persona.

Entre otras posibilidades podemos:

- mostrar u ocultar paneles;
- cambiar la disposición de algunas ventanas;
- modificar el tamaño de determinados elementos;
- configurar distintos parámetros de visualización.

Durante las primeras prácticas utilizaremos prácticamente la configuración predeterminada.

Más adelante aprenderemos a personalizar el entorno para trabajar de una forma más cómoda y eficiente.

---

## 3.11 Primer contacto con el simulador

Ya conoces los principales elementos de la interfaz de CoppeliaSim.

Aunque todavía no hemos desarrollado ninguna simulación, ya eres capaz de:

- identificar las diferentes zonas de trabajo;
- desplazarte por el espacio tridimensional;
- localizar objetos en el árbol de la escena;
- explorar la biblioteca de modelos;
- iniciar y detener una simulación.

En el próximo capítulo comenzaremos a construir nuestra primera escena y añadiremos el primer robot virtual del libro.

Será el inicio de las prácticas de robótica.

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Interfaz de usuario | Conjunto de elementos que permiten interactuar con CoppeliaSim. |
| Vista 3D | Zona principal donde se visualiza y manipula la simulación. |
| Árbol de la escena | Panel que muestra todos los objetos de la simulación organizados jerárquicamente. |
| Modelo | Conjunto de objetos reutilizables que representan un robot, sensor o mecanismo. |
| Biblioteca de modelos | Catálogo de modelos disponibles para incorporar a una escena. |
| Cámara virtual | Punto de vista desde el que observamos la escena. |
| Zoom | Acercamiento o alejamiento de la vista sin modificar la escena. |
| Rotación | Cambio del ángulo de observación de la cámara virtual. |
| Panorámica | Desplazamiento lateral de la cámara sobre la escena. |
| Controles de simulación | Botones que permiten iniciar, pausar y detener una simulación. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Identificar todas las zonas principales de la interfaz de CoppeliaSim.
- ✅ Utilizar la vista tridimensional para explorar una escena.
- ✅ Desplazarte, rotar y hacer zoom sobre el entorno de simulación.
- ✅ Comprender la función del árbol de la escena.
- ✅ Localizar modelos en la biblioteca integrada.
- ✅ Iniciar, pausar y detener una simulación.

A partir de este momento ya puedes desenvolverte con soltura dentro del simulador.

En los siguientes capítulos comenzaremos a construir nuestras propias simulaciones.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Cuál es la función de la vista tridimensional?
2. ¿Qué información muestra el árbol de la escena?
3. ¿Qué diferencia existe entre un modelo y una escena?
4. ¿Para qué sirve la biblioteca de modelos?
5. ¿Qué ocurre al pulsar el botón **Stop** durante una simulación?
6. ¿Qué diferencia existe entre mover la cámara y mover un robot?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar las primeras prácticas.

---

## Práctica guiada

::: practice
title: Explorando la interfaz de CoppeliaSim

difficulty: Muy baja

time: 25 minutos

content:

Abre CoppeliaSim y realiza las siguientes acciones.

1. Localiza la barra de menús.
2. Identifica los botones **Play**, **Pause** y **Stop**.
3. Abre la biblioteca de modelos.
4. Muestra el árbol de la escena.
5. Gira la cámara alrededor de la escena.
6. Acércate y aléjate utilizando el zoom.
7. Desplaza la vista horizontalmente.
8. Abre una escena de ejemplo y explora los objetos que contiene.
9. Inicia y detén la simulación varias veces.
10. Cierra la escena sin guardar los cambios.

El objetivo de esta práctica no consiste en construir una simulación, sino en adquirir soltura utilizando la interfaz.
:::

---

## Reto

::: challenge
title: Descubriendo CoppeliaSim

content:

Explora libremente la biblioteca de modelos durante unos minutos.

Selecciona tres modelos que te llamen la atención y responde a las siguientes preguntas:

- ¿Qué tipo de robot o dispositivo representan?
- ¿En qué aplicación industrial podrían utilizarse?
- ¿Qué sensores o actuadores crees que incorporan?

Comparte tus conclusiones con el resto de la clase.

No te preocupes si todavía no conoces todos los modelos.

La curiosidad será una de tus mejores herramientas durante este libro.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Familiarizar al alumnado con la interfaz de CoppeliaSim.
- Conseguir que todos los estudiantes sean capaces de navegar con comodidad por el espacio tridimensional.
- Comprender la utilidad del árbol de la escena y de la biblioteca de modelos.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Proyector.
- Ratón con rueda de desplazamiento (muy recomendable).

**Consejos metodológicos**

Evita explicar todas las opciones del programa.

Centra la atención únicamente en aquellas herramientas que el alumnado utilizará en las primeras prácticas.

Es recomendable dedicar unos minutos a la exploración libre del simulador antes de comenzar las actividades guiadas.

Muchos estudiantes descubren funcionalidades interesantes simplemente experimentando con la interfaz.
:::

---

## Próximo capítulo

Ya conoces el entorno de trabajo de CoppeliaSim.

Ha llegado el momento de empezar a construir simulaciones.

En el siguiente capítulo crearás tu primera escena desde cero, insertarás un robot móvil utilizando la biblioteca de modelos y aprenderás a manipularlo dentro del entorno tridimensional.

Será el primer paso para comenzar a desarrollar aplicaciones de robótica utilizando CoppeliaSim y Python.
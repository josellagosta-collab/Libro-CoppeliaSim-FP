::: chapter-cover
number: 2
title: Instalación y configuración inicial
time: 2 horas
level: ⭐☆☆☆☆ (Inicial)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Descargar CoppeliaSim EDU desde la web oficial.
- Instalar CoppeliaSim en Windows.
- Comprender la estructura básica de carpetas del programa.
- Realizar el primer arranque del simulador.
- Preparar una carpeta de trabajo para las prácticas del libro.
- Verificar que el entorno está listo para continuar.
:::

# Capítulo 2 · Instalación y configuración inicial

## 2.1 Antes de instalar

Antes de comenzar a trabajar con robots, sensores o programas Python, necesitamos preparar correctamente el entorno.

Una instalación bien organizada evitará muchos problemas más adelante.

En este capítulo instalaremos **CoppeliaSim EDU 4.10.0 rev. 0**, que será la versión de referencia del libro.

::: teacher
content:

Es recomendable que todo el grupo utilice la misma versión de CoppeliaSim.

Si cada alumno trabaja con una versión distinta, pueden cambiar los menús, los nombres de algunas escenas o el funcionamiento de determinados ejemplos.
:::

---

## 2.2 ¿Qué versión vamos a utilizar?

CoppeliaSim dispone de diferentes ediciones.

::: table
caption: Versiones habituales de CoppeliaSim.
content:

| Versión | Uso principal |
|---------|---------------|
| EDU | Educación y aprendizaje |
| Pro | Uso profesional e industrial |
| Player | Ejecución de escenas sin edición |
| Headless | Ejecución sin interfaz gráfica |
:::

En este libro utilizaremos:

**CoppeliaSim EDU 4.10.0 rev. 0**

Esta versión es suficiente para todas las prácticas propuestas.

---

## 2.3 Descarga del programa

La descarga debe realizarse siempre desde la página oficial de Coppelia Robotics.

No es recomendable descargar instaladores desde páginas externas, ya que podrían estar desactualizados o modificados.

Una vez descargado el archivo de instalación, en Windows encontraremos normalmente un fichero ejecutable.

```text
CoppeliaSim_Edu_V4_10_0_rev0_Setup.exe
```

El nombre exacto puede variar ligeramente, pero debe indicar claramente la versión EDU.

::: common-error
content:

Un error frecuente es descargar una versión diferente a la utilizada en clase.

Antes de instalar, comprueba siempre que el archivo corresponde a la versión indicada por el profesor.
:::

---

## 2.4 Instalación en Windows

Para instalar CoppeliaSim en Windows:

1. Ejecuta el instalador descargado.
2. Acepta las condiciones de uso.
3. Selecciona la carpeta de instalación.
4. Finaliza el asistente.
5. Comprueba que aparece el acceso directo en el menú Inicio.

Una ruta habitual de instalación puede ser:

```text
C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu
```

No es obligatorio usar exactamente esta ruta, pero sí es importante recordar dónde se ha instalado el programa.

---

## 2.5 Primer arranque

Una vez instalado, abre CoppeliaSim desde el menú Inicio de Windows.

Durante el primer arranque pueden aparecer mensajes relacionados con la licencia educativa o con la configuración gráfica.

En la mayoría de los casos basta con aceptar las opciones por defecto.

Al abrirse correctamente, veremos una interfaz similar a la que estudiaremos con detalle en el capítulo siguiente.

::: figure
image: ../assets/illustrations/software/coppeliasim.svg
caption: CoppeliaSim será el entorno principal de simulación utilizado durante todo el libro.
:::

---

## 2.6 Comprobación rápida

Antes de continuar, realiza estas comprobaciones:

- CoppeliaSim se abre sin errores.
- Aparece una escena vacía.
- Se muestra la vista 3D.
- Puedes localizar el botón **Play**.
- Puedes cerrar el programa sin problemas.

Si todo esto funciona, la instalación básica es correcta.

::: summary
title: Punto de control
content:

Antes de continuar con el resto del capítulo, asegúrate de que CoppeliaSim se abre correctamente.

Todavía no necesitamos programar nada.

El objetivo de este punto es confirmar que el simulador está instalado y listo para trabajar.
:::

---

## 2.7 Organización de las carpetas de trabajo

Uno de los errores más habituales cuando se comienza a utilizar CoppeliaSim consiste en guardar todas las escenas en cualquier carpeta del ordenador.

Aunque inicialmente puede parecer una buena idea, al cabo de pocas prácticas resulta difícil localizar los archivos y mantener el trabajo organizado.

Por este motivo, a lo largo de este libro seguiremos siempre la misma estructura de carpetas.

```text
C:\CoppeliaSim-FP\
│
├── Escenas\
│
├── Modelos\
│
├── Python\
│
├── Recursos\
│
│   ├── Imágenes\
│   ├── Texturas\
│   └── Documentación\
│
├── Practicas\
│
│   ├── Practica01\
│   ├── Practica02\
│   ├── Practica03\
│   └── ...
│
└── CopiasSeguridad\
```

Esta organización ofrece varias ventajas:

- todas las prácticas estarán localizadas en un único lugar;
- será muy sencillo realizar copias de seguridad;
- evitaremos sobrescribir escenas originales;
- podremos reutilizar modelos entre diferentes proyectos.

::: teacher
content:

Dedica unos minutos durante la primera sesión para que todos los alumnos creen exactamente la misma estructura de carpetas.

Más adelante ahorrarás mucho tiempo cuando tengas que revisar las prácticas de toda la clase.
:::

---

## 2.8 La primera escena

Al abrir CoppeliaSim aparecerá una escena completamente vacía.

Esta escena constituye nuestro espacio de trabajo.

En los próximos capítulos aprenderemos a añadir:

- robots;
- sensores;
- cámaras;
- objetos;
- luces;
- scripts.

Por el momento únicamente necesitamos familiarizarnos con el entorno.

No es recomendable comenzar modificando escenas complejas descargadas de Internet.

Durante las primeras prácticas trabajaremos siempre sobre escenas muy sencillas.

---

## 2.9 Guardar correctamente una escena

Guardar una escena en CoppeliaSim resulta muy parecido a guardar un documento en cualquier otra aplicación.

Sin embargo, es importante adquirir desde el principio algunos buenos hábitos.

La primera vez que guardemos una escena seguiremos estos pasos:

1. Seleccionar **File → Save Scene As...**
2. Acceder a la carpeta **Practicas**.
3. Crear una carpeta específica para la práctica correspondiente.
4. Asignar un nombre descriptivo al archivo.

Por ejemplo:

```text
Practica01_PrimerRobot.ttt
```

Conforme avancemos en el libro utilizaremos una nomenclatura similar para todos los proyectos.

::: common-error
content:

No trabajes nunca directamente sobre una escena original descargada de Internet.

Haz siempre una copia antes de comenzar cualquier modificación.
:::

---

## 2.10 Tipos de archivos de CoppeliaSim

CoppeliaSim utiliza distintos tipos de archivos dependiendo de la información que contienen.

::: table
caption: Principales tipos de archivos utilizados por CoppeliaSim.
content:

| Extensión | Contenido |
|-----------|-----------|
| .ttt | Escena completa |
| .ttm | Modelo reutilizable |
| .simscene.xml | Escena en formato XML |
| .simmodel.xml | Modelo en formato XML |

Durante las primeras prácticas utilizaremos casi exclusivamente archivos **.ttt**.

Más adelante aprenderemos a crear nuestros propios modelos reutilizables utilizando archivos **.ttm**.

---

## 2.11 Preparando el entorno para Python

Aunque todavía no escribiremos ningún programa, conviene preparar desde el principio una carpeta específica para el código fuente.

Dentro de la carpeta principal del curso crea el siguiente directorio:

```text
Python\
```

Más adelante organizaremos esta carpeta de la siguiente forma:

```text
Python\
│
├── practica01.py
├── practica02.py
├── practica03.py
└── ...
```

De esta forma será muy sencillo localizar el código correspondiente a cada práctica.

---

## 2.12 Verificación del entorno

Antes de continuar con el siguiente capítulo realiza la siguiente comprobación.

::: exercise
title: Lista de comprobación

content:

Marca cada punto cuando lo hayas completado.

- ☐ CoppeliaSim está instalado.
- ☐ El programa se abre correctamente.
- ☐ He creado la carpeta principal del curso.
- ☐ He organizado las subcarpetas.
- ☐ Sé guardar una escena.
- ☐ Sé dónde almacenaré mis programas Python.
:::

Si todos los puntos anteriores están completados, el entorno de trabajo está preparado.

En el siguiente capítulo comenzaremos a explorar la interfaz del simulador y aprenderemos a movernos con soltura por la escena tridimensional.

---

::: summary
title: Resumen del capítulo

content:

En este capítulo hemos preparado el entorno de trabajo que utilizaremos durante todo el libro.

Además de instalar correctamente CoppeliaSim, hemos aprendido a organizar nuestras carpetas, guardar escenas y preparar la estructura que utilizaremos para desarrollar los programas en Python.

Una buena organización desde el principio facilitará enormemente el trabajo en los capítulos posteriores.
:::

---

## Para el profesor

::: teacher
title: Organización recomendada
content:

**Duración recomendada**

- 1 sesión de 55 minutos.

**Objetivos**

- Comprobar que todos los alumnos han instalado correctamente CoppeliaSim.
- Unificar la estructura de carpetas del grupo.
- Verificar que todos pueden abrir y guardar escenas.

**Consejo**

No avances al capítulo siguiente hasta comprobar que todos los equipos funcionan correctamente.
:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Instalación | Proceso mediante el cual se prepara un programa para su utilización. |
| CoppeliaSim EDU | Versión de CoppeliaSim destinada al aprendizaje y la docencia. |
| Escena | Archivo que contiene el entorno completo de simulación. |
| Modelo | Conjunto de objetos reutilizables que pueden insertarse en una escena. |
| Proyecto | Organización de escenas, modelos y programas relacionados con una práctica. |
| Carpeta de trabajo | Directorio donde almacenaremos todas las prácticas del libro. |
| Python | Lenguaje de programación que utilizaremos para controlar los robots. |
| Entorno de trabajo | Conjunto de herramientas necesarias para desarrollar las prácticas. |
| Copia de seguridad | Duplicado de los archivos importantes para evitar pérdidas de información. |
| Organización de archivos | Estructura lógica de carpetas y documentos de un proyecto. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Descargar CoppeliaSim desde la página oficial.
- ✅ Instalar correctamente el simulador.
- ✅ Crear una estructura organizada para tus proyectos.
- ✅ Guardar escenas de forma adecuada.
- ✅ Diferenciar entre escenas y modelos.
- ✅ Preparar el entorno que utilizarás durante todo el libro.

Aunque todavía no hemos comenzado a programar, ya dispones de un entorno de trabajo correctamente preparado.

Esto te permitirá concentrarte en el aprendizaje sin tener que preocuparte por problemas de organización.

---

## Autoevaluación

Responde a las siguientes preguntas antes de continuar.

1. ¿Qué versión de CoppeliaSim utilizaremos durante el libro?
2. ¿Qué diferencia existe entre una escena y un modelo?
3. ¿Por qué es recomendable organizar las prácticas en carpetas independientes?
4. ¿Qué extensión tienen normalmente las escenas de CoppeliaSim?
5. ¿Dónde guardarás los programas Python de las prácticas?

Si puedes responder correctamente a estas cuestiones, estás preparado para comenzar a trabajar con el simulador.

---

## Práctica guiada

::: practice
title: Preparación del entorno de trabajo

difficulty: Muy baja

time: 20 minutos

content:

Realiza las siguientes tareas:

1. Comprueba que CoppeliaSim se abre correctamente.
2. Crea la carpeta principal **CoppeliaSim-FP**.
3. Crea todas las subcarpetas propuestas en este capítulo.
4. Abre una escena vacía.
5. Guárdala con el nombre **Practica01_PrimerProyecto.ttt** dentro de la carpeta correspondiente.
6. Cierra el programa y vuelve a abrir la escena para comprobar que se ha guardado correctamente.

Al finalizar esta práctica tendrás preparado el entorno que utilizarás durante todo el libro.
:::

---

## Reto

::: challenge
title: Organiza tu laboratorio virtual

content:

Imagina que dentro de unos meses habrás realizado más de cincuenta prácticas diferentes.

Diseña una estructura de carpetas que te permita localizar rápidamente cualquier escena, programa Python o recurso utilizado durante el curso.

Compárala con la propuesta de este libro e identifica qué ventajas e inconvenientes presenta cada una.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Una sesión de 55 minutos.

**Objetivos de la sesión**

- Verificar que todos los equipos disponen de CoppeliaSim correctamente instalado.
- Comprobar que el alumnado ha creado la estructura de carpetas propuesta.
- Resolver posibles incidencias relacionadas con la instalación o los permisos de escritura.

**Observaciones**

No es necesario explicar todavía el funcionamiento detallado de la interfaz del simulador.

Es suficiente con que todos los alumnos sean capaces de abrir una escena, guardarla y localizar posteriormente el archivo generado.

De este modo, el siguiente capítulo podrá dedicarse íntegramente a conocer el entorno de trabajo sin interrupciones por problemas de instalación.
:::

---

## Próximo capítulo

En el siguiente capítulo conoceremos la interfaz de CoppeliaSim con detalle.

Aprenderás a identificar cada una de las zonas de trabajo del simulador, navegar por el espacio tridimensional, utilizar el árbol de la escena y localizar las herramientas que emplearemos durante el resto del libro.

Al finalizar el próximo capítulo serás capaz de moverte con soltura por el entorno de simulación y comenzarás a trabajar con tu primer robot virtual.
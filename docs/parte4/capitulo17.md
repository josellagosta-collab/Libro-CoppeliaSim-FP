::: chapter-cover
number: 17
title: Introducción a la robótica industrial
time: 4 horas
level: ★★☆☆☆ (Básico)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué diferencia a un robot industrial de un robot móvil.
- Conocer las principales aplicaciones de los robots industriales.
- Identificar las partes que componen un brazo robótico.
- Familiarizarte con el robot **Universal Robots UR3**.
- Cargar el UR3 en una escena de CoppeliaSim.
- Reconocer las articulaciones y el espacio de trabajo del robot.

:::

# Capítulo 17 · Introducción a la robótica industrial

### Del robot móvil al robot manipulador

En la parte anterior del libro hemos aprendido a controlar el **Pioneer P3DX**, un robot móvil capaz de desplazarse por un entorno, evitar obstáculos y tomar decisiones utilizando sensores y visión artificial.

Sin embargo, la mayor parte de los robots que encontramos actualmente en la industria no recorren una fábrica.

Permanecen instalados en una posición fija y realizan millones de movimientos con una precisión extraordinaria.

Estos robots reciben el nombre de **robots manipuladores** o **robots industriales**.

Su misión no consiste en desplazarse, sino en **interactuar con el entorno**.

Recogen piezas de una cinta transportadora, ensamblan componentes electrónicos, paletizan cajas, aplican adhesivos, realizan soldaduras o inspeccionan productos mediante cámaras de visión artificial.

En esta cuarta parte aprenderemos a controlar este tipo de robots utilizando **CoppeliaSim** y **Python**.

Pero, a diferencia de otros manuales donde se utilizan distintos modelos de robot en cada capítulo, aquí trabajaremos siempre con un único protagonista:

**el Universal Robots UR3**.

Este será el mismo robot que utilizaremos desde este capítulo hasta el proyecto final de la Parte IV.

::: figure
image: ../assets/cap17/fig17_1.png
caption: Evolución del libro: del Pioneer P3DX al robot industrial UR3.
:::

::: teacher
content:

Es recomendable comenzar la sesión mostrando al alumnado una fotografía o un vídeo corto del UR3 trabajando en una célula robotizada.

Esto permitirá relacionar inmediatamente la simulación con un robot utilizado habitualmente en empresas y centros de Formación Profesional.

:::

---

## 17.1 Conociendo nuestro robot: el UR3

Durante toda esta parte del libro utilizaremos el **Universal Robots UR3**, un robot colaborativo de seis ejes desarrollado para realizar tareas de manipulación con gran precisión.

Se trata de uno de los robots más utilizados en laboratorios, centros educativos y pequeñas células de automatización debido a su tamaño compacto, facilidad de programación y gran versatilidad.

Aunque existen numerosos fabricantes de robots industriales, el UR3 constituye una excelente plataforma de aprendizaje porque incorpora prácticamente todos los conceptos fundamentales de la robótica moderna.

Con él aprenderemos a:

- controlar individualmente cada articulación;
- mover el efector final hasta una posición determinada;
- planificar trayectorias;
- manipular objetos;
- coordinar el robot con sensores y cámaras;
- desarrollar aplicaciones completas de automatización.

A lo largo de los próximos capítulos iremos ampliando progresivamente la misma escena de simulación.

Cada nuevo concepto se incorporará sobre el trabajo realizado anteriormente, de forma que al finalizar esta parte habremos construido una célula robotizada completa.

::: figure
image: ../assets/cap17/fig17_2.png
caption: Robot Universal Robots UR3 que utilizaremos durante toda la Parte IV.
:::

El hecho de trabajar siempre sobre el mismo robot permitirá centrar la atención en los conceptos de programación y automatización, sin tener que adaptarse continuamente a modelos diferentes.

Además, muchas de las prácticas estarán inspiradas en aplicaciones industriales reales similares a las que pueden encontrarse actualmente en procesos de fabricación, clasificación y manipulación automática.

---

## 17.2 Anatomía del robot UR3

Antes de comenzar a programar un robot industrial es necesario conocer cómo está construido.

A diferencia del Pioneer P3DX, cuyo movimiento dependía principalmente de sus ruedas, el UR3 obtiene toda su movilidad gracias a una cadena de **articulaciones rotacionales**.

Cada una de ellas aporta un nuevo grado de movimiento al robot.

La combinación de todas ellas permite colocar el extremo del brazo prácticamente en cualquier posición dentro de su espacio de trabajo.

Aunque exteriormente el UR3 parece una única estructura metálica, en realidad está formado por varios eslabones unidos mediante seis articulaciones motorizadas.

Cada articulación incorpora un servomotor, un sistema de transmisión y sensores internos que permiten conocer con gran precisión su posición.

::: figure
image: ../assets/cap17/fig17_3.png
caption: Principales elementos que forman el robot Universal Robots UR3.
:::

---

### Las seis articulaciones

El UR3 dispone de **seis grados de libertad**, también llamados **seis ejes**.

Cada eje realiza un movimiento diferente y todos trabajan conjuntamente para posicionar el efector final.

De forma simplificada, podemos identificar las siguientes articulaciones:

| Eje | Denominación habitual | Función principal |
|------|-----------------------|-------------------|
| Eje 1 | Base | Permite que todo el brazo gire sobre su base. |
| Eje 2 | Hombro | Eleva o desciende el brazo principal. |
| Eje 3 | Codo | Modifica el alcance del robot. |
| Eje 4 | Muñeca 1 | Cambia la orientación del antebrazo. |
| Eje 5 | Muñeca 2 | Inclina el efector final. |
| Eje 6 | Muñeca 3 | Gira la herramienta sobre su propio eje. |

Gracias a la combinación de estos seis movimientos el robot puede acceder a una enorme cantidad de posiciones y orientaciones diferentes.

En los próximos capítulos aprenderemos a controlar cada uno de estos ejes desde Python.

::: common-error
content:

Muchos estudiantes intentan memorizar las funciones de todas las articulaciones desde el primer momento.

No es necesario.

Lo importante es comprender que cada eje aporta un movimiento diferente y que todos deben coordinarse para situar correctamente el efector final.

:::

---

## 17.3 El efector final

Si las articulaciones son los músculos del robot, el **efector final** constituye su mano.

Es el elemento encargado de interactuar directamente con el entorno.

Dependiendo de la aplicación, un mismo robot puede utilizar herramientas completamente diferentes.

Algunos ejemplos son:

- pinzas mecánicas;
- ventosas de vacío;
- herramientas de atornillado;
- pistolas de soldadura;
- dispensadores de adhesivo;
- cámaras de visión artificial;
- sensores de inspección.

En este libro utilizaremos principalmente una **pinza mecánica**, ya que nos permitirá desarrollar aplicaciones de manipulación muy similares a las empleadas en procesos industriales reales.

Más adelante aprenderemos a controlar la apertura y el cierre de la pinza desde Python y a sincronizar su funcionamiento con el movimiento del robot.

::: figure
image: ../assets/cap17/fig17_4.png
caption: Diferentes tipos de efectores finales que pueden instalarse en un robot UR3.
:::

---

### Un robot, muchas aplicaciones

Una de las grandes ventajas de los robots industriales es que pueden adaptarse fácilmente a nuevas tareas.

En muchas ocasiones no es necesario cambiar el robot completo.

Basta con sustituir el efector final para transformar completamente su función.

Por ejemplo, un mismo UR3 puede utilizarse durante la mañana para clasificar piezas mediante una pinza y, posteriormente, incorporar una cámara para realizar una inspección visual automática.

Esta enorme versatilidad explica por qué los robots colaborativos se utilizan actualmente en laboratorios, centros logísticos, líneas de montaje y pequeñas células de automatización.

---

## 17.4 Incorporando el UR3 a CoppeliaSim

Ha llegado el momento de comenzar a trabajar con nuestro robot.

Durante toda la Parte IV utilizaremos el modelo del **Universal Robots UR3** incluido en la biblioteca de CoppeliaSim.

Trabajar siempre con el mismo robot nos permitirá centrarnos en los conceptos de programación y automatización sin tener que adaptarnos continuamente a modelos diferentes.

Antes de programarlo debemos aprender a localizarlo dentro de la biblioteca de modelos e incorporarlo correctamente a una escena.

::: figure
image: ../assets/cap17/fig17_5.png
caption: Localización del robot UR3 en la biblioteca de modelos de CoppeliaSim.
:::

---

### Insertar el robot en una escena

El procedimiento es muy similar al que utilizamos cuando incorporamos el Pioneer P3DX.

1. Crear una escena nueva.
2. Abrir la biblioteca de modelos (**Model Browser**).
3. Acceder a la categoría **Robots**.
4. Localizar el modelo **Universal Robots UR3**.
5. Arrastrarlo hasta la vista tridimensional.
6. Soltarlo sobre el plano de trabajo.

En pocos segundos el robot aparecerá completamente preparado para comenzar a trabajar.

Además de la geometría del brazo, el modelo incorpora todas sus articulaciones, elementos de control y la estructura jerárquica necesaria para realizar simulaciones.

::: teacher
content:

Es recomendable pedir al alumnado que dedique unos minutos a explorar el árbol de la escena antes de comenzar a programar el robot.

Identificar visualmente cada articulación facilitará enormemente los ejercicios del capítulo siguiente.

:::

---

### Explorando el árbol de la escena

Una vez insertado el robot podremos observar cómo aparece organizado dentro del **árbol de la escena**.

Cada articulación constituye un objeto independiente.

Esta organización jerárquica permite que el movimiento de una articulación afecte automáticamente a todas las situadas a continuación.

El árbol del UR3 suele presentar una estructura similar a la siguiente:

```text
UR3

├── Base

├── Joint1

├── Joint2

├── Joint3

├── Joint4

├── Joint5

├── Joint6

└── Connection
```

En los próximos capítulos accederemos desde Python a cada una de estas articulaciones utilizando sus correspondientes identificadores (*handles*).

---

## 17.5 El espacio de trabajo

Una de las primeras limitaciones que debemos conocer es que un robot industrial **no puede alcanzar cualquier punto del espacio**.

Cada modelo dispone de una zona determinada dentro de la cual puede mover su efector final.

Esta región recibe el nombre de **espacio de trabajo** o **workspace**.

Puede imaginarse como el volumen máximo que el robot es capaz de recorrer.

::: figure
image: ../assets/cap17/fig17_6.png
caption: Representación aproximada del espacio de trabajo del robot UR3.
:::

El espacio de trabajo depende de varios factores:

- la longitud de los eslabones;
- el recorrido permitido en cada articulación;
- la geometría del propio robot;
- las limitaciones mecánicas del fabricante.

Conocer este espacio resulta fundamental cuando diseñamos una célula robotizada.

Todos los objetos con los que el robot deba interactuar deberán situarse dentro de esta zona.

::: common-error
content:

Un error muy frecuente consiste en colocar una pieza fuera del espacio de trabajo del robot.

En ese caso ninguna programación conseguirá que el UR3 alcance el objeto, ya que se trata de una limitación física del propio manipulador.

:::

---

### Nuestro laboratorio virtual

A partir de este momento utilizaremos siempre la misma escena de trabajo.

En ella iremos incorporando progresivamente todos los elementos necesarios para construir una célula robotizada completa.

Durante los próximos capítulos añadiremos:

- una pinza mecánica;
- piezas para manipular;
- una cinta transportadora;
- sensores;
- cámaras de visión artificial.

Al finalizar la Parte IV habremos construido una instalación muy similar a las utilizadas actualmente en procesos industriales de automatización.

---

## 17.6 Explorando el UR3 en CoppeliaSim

Ya tenemos el robot incorporado a nuestra escena.

Antes de comenzar a programarlo conviene dedicar unos minutos a explorar sus posibilidades utilizando únicamente las herramientas que proporciona CoppeliaSim.

Este primer contacto permitirá comprender mejor cómo está organizado el robot y facilitará enormemente el trabajo que realizaremos en los capítulos siguientes.

::: teacher
content:

No tengas prisa por comenzar a programar.

Permitir que el alumnado manipule el robot manualmente durante unos minutos ayuda a comprender el funcionamiento de las articulaciones y reduce muchos errores posteriores.

:::

---

### Seleccionar una articulación

Cada una de las seis articulaciones del UR3 puede seleccionarse de forma independiente.

Para ello basta con hacer clic sobre la articulación directamente en la vista 3D o seleccionarla desde el árbol de la escena.

Cuando una articulación está seleccionada aparece resaltada, indicando que podremos consultar o modificar sus propiedades.

::: figure
image: ../assets/cap17/fig17_7.png
caption: Selección de una articulación del UR3 desde la vista 3D y desde el árbol de la escena.
:::

---

### Observar el movimiento de los ejes

Una característica muy interesante de CoppeliaSim es que permite mover manualmente las articulaciones del robot para observar su comportamiento.

Durante esta práctica no pretendemos memorizar todos los movimientos.

Simplemente queremos comprobar cómo influye cada eje sobre la posición del brazo.

Realiza la siguiente secuencia:

1. Selecciona la articulación **Joint1**.
2. Modifica ligeramente su posición.
3. Observa cómo gira todo el robot sobre la base.
4. Repite el proceso con **Joint2** y **Joint3**.
5. Finalmente, prueba las articulaciones de la muñeca.

Muy pronto descubrirás que cada eje realiza un movimiento completamente diferente.

---

### Comprendiendo el movimiento combinado

Aunque cada articulación puede moverse de forma independiente, en la práctica casi nunca trabajan por separado.

Cuando el robot debe alcanzar una determinada posición, todas las articulaciones colaboran entre sí.

Este movimiento coordinado es el que permitirá, en los próximos capítulos, desplazar el efector final hasta cualquier punto del espacio de trabajo.

::: common-error
content:

Muchos estudiantes intentan mover únicamente una articulación para alcanzar una posición concreta.

En un robot industrial esto rara vez es suficiente.

Normalmente será necesario coordinar varias articulaciones de forma simultánea.

:::

---

## 17.7 Nuestra primera célula robotizada

Durante toda la Parte IV utilizaremos una única escena de trabajo que irá creciendo progresivamente.

En este capítulo únicamente encontraremos el robot instalado sobre su base.

Sin embargo, en los siguientes capítulos iremos incorporando nuevos elementos hasta construir una auténtica célula robotizada.

La escena terminará incluyendo:

- una mesa de trabajo;
- una pinza mecánica;
- piezas para manipular;
- una cinta transportadora;
- sensores industriales;
- una cámara de visión artificial.

Este enfoque tiene una ventaja muy importante.

En lugar de comenzar una escena nueva en cada capítulo, construiremos un único proyecto que evolucionará paso a paso, exactamente igual que ocurre durante el desarrollo de una instalación industrial real.

::: figure
image: ../assets/cap17/fig17_8.png
caption: Evolución prevista de la escena del UR3 a lo largo de la Parte IV.
:::

---

## 17.8 Práctica guiada: Primer contacto con el UR3

Ha llegado el momento de comprobar que eres capaz de desenvolverte con el robot dentro de CoppeliaSim.

El objetivo de esta práctica no consiste todavía en programar el robot, sino en familiarizarte con su estructura y con el entorno de trabajo que utilizaremos durante toda la Parte IV.

::: practice
title: Explorando el robot UR3

difficulty: Baja

time: 30 minutos

content:

Realiza las siguientes operaciones:

1. Crea una escena nueva en CoppeliaSim.
2. Abre la biblioteca de modelos.
3. Localiza el robot **Universal Robots UR3**.
4. Arrástralo hasta la escena.
5. Comprueba que aparece correctamente en el árbol de la escena.
6. Identifica las seis articulaciones del robot.
7. Selecciona cada articulación desde el árbol.
8. Observa las propiedades de cada una de ellas.
9. Gira la vista alrededor del robot para observarlo desde distintos ángulos.
10. Identifica visualmente la base, el brazo, el antebrazo y el efector final.

Al finalizar la práctica deberás ser capaz de localizar rápidamente cualquier articulación del robot dentro de la escena.

:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Robot industrial | Manipulador programable diseñado para realizar tareas de automatización. |
| Robot colaborativo | Robot preparado para trabajar compartiendo espacio con las personas. |
| UR3 | Robot colaborativo de seis ejes desarrollado por Universal Robots. |
| Articulación | Eje motorizado que proporciona movimiento al robot. |
| Grado de libertad | Movimiento independiente que puede realizar una articulación. |
| Efector final | Herramienta instalada en el extremo del robot para interactuar con el entorno. |
| Espacio de trabajo | Volumen máximo que puede alcanzar el efector final del robot. |
| Árbol de la escena | Estructura jerárquica donde aparecen todos los elementos del robot y de la simulación. |
| Modelo | Conjunto de objetos que forman una única entidad reutilizable en CoppeliaSim. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender qué es un robot industrial.
- ✅ Diferenciar un robot móvil de un robot manipulador.
- ✅ Identificar las principales partes del UR3.
- ✅ Reconocer las seis articulaciones del robot.
- ✅ Comprender el concepto de espacio de trabajo.
- ✅ Insertar el UR3 en una escena de CoppeliaSim.
- ✅ Localizar sus articulaciones desde el árbol de la escena.
- ✅ Comprender cómo evolucionará la célula robotizada durante esta parte del libro.

Ahora ya conoces el robot con el que trabajaremos durante toda la Parte IV.

En el siguiente capítulo comenzaremos a controlarlo mediante programas escritos en Python.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre un robot móvil y un robot industrial?
2. ¿Por qué el UR3 dispone de seis grados de libertad?
3. ¿Qué función desempeña el efector final?
4. ¿Qué entendemos por espacio de trabajo de un robot?
5. ¿Por qué es importante la estructura jerárquica del árbol de la escena?
6. ¿Qué ocurrirá si colocamos una pieza fuera del espacio de trabajo del UR3?
7. ¿Por qué utilizaremos siempre el mismo robot durante toda la Parte IV?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a programar el robot.

---

## Reto

::: challenge
title: Analizando una célula robotizada

content:

Busca en Internet una fotografía de una célula robotizada equipada con un **Universal Robots UR3** o un **UR3e**.

A continuación responde a las siguientes cuestiones:

- ¿Qué tarea realiza el robot?
- ¿Qué tipo de efector final utiliza?
- ¿Qué otros elementos aparecen en la célula (cintas, sensores, cámaras, mesas...)?
- ¿Qué elementos crees que podremos reproducir posteriormente en CoppeliaSim?

Compara tus respuestas con las de tus compañeros y comenta las diferencias observadas.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Una sesión de 55 minutos.

**Objetivos**

- Familiarizar al alumnado con el robot UR3.
- Identificar correctamente todas las articulaciones.
- Comprender el concepto de espacio de trabajo.
- Preparar el inicio de la programación del robot en Python.

**Material necesario**

- Ordenador con CoppeliaSim.
- Modelo UR3 instalado.
- Proyector.

**Consejos metodológicos**

No dediques demasiado tiempo a explicar el funcionamiento interno de las articulaciones.

El objetivo de este capítulo es que el alumnado pierda el miedo al robot y aprenda a reconocer sus componentes.

La programación comenzará en el siguiente capítulo.

:::

---

## Próximo capítulo

Ya conoces la estructura y el funcionamiento general del robot **Universal Robots UR3**.

Ha llegado el momento de comenzar a programarlo.

En el próximo capítulo aprenderás a acceder desde Python a cada una de sus articulaciones, obtener sus identificadores (*handles*) y controlar individualmente el movimiento de todos sus ejes.

Será el primer paso para desarrollar aplicaciones de robótica industrial mediante CoppeliaSim y Python.
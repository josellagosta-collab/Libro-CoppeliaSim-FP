# Capítulo 5 · Manipulación de objetos y sistemas de coordenadas

::: chapter-cover
number: 5
title: Manipulación de objetos y sistemas de coordenadas
time: 4 horas
level: ⭐⭐☆☆☆ (Básico)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Seleccionar correctamente cualquier objeto de una escena.
- Mover objetos con precisión utilizando las herramientas de transformación.
- Comprender el sistema de coordenadas global y local.
- Modificar la posición y la orientación de un robot.
- Interpretar los ejes X, Y y Z en CoppeliaSim.
- Preparar el robot para comenzar a controlarlo mediante Python.

:::

## ¿Por qué es importante conocer los sistemas de coordenadas?

Cuando observamos un robot en CoppeliaSim resulta muy sencillo desplazarlo utilizando el ratón.

Sin embargo, cuando comencemos a programarlo necesitaremos indicar su posición mediante números.

Por ejemplo:

```text
Posición:

X = 1.25 m

Y = -0.80 m

Z = 0.00 m
```

O indicar su orientación:

```text
Rotación:

α = 0°

β = 0°

γ = 90°
```

Por este motivo, antes de escribir una sola línea de código debemos comprender cómo representa CoppeliaSim la posición y la orientación de todos los objetos.

Este capítulo constituye la base sobre la que construiremos toda la programación posterior.

::: teacher
content:

Dedica tiempo suficiente a este capítulo.

La mayoría de los errores que aparecen cuando los alumnos comienzan a programar tienen su origen en una mala comprensión de los sistemas de referencia.

:::

---

## 5.1 Seleccionando objetos

En cualquier simulación necesitaremos modificar continuamente las propiedades de distintos elementos.

Para ello, el primer paso consiste en seleccionarlos correctamente.

Podemos hacerlo de dos formas diferentes:

- haciendo clic directamente sobre el objeto en la vista tridimensional;
- seleccionándolo desde el árbol de la escena.

Cuando un objeto está seleccionado aparecerá resaltado tanto en la vista 3D como en el árbol jerárquico.

Esta doble representación facilita enormemente el trabajo.

::: figure
image: ../assets/cap05/seleccion_objetos.png
caption: Selección de un objeto desde la vista tridimensional y desde el árbol de la escena.
:::

---

## 5.2 Las herramientas de transformación

Una vez seleccionado un objeto podremos modificar su posición y orientación mediante las herramientas de transformación.

Estas herramientas permiten:

- trasladar un objeto;
- rotarlo;
- modificar su posición con precisión.

Durante este capítulo utilizaremos exclusivamente las operaciones de traslación y rotación.

Más adelante aprenderemos otras transformaciones más avanzadas.

::: figure
image: ../assets/cap05/herramientas_transformacion.png
caption: Herramientas de transformación disponibles en CoppeliaSim.
:::

---

## 5.3 Trasladando un objeto

Trasladar un objeto significa cambiar su posición dentro de la escena sin modificar su orientación.

Supongamos que el robot se encuentra inicialmente en el centro del plano.

Podemos desplazarlo:

- hacia delante;
- hacia atrás;
- hacia la izquierda;
- hacia la derecha.

Durante este movimiento el robot seguirá apuntando en la misma dirección.

Únicamente cambiará su posición.

## 5.4 Rotando un objeto

Además de desplazar un objeto, también podemos modificar su orientación.

Rotar un objeto significa cambiar la dirección hacia la que apunta, manteniendo su posición.

En robótica esta operación resulta imprescindible.

Un robot puede encontrarse exactamente en el mismo punto del espacio y, sin embargo, estar orientado hacia direcciones completamente diferentes.

Por ejemplo:

- mirando hacia el norte;
- mirando hacia una estantería;
- orientado hacia una cinta transportadora;
- preparado para recoger una pieza.

En todos estos casos la posición es la misma, pero la orientación cambia.

::: figure
image: ../assets/cap05/rotacion_robot.png
caption: El mismo robot con diferentes orientaciones sobre una misma posición.
:::

---

### Los ejes de rotación

En un espacio tridimensional un objeto puede girar alrededor de tres ejes.

- Eje X
- Eje Y
- Eje Z

Cada uno de ellos produce un efecto diferente sobre el objeto.

En la mayoría de las prácticas de este libro trabajaremos principalmente con giros alrededor del eje **Z**, ya que los robots móviles se desplazan sobre un plano horizontal.

Más adelante estudiaremos situaciones en las que también será necesario utilizar los otros ejes.

---

## 5.5 Sistema de coordenadas global

Todos los objetos de una escena poseen una posición definida respecto a un sistema de referencia común.

Este sistema recibe el nombre de **sistema de coordenadas global**.

Podemos imaginarlo como el mapa general de toda la escena.

Cada objeto dispone de unas coordenadas únicas respecto a este origen.

::: figure
image: ../assets/cap05/coordenadas_globales.png
caption: Sistema de coordenadas global utilizado por CoppeliaSim.
:::

Cuando indiquemos que un robot se encuentra en una determinada posición, normalmente estaremos haciendo referencia a este sistema global.

---

### Interpretando las coordenadas

Supongamos que el robot se encuentra en la siguiente posición:

```text
X = 1.20 m
Y = -0.50 m
Z = 0.00 m
```

Esto significa que:

- se encuentra 1,20 metros desplazado sobre el eje X;
- está situado -0,50 metros sobre el eje Y;
- permanece apoyado sobre el suelo (Z = 0).

En la mayoría de las simulaciones de robots móviles la coordenada Z apenas variará.

---

## 5.6 Sistema de coordenadas local

Además del sistema global, cada objeto dispone de su propio sistema de referencia.

Este sistema recibe el nombre de **sistema de coordenadas local**.

Podemos imaginarlo como unos ejes que viajan junto con el propio objeto.

Si el robot gira, sus ejes locales también giran.

Este concepto resulta fundamental cuando programemos movimientos relativos.

::: figure
image: ../assets/cap05/coordenadas_locales.png
caption: Sistema de coordenadas local asociado al robot.
:::

---

### ¿Por qué existen dos sistemas de referencia?

La existencia de un sistema global y otro local puede parecer innecesaria al principio.

Sin embargo, ambos responden a necesidades diferentes.

El sistema global nos permite localizar cualquier objeto dentro de la escena.

El sistema local nos permite describir movimientos relativos al propio robot.

Por ejemplo:

- avanzar un metro hacia delante;
- girar noventa grados;
- mover un sensor respecto al chasis.

Estos movimientos tienen sentido únicamente desde el punto de vista del propio robot.

::: teacher
content:

No insistas en memorizar las definiciones.

Es mucho más eficaz utilizar ejemplos prácticos donde el alumnado observe cómo cambian los ejes al mover o girar el robot.

:::

---

## 5.7 Posición frente a orientación

Uno de los errores más habituales consiste en confundir ambos conceptos.

La **posición** indica dónde se encuentra un objeto.

La **orientación** indica hacia dónde está dirigido.

Dos robots pueden compartir exactamente la misma posición y, sin embargo, mirar en direcciones opuestas.

Del mismo modo, dos robots pueden tener exactamente la misma orientación y encontrarse en lugares completamente distintos.

Comprender esta diferencia facilitará enormemente el aprendizaje de la programación de movimientos.

::: common-error
content:

Cuando un robot gira sobre sí mismo no cambia su posición.

Únicamente cambia su orientación.

Muchos estudiantes interpretan ambos conceptos como si fueran la misma cosa durante las primeras prácticas.

:::

---

## 5.8 Manipulación precisa mediante propiedades

Mover un objeto con el ratón resulta rápido y cómodo.

Sin embargo, cuando necesitamos situarlo exactamente en una posición concreta utilizaremos el panel de propiedades.

Desde él podremos introducir directamente los valores de:

- posición X;
- posición Y;
- posición Z;
- orientación alrededor de los ejes X, Y y Z.

Este método garantiza una colocación mucho más precisa que el desplazamiento manual.

En simulaciones complejas esta precisión resulta imprescindible.

::: figure
image: ../assets/cap05/propiedades_posicion.png
caption: Edición manual de la posición y orientación de un objeto mediante el panel de propiedades.
:::

---

## 5.9 Primera práctica de posicionamiento

Vamos a comprobar de forma práctica los conceptos estudiados.

Selecciona el robot y realiza las siguientes acciones:

1. Desplázalo aproximadamente un metro hacia delante.
2. Muévelo medio metro hacia la izquierda.
3. Gíralo noventa grados sobre el eje Z.
4. Observa cómo cambian sus ejes locales.
5. Devuelve el robot a su posición inicial utilizando el panel de propiedades.

Repite el ejercicio varias veces hasta sentirte cómodo manipulando el robot.

No te preocupes todavía por la precisión absoluta.

Lo importante es comprender la diferencia entre mover y orientar un objeto.

::: summary
title: Idea clave

content:

Todo objeto de CoppeliaSim posee dos características fundamentales:

- una **posición**, que indica dónde se encuentra;
- una **orientación**, que indica hacia dónde apunta.

Durante los próximos capítulos aprenderemos a modificar ambas propiedades automáticamente mediante programas escritos en Python.
:::

## 5.10 Sistemas de referencia en robótica

Hasta ahora hemos aprendido que todos los objetos poseen una posición y una orientación.

Sin embargo, cuando trabajemos con robots reales y con programas escritos en Python descubriremos que existen diferentes formas de describir un movimiento.

Podemos indicar al robot:

- una posición absoluta dentro de la escena;
- una posición relativa respecto a otro objeto;
- un desplazamiento respecto a su propia orientación.

Elegir correctamente el sistema de referencia es fundamental para que el robot se comporte como esperamos.

Por ejemplo, si ordenamos a un robot avanzar un metro, normalmente esperamos que lo haga **hacia delante**, independientemente de la orientación que tenga en ese momento.

Este tipo de movimiento utiliza el sistema de referencia local del robot.

En cambio, si indicamos unas coordenadas concretas dentro de la escena, estaremos utilizando el sistema de referencia global.

Comprender esta diferencia facilitará enormemente la programación de trayectorias en los próximos capítulos.

---

## 5.11 Ejemplo práctico

Vamos a realizar un pequeño ejercicio para comprobar cómo influyen la posición y la orientación.

Realiza las siguientes acciones:

1. Inserta un robot Pioneer P3DX en una escena nueva.
2. Colócalo en el centro del plano de trabajo.
3. Gíralo 90° sobre el eje Z.
4. Observa la dirección hacia la que apunta.
5. Gíralo otros 90°.
6. Repite la operación hasta completar una vuelta completa.

Durante este ejercicio comprobarás que el robot permanece prácticamente en la misma posición mientras cambia continuamente su orientación.

A continuación desplázalo varios metros sin modificar su orientación.

Ahora ocurre exactamente lo contrario:

- la posición cambia;
- la orientación permanece constante.

Este sencillo ejercicio resume los dos conceptos fundamentales estudiados en este capítulo.

::: figure
image: ../assets/cap05/posicion_orientacion.png
caption: Comparación entre un cambio de posición y un cambio de orientación.
:::

---

## 5.12 Preparando el robot para Python

Ya conocemos suficientemente bien el entorno de simulación como para comenzar a controlarlo mediante programación.

En el siguiente capítulo conectaremos Python con CoppeliaSim por primera vez.

A partir de ese momento dejaremos de mover el robot manualmente y comenzaremos a enviarle órdenes desde nuestros programas.

Todo lo aprendido hasta ahora seguirá siendo imprescindible.

Cuando indiquemos una posición o una orientación mediante Python estaremos utilizando exactamente los mismos conceptos estudiados en este capítulo.

::: summary
title: Idea clave

content:

Antes de programar un robot es imprescindible comprender cómo representa su posición y su orientación.

Python únicamente automatizará operaciones que ahora ya sabemos realizar manualmente.
:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Posición | Lugar que ocupa un objeto dentro de la escena. |
| Orientación | Dirección hacia la que apunta un objeto. |
| Traslación | Cambio de posición sin modificar la orientación. |
| Rotación | Cambio de orientación manteniendo la posición. |
| Sistema de coordenadas global | Referencia común para todos los objetos de la escena. |
| Sistema de coordenadas local | Referencia propia de cada objeto. |
| Ejes X, Y y Z | Sistema utilizado para definir posiciones y orientaciones. |
| Panel de propiedades | Ventana que permite modificar con precisión los parámetros de un objeto. |
| Transformación | Operación que modifica la posición u orientación de un objeto. |
| Robot diferencial | Robot móvil cuyo movimiento depende de la velocidad independiente de sus ruedas. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Seleccionar cualquier objeto de una escena.
- ✅ Mover objetos con precisión.
- ✅ Rotar un robot sobre sus diferentes ejes.
- ✅ Comprender la diferencia entre posición y orientación.
- ✅ Interpretar los sistemas de coordenadas global y local.
- ✅ Preparar una escena para comenzar a trabajar con Python.

Estos conocimientos constituirán la base de todos los programas que desarrollaremos a partir del próximo capítulo.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre trasladar y rotar un objeto?
2. ¿Qué representan los ejes X, Y y Z?
3. ¿Cuándo utilizamos el sistema de coordenadas global?
4. ¿Qué ventajas ofrece el sistema de coordenadas local?
5. ¿Por qué dos robots pueden ocupar la misma posición y tener orientaciones diferentes?
6. ¿Qué información podemos modificar desde el panel de propiedades?

---

## Práctica guiada

::: practice
title: Manipulación precisa de un robot

difficulty: Baja

time: 40 minutos

content:

Realiza la siguiente práctica.

1. Crea una escena nueva.
2. Inserta un robot Pioneer P3DX.
3. Sitúalo en la posición (0,0,0).
4. Gíralo 90° sobre el eje Z.
5. Desplázalo un metro sobre el eje X.
6. Devuélvelo al origen utilizando el panel de propiedades.
7. Repite el ejercicio modificando ahora la coordenada Y.
8. Guarda la escena.

Observa cómo cambian los valores de posición y orientación después de cada operación.
:::

---

## Reto

::: challenge
title: Diseñando una trayectoria

content:

Coloca tres cajas sobre el suelo formando un triángulo.

Sitúa el robot en un vértice.

Sin utilizar todavía Python, intenta orientarlo manualmente para que quede mirando hacia cada una de las cajas.

¿Qué cambios has realizado en cada caso?

¿Ha cambiado únicamente la orientación o también la posición?

Justifica tu respuesta.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Comprender la diferencia entre posición y orientación.
- Introducir los sistemas de referencia utilizados en robótica.
- Preparar al alumnado para comenzar la programación.

**Material necesario**

- Ordenadores con CoppeliaSim EDU instalado.
- Escena creada en el capítulo anterior.

**Sugerencias metodológicas**

Insiste en que los estudiantes verbalicen los movimientos utilizando expresiones como "trasladar", "rotar", "posición" y "orientación".

El uso correcto de esta terminología facilitará enormemente la comprensión de los capítulos dedicados a Python.
:::

---

## Próximo capítulo

Hasta ahora todas las acciones realizadas sobre el robot han sido manuales.

En el próximo capítulo escribiremos nuestro primer programa en Python y estableceremos la primera comunicación con CoppeliaSim.

Será un momento importante del libro, ya que comenzaremos a controlar el simulador mediante código y daremos el primer paso hacia el desarrollo de aplicaciones de robótica completamente automatizadas.
::: chapter-cover
number: 15
title: Seguimiento visual de objetos
time: 7 horas
level: ⭐⭐⭐⭐☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender los principios del seguimiento visual de objetos.
- Calcular el desplazamiento de un objeto dentro de una imagen.
- Mantener un objeto centrado en el campo de visión de una cámara.
- Utilizar la información visual para controlar el movimiento de un robot móvil.
- Desarrollar aplicaciones básicas de seguimiento utilizando CoppeliaSim, Python y OpenCV.
:::

# Capítulo 15 · Seguimiento visual de objetos

## ¿Qué significa seguir un objeto?

En el capítulo anterior aprendimos a detectar y clasificar objetos presentes en una imagen.

Sin embargo, todas las escenas analizadas tenían una característica común: los objetos permanecían inmóviles.

En muchas aplicaciones reales esto no ocurre.

Las piezas avanzan sobre cintas transportadoras, los vehículos se desplazan, las personas caminan y los robots deben reaccionar continuamente a esos movimientos.

En estas situaciones ya no basta con detectar un objeto una única vez.

Es necesario localizarlo de forma continua y actualizar su posición en cada nueva imagen capturada por la cámara.

Este proceso recibe el nombre de **seguimiento visual de objetos** (*Object Tracking*).

::: teacher
content:

Antes de introducir cualquier algoritmo, plantea ejemplos cotidianos.

Cuando una persona sigue con la mirada una pelota en movimiento está realizando una tarea de seguimiento visual.

El objetivo del capítulo consiste en reproducir ese comportamiento utilizando un robot y una cámara.
:::

---

## 15.1 Del reconocimiento al seguimiento

Detectar un objeto significa responder a la pregunta:

> **¿Dónde está el objeto en este instante?**

Seguir un objeto implica responder continuamente a una pregunta diferente:

> **¿Dónde está ahora y hacia dónde se está desplazando?**

Esta diferencia resulta fundamental.

Mientras que la detección puede realizarse sobre una única imagen, el seguimiento requiere analizar una secuencia continua de imágenes.

Cada nueva captura permite actualizar la posición del objeto.

::: figure
image: ../assets/cap15/fig15_1.png
caption: Evolución desde la detección puntual de un objeto hasta su seguimiento continuo en una secuencia de imágenes.
:::

---

## 15.2 Aplicaciones del seguimiento visual

El seguimiento visual está presente en multitud de aplicaciones robóticas e industriales.

Algunos ejemplos son:

- robots móviles que siguen una línea en el suelo;
- brazos robóticos que recogen piezas en movimiento;
- vehículos autónomos que detectan otros vehículos;
- cámaras de vigilancia que mantienen una persona centrada en la imagen;
- drones que siguen automáticamente un objetivo.

En todos estos casos el sistema debe conocer en cada instante la posición del objeto para poder reaccionar correctamente.

---

## 15.3 El ciclo de seguimiento

Aunque existen numerosos algoritmos de seguimiento, todos ellos comparten una estructura muy similar.

El proceso general puede resumirse en los siguientes pasos:

1. Capturar una imagen desde la cámara.
2. Detectar el objeto de interés.
3. Calcular su posición.
4. Comparar la posición con la imagen anterior.
5. Actualizar el movimiento del robot o del sistema.

Este ciclo se repite continuamente mientras la simulación permanece en funcionamiento.

::: figure
image: ../assets/cap15/fig15_2.png
caption: Ciclo básico de un sistema de seguimiento visual en tiempo real.
:::

Gracias a esta actualización continua, el robot puede reaccionar de forma prácticamente inmediata a cualquier cambio observado en la escena.

---

## 15.4 Seguimiento en tiempo real

En robótica no basta con obtener un resultado correcto.

También es necesario obtenerlo con suficiente rapidez.

Un algoritmo muy preciso pero demasiado lento puede resultar inútil si el objeto cambia de posición antes de finalizar el procesamiento.

Por este motivo, los sistemas de seguimiento visual buscan siempre un equilibrio entre:

- precisión;
- velocidad de procesamiento;
- estabilidad frente a cambios de iluminación o movimiento.

En los siguientes apartados aprenderemos a construir un sistema sencillo que permita mantener un objeto continuamente localizado dentro del campo de visión de la cámara.

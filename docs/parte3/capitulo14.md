::: chapter-cover
number: 14
title: Detección y clasificación de objetos
time: 7 horas
level: ⭐⭐⭐⭐☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo localizar objetos dentro de una imagen.
- Obtener la posición de un objeto utilizando OpenCV.
- Calcular el centro y las dimensiones de un objeto detectado.
- Clasificar objetos según su color, tamaño y forma.
- Preparar la información necesaria para controlar un robot mediante visión artificial.
:::

# Capítulo 14 · Detección y clasificación de objetos

## ¿Qué significa detectar un objeto?

En el capítulo anterior aprendimos a procesar imágenes utilizando OpenCV.

Convertimos imágenes a escala de grises, aplicamos umbralizaciones, detectamos colores y localizamos contornos.

Sin embargo, todavía existía una limitación importante.

Aunque éramos capaces de identificar las regiones donde aparecía un determinado color, el programa aún no sabía qué objeto estaba observando.

Detectar un objeto significa mucho más que encontrar un conjunto de píxeles.

Supone obtener información útil que permita responder a preguntas como:

- ¿Dónde se encuentra el objeto?
- ¿Cuál es su tamaño?
- ¿Qué forma tiene?
- ¿De qué color es?
- ¿Cómo puede acceder un robot hasta él?

Responder a estas preguntas constituye el objetivo principal de este capítulo.

::: teacher
content:

Relaciona este contenido con aplicaciones reales.

Por ejemplo, una cámara situada sobre una cinta transportadora debe indicar al robot la posición exacta de cada pieza para que pueda recogerla correctamente.

El alumnado comprenderá mejor la utilidad de estos algoritmos si los asocia desde el principio con aplicaciones industriales.
:::

---

## 14.1 Del procesamiento a la interpretación

Procesar una imagen consiste en transformarla para facilitar su análisis.

Interpretarla significa extraer información útil a partir de ella.

Esta diferencia resulta fundamental.

Durante el procesamiento modificábamos la imagen.

Ahora utilizaremos esa imagen procesada para tomar decisiones.

Por ejemplo:

- localizar una pieza sobre una mesa;
- medir su tamaño;
- identificar su color;
- determinar si cumple determinadas condiciones.

A partir de este momento el robot comenzará realmente a comprender la escena que observa.

::: figure
image: ../assets/cap14/fig14_1.png
caption: Evolución desde la captura de una imagen hasta la interpretación de los objetos presentes en la escena.
:::

---

## 14.2 ¿Cómo identifica un ordenador un objeto?

Cuando una persona observa una fotografía reconoce inmediatamente una esfera, un cubo o un cilindro.

Un ordenador necesita seguir un procedimiento mucho más estructurado.

Habitualmente el proceso consta de las siguientes etapas.

1. Capturar la imagen mediante una cámara.
2. Procesar la imagen.
3. Detectar regiones de interés.
4. Localizar los contornos.
5. Calcular las características del objeto.
6. Clasificar el objeto.

Cada uno de estos pasos aporta nueva información que permitirá al robot comprender mejor su entorno.

---

## 14.3 Características de un objeto

Una vez detectado un objeto podemos calcular numerosas propiedades.

Entre las más utilizadas en robótica encontramos:

- posición;
- anchura;
- altura;
- área;
- perímetro;
- color predominante;
- forma aproximada.

Estas características reciben el nombre de **descriptores**.

Los descriptores permiten comparar objetos y clasificarlos automáticamente.

::: figure
image: ../assets/cap14/fig14_2.png
caption: Principales características geométricas que pueden obtenerse de un objeto detectado.
:::

Por ejemplo, un sistema de clasificación puede decidir que una pieza pertenece a una determinada categoría si presenta un color concreto y un área comprendida dentro de un determinado intervalo.

---

## 14.4 Aplicaciones industriales

La detección automática de objetos está presente en numerosos sistemas industriales.

Algunos ejemplos habituales son:

- clasificación automática de piezas;
- control de calidad;
- detección de productos defectuosos;
- conteo de objetos;
- guiado de robots industriales;
- inspección de envases;
- selección automática de componentes electrónicos.

Muchas de estas aplicaciones siguen exactamente el mismo flujo que desarrollaremos en este capítulo.

La única diferencia suele encontrarse en el grado de complejidad de los algoritmos utilizados.

En el siguiente apartado comenzaremos a localizar automáticamente los objetos presentes en una imagen utilizando OpenCV.
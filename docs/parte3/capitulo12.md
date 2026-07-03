::: chapter-cover
number: 12
title: Visión artificial con CoppeliaSim
time: 5 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué es la visión artificial aplicada a la robótica.
- Identificar las diferencias entre un sensor de visión y otros sensores utilizados hasta ahora.
- Incorporar una cámara a una escena de CoppeliaSim.
- Capturar imágenes desde Python utilizando la API remota.
- Visualizar imágenes mediante OpenCV.
- Guardar fotografías obtenidas durante una simulación.
:::

# Capítulo 12 · Visión artificial con CoppeliaSim

## ¿Por qué enseñar a un robot a ver?

Hasta ahora hemos trabajado con sensores capaces de responder a preguntas muy concretas.

Un sensor de proximidad puede indicar si existe un obstáculo delante del robot.

Un sensor de distancia permite conocer aproximadamente a qué distancia se encuentra un objeto.

Sin embargo, estos sensores proporcionan información muy limitada.

Las personas obtenemos una enorme cantidad de información simplemente observando nuestro entorno.

Somos capaces de distinguir colores, reconocer objetos, interpretar señales, localizar personas e incluso anticipar movimientos.

Dotar a un robot de una capacidad similar constituye uno de los mayores retos de la robótica moderna.

La disciplina encargada de conseguirlo recibe el nombre de **visión artificial** o **visión por computador**.

En este capítulo comenzaremos a utilizar cámaras virtuales dentro de CoppeliaSim para que nuestros programas en Python puedan analizar imágenes y tomar decisiones basadas en ellas.

::: teacher
content:

Relaciona este capítulo con ejemplos cotidianos.

Los estudiantes utilizan continuamente sistemas de visión artificial sin ser conscientes de ello: desbloqueo facial del teléfono móvil, asistentes de conducción, lectores de códigos QR o sistemas automáticos de clasificación de paquetes.
:::

---

## 12.1 ¿Qué es la visión artificial?

La visión artificial es la rama de la robótica y de la inteligencia artificial que permite a un ordenador interpretar imágenes obtenidas mediante una cámara.

El objetivo no consiste únicamente en capturar una fotografía.

Lo realmente importante es extraer información útil de esa imagen.

Por ejemplo, un programa puede determinar:

- dónde se encuentra un objeto;
- cuál es su color;
- cuál es su forma;
- cuánto mide;
- hacia dónde se está desplazando;
- si pertenece a una categoría determinada.

Gracias a esta información, un robot puede adaptar su comportamiento al entorno de forma automática.

La visión artificial constituye actualmente una tecnología imprescindible en numerosos sectores industriales.

::: figure
image: ../assets/cap12/figura12_1.png
caption: La visión artificial permite que un robot interprete visualmente su entorno mediante una cámara y algoritmos de procesamiento de imágenes.
:::

---

## 12.2 ¿Qué es un sensor de visión?

En CoppeliaSim, una cámara recibe el nombre de **Vision Sensor**.

Un sensor de visión simula el funcionamiento de una cámara digital.

Durante cada ciclo de simulación captura una imagen del entorno visible desde su posición.

Posteriormente esa imagen puede procesarse utilizando Python y bibliotecas como OpenCV.

A diferencia de otros sensores estudiados anteriormente, un sensor de visión no devuelve un único valor numérico.

Su salida es una imagen formada por miles de píxeles.

Cada píxel almacena información sobre el color observado en una determinada posición.

Esto permite obtener una enorme cantidad de información sobre la escena.

---

### Comparación con otros sensores

Hasta este momento hemos utilizado sensores especializados.

Cada uno proporcionaba una información muy concreta.

Una cámara, por el contrario, concentra toda esa información en una única imagen que posteriormente deberá analizar el programa.

::: table
caption: Comparación entre diferentes sensores utilizados en robótica.
content:

| Sensor | Información proporcionada |
|---------|---------------------------|
| Sensor de proximidad | Detecta la presencia de un obstáculo. |
| Sensor de distancia | Estima la separación respecto a un objeto. |
| Sensor de visión | Captura una imagen completa del entorno. |
:::

Esta diferencia convierte a las cámaras en uno de los sensores más versátiles, aunque también en uno de los más complejos de utilizar.

---

## 12.3 Aplicaciones reales

Actualmente resulta difícil encontrar una instalación automatizada que no incorpore algún sistema de visión artificial.

Algunas aplicaciones habituales son:

- inspección automática de piezas;
- clasificación de productos;
- lectura de códigos QR y códigos de barras;
- reconocimiento de matrículas;
- guiado de robots móviles;
- detección de personas;
- control de calidad en líneas de producción;
- robots colaborativos con cámaras integradas.

En este libro aprenderemos progresivamente las técnicas necesarias para desarrollar aplicaciones similares utilizando CoppeliaSim y Python.

::: figure
image: ../assets/cap12/figura12_2.png
caption: Ejemplos de aplicaciones industriales de la visión artificial en robótica y automatización.
:::

---

## 12.4 La visión artificial en CoppeliaSim

CoppeliaSim incorpora sensores de visión completamente funcionales que pueden situarse en cualquier lugar de una escena.

Estos sensores permiten:

- capturar imágenes en color;
- obtener mapas de profundidad;
- simular diferentes resoluciones;
- modificar el campo de visión;
- orientar la cámara libremente;
- enviar las imágenes a programas externos mediante la API remota.

Gracias a estas características podremos desarrollar y probar algoritmos de visión artificial sin necesidad de disponer inicialmente de una cámara física.

En el siguiente apartado incorporaremos nuestro primer sensor de visión a una escena y aprenderemos a configurarlo correctamente.
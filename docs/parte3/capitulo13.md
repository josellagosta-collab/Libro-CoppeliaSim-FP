::: chapter-cover
number: 13
title: Procesamiento básico de imágenes
time: 6 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo se representa una imagen digital.
- Diferenciar los distintos canales de color de una imagen RGB.
- Utilizar OpenCV para acceder a los píxeles de una imagen.
- Convertir imágenes entre diferentes espacios de color.
- Preparar imágenes para su posterior procesamiento.
:::

# Capítulo 13 · Procesamiento básico de imágenes

## ¿Por qué es necesario procesar una imagen?

En el capítulo anterior aprendimos a capturar imágenes desde un **Vision Sensor** y a visualizarlas mediante OpenCV.

Sin embargo, una imagen por sí sola no proporciona ninguna información útil a un robot.

Para un ordenador, una fotografía no es más que una enorme colección de números organizados en forma de matriz.

El verdadero objetivo de la visión artificial consiste en transformar esos datos en información que permita tomar decisiones.

Por ejemplo, un robot puede responder a preguntas como:

- ¿Dónde se encuentra una pieza?
- ¿De qué color es?
- ¿Qué forma tiene?
- ¿Cuáles son sus dimensiones?
- ¿Está correctamente colocada?

Responder a estas preguntas requiere procesar previamente la imagen capturada.

En este capítulo aprenderemos las técnicas fundamentales que constituyen la base de prácticamente todos los sistemas modernos de visión artificial.

::: teacher
content:

Insiste en que el procesamiento de imágenes no pretende mejorar el aspecto de una fotografía, sino facilitar que un ordenador pueda interpretarla.

Este cambio de perspectiva suele resultar muy útil para comprender el objetivo real de OpenCV.
:::

---

## 13.1 Una imagen vista por un ordenador

Cuando una persona observa una fotografía identifica inmediatamente colores, objetos y formas.

Un ordenador, sin embargo, únicamente recibe una gran cantidad de valores numéricos.

Cada fotografía puede entenderse como una matriz formada por millones de píxeles.

Cada uno de esos píxeles almacena información sobre el color observado en una posición concreta.

::: figure
image: ../assets/cap13/fig13_1.png
caption: Una imagen digital está formada por una matriz de píxeles, donde cada posición almacena información de color.
:::

Cuanto mayor sea el número de píxeles, mayor será el nivel de detalle de la imagen.

Sin embargo, también aumentará el tiempo necesario para procesarla.

Por este motivo, en robótica suele buscarse un equilibrio entre resolución y velocidad.

---

## 13.2 El modelo de color RGB

La mayoría de las cámaras digitales trabajan utilizando el modelo de color **RGB**.

Su nombre procede de las iniciales de los tres colores primarios de la luz:

- **R (Red)**: rojo.
- **G (Green)**: verde.
- **B (Blue)**: azul.

Cada píxel almacena tres valores independientes correspondientes a estos tres canales.

Combinando diferentes intensidades de rojo, verde y azul es posible representar millones de colores distintos.

::: figure
image: ../assets/cap13/fig13_2.png
caption: Cada píxel de una imagen RGB está formado por tres componentes: rojo, verde y azul.
:::

En OpenCV cada componente suele representarse mediante un número comprendido entre **0** y **255**.

Por ejemplo:

| Color | R | G | B |
|--------|--:|--:|--:|
| Negro | 0 | 0 | 0 |
| Blanco | 255 | 255 | 255 |
| Rojo | 255 | 0 | 0 |
| Verde | 0 | 255 | 0 |
| Azul | 0 | 0 | 255 |
| Amarillo | 255 | 255 | 0 |

Gracias a esta representación matemática, un programa puede analizar cada píxel de manera independiente.

---

## 13.3 Accediendo a los píxeles de una imagen

Cuando OpenCV carga una imagen, la almacena como una matriz multidimensional.

Cada posición de esa matriz corresponde a un píxel.

Esto permite acceder directamente a cualquier punto de la imagen.

Por ejemplo, podremos conocer el color almacenado en una posición concreta o modificarlo mediante programación.

En los siguientes apartados aprenderemos a utilizar esta información para transformar imágenes y facilitar la detección de objetos.

---

## 13.4 Preparando las imágenes para OpenCV

En muchas aplicaciones no resulta conveniente trabajar directamente con la imagen original.

Antes de comenzar el procesamiento suele ser necesario realizar algunas transformaciones.

Entre las más habituales encontramos:

- convertir la imagen a escala de grises;
- eliminar ruido;
- resaltar determinadas zonas;
- aislar colores concretos;
- crear imágenes binarias.

Estas técnicas simplifican enormemente el trabajo de los algoritmos de visión artificial.

En el siguiente apartado comenzaremos con la transformación más utilizada de todas: la conversión a escala de grises.

---

## 13.5 Conversión a escala de grises

Hasta ahora hemos trabajado con imágenes en color.

Sin embargo, en muchas aplicaciones de visión artificial no resulta necesario conservar toda la información cromática.

En numerosas ocasiones basta con conocer la intensidad luminosa de cada píxel.

Para ello se utiliza la **escala de grises**.

En una imagen en escala de grises cada píxel queda representado por un único valor comprendido entre **0** y **255**.

- **0** representa el negro.
- **255** representa el blanco.
- Los valores intermedios corresponden a diferentes tonos de gris.

Al reducir tres componentes de color (R, G y B) a un único valor, la imagen resulta mucho más sencilla de procesar.

::: figure
image: ../assets/cap13/fig13_3.png
caption: Conversión de una imagen RGB a escala de grises.
:::

Además de simplificar el procesamiento, trabajar con imágenes en escala de grises reduce la cantidad de información que debe manejar el programa.

Por este motivo constituye uno de los primeros pasos en numerosos algoritmos de visión artificial.

---

## 13.6 Conversión mediante OpenCV

OpenCV incorpora funciones específicas para convertir imágenes entre distintos espacios de color.

La conversión desde RGB hasta escala de grises puede realizarse con una única instrucción.

```python
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
```

Aunque el nombre de la constante indica **BGR**, no se trata de un error.

OpenCV almacena internamente las imágenes utilizando el orden:

- Azul (Blue)
- Verde (Green)
- Rojo (Red)

Este detalle puede sorprender al principio, pero constituye el comportamiento habitual de la biblioteca.

Tras ejecutar la conversión obtendremos una nueva imagen formada por un único canal de intensidad.

A partir de este momento muchas operaciones de procesamiento serán considerablemente más sencillas.

::: common-error
content:

Uno de los errores más frecuentes consiste en utilizar directamente imágenes RGB con funciones que esperan imágenes en escala de grises.

Comprueba siempre qué tipo de imagen necesita cada función de OpenCV antes de utilizarla.
:::

---

## 13.7 ¿Por qué convertir una imagen a escala de grises?

Puede parecer que eliminar el color supone perder información.

Sin embargo, en muchos problemas ocurre exactamente lo contrario.

Eliminar la información cromática permite centrar la atención únicamente en la forma y la intensidad de los objetos.

Por ejemplo, si queremos detectar el contorno de una pieza metálica, normalmente resulta irrelevante conocer su color.

Lo importante será distinguir claramente el objeto respecto al fondo.

Entre las aplicaciones más habituales encontramos:

- detección de bordes;
- reconocimiento de formas;
- lectura de códigos;
- identificación de texto;
- segmentación de objetos.

En todos estos casos la escala de grises simplifica considerablemente el procesamiento.

---

## 13.8 Imágenes binarias

Una vez convertida la imagen a escala de grises podemos dar un paso más.

En lugar de trabajar con 256 niveles de intensidad, podemos reducir la imagen únicamente a dos posibilidades:

- negro;
- blanco.

Este proceso recibe el nombre de **binarización** o **umbralización** (*Thresholding*).

El resultado es una imagen mucho más sencilla de interpretar.

::: figure
image: ../assets/cap13/fig13_4.png
caption: Proceso de umbralización para obtener una imagen binaria.
:::

En una imagen binaria:

- los píxeles negros suelen representar el fondo;
- los píxeles blancos representan normalmente el objeto de interés.

Aunque esta decisión puede invertirse según la aplicación, el objetivo siempre es separar claramente ambas regiones.

---

## 13.9 El concepto de umbral

La umbralización consiste en comparar cada píxel con un valor denominado **umbral**.

El funcionamiento puede resumirse de la siguiente forma.

Si el valor del píxel es mayor que el umbral:

```text
Píxel → Blanco (255)
```

En caso contrario:

```text
Píxel → Negro (0)
```

Por ejemplo, utilizando un umbral de **120**:

| Intensidad original | Resultado |
|--------------------:|----------|
| 35 | Negro |
| 82 | Negro |
| 119 | Negro |
| 120 | Blanco |
| 180 | Blanco |
| 240 | Blanco |

Gracias a esta transformación el ordenador puede distinguir mucho más fácilmente los objetos presentes en la imagen.

---

## 13.10 Umbralización con OpenCV

OpenCV proporciona la función `threshold()` para realizar este proceso automáticamente.

Un ejemplo sencillo es el siguiente.

```python
_, imagen_binaria = cv2.threshold(
    imagen_gris,
    120,
    255,
    cv2.THRESH_BINARY
)
```

Los parámetros más importantes son:

- imagen de entrada;
- valor del umbral;
- valor asignado a los píxeles blancos;
- tipo de umbralización.

En este capítulo utilizaremos únicamente la modalidad **THRESH_BINARY**.

Más adelante conoceremos otras variantes que permiten resolver problemas más complejos.

::: teacher
content:

Dedica unos minutos a modificar el valor del umbral durante la clase.

Los estudiantes comprenden mucho mejor este concepto cuando observan cómo cambia la imagen al pasar, por ejemplo, de un umbral de 50 a otro de 180.
:::

---

## 13.11 Primera segmentación de objetos

La combinación de escala de grises y umbralización constituye uno de los procedimientos más utilizados en visión artificial.

Gracias a estas dos operaciones podemos separar visualmente los objetos del fondo y preparar la imagen para algoritmos más avanzados.

En el siguiente apartado aprenderemos a aprovechar esta información para detectar colores concretos mediante OpenCV.

---

## 13.12 Detección de colores

Hasta ahora hemos aprendido a simplificar una imagen convirtiéndola a escala de grises y posteriormente en una imagen binaria.

Sin embargo, en muchas aplicaciones industriales el color constituye precisamente la información más importante.

Por ejemplo, una línea de producción puede clasificar piezas rojas, verdes y azules en diferentes contenedores.

Un robot móvil puede seguir una línea amarilla pintada sobre el suelo.

Un sistema de inspección puede comprobar si un piloto luminoso está encendido o apagado.

En todos estos casos necesitamos identificar colores concretos dentro de una imagen.

OpenCV proporciona herramientas muy potentes para realizar esta tarea de forma rápida y eficiente.

::: figure
image: ../assets/cap13/fig13_5.png
caption: Detección de un color específico dentro de una imagen mediante OpenCV.
:::

---

## 13.13 ¿Por qué no utilizar directamente RGB?

Podría parecer lógico detectar un objeto rojo buscando simplemente valores elevados en el canal **R** y valores bajos en **G** y **B**.

Sin embargo, este método presenta importantes inconvenientes.

La iluminación de la escena influye notablemente sobre los valores RGB.

El mismo objeto puede presentar valores diferentes dependiendo de:

- la intensidad de la luz;
- la posición de la cámara;
- las sombras;
- los reflejos.

Para solucionar este problema suele utilizarse otro espacio de color denominado **HSV**.

---

## 13.14 El espacio de color HSV

Las siglas **HSV** corresponden a:

- **H (Hue)**: tono o color.
- **S (Saturation)**: saturación o intensidad del color.
- **V (Value)**: brillo.

Este modelo separa el color de la iluminación, lo que facilita enormemente la detección de objetos.

Por ejemplo, un objeto rojo seguirá teniendo prácticamente el mismo valor de tono aunque cambie ligeramente la iluminación.

::: figure
image: ../assets/cap13/fig13_6.png
caption: Comparación entre los modelos de color RGB y HSV.
:::

Por este motivo, la mayoría de las aplicaciones de visión artificial trabajan internamente utilizando HSV cuando necesitan detectar colores.

---

## 13.15 Conversión de RGB a HSV

OpenCV permite convertir una imagen RGB al espacio HSV mediante una única instrucción.

```python
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
```

Una vez realizada la conversión podremos seleccionar un rango de colores.

Por ejemplo, para detectar un objeto rojo definiremos un intervalo mínimo y máximo de valores HSV.

De esta forma OpenCV podrá identificar únicamente los píxeles pertenecientes a dicho intervalo.

---

## 13.16 Creando una máscara

Una vez definido el rango de color utilizaremos la función `inRange()`.

Esta función compara todos los píxeles de la imagen y genera una nueva imagen denominada **máscara**.

En la máscara:

- los píxeles pertenecientes al color buscado aparecen en blanco;
- el resto de la imagen aparece en negro.

El siguiente ejemplo muestra el procedimiento general.

```python
import numpy as np

limite_inferior = np.array([0, 120, 70])
limite_superior = np.array([10, 255, 255])

mascara = cv2.inRange(
    imagen_hsv,
    limite_inferior,
    limite_superior
)
```

El resultado es una imagen binaria donde únicamente permanecen visibles las regiones cuyo color coincide con el rango especificado.

Esta máscara podrá utilizarse posteriormente para localizar objetos dentro de la escena.

::: common-error
content:

Uno de los errores más habituales consiste en utilizar directamente valores RGB con la función `inRange()`.

Recuerda que previamente debes convertir la imagen al espacio de color HSV.
:::

---

## 13.17 Visualizando la máscara

Una vez creada la máscara podemos visualizarla exactamente igual que cualquier otra imagen.

```python
cv2.imshow("Mascara", mascara)
```

La ventana mostrará únicamente dos colores.

- Blanco: píxeles que cumplen la condición.
- Negro: resto de la imagen.

Esta representación resulta extremadamente útil porque simplifica enormemente el trabajo de los algoritmos posteriores.

En muchos casos la detección de objetos comienza precisamente con la obtención de una máscara binaria.

---

## 13.18 Primera detección de un objeto por color

Como primera práctica utilizaremos una escena formada por varias figuras geométricas de diferentes colores.

El objetivo consistirá en detectar únicamente los objetos de color rojo.

Para ello realizaremos los siguientes pasos.

1. Capturar la imagen desde el Vision Sensor.
2. Convertirla al espacio HSV.
3. Definir el rango correspondiente al color rojo.
4. Generar la máscara.
5. Mostrar el resultado utilizando OpenCV.

Al ejecutar el programa observaremos que únicamente permanecen visibles los objetos cuyo color coincide con el intervalo seleccionado.

En el siguiente apartado aprenderemos a utilizar esta información para localizar automáticamente dichos objetos dentro de la imagen.

::: teacher
content:

Anima al alumnado a modificar los rangos HSV y comprobar cómo cambia la máscara obtenida.

Este sencillo experimento ayuda a comprender que la detección de colores depende de un intervalo de valores y no de un único color exacto.
:::

---

## 13.19 Detección de contornos

Hasta ahora hemos aprendido a obtener una máscara binaria que resalta únicamente los objetos cuyo color coincide con un determinado intervalo.

El siguiente paso consiste en localizar automáticamente dichos objetos dentro de la imagen.

Para ello utilizaremos los **contornos**.

Un contorno es la línea que delimita el borde exterior de un objeto.

Si conseguimos detectar correctamente ese borde, podremos conocer:

- la posición del objeto;
- su tamaño;
- su forma;
- su orientación aproximada.

Los contornos constituyen uno de los recursos más utilizados en visión artificial industrial.

::: figure
image: ../assets/cap13/fig13_7.png
caption: Detección de los contornos de varios objetos presentes en una imagen binaria.
:::

---

## 13.20 Localizando los contornos con OpenCV

OpenCV incorpora la función `findContours()` para localizar automáticamente todos los contornos presentes en una imagen binaria.

Su utilización básica es muy sencilla.

```python
contornos, _ = cv2.findContours(
    mascara,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

El resultado es una colección de contornos.

Cada uno de ellos representa un objeto detectado en la imagen.

Posteriormente podremos recorrer esa colección utilizando un bucle.

```python
for contorno in contornos:
    print(contorno)
```

Aunque inicialmente los datos puedan parecer complejos, en realidad cada contorno está formado por una sucesión de puntos que describen el borde del objeto.

---

## 13.21 Dibujando los contornos

Una vez detectados los contornos resulta muy útil representarlos sobre la imagen original.

De esta forma podremos comprobar visualmente que el algoritmo funciona correctamente.

OpenCV proporciona la función `drawContours()`.

```python
cv2.drawContours(
    imagen,
    contornos,
    -1,
    (0,255,0),
    2
)
```

Al ejecutar el programa aparecerá un borde verde rodeando cada uno de los objetos detectados.

Este sencillo procedimiento facilita enormemente la depuración de aplicaciones de visión artificial.

::: common-error
content:

Si no aparece ningún contorno, comprueba primero la máscara binaria.

En la mayoría de los casos el problema no se encuentra en `findContours()`, sino en un rango HSV incorrecto o en una umbralización inadecuada.
:::

---

## 13.22 Área de un objeto

Una vez localizado un contorno podemos calcular distintas propiedades geométricas.

La más sencilla es el **área**.

OpenCV incorpora la función `contourArea()`.

```python
area = cv2.contourArea(contorno)

print(area)
```

El área se expresa en píxeles cuadrados.

Este dato resulta muy útil para eliminar pequeñas regiones producidas por ruido o para distinguir objetos grandes de otros más pequeños.

En muchas aplicaciones industriales basta con establecer un área mínima para descartar falsas detecciones.

---

## 13.23 Región de interés (ROI)

En ocasiones no resulta necesario procesar toda la imagen.

Podemos limitar el análisis únicamente a una zona concreta.

Esta zona recibe el nombre de **ROI** (*Region of Interest*).

Trabajar con una región de interés presenta varias ventajas.

- Reduce el tiempo de procesamiento.
- Elimina información irrelevante.
- Disminuye la probabilidad de falsas detecciones.

::: figure
image: ../assets/cap13/fig13_8.png
caption: Ejemplo de una región de interés (ROI) utilizada para limitar el procesamiento de la imagen.
:::

Por ejemplo, si sabemos que una cinta transportadora ocupa únicamente la parte inferior de la imagen, podremos ignorar completamente el resto de la escena.

---

## 13.24 Seleccionando una ROI

En OpenCV una región de interés puede obtenerse utilizando la indexación de matrices.

```python
roi = imagen[
    150:350,
    100:500
]
```

A partir de ese momento todas las operaciones de procesamiento podrán realizarse únicamente sobre la región seleccionada.

Esto reduce considerablemente el tiempo de cálculo, especialmente cuando se trabaja con imágenes de alta resolución.

---

## 13.25 Primera aplicación completa

Ya disponemos de todos los elementos necesarios para desarrollar una aplicación sencilla de visión artificial.

El procedimiento completo será el siguiente.

1. Capturar la imagen desde el Vision Sensor.
2. Convertirla al espacio HSV.
3. Detectar un color determinado.
4. Generar la máscara binaria.
5. Localizar los contornos.
6. Dibujar los contornos sobre la imagen.
7. Mostrar el resultado utilizando OpenCV.

Este flujo constituye la base de numerosos sistemas industriales de inspección y clasificación automática.

En el siguiente capítulo utilizaremos exactamente este procedimiento para detectar objetos, calcular su posición y obtener sus coordenadas dentro de la imagen.

::: practice
title: Detectando objetos por color

difficulty: Media

time: 45 minutos

content:

Construye una escena con varias figuras geométricas de diferentes colores.

Desarrolla un programa que:

1. Capture la imagen del Vision Sensor.
2. Convierta la imagen al espacio HSV.
3. Detecte únicamente los objetos de color azul.
4. Genere la máscara correspondiente.
5. Localice todos los contornos.
6. Dibuje los contornos sobre la imagen original.
7. Muestre el resultado utilizando OpenCV.

Como ampliación, modifica el programa para detectar dos colores distintos y comparar el número de objetos encontrados para cada uno de ellos.
:::

::: teacher
content:

Es recomendable que el alumnado experimente con diferentes valores HSV y observe cómo afectan a la detección de contornos.

Esta práctica ayuda a comprender la importancia de una buena segmentación antes de aplicar algoritmos más avanzados.
:::

---

# Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Imagen digital | Conjunto de píxeles organizados en filas y columnas que representan visualmente una escena. |
| Píxel | Unidad mínima de una imagen digital que almacena información de color o intensidad. |
| Modelo RGB | Espacio de color basado en los componentes rojo, verde y azul. |
| Modelo HSV | Espacio de color basado en tono, saturación y brillo, especialmente útil para detectar colores. |
| Escala de grises | Representación de una imagen utilizando únicamente niveles de intensidad. |
| Umbralización | Conversión de una imagen en escala de grises en una imagen binaria mediante un valor de umbral. |
| Máscara | Imagen binaria que resalta únicamente las regiones que cumplen una determinada condición. |
| Contorno | Línea que delimita el borde exterior de un objeto detectado en una imagen. |
| ROI (Region of Interest) | Zona concreta de la imagen sobre la que se realiza el procesamiento. |
| OpenCV | Biblioteca de visión artificial utilizada para procesar imágenes y vídeos desde Python. |
:::

---

# En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender cómo representa un ordenador una imagen digital.
- ✅ Diferenciar los modelos de color RGB y HSV.
- ✅ Convertir imágenes a escala de grises mediante OpenCV.
- ✅ Aplicar umbralizaciones para obtener imágenes binarias.
- ✅ Detectar colores utilizando máscaras HSV.
- ✅ Localizar contornos de objetos.
- ✅ Trabajar con regiones de interés (ROI).
- ✅ Preparar imágenes para aplicaciones reales de visión artificial.

A partir de este momento ya dispones de las herramientas básicas necesarias para comenzar a detectar y analizar objetos presentes en una imagen.

---

# Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencias existen entre los modelos de color RGB y HSV?
2. ¿Por qué resulta útil convertir una imagen a escala de grises?
3. ¿Qué función realiza una umbralización?
4. ¿Qué es una máscara y para qué se utiliza?
5. ¿Qué información proporciona un contorno?
6. ¿Qué ventajas ofrece trabajar únicamente con una región de interés (ROI)?
7. ¿Por qué OpenCV utiliza normalmente el espacio HSV para detectar colores?

Si puedes responder correctamente a todas estas preguntas, estás preparado para comenzar a detectar y clasificar objetos mediante visión artificial.

---

# Práctica guiada

::: practice
title: Detección de objetos mediante procesamiento de imágenes

difficulty: Media

time: 60 minutos

content:

Crea una escena formada por varias figuras geométricas de diferentes colores y desarrolla un programa que realice las siguientes operaciones.

1. Captura una imagen desde el Vision Sensor.
2. Convierte la imagen al espacio HSV.
3. Detecta únicamente los objetos de color verde.
4. Genera la máscara correspondiente.
5. Localiza todos los contornos encontrados.
6. Dibuja los contornos sobre la imagen original.
7. Limita el procesamiento utilizando una región de interés.
8. Muestra simultáneamente la imagen original, la máscara y la imagen con los contornos detectados.

Comprueba cómo varían los resultados al modificar el rango HSV y el tamaño de la región de interés.
:::

---

# Reto

::: challenge
title: Sistema de clasificación por colores

content:

Diseña una pequeña estación de clasificación virtual formada por varias piezas de distintos colores.

Desarrolla un programa capaz de:

- detectar automáticamente cada color;
- contar el número de objetos encontrados;
- calcular el área aproximada de cada objeto;
- mostrar los contornos sobre la imagen original.

Como ampliación, intenta identificar cuál es el objeto de mayor tamaño presente en la escena.

Este ejercicio reproduce el funcionamiento básico de numerosos sistemas de inspección industrial utilizados actualmente en líneas automáticas de producción.
:::

---

# Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre dos y tres sesiones de 55 minutos.

**Objetivos**

- Comprender la representación digital de una imagen.
- Introducir el procesamiento de imágenes mediante OpenCV.
- Aprender a detectar colores utilizando el espacio HSV.
- Utilizar contornos para localizar objetos.
- Optimizar el procesamiento mediante regiones de interés.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Python.
- Biblioteca OpenCV (`opencv-python`).
- Escena con un Vision Sensor y varios objetos de colores.

**Consejos metodológicos**

Conviene que el alumnado experimente modificando los rangos HSV para comprobar cómo afectan a la detección de objetos.

También resulta recomendable utilizar escenas con diferentes condiciones de iluminación para justificar por qué el espacio HSV ofrece mejores resultados que RGB en tareas de segmentación por color.

Antes de finalizar el capítulo, realiza una demostración completa del flujo de procesamiento:

Imagen → HSV → Máscara → Contornos → ROI → Resultado final.

Esta visión global facilitará la comprensión del siguiente capítulo.
:::

---

# Próximo capítulo

Hasta ahora hemos aprendido a procesar imágenes y a obtener información básica sobre los objetos presentes en una escena.

Ha llegado el momento de utilizar toda esa información para desarrollar aplicaciones completas de visión artificial.

En el siguiente capítulo aprenderás a detectar y clasificar objetos automáticamente, calcular sus dimensiones, localizar su posición dentro de la imagen y obtener sus coordenadas para que un robot pueda interactuar con ellos.

Este será el primer paso hacia aplicaciones de inspección industrial, clasificación automática y manipulación robótica basadas en visión artificial.
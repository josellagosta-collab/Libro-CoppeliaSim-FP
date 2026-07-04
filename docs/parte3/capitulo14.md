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

---

## 14.5 Localizando un objeto dentro de una imagen

Una vez detectado un objeto mediante su contorno, el siguiente paso consiste en conocer su posición.

Esta información resulta imprescindible en numerosas aplicaciones robóticas.

Por ejemplo:

- un brazo robótico necesita conocer dónde se encuentra una pieza para poder recogerla;
- un robot móvil debe localizar una línea para poder seguirla;
- un sistema de inspección necesita saber dónde aparece un defecto sobre una superficie.

En todos estos casos no basta con detectar el objeto.

También es necesario conocer su ubicación dentro de la imagen.

---

## 14.6 El rectángulo envolvente (*Bounding Box*)

La forma más sencilla de localizar un objeto consiste en calcular el rectángulo más pequeño que lo contiene completamente.

Este rectángulo recibe el nombre de **Bounding Box** o **rectángulo envolvente**.

OpenCV permite obtenerlo fácilmente mediante la función `boundingRect()`.

```python
x, y, ancho, alto = cv2.boundingRect(contorno)
```

Esta función devuelve cuatro valores.

| Variable | Significado |
|----------|-------------|
| `x` | Coordenada horizontal de la esquina superior izquierda. |
| `y` | Coordenada vertical de la esquina superior izquierda. |
| `ancho` | Anchura del rectángulo. |
| `alto` | Altura del rectángulo. |

Con estos cuatro datos ya conocemos la posición aproximada del objeto dentro de la imagen.

::: figure
image: ../assets/cap14/fig14_3.png
caption: Rectángulo envolvente (Bounding Box) obtenido a partir del contorno de un objeto.
:::

---

## 14.7 Dibujando el rectángulo

Una vez calculado el rectángulo podemos representarlo sobre la imagen.

Esto facilita comprobar visualmente que la detección se ha realizado correctamente.

```python
cv2.rectangle(
    imagen,
    (x, y),
    (x + ancho, y + alto),
    (0,255,0),
    2
)
```

Al ejecutar el programa aparecerá un rectángulo verde rodeando completamente el objeto detectado.

Este procedimiento se utiliza continuamente en aplicaciones industriales y constituye una de las representaciones más habituales de la visión artificial.

::: common-error
content:

Si el rectángulo aparece desplazado o rodea zonas que no pertenecen al objeto, revisa primero la máscara binaria y el contorno obtenido.

Un contorno incorrecto siempre producirá un rectángulo incorrecto.
:::

---

## 14.8 Calculando el centro del objeto

Además de conocer la posición del rectángulo, normalmente interesa calcular el punto central del objeto.

El centro puede obtenerse mediante una sencilla operación matemática.

```python
centro_x = x + ancho // 2
centro_y = y + alto // 2
```

Las coordenadas `(centro_x, centro_y)` representan el centro aproximado del objeto dentro de la imagen.

Este punto será especialmente importante cuando el robot deba desplazarse hacia un objeto o mantenerlo centrado en la imagen.

::: figure
image: ../assets/cap14/fig14_4.png
caption: Cálculo del centro del objeto a partir del rectángulo envolvente.
:::

---

## 14.9 Representando el centro

Para facilitar la depuración del programa resulta muy útil dibujar el centro del objeto.

OpenCV proporciona la función `circle()`.

```python
cv2.circle(
    imagen,
    (centro_x, centro_y),
    5,
    (0,0,255),
    -1
)
```

El resultado será un pequeño punto rojo situado en el centro del objeto.

De esta forma podremos comprobar inmediatamente si el cálculo es correcto.

En aplicaciones de seguimiento visual este punto suele utilizarse como referencia para controlar el movimiento del robot.

---

## 14.10 Mostrando las coordenadas

También podemos escribir sobre la imagen las coordenadas obtenidas.

```python
texto = f"({centro_x}, {centro_y})"

cv2.putText(
    imagen,
    texto,
    (x, y - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (255,255,255),
    2
)
```

De esta forma la imagen mostrará tanto el rectángulo envolvente como las coordenadas del objeto.

Esta representación resulta muy útil durante el desarrollo y la depuración de aplicaciones de visión artificial.

---

## 14.11 Primera localización automática

Ya disponemos de todos los elementos necesarios para localizar automáticamente un objeto.

El procedimiento completo será el siguiente.

1. Capturar la imagen desde el Vision Sensor.
2. Procesarla utilizando OpenCV.
3. Detectar el objeto.
4. Obtener el contorno.
5. Calcular el rectángulo envolvente.
6. Calcular el centro del objeto.
7. Dibujar el rectángulo y el punto central.
8. Mostrar las coordenadas sobre la imagen.

Este flujo constituye la base de numerosos sistemas de guiado visual utilizados en robótica industrial.

::: practice
title: Localización de un objeto

difficulty: Media

time: 45 minutos

content:

Construye una escena con varios objetos de diferentes colores.

Desarrolla un programa que:

1. Detecte únicamente los objetos verdes.
2. Obtenga el rectángulo envolvente de cada uno.
3. Dibuje el rectángulo sobre la imagen.
4. Calcule el centro de cada objeto.
5. Muestre las coordenadas correspondientes.

Como ampliación, identifica cuál de los objetos detectados se encuentra más próximo al centro de la imagen.
:::

::: teacher
content:

Es recomendable utilizar inicialmente objetos separados entre sí.

Una vez comprendido el funcionamiento del algoritmo, pueden introducirse objetos parcialmente superpuestos para analizar cómo afectan a la detección de contornos y al cálculo del rectángulo envolvente.
:::

---

## 14.12 Midiendo un objeto

Localizar un objeto constituye únicamente el primer paso.

En la mayoría de las aplicaciones industriales también resulta necesario conocer sus dimensiones.

Por ejemplo, un sistema de clasificación puede separar piezas grandes de piezas pequeñas.

Del mismo modo, un robot puede decidir si una pieza es válida o defectuosa comparando sus dimensiones con unas medidas de referencia.

OpenCV permite obtener esta información de forma muy sencilla.

---

## 14.13 Anchura y altura

Recordemos que la función `boundingRect()` devuelve cuatro valores:

```python
x, y, ancho, alto = cv2.boundingRect(contorno)
```

Además de indicar la posición del objeto, estos valores también representan las dimensiones del rectángulo envolvente.

Podemos mostrarlas fácilmente.

```python
print("Anchura:", ancho)
print("Altura :", alto)
```

Aunque estas medidas se expresan en **píxeles**, ya permiten comparar objetos entre sí.

::: figure
image: ../assets/cap14/fig14_5.png
caption: Obtención de la anchura y la altura de un objeto mediante su rectángulo envolvente.
:::

Por ejemplo, si dos objetos aparecen a la misma distancia de la cámara, el de mayor anchura en píxeles será también el de mayor tamaño físico.

---

## 14.14 Área del objeto

Otra característica muy utilizada es el área.

En OpenCV puede calcularse mediante la función:

```python
area = cv2.contourArea(contorno)
```

El resultado representa el número aproximado de píxeles que ocupa el objeto.

Por ejemplo:

```text
Área = 4385 píxeles²
```

Esta información permite:

- eliminar pequeñas detecciones producidas por ruido;
- distinguir piezas grandes y pequeñas;
- realizar controles dimensionales básicos.

::: common-error
content:

No confundas el área del contorno con el área del rectángulo envolvente.

El rectángulo siempre ocupa una superficie igual o mayor que el objeto detectado.
:::

---

## 14.15 Perímetro del contorno

Además del área también podemos calcular el perímetro del objeto.

OpenCV incorpora la función:

```python
perimetro = cv2.arcLength(contorno, True)
```

Este valor representa la longitud total del borde del objeto.

Aunque en este capítulo no profundizaremos en su utilización, el perímetro resulta muy útil para reconocer determinadas formas geométricas.

Por ejemplo, dos objetos pueden tener la misma área pero perímetros muy diferentes.

---

## 14.16 Coordenadas del objeto

Ya conocemos el centro del objeto.

Podemos utilizarlo como coordenada representativa de su posición.

```python
print(f"Centro: ({centro_x}, {centro_y})")
```

Estas coordenadas indican dónde aparece el objeto dentro de la imagen.

Es importante comprender que todavía **no representan una posición real en el espacio**.

Simplemente indican la posición del objeto sobre la fotografía capturada por la cámara.

En capítulos posteriores aprenderemos a relacionar estas coordenadas con posiciones reales dentro del entorno de CoppeliaSim.

::: figure
image: ../assets/cap14/fig14_6.png
caption: Coordenadas del centro del objeto dentro del sistema de referencia de la imagen.
:::

---

## 14.17 Comparando objetos

Una vez obtenidas las principales características podemos comparar diferentes objetos.

Supongamos una escena con varias piezas.

| Objeto | Anchura | Altura | Área |
|--------|---------:|--------:|------:|
| Cubo rojo | 62 px | 60 px | 3510 |
| Cilindro verde | 58 px | 104 px | 4748 |
| Esfera azul | 55 px | 55 px | 2365 |

A partir de esta información el programa puede responder preguntas como:

- ¿Cuál es el objeto más grande?
- ¿Cuál ocupa mayor superficie?
- ¿Cuál presenta mayor altura?

Este tipo de comparaciones constituye la base de numerosos sistemas de inspección industrial.

---

## 14.18 Clasificación por tamaño

Una aplicación muy habitual consiste en clasificar automáticamente las piezas según su tamaño.

Por ejemplo:

```python
if area > 4000:
    categoria = "Grande"
else:
    categoria = "Pequeña"
```

Aunque este criterio es muy sencillo, reproduce el funcionamiento básico de numerosos sistemas industriales de clasificación automática.

Posteriormente podremos combinar esta información con el color y la forma para obtener clasificaciones mucho más completas.

---

## 14.19 Primera inspección dimensional

Ya disponemos de los elementos necesarios para realizar una inspección básica.

El procedimiento completo será el siguiente.

1. Capturar la imagen.
2. Detectar el objeto.
3. Obtener el contorno.
4. Calcular el rectángulo envolvente.
5. Medir anchura y altura.
6. Calcular el área.
7. Obtener las coordenadas del centro.
8. Clasificar el objeto según su tamaño.

Este flujo constituye la base de numerosos sistemas de inspección automática utilizados en la industria.

::: practice
title: Midiendo objetos mediante visión artificial

difficulty: Media

time: 50 minutos

content:

Crea una escena con varios objetos geométricos de diferentes dimensiones.

Desarrolla un programa que:

1. Detecte todos los objetos presentes en la imagen.
2. Calcule su rectángulo envolvente.
3. Obtenga la anchura y la altura de cada uno.
4. Calcule el área del contorno.
5. Muestre las coordenadas del centro.
6. Clasifique automáticamente los objetos como **grandes** o **pequeños** utilizando un umbral de área.

Como ampliación, muestra sobre la imagen el nombre de la categoría asignada a cada objeto.
:::

::: teacher
content:

Conviene insistir en que todas las medidas obtenidas en este capítulo están expresadas en píxeles.

Más adelante se explicará cómo transformar estas medidas en dimensiones reales mediante la calibración de la cámara y la relación entre píxeles y unidades físicas.
:::

---

## 14.20 Clasificando objetos

Detectar un objeto constituye únicamente el primer paso.

En muchas aplicaciones industriales el objetivo final consiste en identificar a qué categoría pertenece dicho objeto.

Este proceso recibe el nombre de **clasificación**.

Clasificar significa asignar un objeto a un grupo determinado utilizando una o varias de sus características.

Por ejemplo, una línea de producción puede separar automáticamente piezas según:

- su color;
- su tamaño;
- su forma;
- su posición;
- o una combinación de todas ellas.

La clasificación automática constituye uno de los pilares fundamentales de la visión artificial industrial.

---

## 14.21 Clasificación por color

La forma más sencilla de clasificar un objeto consiste en utilizar el color detectado durante el procesamiento de la imagen.

Por ejemplo, podemos establecer las siguientes categorías:

| Color detectado | Categoría |
|-----------------|-----------|
| Rojo | Pieza tipo A |
| Verde | Pieza tipo B |
| Azul | Pieza tipo C |

El algoritmo únicamente tendrá que comprobar qué intervalo HSV ha permitido detectar el objeto para asignarle la categoría correspondiente.

::: figure
image: ../assets/cap14/fig14_7.png
caption: Clasificación automática de objetos según su color.
:::

Este procedimiento se utiliza con frecuencia en líneas de producción donde diferentes piezas comparten la misma forma, pero se distinguen por su color.

---

## 14.22 Clasificación por tamaño

Otra estrategia habitual consiste en utilizar las dimensiones del objeto.

Recordemos que anteriormente calculamos:

- anchura;
- altura;
- área.

A partir de estos valores podemos definir diferentes categorías.

```python
if area > 5000:
    categoria = "Grande"
elif area > 2500:
    categoria = "Mediana"
else:
    categoria = "Pequeña"
```

Este criterio resulta especialmente útil cuando todas las piezas presentan el mismo color, pero diferentes dimensiones.

---

## 14.23 Clasificación por forma

Además del color y el tamaño, también es posible distinguir objetos por su geometría.

Aunque existen numerosos algoritmos para reconocer formas, una primera aproximación consiste en analizar el número de lados del contorno aproximado.

Por ejemplo:

| Forma | Característica |
|--------|----------------|
| Triángulo | 3 vértices |
| Rectángulo | 4 vértices |
| Pentágono | 5 vértices |
| Círculo | Contorno prácticamente continuo |

OpenCV dispone de funciones que permiten aproximar un contorno mediante segmentos rectos y calcular el número de vértices.

En capítulos posteriores utilizaremos estas funciones para desarrollar sistemas de reconocimiento más avanzados.

::: figure
image: ../assets/cap14/fig14_8.png
caption: Clasificación básica de objetos según su forma geométrica.
:::

---

## 14.24 Combinando varios criterios

Los sistemas industriales reales rara vez utilizan un único criterio de clasificación.

Lo habitual consiste en combinar varios descriptores para obtener resultados más fiables.

Por ejemplo, un sistema puede aplicar las siguientes reglas:

- Color rojo **y** área superior a 4 000 píxeles² → Pieza tipo A.
- Color verde **y** forma circular → Pieza tipo B.
- Color azul **y** anchura inferior a 60 píxeles → Pieza tipo C.

Este enfoque reduce significativamente los errores de clasificación.

---

## 14.25 Mostrando la categoría sobre la imagen

Una vez determinada la categoría, podemos mostrarla directamente sobre la imagen utilizando `cv2.putText()`.

```python
cv2.putText(
    imagen,
    categoria,
    (x, y - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255,255,255),
    2
)
```

El resultado será una imagen en la que cada objeto aparece acompañado de su nombre o categoría.

Esta representación facilita la comprobación visual del funcionamiento del algoritmo.

::: common-error
content:

No clasifiques un objeto utilizando un único criterio cuando existan otros descriptores disponibles.

La combinación de color, tamaño y forma suele ofrecer resultados mucho más robustos.
:::

---

## 14.26 Preparando un sistema de clasificación

Ya disponemos de todos los elementos necesarios para construir una pequeña estación de clasificación automática.

El flujo completo será el siguiente.

1. Capturar la imagen desde el Vision Sensor.
2. Detectar todos los objetos presentes.
3. Obtener sus contornos.
4. Calcular dimensiones y coordenadas.
5. Determinar el color predominante.
6. Clasificar cada objeto.
7. Mostrar el resultado sobre la imagen.

Este procedimiento reproduce el funcionamiento básico de numerosos sistemas de inspección industrial utilizados en procesos automáticos de fabricación.

::: practice
title: Clasificación automática de piezas

difficulty: Media

time: 60 minutos

content:

Construye una escena formada por varios cubos, cilindros y esferas de diferentes colores y tamaños.

Desarrolla un programa que:

1. Detecte todos los objetos presentes en la imagen.
2. Calcule el área y el centro de cada uno.
3. Determine el color predominante.
4. Clasifique los objetos según:
   - color;
   - tamaño;
   - forma aproximada.
5. Dibuje el rectángulo envolvente.
6. Muestre la categoría asignada sobre la imagen.

Como ampliación, cuenta automáticamente cuántos objetos pertenecen a cada categoría y muestra el resultado por consola.
:::

::: teacher
content:

Es recomendable comenzar utilizando objetos claramente diferenciados por color y tamaño.

Posteriormente pueden introducirse piezas con características similares para analizar las limitaciones de los algoritmos basados únicamente en reglas simples y preparar la transición hacia técnicas de clasificación más avanzadas.
:::

---

## 14.27 Construyendo una estación de clasificación automática

A lo largo de este capítulo hemos aprendido a detectar objetos, localizar su posición, medir sus dimensiones y clasificarlos utilizando diferentes características.

Ha llegado el momento de integrar todos estos conocimientos en una única aplicación.

Desarrollaremos una pequeña estación de clasificación automática similar a las utilizadas en numerosos procesos industriales.

La escena estará formada por:

- una mesa de trabajo;
- varias piezas geométricas de distintos colores;
- un Vision Sensor situado sobre la escena.

Nuestro programa será capaz de analizar automáticamente todos los objetos visibles.

::: figure
image: ../assets/cap14/fig14_9.png
caption: Estación virtual de clasificación automática basada en visión artificial.
:::

---

## 14.28 Flujo completo del algoritmo

El programa seguirá siempre la misma secuencia de trabajo.

1. Capturar la imagen desde el Vision Sensor.
2. Convertir la imagen al espacio HSV.
3. Detectar los objetos mediante una máscara de color.
4. Localizar los contornos.
5. Obtener el rectángulo envolvente.
6. Calcular el centro del objeto.
7. Medir anchura, altura y área.
8. Clasificar cada objeto.
9. Mostrar el resultado sobre la imagen.

Aunque pueda parecer un proceso largo, la mayoría de estas operaciones se ejecutan en apenas unas milésimas de segundo.

Este mismo flujo aparece en numerosas aplicaciones industriales de inspección automática.

---

## 14.29 Procesando todos los objetos

Hasta ahora hemos trabajado con un único objeto.

Sin embargo, una escena puede contener varios elementos simultáneamente.

Para procesarlos recorreremos todos los contornos detectados mediante un bucle.

```python
for contorno in contornos:

    x, y, ancho, alto = cv2.boundingRect(contorno)

    area = cv2.contourArea(contorno)

    centro_x = x + ancho // 2
    centro_y = y + alto // 2

    # Clasificación del objeto
```

Cada iteración procesa un objeto distinto.

Gracias a este procedimiento el número de piezas presentes en la escena deja de ser un problema.

---

## 14.30 Mostrando la información obtenida

Una vez analizado cada objeto podemos representar sus características directamente sobre la imagen.

Por ejemplo:

- rectángulo envolvente;
- punto central;
- categoría;
- área;
- coordenadas.

El resultado será una escena similar a la siguiente.

::: figure
image: ../assets/cap14/fig14_10.png
caption: Resultado final del sistema de clasificación mostrando la información obtenida para cada objeto.
:::

Esta representación facilita enormemente la comprobación del funcionamiento del algoritmo y constituye una herramienta muy útil durante la fase de desarrollo.

---

## 14.31 Limitaciones del sistema

Aunque el algoritmo desarrollado funciona correctamente en escenas sencillas, presenta algunas limitaciones.

Por ejemplo:

- objetos parcialmente ocultos;
- cambios bruscos de iluminación;
- piezas muy próximas entre sí;
- colores muy similares;
- reflejos sobre las superficies.

Estas situaciones pueden dificultar la detección y producir clasificaciones incorrectas.

En aplicaciones industriales reales suelen emplearse técnicas más avanzadas para resolver estos problemas.

No obstante, el procedimiento estudiado en este capítulo constituye la base sobre la que se construyen muchos sistemas profesionales.

::: common-error
content:

No esperes que un algoritmo basado únicamente en reglas simples funcione correctamente en cualquier situación.

La calidad de la iluminación, la posición de la cámara y la correcta segmentación de la imagen influyen directamente en los resultados obtenidos.
:::

---

## 14.32 Aplicaciones reales

Los algoritmos desarrollados durante este capítulo pueden encontrarse en numerosos sistemas industriales.

Algunos ejemplos son:

- clasificación automática de frutas y hortalizas;
- selección de piezas por color;
- inspección de envases;
- verificación de componentes electrónicos;
- control de calidad en líneas de producción;
- conteo automático de productos.

En todos estos casos la visión artificial permite automatizar tareas que resultarían muy difíciles o repetitivas para una persona.

---

## 14.33 Preparando el siguiente paso

Hasta ahora el robot únicamente ha observado una escena estática.

Sin embargo, en muchas aplicaciones los objetos se encuentran en movimiento.

Por ejemplo:

- una pelota rodando;
- una cinta transportadora;
- un vehículo autónomo;
- una persona caminando.

En estas situaciones ya no basta con detectar un objeto.

También es necesario seguir su movimiento de forma continua.

Ese será precisamente el objetivo del siguiente capítulo.

::: practice
title: Sistema completo de clasificación

difficulty: Media-Alta

time: 75 minutos

content:

Construye una escena formada por varias figuras geométricas de diferentes colores y tamaños.

Desarrolla un programa que:

1. Capture la imagen desde el Vision Sensor.
2. Detecte todos los objetos presentes.
3. Obtenga el contorno de cada uno.
4. Calcule su rectángulo envolvente.
5. Determine el centro.
6. Calcule el área.
7. Clasifique cada objeto utilizando color y tamaño.
8. Muestre toda la información sobre la imagen.
9. Indique por consola el número total de objetos detectados y cuántos pertenecen a cada categoría.

Como ampliación, modifica la escena añadiendo nuevos objetos y comprueba que el programa continúa funcionando correctamente sin necesidad de realizar cambios en el algoritmo.
:::

::: teacher
content:

Esta práctica constituye un excelente proyecto integrador para comprobar que el alumnado domina todos los conceptos introducidos en los capítulos 12, 13 y 14.

Antes de continuar con el Capítulo 15, conviene verificar que todos los estudiantes son capaces de desarrollar de forma autónoma el flujo completo de detección, medición y clasificación de objetos.
:::

---

# Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Detección de objetos | Proceso mediante el cual se localizan automáticamente los objetos presentes en una imagen. |
| Contorno | Conjunto de puntos que delimitan el borde exterior de un objeto. |
| Bounding Box | Rectángulo mínimo que contiene completamente un objeto detectado. |
| Centro del objeto | Punto central calculado a partir del rectángulo envolvente. |
| Coordenadas de imagen | Posición de un objeto expresada mediante los ejes X e Y de la imagen. |
| Área | Superficie ocupada por un objeto, expresada normalmente en píxeles cuadrados. |
| Perímetro | Longitud del borde exterior de un objeto detectado. |
| Descriptor | Característica utilizada para describir un objeto, como el color, el tamaño o la forma. |
| Clasificación | Proceso de asignar un objeto a una categoría utilizando uno o varios descriptores. |
| Visión artificial | Disciplina que permite obtener información útil a partir de imágenes digitales para facilitar la toma de decisiones. |
:::

---

# En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Detectar objetos dentro de una imagen utilizando OpenCV.
- ✅ Obtener el rectángulo envolvente (*Bounding Box*).
- ✅ Calcular el centro de un objeto.
- ✅ Medir su anchura, altura, área y perímetro.
- ✅ Obtener las coordenadas del objeto dentro de la imagen.
- ✅ Clasificar objetos según su color, tamaño y forma.
- ✅ Desarrollar un sistema básico de clasificación automática.

A partir de este momento ya dispones de los conocimientos necesarios para desarrollar aplicaciones de visión artificial capaces de localizar y clasificar objetos presentes en una escena.

---

# Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué información proporciona un *Bounding Box*?
2. ¿Cómo se calcula el centro de un objeto?
3. ¿Qué diferencia existe entre el área del contorno y el área del rectángulo envolvente?
4. ¿Qué son los descriptores de un objeto?
5. ¿Qué ventajas ofrece combinar color, tamaño y forma durante la clasificación?
6. ¿Por qué resulta útil representar gráficamente el centro y el rectángulo envolvente?
7. ¿Qué limitaciones presenta un sistema de clasificación basado únicamente en reglas simples?

Si puedes responder correctamente a todas estas preguntas, estás preparado para desarrollar aplicaciones de seguimiento visual.

---

# Práctica guiada

::: practice
title: Clasificación automática de objetos

difficulty: Media-Alta

time: 75 minutos

content:

Construye una escena formada por varias figuras geométricas de distintos colores y tamaños.

Desarrolla un programa que:

1. Capture la imagen desde el Vision Sensor.
2. Detecte todos los objetos presentes.
3. Obtenga el contorno de cada uno.
4. Calcule el rectángulo envolvente.
5. Determine el centro del objeto.
6. Calcule el área y las dimensiones principales.
7. Clasifique automáticamente cada objeto utilizando su color y tamaño.
8. Muestre sobre la imagen:
   - el rectángulo envolvente;
   - el punto central;
   - las coordenadas;
   - la categoría asignada.
9. Indique por consola el número total de objetos detectados y cuántos pertenecen a cada categoría.

Como ampliación, añade nuevos objetos a la escena y comprueba que el algoritmo continúa funcionando correctamente sin necesidad de modificar el código.
:::

---

# Reto

::: challenge
title: Sistema inteligente de inspección visual

content:

Diseña una estación virtual de inspección formada por varias piezas de diferentes formas, colores y tamaños.

Desarrolla un programa capaz de:

- detectar automáticamente todos los objetos presentes;
- clasificarlos según distintos criterios;
- identificar cuál es el objeto de mayor tamaño;
- contar cuántos objetos pertenecen a cada categoría;
- mostrar toda la información obtenida sobre la imagen.

Como ampliación, intenta detectar si aparece un objeto que no cumple ninguna de las categorías definidas y márcalo como **Objeto desconocido**.

Este reto reproduce el funcionamiento básico de muchos sistemas de inspección industrial utilizados en líneas automáticas de fabricación.
:::

---

# Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre dos y tres sesiones de 55 minutos.

**Objetivos**

- Consolidar el uso de OpenCV para la detección de objetos.
- Comprender el cálculo de posiciones y dimensiones.
- Introducir los principios de la clasificación automática.
- Integrar todos los contenidos desarrollados en los capítulos 12, 13 y 14.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Python.
- Biblioteca OpenCV (`opencv-python`).
- Escena con un Vision Sensor y varios objetos geométricos de distintos colores.

**Consejos metodológicos**

Es recomendable dedicar una sesión completa a la realización de una aplicación integradora.

Permite que el alumnado experimente modificando colores, tamaños y posiciones de los objetos para comprobar cómo afectan estos cambios al proceso de detección y clasificación.

Antes de comenzar el Capítulo 15, verifica que todos los estudiantes comprenden el flujo completo:

Captura → Procesamiento → Detección → Medición → Clasificación.

Esta visión global facilitará enormemente la comprensión del seguimiento visual de objetos.
:::

---

# Próximo capítulo

Hasta ahora el robot ha aprendido a observar una escena, detectar objetos y clasificarlos utilizando distintas características.

Sin embargo, todas las escenas analizadas eran estáticas.

En numerosas aplicaciones reales los objetos se encuentran en movimiento: una pelota que rueda, una cinta transportadora, un vehículo autónomo o una persona caminando.

En el siguiente capítulo aprenderás a realizar **seguimiento visual de objetos**. Utilizarás la información proporcionada por la cámara para mantener un objeto centrado en la imagen, seguir trayectorias y controlar el movimiento del robot en función de lo que está viendo.

Este será el primer capítulo en el que la **visión artificial** influirá directamente en el comportamiento dinámico del robot, marcando el paso desde la simple percepción hacia la interacción inteligente con el entorno.
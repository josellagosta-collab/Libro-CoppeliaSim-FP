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

## 12.5 Añadiendo un sensor de visión a una escena

Hasta este momento hemos estudiado la visión artificial desde un punto de vista conceptual.

Ha llegado el momento de comenzar a trabajar con cámaras dentro de CoppeliaSim.

En este apartado incorporaremos nuestro primer **Vision Sensor** a una escena y aprenderemos a configurar sus principales propiedades.

Aunque inicialmente utilizaremos la cámara únicamente para observar la escena, en los siguientes apartados accederemos a las imágenes desde Python y desarrollaremos nuestras primeras aplicaciones de visión artificial.

::: teacher
content:

Antes de comenzar, recuerda al alumnado que una cámara no "ve" automáticamente.

El sensor únicamente captura imágenes.

Será el programa desarrollado en Python quien posteriormente analice esas imágenes para obtener información útil.
:::

---

## 12.6 El objeto Vision Sensor

En CoppeliaSim las cámaras reciben el nombre de **Vision Sensor**.

Este objeto simula el funcionamiento de una cámara digital real.

Cada vez que la simulación avanza un paso, el sensor captura una imagen de todo aquello que se encuentra dentro de su campo de visión.

La imagen queda disponible para que otros elementos de la simulación o una aplicación externa puedan procesarla.

::: figure
image: ../assets/cap12/fig12_3.png
caption: Inserción de un Vision Sensor desde el menú Add de CoppeliaSim.
:::

Al insertar un sensor de visión aparecerá un nuevo objeto en el árbol de la escena.

Como cualquier otro objeto de CoppeliaSim, podremos moverlo, rotarlo o cambiar su nombre.

---

### ¿Cómo funciona una cámara virtual?

Podemos imaginar un Vision Sensor como una pequeña cámara colocada dentro del escenario.

Todo aquello que la cámara tenga delante podrá aparecer en la imagen capturada.

En cambio, los objetos situados detrás de la cámara o fuera de su ángulo de visión no serán visibles.

Este comportamiento es idéntico al de una cámara fotográfica convencional.

---

### Campo de visión

Uno de los parámetros más importantes de cualquier cámara es su **campo de visión** (*Field of View*).

Este parámetro determina la amplitud de la escena que puede observar el sensor.

Un campo de visión amplio permite capturar una zona mayor del entorno.

Sin embargo, los objetos aparecerán más pequeños.

Por el contrario, un campo de visión reducido proporciona una imagen más cercana, aunque cubre una región menor.

::: figure
image: ../assets/cap12/fig12_4.png
caption: Comparación entre un campo de visión amplio y otro reducido.
:::

En aplicaciones de inspección industrial suele utilizarse un campo de visión relativamente reducido para obtener imágenes con mayor nivel de detalle.

Por el contrario, en robots móviles resulta habitual utilizar cámaras con un campo de visión más amplio para observar una mayor parte del entorno.

---

## 12.7 Propiedades principales del Vision Sensor

Seleccionando la cámara y accediendo a sus propiedades podremos modificar distintos parámetros.

Durante este capítulo trabajaremos únicamente con los más importantes.

::: table
caption: Propiedades básicas de un Vision Sensor.
content:

| Propiedad | Descripción |
|------------|-------------|
| Resolution | Número de píxeles que forman la imagen. |
| Perspective angle | Campo de visión de la cámara. |
| Near clipping plane | Distancia mínima visible. |
| Far clipping plane | Distancia máxima visible. |
| Explicit handling | Permite controlar cuándo captura imágenes el sensor. |

:::

No es necesario modificar todos estos parámetros desde el principio.

Utilizaremos inicialmente la configuración predeterminada de CoppeliaSim.

Más adelante aprenderemos cuándo conviene ajustar cada uno de ellos.

---

### Resolución de la imagen

La resolución indica el número de píxeles que componen la imagen capturada.

Por ejemplo:

- 320 × 240 píxeles.
- 640 × 480 píxeles.
- 1280 × 720 píxeles.

Cuanto mayor sea la resolución, mayor será el nivel de detalle.

Sin embargo, también aumentará el tiempo necesario para procesar cada imagen.

En aplicaciones de robótica suele buscarse un equilibrio entre calidad y velocidad de procesamiento.

---

### Distancias de recorte

El Vision Sensor también permite definir una distancia mínima y otra máxima de observación.

Los objetos situados fuera de ese intervalo no aparecerán correctamente en la imagen.

Esta característica resulta especialmente útil para eliminar información innecesaria y reducir el procesamiento posterior.

::: common-error
content:

Muchos estudiantes creen que la cámara está averiada cuando no visualiza determinados objetos.

En realidad, con frecuencia dichos objetos se encuentran fuera del rango de visión configurado en el sensor.
:::

---

## 12.8 Nuestra primera cámara

Como primer ejercicio incorporaremos una cámara sobre una escena sencilla formada por varios objetos geométricos.

El objetivo todavía no consiste en programar nada.

Simplemente comprobaremos que el Vision Sensor captura correctamente la imagen del entorno.

En el siguiente apartado aprenderemos a enviar esa imagen a un programa desarrollado en Python para comenzar a procesarla mediante OpenCV.

---

## 12.9 Capturando imágenes desde Python

Hasta ahora la cámara únicamente ha permanecido dentro de la escena de CoppeliaSim.

Sin embargo, el verdadero potencial de un **Vision Sensor** aparece cuando una aplicación externa puede acceder a las imágenes que captura.

En nuestro caso será un programa desarrollado en Python quien solicite continuamente las imágenes al simulador.

A partir de ese momento podremos analizarlas, almacenarlas o utilizarlas para controlar el comportamiento del robot.

El proceso completo resulta mucho más sencillo de lo que puede parecer.

::: figure
image: ../assets/cap12/fig12_5.png
caption: Flujo de comunicación entre CoppeliaSim, el Vision Sensor y una aplicación Python.
:::

Durante cada ciclo de simulación ocurre lo siguiente:

1. El Vision Sensor captura una imagen.
2. CoppeliaSim almacena dicha imagen.
3. Python solicita la imagen mediante la API remota.
4. El programa recibe la imagen.
5. Posteriormente podrá visualizarla o procesarla utilizando OpenCV.

Aunque en este capítulo todavía no realizaremos procesamiento de imágenes, comprender este flujo facilitará enormemente el trabajo en los siguientes capítulos.

---

## 12.10 Obteniendo la imagen del Vision Sensor

La API remota de CoppeliaSim proporciona funciones específicas para acceder a la información capturada por una cámara.

El primer paso consiste en obtener el identificador (*handle*) del Vision Sensor.

Una vez localizado el sensor, podremos solicitar la imagen capturada durante la simulación.

El procedimiento general será muy parecido al utilizado anteriormente con los sensores de proximidad.

Primero localizaremos el objeto y, posteriormente, leeremos la información que proporciona.

---

### Programa básico

El siguiente ejemplo muestra la estructura general necesaria para obtener una imagen desde un Vision Sensor.

```python
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')

visionSensor = sim.getObject('/Vision_sensor')

sim.startSimulation()

image, resolution = sim.getVisionSensorImg(visionSensor)

print("Resolución:", resolution)

sim.stopSimulation()
```

Aunque el programa es muy breve, internamente se están realizando varias operaciones importantes.

En primer lugar se establece la conexión con CoppeliaSim.

A continuación se obtiene el identificador del Vision Sensor.

Finalmente se solicita la imagen capturada por la cámara.

---

### ¿Qué devuelve realmente la cámara?

La función `getVisionSensorImg()` devuelve dos valores.

El primero contiene la imagen capturada.

El segundo indica la resolución utilizada por el sensor.

Por ejemplo:

```text
Resolución: [512, 512]
```

Esto significa que la cámara ha capturado una imagen formada por **512 píxeles de ancho** y **512 píxeles de alto**.

Posteriormente veremos que esa imagen está formada por miles de píxeles individuales.

Cada uno de ellos almacena información sobre el color observado en una posición concreta.

::: figure
image: ../assets/cap12/fig12_6.png
caption: Una imagen digital está formada por miles de píxeles organizados en una matriz.
:::

---

## 12.11 Comprendiendo la imagen recibida

Aunque normalmente pensamos en una fotografía como una única imagen, para un ordenador no es más que una enorme colección de datos.

Cada píxel contiene información sobre su color.

La imagen completa puede interpretarse como una gran matriz formada por filas y columnas.

Por ejemplo, una imagen de 640 × 480 contiene:

- 640 columnas.
- 480 filas.
- 307 200 píxeles.

Cada uno de esos píxeles podrá analizarse posteriormente mediante OpenCV.

Gracias a ello podremos detectar colores, localizar objetos, medir dimensiones o identificar patrones visuales.

Durante este capítulo todavía no modificaremos ningún píxel.

Nuestro objetivo consiste únicamente en comprobar que Python recibe correctamente la información enviada por el Vision Sensor.

::: teacher
content:

Insiste en que el alumnado no memorice todavía las funciones de OpenCV.

Es mucho más importante comprender que una imagen no deja de ser una matriz de datos sobre la que posteriormente podrán aplicarse diferentes algoritmos de procesamiento.
:::

---

## 12.12 Preparando el procesamiento de imágenes

Ya somos capaces de capturar imágenes desde un Vision Sensor utilizando Python.

Sin embargo, todavía no podemos ver esas imágenes.

La información recibida sigue siendo simplemente un conjunto de datos almacenados en memoria.

En el siguiente apartado aprenderemos a convertir esos datos en una imagen visible utilizando OpenCV.

A partir de ese momento comenzaremos realmente a trabajar con visión artificial.

---

## 12.13 Visualizando imágenes con OpenCV

Hasta este momento hemos conseguido que Python reciba correctamente la imagen capturada por el Vision Sensor.

Sin embargo, todavía no podemos verla.

La información recibida sigue siendo una secuencia de datos almacenada en memoria.

Para visualizar esa imagen utilizaremos una de las bibliotecas más utilizadas en visión artificial: **OpenCV**.

OpenCV (*Open Source Computer Vision Library*) es una biblioteca de código abierto diseñada para el procesamiento de imágenes y visión artificial.

Actualmente se utiliza en miles de aplicaciones relacionadas con:

- robótica;
- vehículos autónomos;
- inspección industrial;
- medicina;
- inteligencia artificial;
- reconocimiento facial.

En los próximos capítulos aprenderemos a utilizar muchas de sus funciones.

Por el momento nos limitaremos a mostrar la imagen capturada por la cámara.

::: figure
image: ../assets/cap12/fig12_7.png
caption: Flujo de visualización de una imagen utilizando OpenCV.
:::

---

## 12.14 Mostrando la imagen en una ventana

Una vez obtenida la imagen desde CoppeliaSim, OpenCV permite visualizarla mediante una ventana independiente.

El procedimiento general consiste en tres pasos:

1. Obtener la imagen del Vision Sensor.
2. Convertir los datos al formato adecuado.
3. Mostrar la imagen utilizando OpenCV.

El siguiente ejemplo resume el proceso.

```python
import cv2
import numpy as np

# Conversión de la imagen recibida
imagen = np.frombuffer(image, dtype=np.uint8)
imagen = imagen.reshape(resolution[1], resolution[0], 3)

# Mostrar la imagen
cv2.imshow("Vision Sensor", imagen)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

Al ejecutar el programa aparecerá una ventana mostrando exactamente la misma escena observada por la cámara de CoppeliaSim.

En ese momento ya estaremos utilizando una aplicación real de visión artificial.

---

### ¿Por qué utilizamos OpenCV?

Aunque Python dispone de otras bibliotecas para trabajar con imágenes, OpenCV ofrece numerosas ventajas.

Entre ellas destacan:

- gran velocidad de procesamiento;
- compatibilidad con múltiples sistemas operativos;
- enorme cantidad de algoritmos incorporados;
- amplia documentación;
- utilización en aplicaciones profesionales.

Por este motivo OpenCV se ha convertido en el estándar de facto para el aprendizaje y el desarrollo de aplicaciones de visión artificial.

::: teacher
content:

No intentes explicar todavía todas las funciones de OpenCV.

El objetivo del capítulo consiste únicamente en comprobar que el alumnado es capaz de visualizar correctamente la imagen capturada por el Vision Sensor.

Los algoritmos de procesamiento se estudiarán con detalle en el capítulo siguiente.
:::

---

## 12.15 Guardando una fotografía

Además de visualizar la imagen, OpenCV también permite almacenarla en un archivo.

Esta posibilidad resulta muy útil cuando queremos crear conjuntos de imágenes para entrenar modelos de inteligencia artificial o documentar una simulación.

Guardar una fotografía es muy sencillo.

```python
cv2.imwrite("captura.png", imagen)
```

Tras ejecutar esta instrucción aparecerá un archivo denominado **captura.png** en el directorio de trabajo.

Ese archivo contendrá exactamente la imagen observada por el Vision Sensor en el momento de la captura.

::: figure
image: ../assets/cap12/fig12_8.png
caption: Captura de una imagen obtenida desde el Vision Sensor y almacenada en un archivo PNG.
:::

---

## 12.16 Primera aplicación práctica

Como primera práctica realizaremos una escena muy sencilla.

Crearemos una mesa con varios objetos de diferentes colores.

Posteriormente situaremos un Vision Sensor frente a ellos y ejecutaremos el programa desarrollado en este capítulo.

Nuestro objetivo será comprobar que:

- la cámara captura correctamente la escena;
- Python recibe la imagen;
- OpenCV la muestra en pantalla;
- la fotografía puede almacenarse correctamente en un archivo.

Todavía no analizaremos la imagen.

Ese será precisamente el objetivo del siguiente capítulo.

::: practice
title: Primera captura de imágenes

difficulty: Baja

time: 30 minutos

content:

1. Crea una escena vacía.
2. Inserta tres objetos geométricos de distintos colores.
3. Añade un Vision Sensor orientado hacia los objetos.
4. Ejecuta la simulación.
5. Obtén la imagen desde Python.
6. Muéstrala utilizando OpenCV.
7. Guarda la fotografía con el nombre **captura.png**.
8. Comprueba que el archivo se ha creado correctamente.

Al finalizar esta práctica habrás desarrollado tu primera aplicación completa de visión artificial utilizando CoppeliaSim, Python y OpenCV.
:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Visión artificial | Disciplina que permite a un ordenador interpretar imágenes capturadas por una cámara. |
| Vision Sensor | Cámara virtual de CoppeliaSim utilizada para capturar imágenes de la escena. |
| Campo de visión (Field of View) | Ángulo que determina la porción del entorno visible por la cámara. |
| Resolución | Número de píxeles que forman una imagen digital. |
| Píxel | Unidad mínima que compone una imagen digital y almacena información de color. |
| API remota | Sistema de comunicación que permite a Python acceder a los datos de CoppeliaSim. |
| OpenCV | Biblioteca de visión artificial utilizada para visualizar y procesar imágenes. |
| Captura de imagen | Obtención de una fotografía desde el Vision Sensor. |
| Imagen digital | Matriz formada por píxeles que representa visualmente una escena. |
| Archivo PNG | Formato utilizado para almacenar imágenes sin pérdida de calidad. |
:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender qué es la visión artificial y sus principales aplicaciones.
- ✅ Insertar y configurar un Vision Sensor en una escena de CoppeliaSim.
- ✅ Comprender las propiedades fundamentales de una cámara virtual.
- ✅ Obtener imágenes desde Python utilizando la API remota.
- ✅ Visualizar imágenes mediante OpenCV.
- ✅ Guardar fotografías capturadas durante una simulación.

A partir de este momento ya dispones de todos los conocimientos necesarios para comenzar a desarrollar aplicaciones básicas de visión artificial.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencias existen entre un sensor de proximidad y un Vision Sensor?
2. ¿Qué representa el campo de visión de una cámara?
3. ¿Qué información devuelve la función `getVisionSensorImg()`?
4. ¿Qué es un píxel?
5. ¿Qué ventajas ofrece OpenCV para trabajar con imágenes?
6. ¿Cómo puede almacenarse una fotografía capturada desde un Vision Sensor?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a procesar imágenes mediante OpenCV.

---

## Práctica guiada

::: practice

title: Primera aplicación de visión artificial

difficulty: Baja

time: 45 minutos

content:

Desarrolla una escena formada por varios objetos geométricos de diferentes colores y realiza las siguientes tareas.

1. Inserta un Vision Sensor.
2. Oriéntalo hacia los objetos.
3. Ejecuta la simulación.
4. Obtén la imagen desde Python.
5. Muéstrala utilizando OpenCV.
6. Guarda la fotografía como **captura.png**.
7. Modifica la posición de la cámara y repite la captura.
8. Cambia la resolución del Vision Sensor y observa las diferencias obtenidas.

El objetivo consiste en comprobar el funcionamiento completo del sistema de adquisición de imágenes.
:::

---

## Reto

::: challenge
title: Diseñando un sistema de inspección visual

content:

Diseña una escena que simule una pequeña estación de inspección industrial.

La escena deberá incluir:

- una mesa de trabajo;
- varios objetos geométricos de diferentes colores;
- un Vision Sensor situado sobre la mesa.

Captura varias imágenes modificando:

- la posición de la cámara;
- la orientación;
- el campo de visión;
- la resolución.

Analiza cómo afectan estos cambios a la imagen obtenida.

No es necesario procesar todavía las imágenes.

El objetivo consiste en comprender cómo influyen los parámetros de una cámara en la información capturada.
:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender el funcionamiento básico de un Vision Sensor.
- Capturar imágenes desde Python utilizando la API remota.
- Visualizar imágenes mediante OpenCV.
- Introducir los conceptos fundamentales que se desarrollarán en el procesamiento de imágenes.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Python.
- Biblioteca OpenCV (`opencv-python`).
- Proyecto de ejemplo con un Vision Sensor.

**Consejos metodológicos**

No dediques demasiado tiempo a explicar OpenCV en profundidad.

El objetivo del capítulo consiste únicamente en demostrar que una imagen puede capturarse, visualizarse y almacenarse correctamente.

Todo el procesamiento de imágenes se desarrollará progresivamente durante el Capítulo 13.

Resulta recomendable realizar varias capturas modificando la posición y orientación de la cámara para que el alumnado comprenda intuitivamente el funcionamiento del campo de visión.
:::

---

## Próximo capítulo

Ya eres capaz de capturar imágenes desde un Vision Sensor y acceder a ellas desde Python.

Ha llegado el momento de comenzar a interpretarlas.

En el siguiente capítulo aprenderás a procesar imágenes utilizando OpenCV.

Descubrirás cómo trabajar con los distintos canales de color, convertir imágenes a escala de grises, aplicar umbralizaciones, detectar contornos e identificar objetos.

Será el primer paso para que nuestros robots no solo puedan ver su entorno, sino también comprender la información contenida en las imágenes.
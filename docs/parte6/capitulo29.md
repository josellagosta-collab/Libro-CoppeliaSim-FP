::: chapter-cover
number: 29
title: Integración de visión artificial
time: 5 horas
level: ⭐⭐⭐⭐⭐ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender el papel de la visión artificial en una célula robotizada.
- Identificar los elementos que forman un sistema de visión industrial.
- Integrar una cámara en una célula robotizada desarrollada en CoppeliaSim.
- Comprender el flujo de adquisición y procesamiento de imágenes.
- Analizar cómo la visión artificial mejora la automatización de los procesos industriales.
:::

# Capítulo 29 · Integración de visión artificial

### ¿Por qué incorporar visión artificial?

Hasta ahora el sistema de clasificación desarrollado en los capítulos anteriores ha tomado sus decisiones utilizando información procedente de sensores fotoeléctricos.

Aunque este método resulta suficiente para detectar la presencia de una pieza, presenta importantes limitaciones cuando es necesario reconocer características más complejas, como el color, la forma, el tamaño o la orientación de un objeto.

La visión artificial permite superar estas limitaciones proporcionando al sistema una gran cantidad de información obtenida directamente mediante cámaras industriales.

Gracias a ella es posible identificar automáticamente piezas, detectar defectos de fabricación, localizar objetos sobre una cinta transportadora o guiar el movimiento de un robot con gran precisión.

Actualmente, la visión artificial constituye una de las tecnologías más utilizadas dentro de la Industria 4.0 y forma parte de innumerables procesos de fabricación, inspección y control de calidad.

En este capítulo incorporaremos una cámara industrial a la célula robotizada desarrollada anteriormente para comprender cómo se integra dentro del flujo general de funcionamiento.

::: teacher
content:

Antes de comenzar este capítulo resulta recomendable recordar el funcionamiento de la célula robotizada desarrollada en el capítulo anterior.

El alumnado debe comprender que la cámara no sustituye al robot ni a los sensores, sino que aporta información adicional que permite tomar decisiones mucho más precisas.

Puede aprovecharse este momento para mostrar ejemplos reales de sistemas de visión industrial utilizados en líneas de producción automatizadas.
:::

---

## 29.1 ¿Qué es un sistema de visión artificial?

Un sistema de visión artificial es un conjunto de dispositivos capaces de capturar imágenes del entorno, procesarlas y obtener información útil para automatizar una determinada tarea.

Aunque existen numerosas configuraciones, la mayoría de los sistemas de visión industrial están formados por los siguientes elementos:

- una cámara industrial;
- un sistema de iluminación;
- un ordenador o controlador encargado del procesamiento;
- un software de análisis de imágenes;
- un sistema de comunicación con el resto de la instalación.

La cámara captura continuamente imágenes de la escena.

Estas imágenes son analizadas mediante diferentes algoritmos capaces de localizar objetos, medir dimensiones, identificar colores o detectar posibles defectos.

La información obtenida se transmite posteriormente al sistema de control para que el robot pueda actuar en consecuencia.

::: figure
image: ../assets/cap29/fig29_1.png
caption: Componentes principales de un sistema de visión artificial integrado en una célula robotizada.
:::

En una instalación industrial moderna, la cámara se convierte en un sensor avanzado capaz de proporcionar mucha más información que un sensor de presencia convencional.

---

## 29.2 Integración de la cámara en la célula robotizada

Para incorporar la visión artificial a nuestro proyecto utilizaremos la misma célula robotizada desarrollada durante el capítulo anterior.

La principal diferencia consistirá en añadir una cámara situada sobre la zona de inspección de la cinta transportadora.

Desde esta posición podrá observar todas las piezas antes de que lleguen al área de trabajo del robot.

De esta forma, el sistema dispondrá del tiempo suficiente para procesar la imagen, identificar el objeto y comunicar el resultado al controlador antes de que el robot deba manipular la pieza.

Esta disposición reproduce el funcionamiento habitual de numerosas líneas de producción automatizadas.

La separación entre la zona de inspección y la zona de manipulación permite que la identificación de la pieza se realice mientras ésta continúa desplazándose por la cinta transportadora, reduciendo así el tiempo de ciclo de la instalación.

::: figure
image: ../assets/cap29/fig29_2.png
caption: Integración de una cámara industrial sobre la zona de inspección de la célula robotizada.
:::

---

## 29.3 Flujo de adquisición de imágenes

Una vez instalada la cámara sobre la célula robotizada, el siguiente paso consiste en comprender cómo se obtiene la información necesaria para identificar las piezas.

Aunque para el usuario todo el proceso parece instantáneo, internamente se producen varias etapas perfectamente sincronizadas.

Cada vez que una pieza entra en la zona de inspección, la cámara captura una imagen de alta resolución.

Esta imagen es enviada inmediatamente al sistema de procesamiento, donde diferentes algoritmos analizan su contenido para localizar el objeto y extraer las características necesarias para su identificación.

Entre las operaciones más habituales encontramos:

- localización de la pieza dentro de la imagen;
- eliminación del ruido;
- mejora del contraste;
- detección de bordes;
- segmentación del objeto;
- extracción de características.

Una vez completado este proceso, el sistema genera un conjunto de datos que describen la pieza observada.

Esta información será utilizada posteriormente para decidir qué operación deberá realizar el robot.

::: figure
image: ../assets/cap29/fig29_3.png
caption: Flujo completo de adquisición y procesamiento de imágenes en un sistema de visión artificial.
:::

En aplicaciones industriales este proceso suele completarse en pocos milisegundos, permitiendo inspeccionar cientos o incluso miles de piezas cada hora.

---

## 29.4 Identificación automática de objetos

Después de procesar la imagen, el sistema debe determinar qué tipo de objeto está observando.

Dependiendo de la aplicación, esta identificación puede realizarse utilizando diferentes características visuales.

Las más utilizadas son:

- color;
- forma;
- dimensiones;
- posición;
- orientación;
- textura;
- presencia de marcas o códigos.

En nuestro proyecto comenzaremos utilizando criterios sencillos para facilitar la comprensión del proceso.

Más adelante podremos incorporar algoritmos mucho más avanzados basados en aprendizaje automático e inteligencia artificial.

Una vez identificada la pieza, el sistema genera una etiqueta que será enviada al controlador del robot.

Esta etiqueta contendrá toda la información necesaria para decidir el destino final del objeto.

::: table
caption: Ejemplo de información obtenida durante el proceso de identificación.
content:

| Característica | Valor obtenido | Utilización |
|----------------|---------------|-------------|
| Color | Verde | Clasificación |
| Forma | Cilíndrica | Verificación |
| Posición X,Y | (245, 128) | Guiado del robot |
| Orientación | 35° | Cálculo de la pinza |
| Estado | Correcta | Continuar proceso |

:::

Gracias a esta información, el robot puede adaptar automáticamente su movimiento a cada pieza sin necesidad de programar una trayectoria diferente para cada caso.

::: figure
image: ../assets/cap29/fig29_4.png
caption: Identificación automática de las características visuales de una pieza mediante visión artificial.
:::

---

## 29.5 Comunicación entre el sistema de visión y el robot

Una vez que el sistema de visión ha identificado correctamente la pieza, es necesario transmitir esta información al robot para que pueda actuar en consecuencia.

En una instalación industrial moderna esta comunicación debe realizarse de forma rápida, fiable y sincronizada con el movimiento de la cinta transportadora.

El sistema de visión no mueve directamente el robot.

Su función consiste en proporcionar información sobre la pieza inspeccionada para que el controlador de la célula determine la operación que debe realizar el manipulador.

Normalmente, la información enviada incluye datos como:

- tipo de pieza;
- posición dentro de la cinta;
- orientación;
- dimensiones principales;
- nivel de confianza de la identificación;
- estado de la inspección.

El controlador recibe esta información y genera las órdenes necesarias para que el robot ejecute el movimiento adecuado.

Este intercambio de información debe realizarse antes de que la pieza alcance la zona de trabajo del robot.

De esta forma, el manipulador ya conoce qué operación deberá realizar cuando el objeto llegue a su posición de recogida.

::: figure
image: ../assets/cap29/fig29_5.png
caption: Comunicación entre el sistema de visión artificial, el controlador y el robot industrial.
:::

Una correcta sincronización entre la velocidad de la cinta transportadora, el tiempo de procesamiento de la imagen y el movimiento del robot resulta fundamental para garantizar un funcionamiento continuo de la instalación.

---

## 29.6 Calibración de la cámara

Uno de los aspectos más importantes de cualquier sistema de visión artificial es la calibración.

Aunque la cámara capture correctamente las imágenes, el robot necesita conocer la posición real de cada pieza dentro del espacio de trabajo.

La calibración consiste en establecer la relación entre las coordenadas de la imagen capturada por la cámara y las coordenadas físicas utilizadas por el robot.

Gracias a este proceso, una posición determinada en la imagen puede transformarse en una posición real que el manipulador puede alcanzar con precisión.

En aplicaciones industriales esta transformación suele realizarse mediante diferentes técnicas matemáticas y patrones de calibración.

En CoppeliaSim este proceso puede simularse de forma muy sencilla, permitiendo comprender la importancia que tiene una correcta alineación entre la cámara y el robot.

Una calibración incorrecta puede provocar errores como:

- desplazamientos durante la recogida;
- piezas mal clasificadas;
- colisiones con otros elementos;
- pérdida de precisión en el posicionamiento.

Por este motivo, la calibración constituye una de las primeras operaciones que se realizan antes de poner en funcionamiento cualquier sistema de visión industrial.

::: figure
image: ../assets/cap29/fig29_6.png
caption: Relación entre el sistema de coordenadas de la cámara y el sistema de coordenadas del robot mediante el proceso de calibración.
:::

---

## 29.7 Aplicaciones de la visión artificial en robótica industrial

La incorporación de sistemas de visión artificial ha transformado profundamente la automatización industrial.

Mientras que los primeros robots únicamente podían ejecutar movimientos previamente programados, los sistemas actuales son capaces de adaptar su comportamiento en función de la información capturada por las cámaras.

Esta capacidad permite aumentar considerablemente la flexibilidad de las instalaciones y reducir la necesidad de realizar ajustes mecánicos cuando cambian las piezas o el proceso de fabricación.

Entre las aplicaciones más habituales de la visión artificial destacan:

- identificación automática de piezas;
- clasificación por color, forma o dimensiones;
- guiado del robot (*Vision Guided Robotics*);
- inspección de calidad;
- detección de defectos superficiales;
- lectura de códigos de barras y códigos QR;
- verificación de montajes;
- control dimensional;
- localización de objetos desordenados (*Bin Picking*).

En la mayoría de estas aplicaciones la cámara actúa como un sensor inteligente capaz de proporcionar información mucho más rica que un sensor convencional.

Gracias a ello, el robot puede adaptar continuamente sus movimientos a las condiciones reales del entorno.

::: figure
image: ../assets/cap29/fig29_7.png
caption: Principales aplicaciones de la visión artificial en robótica industrial.
:::

Cada una de estas aplicaciones utiliza algoritmos específicos de procesamiento de imágenes, aunque todas ellas siguen un esquema de funcionamiento muy similar: capturar, procesar, decidir y actuar.

---

## 29.8 Beneficios de integrar visión artificial en una célula robotizada

La utilización de cámaras industriales aporta numerosas ventajas respecto a los sistemas tradicionales basados únicamente en sensores discretos.

En primer lugar, permite que una misma instalación pueda adaptarse automáticamente a diferentes tipos de piezas sin modificar la programación del robot.

Además, incrementa la precisión del proceso, ya que las decisiones se toman a partir de información visual obtenida en tiempo real.

Entre los principales beneficios destacan:

- mayor flexibilidad de producción;
- reducción de errores de clasificación;
- incremento de la calidad del producto;
- disminución del tiempo de preparación de la línea;
- mayor trazabilidad del proceso;
- reducción de costes de producción;
- integración con sistemas de Industria 4.0.

Estas ventajas explican por qué la visión artificial se ha convertido en una tecnología imprescindible en sectores como la automoción, la industria alimentaria, la fabricación electrónica o la logística automatizada.

::: table
caption: Comparación entre una célula robotizada con y sin visión artificial.
content:

| Característica | Sin visión artificial | Con visión artificial |
|----------------|----------------------|-----------------------|
| Adaptación a nuevas piezas | Baja | Muy alta |
| Precisión en la identificación | Limitada | Muy elevada |
| Flexibilidad | Reducida | Elevada |
| Automatización | Parcial | Completa |
| Control de calidad | Limitado | Automatizado |
| Integración Industria 4.0 | Parcial | Completa |

:::

::: figure
image: ../assets/cap29/fig29_8.png
caption: Comparación entre una célula robotizada convencional y otra equipada con visión artificial.
:::

---

## 29.9 Validación del sistema de visión artificial

Una vez integrada la cámara dentro de la célula robotizada, es imprescindible comprobar que todo el sistema funciona correctamente antes de utilizarlo en una aplicación industrial.

La validación de un sistema de visión artificial consiste en verificar que la información obtenida por la cámara es precisa, consistente y suficientemente rápida para permitir que el robot tome decisiones en tiempo real.

Durante esta fase deben comprobarse diversos aspectos del proceso de inspección:

- la cámara detecta correctamente todas las piezas;
- la iluminación permanece estable durante toda la simulación;
- las imágenes presentan la calidad suficiente para su procesamiento;
- la identificación coincide con el tipo real de la pieza;
- la comunicación con el controlador no presenta pérdidas de información;
- el robot ejecuta la acción correspondiente a cada resultado obtenido.

En CoppeliaSim estas comprobaciones pueden realizarse ejecutando múltiples ciclos consecutivos y observando tanto el comportamiento del robot como la información proporcionada por el sistema de visión.

::: figure
image: ../assets/cap29/fig29_9.png
caption: Validación completa del sistema de visión artificial integrado en la célula robotizada.
:::

Detectar posibles errores durante esta fase evita problemas posteriores cuando la aplicación evoluciona hacia proyectos más complejos.

---

## 29.10 Preparación para sistemas inteligentes basados en IA

La visión artificial constituye uno de los pilares fundamentales sobre los que se apoyan las aplicaciones actuales de inteligencia artificial en robótica.

Una vez que el sistema es capaz de capturar imágenes y extraer información relevante, resulta posible incorporar algoritmos mucho más avanzados para automatizar tareas que anteriormente requerían intervención humana.

Entre las aplicaciones más representativas encontramos:

- reconocimiento automático de objetos mediante redes neuronales;
- detección de defectos utilizando aprendizaje profundo (*Deep Learning*);
- clasificación inteligente de productos;
- estimación automática de posiciones y orientaciones;
- inspección de calidad basada en inteligencia artificial;
- aprendizaje continuo a partir de nuevos datos.

En los próximos años estas tecnologías desempeñarán un papel cada vez más importante en la automatización industrial.

Gracias a herramientas como CoppeliaSim es posible desarrollar y validar este tipo de soluciones antes de trasladarlas a una instalación física.

Nuestro sistema robotizado dispone ya de todos los elementos necesarios para evolucionar hacia una célula inteligente completamente integrada dentro del paradigma de la Industria 4.0.

::: figure
image: ../assets/cap29/fig29_10.png
caption: Evolución desde un sistema de visión artificial convencional hacia una célula robotizada inteligente basada en inteligencia artificial.
:::

---

## Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Visión artificial | Tecnología que permite capturar, procesar e interpretar imágenes para automatizar tareas industriales. |
| Cámara industrial | Dispositivo encargado de adquirir imágenes de las piezas durante el proceso de producción. |
| Procesamiento de imágenes | Conjunto de algoritmos utilizados para analizar las imágenes capturadas por la cámara. |
| Extracción de características | Obtención de información relevante de una imagen, como color, forma, tamaño o posición. |
| Calibración | Proceso que relaciona las coordenadas de la imagen con las coordenadas físicas del robot. |
| Guiado por visión (*Vision Guided Robotics*) | Técnica que permite al robot adaptar sus movimientos utilizando información visual. |
| Bin Picking | Aplicación de visión artificial destinada a localizar y recoger piezas desordenadas en un contenedor. |
| Detección de defectos | Identificación automática de anomalías durante el proceso de inspección. |
| Comunicación industrial | Intercambio de información entre la cámara, el sistema de control y el robot mediante protocolos industriales. |
| Inteligencia Artificial aplicada a visión | Utilización de algoritmos de aprendizaje automático para mejorar la identificación y clasificación de objetos. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender el funcionamiento general de un sistema de visión artificial.
- ✅ Identificar los componentes que forman una solución de visión industrial.
- ✅ Integrar una cámara en una célula robotizada desarrollada en CoppeliaSim.
- ✅ Comprender el flujo de adquisición y procesamiento de imágenes.
- ✅ Analizar la comunicación entre el sistema de visión y el robot.
- ✅ Entender la importancia de la calibración de la cámara.
- ✅ Conocer las principales aplicaciones de la visión artificial en la industria.
- ✅ Valorar cómo la Inteligencia Artificial amplía las capacidades de los sistemas de visión.

La célula robotizada ya es capaz de observar su entorno y utilizar esa información para tomar decisiones mucho más precisas y flexibles.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué ventajas aporta la visión artificial frente a un sensor fotoeléctrico convencional?
2. ¿Cuáles son los principales componentes de un sistema de visión industrial?
3. ¿Qué etapas forman el flujo de adquisición y procesamiento de imágenes?
4. ¿Por qué es necesaria la calibración entre la cámara y el robot?
5. ¿Qué información puede enviar el sistema de visión al controlador de la célula?
6. ¿Qué aplicaciones industriales utilizan actualmente visión artificial?
7. ¿Cómo puede la Inteligencia Artificial mejorar un sistema de visión industrial?

Si puedes responder correctamente a todas ellas, estás preparado para integrar sistemas de visión artificial en aplicaciones robotizadas reales.

---

## Práctica guiada

::: practice
title: Integración de una cámara industrial en una célula robotizada

difficulty: Media-Alta

time: 90 minutos

content:

Integra un sistema básico de visión artificial en la célula robotizada desarrollada en los capítulos anteriores.

1. Abre el proyecto de clasificación realizado en el capítulo 28.
2. Incorpora una cámara sobre la cinta transportadora.
3. Sitúa la zona de inspección antes del área de trabajo del robot.
4. Define el flujo de adquisición de imágenes.
5. Representa el procesamiento de la información mediante un diagrama funcional.
6. Relaciona la información obtenida con el movimiento del robot.
7. Analiza la importancia de la calibración entre cámara y manipulador.
8. Ejecuta varias simulaciones comprobando el funcionamiento general del sistema.
9. Identifica posibles mejoras para aumentar la precisión de la clasificación.
10. Guarda el proyecto para utilizarlo en el capítulo siguiente.

El objetivo de esta práctica consiste en comprender cómo se integra un sistema de visión artificial dentro de una célula robotizada industrial.

:::

---

## Reto

::: challenge
title: Diseñando una estación inteligente de inspección

content:

Una empresa desea automatizar el control de calidad de una línea de producción.

Diseña una propuesta indicando:

- la posición óptima de la cámara;
- el sistema de iluminación más adecuado;
- qué características deberían inspeccionarse;
- cómo comunicarías la información con el robot;
- qué criterios utilizarías para aceptar o rechazar una pieza;
- qué algoritmos de Inteligencia Artificial podrían incorporarse en una segunda fase.

Realiza un esquema general de la instalación y justifica todas las decisiones adoptadas.

Compara posteriormente tu solución con la de otros compañeros y analiza las ventajas e inconvenientes de cada propuesta.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Comprender el funcionamiento de un sistema de visión artificial.
- Analizar el flujo de adquisición y procesamiento de imágenes.
- Introducir los conceptos básicos de calibración entre cámara y robot.
- Relacionar la visión artificial con aplicaciones reales de Industria 4.0 e Inteligencia Artificial.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Escena desarrollada en el capítulo anterior.
- Modelos de cámaras industriales.
- Presentación o vídeos de aplicaciones reales de visión artificial.

**Consejos metodológicos**

Conviene insistir en que la visión artificial no sustituye al robot, sino que amplía enormemente sus capacidades al proporcionarle información del entorno.

Resulta especialmente interesante mostrar ejemplos reales de inspección automática, guiado de robots y control de calidad para que el alumnado relacione los conceptos aprendidos con aplicaciones presentes en la industria actual.

Si el tiempo lo permite, puede plantearse un pequeño debate sobre el impacto de la Inteligencia Artificial en la evolución de los sistemas de visión industrial.

:::

---

## Próximo capítulo

Con la incorporación de la visión artificial, la célula robotizada ya es capaz de **percibir**, **analizar** y **tomar decisiones** a partir de la información capturada por una cámara industrial.

En el siguiente y último capítulo del libro integraremos todos los conocimientos adquiridos para desarrollar un **proyecto completo de Industria 4.0**, combinando robótica, visión artificial, comunicaciones industriales, Python y gemelo digital dentro de una única aplicación.

Este proyecto final servirá como síntesis de todo el recorrido realizado a lo largo del libro y mostrará cómo las diferentes tecnologías estudiadas trabajan conjuntamente para construir una célula robotizada inteligente.
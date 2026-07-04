::: chapter-cover
number: 16
title: Proyecto final de percepción
time: 8 horas
level: ⭐⭐⭐⭐⭐ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Integrar en un único proyecto todos los conocimientos adquiridos sobre visión artificial.
- Configurar una escena completa con un Pioneer P3DX y un Vision Sensor.
- Desarrollar una aplicación en Python capaz de capturar, procesar e interpretar imágenes.
- Controlar el movimiento del robot a partir de la información obtenida mediante OpenCV.
- Comprender cómo se construye un sistema básico de percepción robótica en tiempo real.
:::

# Capítulo 16 · Proyecto final de percepción

## Uniendo todas las piezas

A lo largo de esta Parte III hemos aprendido numerosas técnicas relacionadas con la visión artificial.

Comenzamos capturando imágenes mediante un Vision Sensor.

Posteriormente aprendimos a procesarlas utilizando OpenCV.

Después fuimos capaces de detectar objetos, calcular sus dimensiones, clasificarlos y, finalmente, controlar el movimiento del Pioneer P3DX utilizando la información proporcionada por la cámara.

Ha llegado el momento de integrar todos estos conocimientos en un único proyecto.

Este proyecto reproducirá, de forma simplificada, el funcionamiento de un sistema de percepción robótica similar a los utilizados en numerosos entornos industriales y de investigación.

::: teacher
content:

Antes de comenzar el proyecto, dedica unos minutos a recordar los conceptos más importantes de los capítulos anteriores.

Es recomendable que el alumnado identifique por sí mismo las diferentes etapas del flujo de percepción antes de comenzar la implementación.
:::

---

## 16.1 Objetivo del proyecto

El objetivo será desarrollar un robot capaz de interpretar su entorno utilizando únicamente la información capturada por una cámara.

El sistema deberá realizar automáticamente las siguientes tareas:

- capturar imágenes;
- detectar un objeto de interés;
- calcular su posición;
- determinar el error visual;
- modificar el movimiento del Pioneer P3DX para mantener el objeto centrado.

Aunque el proyecto es relativamente sencillo, reproduce el esquema básico utilizado por muchos sistemas robóticos reales.

::: figure
image: ../assets/cap16/fig16_1.png
caption: Arquitectura general del proyecto final de percepción.
:::

---

## 16.2 Arquitectura del sistema

Nuestro sistema estará formado por cuatro elementos principales.

1. **Pioneer P3DX**, encargado del desplazamiento.
2. **Vision Sensor**, responsable de capturar imágenes.
3. **Python y OpenCV**, donde se realizará el procesamiento visual.
4. **Algoritmo de control**, que decidirá el movimiento del robot.

Cada uno de estos componentes desempeña una función específica.

La colaboración entre todos ellos permitirá que el robot perciba el entorno y actúe en consecuencia.

---

## 16.3 Flujo de funcionamiento

Durante toda la simulación el sistema ejecutará continuamente el siguiente ciclo.

1. Capturar una imagen desde el Vision Sensor.
2. Procesar la imagen mediante OpenCV.
3. Detectar el objeto seleccionado.
4. Calcular su posición dentro de la imagen.
5. Obtener el error visual.
6. Determinar el movimiento del Pioneer P3DX.
7. Actualizar las velocidades de las ruedas.
8. Repetir el proceso.

Este flujo constituye el núcleo del proyecto y será el encargado de mantener el robot funcionando en tiempo real.

::: figure
image: ../assets/cap16/fig16_2.png
caption: Flujo general del sistema de percepción robótica desarrollado en este capítulo.
:::

---

## 16.4 Organización del proyecto

Para facilitar el desarrollo del programa, dividiremos el trabajo en varios módulos claramente diferenciados.

- Captura de imágenes.
- Procesamiento visual.
- Detección del objeto.
- Cálculo del error.
- Control del robot.

Esta organización hará que el código resulte más claro, más fácil de mantener y más sencillo de ampliar en futuros proyectos.

En las siguientes entregas construiremos cada uno de estos bloques hasta completar un sistema funcional de percepción robótica.

---

## 16.5 Estructurando el programa

Un proyecto de percepción puede crecer rápidamente en complejidad.

Por este motivo resulta recomendable dividir el programa en pequeños bloques funcionales, cada uno encargado de una tarea concreta.

En nuestro proyecto utilizaremos la siguiente organización:

- inicialización de la conexión con CoppeliaSim;
- captura de imágenes;
- procesamiento mediante OpenCV;
- detección del objeto;
- cálculo del error visual;
- control del Pioneer P3DX.

Esta estructura facilitará el mantenimiento del código y permitirá reutilizar gran parte de los módulos en futuros proyectos.

::: figure
image: ../assets/cap16/fig16_3.png
caption: Organización modular del programa de percepción desarrollado en Python.
:::

---

## 16.6 Capturando imágenes desde el Vision Sensor

El primer paso consiste en obtener continuamente las imágenes generadas por el Vision Sensor.

Cada imagen será procesada inmediatamente mediante OpenCV.

Conceptualmente el funcionamiento será el siguiente:

```text
Vision Sensor
      │
      ▼
Imagen
      │
      ▼
OpenCV
```

En la práctica, este proceso se repetirá decenas de veces por segundo.

De este modo el robot dispondrá siempre de una representación actualizada de su entorno.

---

## 16.7 Procesando la imagen

Una vez capturada la imagen, comenzará el procesamiento.

En nuestro proyecto aplicaremos las mismas etapas estudiadas durante los capítulos anteriores.

1. Conversión del formato de la imagen.
2. Transformación al espacio de color adecuado.
3. Segmentación del objeto.
4. Eliminación de pequeñas imperfecciones.
5. Obtención de los contornos.

Cada una de estas operaciones prepara la información necesaria para localizar correctamente el objeto.

::: figure
image: ../assets/cap16/fig16_4.png
caption: Etapas principales del procesamiento de imágenes mediante OpenCV.
:::

---

## 16.8 Detectando el objeto de interés

Tras procesar la imagen podremos localizar el objeto seleccionado.

En este proyecto utilizaremos una pelota roja como objetivo de seguimiento.

El algoritmo deberá:

- localizar su contorno;
- calcular su centro;
- determinar sus coordenadas;
- representar gráficamente el resultado.

Una vez obtenida esta información estaremos preparados para calcular el error visual.

---

## 16.9 Organización del bucle principal

Todo el sistema funcionará dentro de un único bucle de ejecución.

```python
while True:

    imagen = capturar_imagen()

    objeto = detectar_objeto(imagen)

    calcular_error(objeto)

    controlar_robot()

    mostrar_resultado()
```

Aunque este ejemplo está simplificado, refleja perfectamente la arquitectura del proyecto.

Cada iteración actualiza la percepción del entorno y permite que el Pioneer P3DX reaccione inmediatamente a cualquier cambio observado por la cámara.

---

## 16.10 Verificando el funcionamiento

Antes de controlar el robot es importante comprobar que la percepción funciona correctamente.

Para ello mostraremos en pantalla:

- la imagen capturada;
- el objeto detectado;
- el centro del objeto;
- el rectángulo envolvente;
- las coordenadas obtenidas.

Si estos elementos aparecen correctamente representados, podremos afirmar que la fase de percepción se ha completado con éxito.

::: common-error
content:

No intentes depurar simultáneamente la captura de imágenes y el movimiento del robot.

Comprueba primero que la detección del objeto funciona correctamente y, únicamente después, integra el algoritmo de navegación.

Esta forma de trabajar simplifica enormemente la localización de errores.
:::

---

## 16.11 Preparando la integración

Llegados a este punto ya disponemos de un sistema capaz de:

- capturar imágenes;
- procesarlas con OpenCV;
- detectar un objeto;
- calcular su posición.

En la siguiente entrega utilizaremos toda esta información para controlar el Pioneer P3DX y construir un auténtico sistema de percepción robótica en tiempo real.

::: practice
title: Verificación del sistema de percepción

difficulty: Alta

time: 60 minutos

content:

Completa la escena creada en la entrega anterior y desarrolla un programa que:

1. Capture imágenes desde el Vision Sensor.
2. Procese la imagen utilizando OpenCV.
3. Detecte una pelota roja.
4. Dibuje su contorno.
5. Calcule su centro.
6. Muestre las coordenadas sobre la imagen.
7. Visualice el resultado en tiempo real.

Como ampliación, modifica el programa para detectar dos objetos de colores diferentes y representa ambos simultáneamente.
:::

::: teacher
content:

Esta práctica constituye un punto de control muy importante.

Antes de continuar con la navegación del Pioneer P3DX, verifica que todos los estudiantes obtienen una detección estable y continua del objeto.

Resolver ahora los posibles problemas de percepción evitará dificultades durante la integración del sistema completo.
:::

---

## 16.12 Integrando percepción y navegación

Hasta este momento hemos desarrollado dos bloques de trabajo independientes.

Por un lado, el sistema de percepción es capaz de:

- capturar imágenes;
- detectar un objeto;
- calcular su posición;
- obtener el error visual.

Por otro, el Pioneer P3DX puede desplazarse modificando la velocidad de sus ruedas.

Ha llegado el momento de unir ambos sistemas.

A partir de ahora, el movimiento del robot dependerá exclusivamente de la información obtenida por el Vision Sensor.

::: figure
image: ../assets/cap16/fig16_5.png
caption: Integración del sistema de percepción con el control del Pioneer P3DX.
:::

---

## 16.13 El ciclo completo de decisión

Cada iteración del programa seguirá siempre la misma secuencia.

1. Capturar una imagen.
2. Detectar el objeto.
3. Calcular el error visual.
4. Decidir el movimiento.
5. Enviar velocidades al Pioneer P3DX.
6. Capturar una nueva imagen.

Este ciclo constituye un auténtico sistema de control en tiempo real.

Mientras la simulación permanezca activa, el robot repetirá continuamente estas operaciones.

---

## 16.14 Calculando las velocidades

El algoritmo utilizará el error horizontal para modificar la velocidad relativa de las ruedas.

Conceptualmente el comportamiento será:

```python
if error_x < -15:

    rueda_izquierda = 1.5
    rueda_derecha   = 3.0

elif error_x > 15:

    rueda_izquierda = 3.0
    rueda_derecha   = 1.5

else:

    rueda_izquierda = 3.0
    rueda_derecha   = 3.0
```

Aunque este algoritmo es muy sencillo, resulta suficiente para mantener el objeto aproximadamente centrado durante la navegación.

::: figure
image: ../assets/cap16/fig16_6.png
caption: Conversión del error visual en velocidades para las ruedas del Pioneer P3DX.
:::

---

## 16.15 Observando el comportamiento del robot

Una vez integrado el sistema completo, podremos comprobar fácilmente su funcionamiento.

Cuando el objeto permanezca centrado:

- el Pioneer avanzará en línea recta.

Si el objeto se desplaza hacia la izquierda:

- el robot girará hacia la izquierda.

Si el objeto aparece a la derecha:

- corregirá su trayectoria girando hacia la derecha.

El comportamiento observado será muy similar al de un robot móvil real guiado mediante visión artificial.

---

## 16.16 Probando diferentes situaciones

Una de las ventajas de trabajar con CoppeliaSim es la posibilidad de modificar la escena de forma inmediata.

Durante las pruebas conviene experimentar con distintas situaciones.

Por ejemplo:

- variar la posición inicial del objeto;
- modificar la velocidad del robot;
- desplazar el objeto manualmente;
- cambiar la iluminación de la escena;
- introducir obstáculos.

Estas pruebas permiten comprobar la robustez del algoritmo y detectar posibles mejoras.

---

## 16.17 Analizando los resultados

Durante la simulación es recomendable observar simultáneamente:

- la ventana de OpenCV;
- el movimiento del Pioneer P3DX;
- los valores del error visual mostrados por consola.

La comparación entre estos tres elementos facilita enormemente la comprensión del funcionamiento interno del sistema.

::: common-error
content:

No aumentes la complejidad del escenario hasta comprobar que el algoritmo funciona correctamente con un único objeto.

La depuración resulta mucho más sencilla cuando las pruebas se realizan de forma progresiva.
:::

---

## 16.18 Un proyecto preparado para crecer

Aunque el proyecto desarrollado durante este capítulo es relativamente sencillo, su arquitectura permite incorporar fácilmente nuevas funcionalidades.

Entre las posibles ampliaciones destacan:

- seguimiento de varios objetos;
- reconocimiento automático de diferentes colores;
- integración con sensores de proximidad;
- planificación básica de trayectorias;
- incorporación de algoritmos de inteligencia artificial.

De este modo, el proyecto puede evolucionar gradualmente hacia aplicaciones mucho más complejas sin necesidad de modificar su estructura general.

::: practice
title: Integración completa del sistema

difficulty: Alta

time: 90 minutos

content:

Integra todos los módulos desarrollados durante el capítulo.

El programa deberá:

1. Capturar imágenes desde el Vision Sensor.
2. Procesarlas utilizando OpenCV.
3. Detectar una pelota roja.
4. Calcular el error horizontal.
5. Determinar las velocidades de las ruedas.
6. Controlar el Pioneer P3DX.
7. Mostrar sobre la imagen:
   - el centro del objeto;
   - el centro de la imagen;
   - la línea de error;
   - el valor del error horizontal.
8. Verificar que el robot mantiene la pelota centrada durante toda la simulación.

Como ampliación, modifica el algoritmo para que el robot reduzca automáticamente su velocidad cuando el objeto permanezca dentro de la zona de tolerancia.
:::

::: teacher
content:

Esta práctica representa el momento culminante de toda la Parte III.

Es recomendable dedicar tiempo suficiente para que el alumnado experimente con distintos escenarios y comprenda cómo pequeñas variaciones en el algoritmo de control afectan al comportamiento global del robot.

Antes de pasar al cierre del capítulo, conviene realizar una demostración completa del sistema funcionando en tiempo real.
:::

---

## 16.19 El proyecto completo

Después de varias entregas hemos construido, paso a paso, todos los componentes necesarios para desarrollar un sistema de percepción robótica.

Nuestro proyecto integra:

- un Pioneer P3DX;
- un Vision Sensor;
- un programa desarrollado en Python;
- OpenCV para el procesamiento de imágenes;
- un algoritmo de decisión;
- un sistema de navegación autónoma.

Cada uno de estos elementos colabora para que el robot sea capaz de interpretar lo que observa y reaccionar en consecuencia.

::: figure
image: ../assets/cap16/fig16_7.png
caption: Arquitectura completa del proyecto final de percepción.
:::

---

## 16.20 Funcionamiento global

Cuando iniciamos la simulación, el sistema comienza a ejecutar continuamente el siguiente ciclo.

1. El Vision Sensor captura una nueva imagen.
2. OpenCV procesa la información visual.
3. Se detecta el objeto de interés.
4. Se calcula el error visual.
5. El algoritmo decide el movimiento.
6. El Pioneer P3DX modifica la velocidad de sus ruedas.
7. El proceso vuelve a comenzar.

Gracias a este funcionamiento continuo, el robot mantiene una percepción actualizada de su entorno.

---

## 16.21 Verificando el proyecto

Antes de considerar finalizado el sistema conviene comprobar que todas las etapas funcionan correctamente.

Durante las pruebas deberíamos verificar que:

- la cámara captura imágenes sin interrupciones;
- el objeto se detecta correctamente;
- el cálculo del error es estable;
- el Pioneer responde adecuadamente a los desplazamientos del objeto;
- el seguimiento permanece operativo durante toda la simulación.

::: figure
image: ../assets/cap16/fig16_8.png
caption: Verificación del funcionamiento del proyecto completo durante la simulación.
:::

---

## 16.22 Posibles ampliaciones

El proyecto desarrollado constituye una excelente base para seguir avanzando.

Algunas ampliaciones interesantes podrían ser:

- detectar varios objetos simultáneamente;
- seguir únicamente un color determinado;
- incorporar sensores de proximidad para evitar obstáculos;
- combinar visión artificial y navegación autónoma;
- utilizar modelos de inteligencia artificial para reconocer objetos complejos.

Todas estas mejoras reutilizan prácticamente la misma arquitectura desarrollada en este capítulo.

---

## 16.23 Preparando el siguiente paso

Con este proyecto concluye el recorrido dedicado a la percepción visual.

El Pioneer P3DX ya es capaz de:

- observar su entorno;
- interpretar imágenes;
- localizar objetos;
- clasificarlos;
- seguir su movimiento;
- modificar automáticamente su trayectoria.

Sin embargo, hasta ahora el robot únicamente ha utilizado la información visual para desplazarse.

En muchas aplicaciones industriales resulta necesario realizar una acción física sobre los objetos detectados.

Por ejemplo:

- recoger una pieza;
- moverla;
- clasificarla;
- depositarla en otra posición.

Para realizar estas tareas necesitaremos un tipo de robot diferente.

Ese será precisamente el objetivo de la siguiente parte del libro.

::: common-error
content:

No consideres terminado un proyecto únicamente porque el robot se mueve.

Un sistema robótico completo debe verificarse en diferentes situaciones para comprobar que mantiene un comportamiento estable incluso cuando cambian las condiciones de la escena.
:::

---

## 16.24 Conclusiones del proyecto

El proyecto desarrollado durante este capítulo representa un sistema de percepción robótica completamente funcional.

Aunque se trata de una versión didáctica, reproduce fielmente las etapas fundamentales presentes en numerosos sistemas industriales:

- adquisición de información;
- procesamiento de imágenes;
- toma de decisiones;
- actuación sobre el entorno.

Estos mismos principios se encuentran en robots móviles, vehículos autónomos, sistemas de inspección visual y numerosas aplicaciones de automatización industrial.

::: practice
title: Proyecto integrador de percepción robótica

difficulty: Alta

time: 120 minutos

content:

Desarrolla un proyecto completo que integre todos los conocimientos adquiridos durante la Parte III.

El sistema deberá:

1. Capturar imágenes desde un Vision Sensor.
2. Procesarlas utilizando OpenCV.
3. Detectar una pelota roja.
4. Calcular continuamente su posición.
5. Obtener el error respecto al centro de la imagen.
6. Controlar el movimiento del Pioneer P3DX.
7. Mantener el objeto centrado durante toda la simulación.
8. Mostrar información gráfica sobre la imagen procesada.
9. Verificar el funcionamiento del sistema en diferentes escenarios.

Como ampliación, incorpora un segundo objeto de distinto color y modifica el algoritmo para seleccionar automáticamente cuál debe seguir el robot.
:::

::: teacher
content:

Este proyecto constituye la actividad integradora de toda la Parte III.

Se recomienda permitir que cada grupo de estudiantes introduzca pequeñas mejoras personales en el algoritmo, favoreciendo así la creatividad y la experimentación.

El objetivo principal no es únicamente que el robot funcione, sino que el alumnado comprenda cómo interactúan todos los módulos que forman un sistema moderno de percepción robótica.
:::

---

# Conceptos clave

Antes de continuar con la siguiente parte del libro, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Sistema de percepción | Conjunto de sensores y algoritmos que permiten al robot obtener información del entorno y utilizarla para tomar decisiones. |
| Visión artificial | Disciplina que permite interpretar imágenes digitales para comprender el entorno del robot. |
| OpenCV | Biblioteca utilizada para el procesamiento y análisis de imágenes mediante Python. |
| Detección de objetos | Proceso de localizar automáticamente un objeto dentro de una imagen. |
| Error visual | Diferencia entre la posición del objeto detectado y el punto de referencia de la imagen. |
| Bucle de control | Ciclo continuo formado por captura, procesamiento, decisión y actuación. |
| Navegación visual | Desplazamiento del robot utilizando la información obtenida por una cámara. |
| Arquitectura modular | Organización del programa en módulos independientes que colaboran entre sí. |
| Procesamiento en tiempo real | Capacidad del sistema para analizar continuamente nuevas imágenes y reaccionar inmediatamente. |
| Integración | Combinación de todos los módulos para construir un sistema robótico funcional. |
:::

---

# En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Diseñar un sistema completo de percepción robótica.
- ✅ Configurar una escena de trabajo con un Pioneer P3DX y un Vision Sensor.
- ✅ Integrar Python y OpenCV dentro de un único proyecto.
- ✅ Detectar un objeto y calcular su posición.
- ✅ Utilizar el error visual para controlar el movimiento del robot.
- ✅ Construir un sistema completo de percepción y navegación en tiempo real.
- ✅ Comprender cómo se estructura una aplicación moderna de visión artificial.

Con este proyecto final has integrado todos los conocimientos desarrollados a lo largo de la Parte III.

---

# Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué módulos forman el sistema completo de percepción desarrollado en este capítulo?
2. ¿Qué función desempeña el Vision Sensor dentro del proyecto?
3. ¿Por qué es importante organizar el programa en módulos independientes?
4. ¿Qué papel desempeña OpenCV en el sistema?
5. ¿Cómo influye el error visual en el movimiento del Pioneer P3DX?
6. ¿Por qué el procesamiento debe ejecutarse de forma continua?
7. ¿Qué ventajas ofrece integrar percepción y navegación en un único sistema?

Si puedes responder correctamente a todas estas preguntas, has adquirido una base sólida sobre percepción robótica mediante visión artificial.

---

# Práctica guiada

::: practice
title: Proyecto final de percepción robótica

difficulty: Muy alta

time: 120 minutos

content:

Desarrolla un proyecto completo que integre todos los contenidos estudiados durante la Parte III.

El sistema deberá:

1. Capturar imágenes desde un Vision Sensor.
2. Procesarlas utilizando OpenCV.
3. Detectar una pelota roja.
4. Calcular continuamente su posición.
5. Obtener el error respecto al centro de la imagen.
6. Controlar el movimiento del Pioneer P3DX.
7. Mantener el objeto centrado durante toda la simulación.
8. Mostrar información gráfica sobre la imagen procesada.
9. Comprobar el funcionamiento del sistema en diferentes escenarios.

Como ampliación, incorpora un segundo objeto de otro color y añade un selector que permita elegir cuál debe seguir el robot.
:::

---

# Reto

::: challenge
title: Sistema inteligente de exploración visual

content:

Diseña una escena en la que el Pioneer P3DX deba recorrer un entorno identificando diferentes objetos mediante visión artificial.

El robot deberá:

- detectar automáticamente los objetos visibles;
- seleccionar el objetivo de interés;
- aproximarse hasta él utilizando navegación visual;
- detenerse cuando alcance una distancia determinada;
- reanudar la búsqueda de un nuevo objetivo.

Como ampliación, incorpora obstáculos y combina la información del Vision Sensor con los sensores de proximidad para mejorar la navegación.

Este reto reproduce el funcionamiento básico de numerosos robots móviles utilizados en inspección, logística y exploración autónoma.
:::

---

# Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre dos y tres sesiones de 55 minutos.

**Objetivos**

- Integrar todos los conocimientos adquiridos durante la Parte III.
- Consolidar el uso conjunto de CoppeliaSim, Python y OpenCV.
- Comprender la arquitectura de un sistema moderno de percepción robótica.
- Preparar al alumnado para el trabajo con robots industriales.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Python.
- Biblioteca OpenCV (`opencv-python`).
- Escena con un Pioneer P3DX, un Vision Sensor y diferentes objetos de prueba.

**Consejos metodológicos**

Es recomendable dedicar una sesión completa a la integración del proyecto y otra a la experimentación.

Permite que el alumnado modifique el algoritmo, pruebe diferentes escenarios y analice cómo afectan esos cambios al comportamiento del robot.

Antes de comenzar la Parte IV, verifica que todos los estudiantes comprenden el flujo completo:

Percepción → Procesamiento → Decisión → Actuación.

Este esquema será la base sobre la que se construirá el trabajo con brazos robóticos industriales.
:::

---

# Fin de la Parte III

Con este capítulo concluye la **Parte III: Percepción avanzada y visión artificial**.

A lo largo de estos cinco capítulos el robot ha aprendido a utilizar uno de los sensores más importantes de la robótica moderna: la cámara.

Primero aprendió a capturar imágenes, después a procesarlas mediante OpenCV, posteriormente a detectar y clasificar objetos y, finalmente, a utilizar esa información para navegar de forma autónoma.

Esta evolución reproduce el camino seguido por muchos sistemas robóticos actuales, en los que la percepción constituye el punto de partida para cualquier proceso de automatización inteligente.

---

# Próxima parte

Hasta ahora el protagonista del libro ha sido el **Pioneer P3DX**, un robot móvil capaz de desplazarse y comprender visualmente su entorno.

Ha llegado el momento de dar un paso más.

En la **Parte IV: Robótica industrial y manipulación** conocerás un nuevo tipo de robot: el **Universal Robots UR3**.

Aprenderás cómo está construido un brazo robótico industrial, cómo controlar sus articulaciones, cómo mover su efector final y cómo manipular objetos con precisión dentro de CoppeliaSim utilizando Python.

La percepción ya está resuelta.

Ahora el robot aprenderá a **interactuar físicamente con el entorno**, iniciando el recorrido por la robótica industrial y la automatización avanzada.
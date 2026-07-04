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

---

## 15.5 El centro de la imagen

En el capítulo anterior aprendimos a calcular el centro de un objeto utilizando su rectángulo envolvente.

Sin embargo, para seguir un objeto no basta con conocer su posición.

También necesitamos compararla con un punto de referencia.

Ese punto de referencia será el **centro de la imagen**.

En una imagen de **640 × 480 píxeles**, el centro se encuentra en:

```text
Centro = (320, 240)
```

Mientras el objeto permanezca cerca de ese punto podremos considerar que está correctamente centrado.

::: figure
image: ../assets/cap15/fig15_3.png
caption: El centro de la imagen se utiliza como referencia para evaluar la posición del objeto.
:::

---

## 15.6 Calculando el error visual

Supongamos que el centro del objeto detectado se encuentra en:

```text
Objeto = (260, 240)
```

La diferencia respecto al centro de la imagen será:

```python
error_x = centro_objeto_x - centro_imagen_x
error_y = centro_objeto_y - centro_imagen_y
```

En nuestro ejemplo:

```text
error_x = 260 − 320 = −60

error_y = 240 − 240 = 0
```

Esto significa que el objeto aparece desplazado **60 píxeles hacia la izquierda**.

Este desplazamiento recibe el nombre de **error visual**.

---

## 15.7 Interpretando el error

El signo del error proporciona información muy útil.

### Error horizontal

| Valor | Interpretación |
|--------|----------------|
| Negativo | El objeto está a la izquierda. |
| Cero | El objeto está centrado. |
| Positivo | El objeto está a la derecha. |

### Error vertical

| Valor | Interpretación |
|--------|----------------|
| Negativo | El objeto está por encima del centro. |
| Cero | El objeto está centrado verticalmente. |
| Positivo | El objeto está por debajo del centro. |

::: figure
image: ../assets/cap15/fig15_4.png
caption: Interpretación del error visual en los ejes horizontal y vertical.
:::

Gracias a esta información el robot podrá decidir cómo debe moverse para mantener el objeto centrado.

---

## 15.8 Representando el error

Durante el desarrollo de una aplicación resulta muy útil mostrar el centro de la imagen y el centro del objeto.

También podemos dibujar una línea que una ambos puntos.

```python
cv2.line(
    imagen,
    (centro_imagen_x, centro_imagen_y),
    (centro_objeto_x, centro_objeto_y),
    (0,255,0),
    2
)
```

Esta representación facilita comprobar visualmente el desplazamiento del objeto.

Cuando la línea desaparece significa que ambos centros coinciden y el error es prácticamente nulo.

---

## 15.9 Zona de tolerancia

En la práctica no resulta necesario mantener el objeto exactamente sobre el centro de la imagen.

Pequeñas desviaciones suelen ser aceptables.

Por este motivo se define una **zona de tolerancia**.

Por ejemplo:

```text
±15 píxeles
```

Mientras el error permanezca dentro de ese intervalo, el robot no realizará ninguna corrección.

Este criterio evita movimientos continuos e innecesarios.

::: common-error
content:

Intentar corregir incluso desplazamientos de uno o dos píxeles suele provocar movimientos bruscos e inestables.

Siempre es recomendable definir una pequeña zona de tolerancia alrededor del centro de la imagen.
:::

---

## 15.10 Primer algoritmo de seguimiento

El algoritmo básico de seguimiento puede resumirse mediante las siguientes reglas.

```text
Si error_x < -15
        Girar a la izquierda

Si error_x > 15
        Girar a la derecha

Si -15 ≤ error_x ≤ 15
        Continuar recto
```

Observa que todavía no estamos calculando velocidades.

Únicamente estamos tomando decisiones sencillas a partir de la posición del objeto.

En el siguiente apartado utilizaremos estas reglas para controlar directamente el movimiento del Pioneer P3DX.

---

## 15.11 Visualizando el seguimiento

Antes de mover el robot conviene comprobar que el cálculo del error es correcto.

Para ello mostraremos simultáneamente:

- el centro de la imagen;
- el centro del objeto;
- la línea que une ambos puntos;
- el valor numérico del error horizontal.

De esta forma podremos verificar visualmente el funcionamiento del algoritmo antes de comenzar a controlar el robot.

::: practice
title: Calculando el error visual

difficulty: Media

time: 45 minutos

content:

Construye una escena con un Pioneer P3DX equipado con un Vision Sensor y una pelota de color rojo.

Desarrolla un programa que:

1. Detecte la pelota mediante OpenCV.
2. Calcule el centro de la imagen.
3. Obtenga el centro de la pelota.
4. Calcule el error horizontal y vertical.
5. Dibuje ambos centros sobre la imagen.
6. Una ambos puntos mediante una línea.
7. Muestre el valor del error en tiempo real.

Comprueba cómo cambia el error al desplazar la pelota por diferentes zonas de la escena.
:::

::: teacher
content:

No introduzcas todavía ningún algoritmo de control.

Es importante que el alumnado comprenda primero el significado del error visual y cómo evoluciona cuando cambia la posición del objeto.

Una vez interiorizado este concepto, el control del robot resultará mucho más sencillo de entender.
:::

---

## 15.12 Del error visual al movimiento del robot

En la entrega anterior aprendimos a calcular el error entre el centro de la imagen y el centro del objeto detectado.

Ahora utilizaremos esa información para controlar directamente el movimiento del Pioneer P3DX.

La idea es muy sencilla.

Si el objeto aparece desplazado hacia la izquierda, el robot girará a la izquierda.

Si aparece desplazado hacia la derecha, girará a la derecha.

Cuando el objeto permanezca centrado, el robot continuará avanzando.

Este comportamiento reproduce el funcionamiento básico de numerosos robots móviles guiados por visión artificial.

---

## 15.13 Tomando decisiones

El algoritmo puede resumirse mediante unas reglas muy sencillas.

```text
Objeto a la izquierda
        ↓
Girar a la izquierda

Objeto centrado
        ↓
Avanzar

Objeto a la derecha
        ↓
Girar a la derecha
```

Aunque estas reglas parecen muy simples, constituyen la base de numerosos sistemas de navegación visual.

::: figure
image: ../assets/cap15/fig15_5.png
caption: Conversión del error visual en órdenes de movimiento del Pioneer P3DX.
:::

---

## 15.14 Controlando el giro

Supongamos que disponemos del valor del error horizontal.

Podemos utilizarlo para decidir el sentido de giro.

```python
if error_x < -15:
    print("Girar a la izquierda")

elif error_x > 15:
    print("Girar a la derecha")

else:
    print("Avanzar")
```

En esta primera aproximación todavía no controlaremos la velocidad exacta del robot.

Nuestro objetivo consiste únicamente en comprobar que las decisiones tomadas coinciden con la posición del objeto.

---

## 15.15 Enviando órdenes al Pioneer P3DX

Una vez tomada la decisión, debemos transformar esa información en velocidades para las ruedas del robot.

Conceptualmente el comportamiento será el siguiente.

| Situación | Rueda izquierda | Rueda derecha |
|-----------|----------------:|--------------:|
| Girar a la izquierda | Baja velocidad | Alta velocidad |
| Avanzar | Igual velocidad | Igual velocidad |
| Girar a la derecha | Alta velocidad | Baja velocidad |

Gracias a esta diferencia de velocidades, el Pioneer P3DX podrá orientar su cámara hacia el objeto.

::: figure
image: ../assets/cap15/fig15_6.png
caption: Control diferencial de las ruedas del Pioneer P3DX para mantener el objeto centrado.
:::

---

## 15.16 Un ejemplo sencillo

El siguiente fragmento resume la lógica de control.

```python
if error_x < -15:

    velocidad_izquierda = 1.5
    velocidad_derecha   = 3.0

elif error_x > 15:

    velocidad_izquierda = 3.0
    velocidad_derecha   = 1.5

else:

    velocidad_izquierda = 3.0
    velocidad_derecha   = 3.0
```

Observa que únicamente modificamos las velocidades de las ruedas.

No necesitamos calcular ángulos ni trayectorias complejas.

El propio movimiento diferencial del robot corrige el error visual.

---

## 15.17 Corrección continua

El seguimiento visual no consiste en ejecutar una única decisión.

El proceso debe repetirse continuamente.

En cada iteración del programa se realizan siempre los mismos pasos.

1. Capturar una nueva imagen.
2. Detectar el objeto.
3. Calcular el error.
4. Actualizar las velocidades.
5. Mover el robot.
6. Volver a comenzar.

Este ciclo se ejecuta decenas de veces por segundo, permitiendo que el Pioneer P3DX mantenga el objeto dentro de su campo de visión.

::: common-error
content:

No calcules el error una única vez al inicio del programa.

El objeto puede cambiar de posición continuamente, por lo que el error debe recalcularse en cada nueva imagen capturada por el Vision Sensor.
:::

---

## 15.18 Primera demostración

Como primera práctica utilizaremos una pelota roja situada frente al Pioneer P3DX.

Mientras la pelota permanezca inmóvil, el robot deberá mantenerla centrada.

Posteriormente desplazaremos manualmente la pelota hacia la izquierda y hacia la derecha.

El robot deberá girar automáticamente para volver a centrarla.

Esta será la primera aplicación del libro en la que el movimiento del robot dependerá directamente de la información proporcionada por una cámara.

::: practice
title: Control visual del Pioneer P3DX

difficulty: Media

time: 60 minutos

content:

Construye una escena formada por un Pioneer P3DX equipado con un Vision Sensor y una pelota roja situada frente al robot.

Desarrolla un programa que:

1. Detecte la pelota mediante OpenCV.
2. Calcule el error horizontal.
3. Decida el movimiento del robot.
4. Modifique las velocidades de las ruedas.
5. Mantenga la pelota centrada en la imagen.

Como ampliación, cambia la posición inicial de la pelota y observa cómo reacciona el robot hasta volver a centrarla.
:::

::: teacher
content:

Es recomendable comenzar con movimientos lentos y una única pelota de color bien diferenciado.

Una vez que el alumnado comprenda el funcionamiento del algoritmo, podrá aumentar la velocidad del robot y experimentar con trayectorias más complejas.
:::

---

## 15.19 Seguimiento de una pelota

Una de las aplicaciones más sencillas del seguimiento visual consiste en seguir una pelota de color.

La idea es muy simple.

Mientras la pelota permanezca dentro del campo de visión del Vision Sensor, el Pioneer P3DX ajustará continuamente su dirección para mantenerla centrada.

El algoritmo se ejecutará de forma repetitiva.

1. Capturar una imagen.
2. Detectar la pelota mediante su color.
3. Calcular el centro de la pelota.
4. Obtener el error visual.
5. Corregir la trayectoria del robot.

Este ciclo se repetirá continuamente durante toda la simulación.

::: figure
image: ../assets/cap15/fig15_7.png
caption: Seguimiento automático de una pelota utilizando el Vision Sensor del Pioneer P3DX.
:::

---

## 15.20 Ajustando la velocidad

Hasta ahora hemos utilizado únicamente tres acciones.

- Girar a la izquierda.
- Avanzar.
- Girar a la derecha.

Sin embargo, este comportamiento produce movimientos algo bruscos.

Podemos conseguir un seguimiento mucho más suave haciendo que la velocidad dependa del valor del error.

Por ejemplo:

```python
if abs(error_x) < 15:

    velocidad = 3.0

elif abs(error_x) < 60:

    velocidad = 2.0

else:

    velocidad = 1.0
```

Cuanto menor sea el error, más estable será el movimiento del robot.

Este principio constituye la base de numerosos sistemas de guiado visual.

---

## 15.21 Seguimiento de una línea

Otra aplicación muy utilizada consiste en seguir una línea marcada sobre el suelo.

En este caso, el Vision Sensor observa continuamente una franja situada delante del robot.

El programa detecta la posición de la línea y calcula su desplazamiento respecto al centro de la imagen.

Si la línea aparece desplazada hacia la izquierda, el Pioneer girará hacia la izquierda.

Si aparece desplazada hacia la derecha, corregirá su trayectoria en sentido contrario.

::: figure
image: ../assets/cap15/fig15_8.png
caption: Seguimiento de una línea mediante visión artificial utilizando OpenCV.
:::

Este procedimiento es muy similar al utilizado por numerosos robots educativos y vehículos autónomos.

---

## 15.22 Comparando ambas aplicaciones

Aunque seguir una pelota y seguir una línea parecen tareas diferentes, ambas utilizan exactamente el mismo esquema de funcionamiento.

| Seguimiento de pelota | Seguimiento de línea |
|-----------------------|----------------------|
| Detectar la pelota. | Detectar la línea. |
| Calcular su centro. | Calcular el centro de la línea. |
| Obtener el error. | Obtener el error. |
| Corregir la trayectoria. | Corregir la trayectoria. |

La única diferencia reside en el tipo de objeto detectado.

El algoritmo de control permanece prácticamente igual.

---

## 15.23 Mejorando la estabilidad

En aplicaciones reales es frecuente introducir pequeñas mejoras para conseguir movimientos más suaves.

Algunas estrategias habituales son:

- limitar la velocidad máxima;
- suavizar las correcciones;
- ignorar pequeñas variaciones del error;
- filtrar el ruido producido por la cámara.

Gracias a estas técnicas el robot evita realizar movimientos bruscos y consigue trayectorias mucho más estables.

::: common-error
content:

No aumentes excesivamente la velocidad del Pioneer P3DX durante las primeras pruebas.

Si el robot gira demasiado rápido, puede perder el objeto del campo de visión y el seguimiento dejará de funcionar correctamente.
:::

---

## 15.24 Dos aplicaciones, un mismo algoritmo

Llegados a este punto podemos observar una idea muy importante.

No estamos desarrollando un algoritmo diferente para cada problema.

Estamos reutilizando exactamente el mismo procedimiento.

Únicamente cambia el objeto que deseamos detectar.

Este enfoque permite construir aplicaciones muy flexibles reutilizando gran parte del código.

En capítulos posteriores volveremos a utilizar esta misma filosofía para controlar brazos robóticos y sistemas completos de automatización.

::: practice
title: Siguiendo una pelota y una línea

difficulty: Media-Alta

time: 75 minutos

content:

Construye dos escenas diferentes.

**Escena 1**

- Pioneer P3DX.
- Vision Sensor.
- Pelota roja.

Desarrolla un programa capaz de mantener la pelota centrada en la imagen.

**Escena 2**

- Pioneer P3DX.
- Línea negra sobre el suelo.

Desarrolla un programa que permita al robot seguir automáticamente la trayectoria de la línea.

Como ampliación, compara ambos programas e identifica qué partes del algoritmo son comunes y cuáles cambian en cada aplicación.
:::

::: teacher
content:

Este ejercicio resulta especialmente útil para que el alumnado descubra que muchos problemas de robótica comparten la misma estructura de resolución.

Conviene dedicar unos minutos al final de la práctica para comparar ambos algoritmos y destacar que el proceso de detección, cálculo del error y corrección del movimiento permanece prácticamente invariable.
:::

---

## 15.25 Construyendo un sistema completo de seguimiento visual

Ha llegado el momento de integrar todos los conceptos estudiados durante este capítulo.

Nuestro objetivo será desarrollar un sistema completo capaz de:

- detectar un objeto mediante el Vision Sensor;
- calcular su posición dentro de la imagen;
- determinar el error visual;
- modificar continuamente la trayectoria del Pioneer P3DX para mantener el objeto centrado.

Este procedimiento constituye la base de numerosos robots autónomos utilizados actualmente en investigación, logística e industria.

::: figure
image: ../assets/cap15/fig15_9.png
caption: Sistema completo de seguimiento visual utilizando CoppeliaSim, Python y OpenCV.
:::

---

## 15.26 Flujo completo del algoritmo

El funcionamiento del programa puede resumirse mediante la siguiente secuencia.

1. Capturar una imagen desde el Vision Sensor.
2. Procesar la imagen mediante OpenCV.
3. Detectar el objeto de interés.
4. Calcular el centro del objeto.
5. Obtener el error visual.
6. Determinar el movimiento necesario.
7. Enviar las velocidades al Pioneer P3DX.
8. Repetir el proceso.

Todo este ciclo se ejecuta continuamente mientras la simulación permanece activa.

Gracias a ello, el robot puede adaptarse instantáneamente a cualquier cambio observado en la escena.

---

## 15.27 Procesamiento en tiempo real

Una característica fundamental del seguimiento visual es que el programa nunca finaliza mientras el robot permanece en funcionamiento.

El algoritmo se ejecuta dentro de un bucle continuo.

```python
while True:

    capturar_imagen()

    detectar_objeto()

    calcular_error()

    mover_robot()
```

Cada iteración actualiza la información proporcionada por la cámara y adapta el movimiento del Pioneer P3DX.

Aunque este ejemplo está simplificado, representa fielmente la estructura utilizada en aplicaciones reales.

---

## 15.28 Comportamiento del robot

Cuando el algoritmo funciona correctamente, el comportamiento del robot resulta muy natural.

- Si el objeto permanece centrado, el Pioneer continúa avanzando.
- Si el objeto se desplaza hacia la izquierda, el robot gira hacia la izquierda.
- Si el objeto se desplaza hacia la derecha, corrige su trayectoria hacia la derecha.
- Cuando el objeto vuelve al centro, el movimiento recupera su estabilidad.

::: figure
image: ../assets/cap15/fig15_10.png
caption: Respuesta del Pioneer P3DX ante diferentes posiciones del objeto detectado.
:::

Este comportamiento reproduce el funcionamiento básico de numerosos robots guiados mediante visión artificial.

---

## 15.29 Posibles mejoras

El algoritmo desarrollado durante este capítulo constituye una excelente base para comenzar a trabajar con seguimiento visual.

No obstante, existen numerosas mejoras que podrían incorporarse.

Entre ellas destacan:

- utilizar un control proporcional para suavizar el movimiento;
- adaptar automáticamente la velocidad del robot;
- seguir objetos de diferentes colores;
- combinar la información de varios sensores;
- utilizar técnicas de aprendizaje automático para reconocer objetos complejos.

Todas estas mejoras forman parte de aplicaciones reales de robótica y visión artificial.

::: common-error
content:

No intentes añadir demasiadas mejoras al mismo tiempo.

Comprueba primero que el algoritmo básico funciona correctamente y, posteriormente, incorpora nuevas funcionalidades de forma progresiva.
:::

---

## 15.30 Del seguimiento visual a la percepción inteligente

Durante este capítulo el robot ha aprendido a reaccionar ante la información proporcionada por una cámara.

Sin embargo, todavía responde únicamente a reglas sencillas.

En aplicaciones más avanzadas, el robot no solo sigue objetos.

También interpreta escenas completas, identifica diferentes elementos, toma decisiones complejas y combina la información visual con otros sensores.

Ese será precisamente el objetivo del siguiente capítulo.

::: practice
title: Sistema completo de seguimiento visual

difficulty: Alta

time: 90 minutos

content:

Construye una escena formada por:

- un Pioneer P3DX;
- un Vision Sensor;
- una pelota roja.

Desarrolla un programa que:

1. Detecte la pelota utilizando OpenCV.
2. Calcule continuamente el centro del objeto.
3. Obtenga el error horizontal.
4. Ajuste las velocidades de las ruedas del Pioneer P3DX.
5. Mantenga la pelota centrada durante todo el recorrido.
6. Muestre sobre la imagen:
   - el centro de la imagen;
   - el centro del objeto;
   - la línea de error;
   - el valor del error horizontal.

Como ampliación, modifica el programa para que el robot reduzca automáticamente su velocidad cuando el error sea muy pequeño y aumente la precisión del seguimiento.
:::

::: teacher
content:

Esta práctica constituye un excelente proyecto integrador de toda la Parte III.

El alumnado comprobará cómo conceptos estudiados en distintos capítulos —captura de imágenes, procesamiento con OpenCV, detección de objetos y cálculo del error visual— se combinan para construir un sistema robótico funcional.

Antes de comenzar el Capítulo 16, conviene verificar que todos los estudiantes comprenden el ciclo completo de percepción y control en tiempo real.
:::

---

# Conceptos clave

Antes de continuar con el siguiente capítulo, asegúrate de comprender los siguientes conceptos.

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Seguimiento visual | Proceso mediante el cual un robot localiza continuamente un objeto en una secuencia de imágenes. |
| Error visual | Diferencia entre la posición del objeto y el centro de la imagen. |
| Centro de la imagen | Punto de referencia utilizado para calcular el error visual. |
| Zona de tolerancia | Área alrededor del centro de la imagen donde no es necesario corregir el movimiento del robot. |
| Control diferencial | Técnica utilizada por robots móviles en la que el movimiento se obtiene modificando la velocidad relativa de las ruedas. |
| Tiempo real | Capacidad de un sistema para reaccionar de forma inmediata a los cambios observados por la cámara. |
| Seguimiento de objetos | Aplicación que mantiene un objeto continuamente localizado durante su movimiento. |
| Seguimiento de líneas | Técnica utilizada para que un robot permanezca sobre una trayectoria marcada en el suelo. |
| Corrección de trayectoria | Ajuste continuo del movimiento del robot a partir del error visual. |
| Bucle de control | Secuencia repetitiva de captura, procesamiento, decisión y actuación. |
:::

---

# En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender el funcionamiento del seguimiento visual.
- ✅ Calcular el error entre el objeto y el centro de la imagen.
- ✅ Interpretar el significado del error horizontal y vertical.
- ✅ Controlar el movimiento del Pioneer P3DX utilizando la información de una cámara.
- ✅ Implementar el seguimiento de una pelota.
- ✅ Desarrollar un algoritmo básico de seguimiento de líneas.
- ✅ Construir un sistema completo de seguimiento visual en tiempo real.

A partir de este momento ya puedes desarrollar robots móviles que reaccionen automáticamente a la información obtenida mediante visión artificial.

---

# Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre detectar un objeto y realizar su seguimiento?
2. ¿Qué representa el error visual?
3. ¿Por qué se utiliza el centro de la imagen como referencia?
4. ¿Qué función desempeña la zona de tolerancia?
5. ¿Cómo influye el error horizontal en el movimiento del Pioneer P3DX?
6. ¿Qué ventajas ofrece un control continuo frente a una única corrección?
7. ¿Qué elementos forman el bucle completo de seguimiento visual?

Si puedes responder correctamente a todas estas preguntas, estás preparado para desarrollar aplicaciones completas de percepción robótica.

---

# Práctica guiada

::: practice
title: Robot con seguimiento visual en tiempo real

difficulty: Alta

time: 90 minutos

content:

Construye una escena formada por:

- un Pioneer P3DX;
- un Vision Sensor;
- una pelota roja;
- una línea negra sobre el suelo.

Desarrolla dos programas independientes.

**Programa 1**

- Detecta la pelota.
- Calcula el error visual.
- Mantén la pelota centrada modificando la velocidad de las ruedas.

**Programa 2**

- Detecta la línea.
- Calcula el desplazamiento respecto al centro de la imagen.
- Corrige continuamente la trayectoria del robot para seguir la línea.

Como ampliación, compara ambos programas e identifica qué partes del algoritmo son comunes y cuáles dependen del objeto detectado.
:::

---

# Reto

::: challenge
title: Robot explorador guiado por visión

content:

Diseña un sistema en el que el Pioneer P3DX deba localizar automáticamente una pelota roja situada en diferentes posiciones de la escena.

El robot deberá:

- detectar la pelota;
- orientar su cámara hacia ella;
- mantenerla centrada durante todo el recorrido;
- continuar el seguimiento aunque la pelota cambie de posición.

Como ampliación, añade una segunda pelota de distinto color y modifica el programa para que el robot siga únicamente la pelota roja.

Este reto reproduce el funcionamiento básico de numerosos robots móviles utilizados en inspección, vigilancia y seguimiento automático.
:::

---

# Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre dos y tres sesiones de 55 minutos.

**Objetivos**

- Comprender el funcionamiento del seguimiento visual.
- Relacionar la percepción visual con el movimiento del robot.
- Consolidar el uso conjunto de CoppeliaSim, Python y OpenCV.
- Introducir los fundamentos del control visual en tiempo real.

**Material necesario**

- Ordenador con CoppeliaSim instalado.
- Python.
- Biblioteca OpenCV (`opencv-python`).
- Escenas con un Pioneer P3DX, un Vision Sensor, una pelota roja y una línea negra.

**Consejos metodológicos**

Conviene comenzar utilizando escenas sencillas con un único objeto claramente diferenciable.

Posteriormente puede aumentarse progresivamente la dificultad incorporando movimientos más rápidos, varios objetos o cambios de iluminación.

Antes de comenzar el proyecto final de la Parte III, verifica que el alumnado comprende completamente el ciclo:

Captura → Detección → Error → Decisión → Movimiento → Nueva captura.

Este flujo constituye uno de los fundamentos de la robótica móvil basada en visión artificial.
:::

---

# Próximo capítulo

Durante los capítulos 12, 13, 14 y 15 hemos recorrido el camino completo desde la captura de imágenes hasta el control de un robot mediante visión artificial.

Ha llegado el momento de integrar todos esos conocimientos en un único proyecto.

En el siguiente capítulo desarrollarás un **sistema completo de percepción**, combinando un Vision Sensor, OpenCV, navegación autónoma y toma de decisiones para construir un robot capaz de interpretar su entorno y actuar en consecuencia.

Este proyecto servirá como cierre de la **Parte III: Percepción avanzada y visión artificial**, y constituirá el puente natural hacia la Parte IV, donde el robot utilizará esa percepción para manipular objetos mediante un brazo robótico industrial.
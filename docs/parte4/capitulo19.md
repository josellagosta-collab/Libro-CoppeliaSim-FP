::: chapter-cover
number: 19
title: Cinemática directa e inversa
time: 6 horas
level: ★★★★☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué es la cinemática de un robot industrial.
- Diferenciar la cinemática directa de la cinemática inversa.
- Entender la relación entre las articulaciones y el efector final.
- Conocer los sistemas de referencia utilizados por el UR3.
- Comprender el papel de los objetos **Tip** y **Target** en CoppeliaSim.
- Preparar el robot para realizar movimientos cartesianos.

:::

# Capítulo 19 · Cinemática directa e inversa

### Del movimiento de las articulaciones al movimiento del robot

En el capítulo anterior aprendimos a controlar individualmente las seis articulaciones del **Universal Robots UR3**.

Fuimos capaces de obtener los *handles*, establecer posiciones, leer el estado de cada eje y ejecutar movimientos coordinados.

Sin embargo, existe una forma mucho más intuitiva de programar un robot industrial.

Imagina que deseas recoger una pieza situada sobre una mesa.

¿Serías capaz de calcular manualmente el ángulo exacto que debe adoptar cada una de las seis articulaciones para que la pinza llegue exactamente hasta ella?

Probablemente no.

Y, de hecho, en la industria nadie programa un robot de esa forma.

Lo habitual consiste en indicar **dónde queremos que llegue la herramienta**, dejando que el propio robot calcule automáticamente la posición que debe adoptar cada una de sus articulaciones.

Ese proceso recibe el nombre de **cinemática**.

A lo largo de este capítulo aprenderemos cómo CoppeliaSim realiza estos cálculos utilizando el modelo del **UR3**, permitiéndonos trabajar de una forma mucho más sencilla y cercana a la programación empleada en aplicaciones industriales reales.

::: figure
image: ../assets/cap19/fig19_1.png
caption: Del control de las articulaciones al control del efector final del UR3.
:::

::: teacher
content:

Antes de introducir nuevos conceptos, recuerda al alumnado cómo se controlaban las articulaciones en el capítulo anterior.

Resulta muy útil plantear la siguiente pregunta:

"¿Qué sería más cómodo, indicar seis ángulos diferentes o simplemente decirle al robot dónde queremos colocar la pinza?"

Esta reflexión ayudará a comprender la necesidad de la cinemática.

:::

---

## 19.1 ¿Qué es la cinemática?

La **cinemática** es la rama de la robótica que estudia el movimiento de un robot sin tener en cuenta las fuerzas que lo producen.

Su objetivo consiste en describir la relación existente entre las articulaciones del robot y la posición que ocupa su herramienta en el espacio.

En un brazo robótico como el **UR3**, ambas cosas están completamente relacionadas.

Cada vez que una articulación gira, cambia la posición del efector final.

Del mismo modo, cada vez que deseamos situar la herramienta en un punto determinado, será necesario calcular la posición adecuada para todas las articulaciones.

Por tanto, la cinemática responde a dos preguntas fundamentales:

- ¿Dónde se encuentra la herramienta cuando conocemos la posición de todas las articulaciones?
- ¿Qué posición deben adoptar las articulaciones para que la herramienta llegue a un punto concreto?

Estas dos cuestiones dan lugar a dos problemas diferentes, conocidos como **cinemática directa** y **cinemática inversa**, que estudiaremos en los siguientes apartados.

::: figure
image: ../assets/cap19/fig19_2.png
caption: Relación entre las articulaciones del UR3 y la posición del efector final.
:::

---

### Un ejemplo cotidiano

Para comprender mejor este concepto, piensa en tu propio brazo.

Si mantienes la mano extendida frente a ti y comienzas a mover el hombro, el codo o la muñeca, observarás que la posición de la mano cambia continuamente.

No necesitas pensar en las coordenadas exactas de cada articulación.

Simplemente decides dónde quieres colocar la mano y tu cerebro coordina automáticamente todos los movimientos necesarios.

En cierto modo, un robot industrial realiza un proceso muy parecido.

La diferencia es que, en lugar de un cerebro, utiliza algoritmos matemáticos capaces de calcular la posición de cada articulación con una enorme precisión.

Durante este capítulo utilizaremos CoppeliaSim para visualizar estos cálculos sin necesidad de profundizar en formulaciones matemáticas complejas.

Nuestro objetivo será comprender **cómo trabaja el robot**, no memorizar ecuaciones.


---

## 19.2 Cinemática directa y cinemática inversa

En el apartado anterior vimos que la cinemática estudia la relación existente entre las articulaciones del robot y la posición de su efector final.

Sin embargo, esta relación puede plantearse de dos formas diferentes.

Dependiendo de cuál sea la información de partida, hablaremos de **cinemática directa** o de **cinemática inversa**.

Ambos conceptos constituyen la base del funcionamiento de cualquier robot industrial moderno.

---

### Cinemática directa

La **cinemática directa** responde a la siguiente pregunta:

> **Si conocemos la posición de todas las articulaciones del robot, ¿dónde se encuentra el efector final?**

En este caso conocemos el ángulo de cada uno de los seis ejes del UR3.

A partir de esa información, el robot calcula automáticamente la posición y la orientación de la herramienta.

Podemos representar este proceso de la siguiente forma:

```text
Articulaciones
(Joint1...Joint6)

        │
        ▼

 Cinemática directa

        │
        ▼

Efector final

(X, Y, Z, Rx, Ry, Rz)
```

Es decir, partimos de las articulaciones y obtenemos la posición de la herramienta.

::: figure
image: ../assets/cap19/fig19_3.png
caption: Funcionamiento de la cinemática directa en el UR3.
:::

---

### Cinemática inversa

La **cinemática inversa** plantea exactamente el problema contrario.

En este caso la pregunta es:

> **Si queremos colocar el efector final en un punto determinado, ¿qué posición deben adoptar las articulaciones?**

Ahora conocemos el destino de la herramienta.

Será el propio robot quien calcule automáticamente el ángulo que debe adoptar cada una de sus articulaciones para alcanzar ese punto.

El proceso puede representarse así:

```text
Efector final

(X, Y, Z, Rx, Ry, Rz)

        │
        ▼

 Cinemática inversa

        │
        ▼

Articulaciones

(Joint1...Joint6)
```

En robótica industrial esta es, con diferencia, la forma de trabajo más habitual.

El programador indica únicamente el punto de destino y el controlador del robot realiza todos los cálculos necesarios.

::: figure
image: ../assets/cap19/fig19_4.png
caption: Funcionamiento de la cinemática inversa en el UR3.
:::

---

## Comparando ambos métodos

Aunque ambos conceptos están estrechamente relacionados, su punto de partida es completamente diferente.

| Cinemática directa | Cinemática inversa |
|--------------------|--------------------|
| Se conocen las articulaciones. | Se conoce la posición del efector final. |
| Se calcula la posición de la herramienta. | Se calculan los ángulos de las articulaciones. |
| El movimiento parte de los ejes. | El movimiento parte del objetivo. |
| Muy utilizada para conocer el estado del robot. | Muy utilizada para programar movimientos industriales. |

Como puedes observar, ambos procesos son complementarios.

Uno permite saber **dónde está el robot** y el otro **cómo debe moverse para llegar a un destino**.

::: teacher
content:

No es necesario profundizar todavía en los algoritmos matemáticos que resuelven la cinemática inversa.

Lo importante es que el alumnado comprenda qué información conoce el robot en cada caso y cuál debe calcular.

Más adelante comprobarán que CoppeliaSim realiza automáticamente estos cálculos.

:::

---

### ¿Cuál utilizaremos en este libro?

Aunque conoceremos ambos conceptos, durante las prácticas trabajaremos principalmente con **cinemática inversa**.

En lugar de calcular manualmente los seis ángulos del UR3, indicaremos la posición que deseamos alcanzar y dejaremos que CoppeliaSim resuelva automáticamente el problema.

Este enfoque coincide con la forma de programar utilizada en la mayoría de los robots industriales actuales y permitirá desarrollar aplicaciones mucho más sencillas, claras y fáciles de mantener.

---

## 19.3 Los objetos *Tip* y *Target*

Hasta ahora hemos hablado de mover el efector final hasta una determinada posición.

Pero...

¿Cómo sabe CoppeliaSim cuál es la posición actual del robot?

¿Y cómo indicamos el punto al que queremos que se desplace?

La respuesta está en dos objetos muy importantes que incorpora el modelo del **UR3**:

- **Tip**
- **Target**

Estos dos elementos son la base del funcionamiento de la cinemática inversa dentro de CoppeliaSim.

---

### ¿Qué es el Tip?

El **Tip** representa la posición real del efector final.

Podemos imaginarlo como un pequeño punto invisible situado exactamente en el extremo de la herramienta del robot.

Cuando las articulaciones se mueven, el **Tip** también cambia de posición.

En todo momento indica dónde se encuentra realmente el efector final.

::: figure
image: ../assets/cap19/fig19_5.png
caption: El objeto **Tip** representa la posición real del efector final del UR3.
:::

---

### ¿Qué es el Target?

El **Target** representa el destino al que queremos desplazar el robot.

En lugar de mover directamente las articulaciones, moveremos este objeto dentro del espacio de trabajo.

La cinemática inversa calculará automáticamente los ángulos necesarios para que el **Tip** alcance el **Target**.

Desde el punto de vista del programador, el proceso resulta extremadamente sencillo.

Únicamente debemos indicar dónde queremos colocar el **Target**.

El resto del trabajo lo realizará CoppeliaSim.

::: figure
image: ../assets/cap19/fig19_6.png
caption: El objeto **Target** define el punto que debe alcanzar el efector final.
:::

---

## Trabajando juntos

Podemos entender ambos objetos mediante una analogía muy sencilla.

Imagina que paseas a tu perro utilizando una correa.

- Tú representas el **Target**.
- El perro representa el **Tip**.

Cada vez que cambias de posición, el perro intenta seguirte.

Del mismo modo, cuando desplazamos el **Target**, el robot mueve automáticamente todas sus articulaciones para que el **Tip** llegue hasta él.

Esta analogía ayuda a comprender por qué no necesitamos calcular manualmente los seis ángulos del UR3.

---

### Un movimiento completamente diferente

Observa la diferencia con el capítulo anterior.

Antes escribíamos programas como este:

```python
Joint1 = 30°
Joint2 = -45°
Joint3 = 60°
...
```

Ahora podremos pensar de una forma mucho más natural.

Nuestro objetivo será simplemente indicar:

```text
Mover el efector final a:

X = 350 mm
Y = -150 mm
Z = 250 mm
```

Será el propio controlador cinemático quien determine la posición que debe adoptar cada articulación.

::: teacher
content:

Insiste en que el alumnado no confunda el **Tip** con el **Target**.

El Tip indica la posición **real** del efector final.

El Target representa la posición **deseada**.

La misión de la cinemática inversa consiste precisamente en conseguir que ambos coincidan.

:::

---

## ¿Dónde aparecen en el árbol de la escena?

Si desplegamos el modelo del **UR3** en el árbol de la escena, observaremos que ambos objetos forman parte del robot.

Habitualmente aparecen próximos al efector final y constituyen el núcleo del mecanismo de cinemática inversa.

En los próximos apartados aprenderemos a acceder a ellos desde Python y a desplazarlos mediante programación para mover el robot sin necesidad de calcular manualmente las posiciones de sus articulaciones.

::: common-error
content:

No intentes mover simultáneamente las articulaciones y el **Target**.

Durante las prácticas de cinemática trabajaremos siempre desplazando el **Target**, dejando que CoppeliaSim calcule automáticamente el movimiento del resto del robot.

:::

---

## 19.4 Coordenadas cartesianas y sistemas de referencia

En el apartado anterior vimos que, utilizando la cinemática inversa, basta con indicar la posición del **Target** para que el robot calcule automáticamente el movimiento de sus articulaciones.

Pero...

¿Cómo describimos esa posición?

La respuesta es mediante un **sistema de coordenadas cartesianas**.

Gracias a él podemos indicar con precisión el lugar donde queremos situar el efector final del **UR3**.

---

### El sistema de coordenadas XYZ

CoppeliaSim utiliza un sistema de coordenadas tridimensional formado por tres ejes perpendiculares.

- **Eje X**: desplazamiento izquierda–derecha.
- **Eje Y**: desplazamiento hacia delante–hacia atrás.
- **Eje Z**: desplazamiento vertical.

Cada punto del espacio queda definido mediante tres valores:

- **X**
- **Y**
- **Z**

Por ejemplo:

```text
X = 350 mm
Y = -150 mm
Z = 250 mm
```

Estas coordenadas indican la posición exacta que deberá alcanzar el efector final.

::: figure
image: ../assets/cap19/fig19_7.png
caption: Sistema de coordenadas cartesianas utilizado por el UR3 en CoppeliaSim.
:::

---

### El origen de coordenadas

Todo sistema cartesiano necesita un punto de referencia.

Ese punto recibe el nombre de **origen**.

En el caso del UR3, normalmente el origen coincide con la base del robot.

Todas las posiciones del efector final se calculan tomando este punto como referencia.

Si desplazamos el robot dentro de la escena, también cambiará la posición relativa de su sistema de coordenadas.

Por este motivo resulta tan importante comprender desde qué referencia estamos trabajando.

---

## Posición y orientación

Hasta ahora únicamente hemos hablado de la posición del efector final.

Sin embargo, una herramienta no solo debe llegar a un punto determinado.

También debe hacerlo con la orientación adecuada.

Por ejemplo, una pinza puede necesitar aproximarse a una pieza:

- desde arriba;
- desde un lateral;
- con una determinada inclinación.

Por este motivo, la posición completa del efector final queda definida mediante seis valores.

| Parámetro | Significado |
|-----------|-------------|
| X | Posición horizontal |
| Y | Posición longitudinal |
| Z | Altura |
| Rx | Giro alrededor del eje X |
| Ry | Giro alrededor del eje Y |
| Rz | Giro alrededor del eje Z |

Los tres primeros describen la **posición**.

Los tres últimos describen la **orientación**.

::: figure
image: ../assets/cap19/fig19_8.png
caption: Posición (X, Y, Z) y orientación (Rx, Ry, Rz) del efector final del UR3.
:::

---

### ¿Por qué es importante la orientación?

Imagina que deseas introducir un tornillo en un orificio.

Aunque el robot llegue exactamente al punto correcto, la operación fracasará si el destornillador está inclinado.

Lo mismo ocurre al insertar una pieza en un alojamiento o al recoger un objeto con una ventosa.

La orientación resulta tan importante como la posición.

Por este motivo, los robots industriales siempre calculan ambos aspectos de forma simultánea.

::: teacher
content:

Durante las primeras prácticas conviene trabajar únicamente con cambios de posición, manteniendo fija la orientación del efector final.

Una vez que el alumnado domine los movimientos cartesianos, podrá comenzar a experimentar con los giros alrededor de los ejes X, Y y Z.

:::

---

## Visualizando los ejes en CoppeliaSim

Cuando seleccionamos el **Tip** o el **Target**, CoppeliaSim muestra un pequeño sistema de ejes de colores.

Cada color identifica uno de los ejes cartesianos:

- **Rojo** → eje X.
- **Verde** → eje Y.
- **Azul** → eje Z.

Estos indicadores permiten comprender rápidamente cómo está orientada la herramienta y facilitan enormemente la programación de movimientos precisos.

En el próximo apartado aprenderemos a modificar estas coordenadas desde Python para mover el **Target** y comprobar cómo el UR3 calcula automáticamente la posición de todas sus articulaciones.

---

## 19.5 Moviendo el *Target* desde Python

Ya conocemos los objetos **Tip** y **Target**.

También sabemos que la cinemática inversa intentará hacer coincidir ambos automáticamente.

Ha llegado el momento de comprobarlo mediante un programa en Python.

A partir de este apartado dejaremos de indicar el ángulo de cada articulación y comenzaremos a trabajar directamente con la posición del **Target**.

Este será el método que utilizaremos durante el resto de la Parte IV.

---

### Obteniendo el *handle* del Target

Al igual que cualquier otro objeto de CoppeliaSim, el **Target** posee su propio *handle*.

Podemos obtenerlo utilizando la función `sim.getObject()`.

```python
target = sim.getObject('/UR3/Target')
```

Una vez obtenido el identificador, podremos consultar o modificar su posición desde Python.

::: figure
image: ../assets/cap19/fig19_9.png
caption: Obtención del *handle* del objeto **Target** para controlar el movimiento cartesiano del UR3.
:::

---

## Leyendo la posición del Target

La función `sim.getObjectPosition()` permite conocer la posición actual de un objeto respecto a un sistema de referencia.

```python
posicion = sim.getObjectPosition(target, -1)

print(posicion)
```

La variable `posicion` contendrá una lista con tres valores:

```text
[X, Y, Z]
```

Estos valores representan las coordenadas cartesianas del **Target**.

Durante las prácticas utilizaremos con frecuencia esta función para comprobar la posición del robot antes y después de un movimiento.

---

## Modificando la posición

Para desplazar el **Target** utilizaremos la función `sim.setObjectPosition()`.

```python
sim.setObjectPosition(
    target,
    -1,
    [0.35, -0.15, 0.25]
)
```

En este ejemplo estamos indicando que el **Target** debe situarse en:

- X = 0,35 m
- Y = –0,15 m
- Z = 0,25 m

Observa que CoppeliaSim trabaja con **metros**, no con milímetros.

Al ejecutar el programa, el robot calculará automáticamente la posición necesaria para que el **Tip** alcance ese nuevo destino.

::: figure
image: ../assets/cap19/fig19_10.png
caption: Movimiento del objeto **Target** y respuesta automática del UR3 mediante cinemática inversa.
:::

---

### ¿Qué ocurre internamente?

Aunque nuestro programa únicamente modifica las coordenadas del **Target**, CoppeliaSim realiza internamente una gran cantidad de cálculos.

De forma simplificada, el proceso es el siguiente:

1. Python modifica la posición del **Target**.
2. El solucionador de cinemática inversa calcula una nueva configuración articular.
3. Las seis articulaciones del UR3 comienzan a moverse.
4. El **Tip** alcanza finalmente la posición del **Target**.

Todo este proceso sucede de forma automática y transparente para el programador.

---

### Ventajas de este enfoque

Trabajar desplazando el **Target** presenta numerosas ventajas frente al control directo de las articulaciones.

- El código resulta mucho más sencillo.
- No es necesario calcular ángulos manualmente.
- Los movimientos son más naturales.
- Es más fácil reutilizar programas.
- Se aproxima al modo de programación utilizado en robots industriales reales.

Por este motivo, la mayoría de las aplicaciones que desarrollaremos en los próximos capítulos utilizarán este método de trabajo.

::: teacher
content:

Anima al alumnado a mover el **Target** manualmente desde la escena antes de ejecutar el programa.

Observar cómo el UR3 sigue el movimiento en tiempo real ayuda a comprender el funcionamiento de la cinemática inversa y facilita la transición hacia la programación mediante coordenadas cartesianas.

:::

---

### Preparando el siguiente capítulo

Ya somos capaces de mover el efector final indicando únicamente el punto que debe alcanzar.

En el próximo capítulo aprovecharemos esta capacidad para desarrollar las primeras operaciones de manipulación.

El UR3 aprenderá a aproximarse a una pieza, recogerla mediante una pinza y depositarla en otra posición, construyendo nuestras primeras secuencias de **pick & place**.

---

## 19.6 Programando trayectorias cartesianas

Hasta ahora hemos desplazado el **Target** hasta una única posición.

Sin embargo, en una aplicación industrial el robot rara vez realiza un único movimiento.

Lo habitual es que deba desplazarse sucesivamente entre diferentes puntos del espacio para recoger piezas, inspeccionarlas, ensamblarlas o depositarlas en otro lugar.

A esta sucesión de posiciones la denominaremos **trayectoria cartesiana**.

---

### Definiendo varios puntos

Una forma sencilla de programar una trayectoria consiste en almacenar las posiciones del **Target** en una lista.

Cada elemento contendrá las coordenadas cartesianas de un punto.

```python
trayectoria = [
    [0.35, -0.15, 0.25],
    [0.40, -0.10, 0.22],
    [0.45, -0.05, 0.20],
    [0.40,  0.00, 0.25]
]
```

Cada posición representa un punto que deberá alcanzar el efector final del UR3.

::: figure
image: ../assets/cap19/fig19_11.png
caption: Trayectoria cartesiana formada por varios puntos objetivo para el efector final del UR3.
:::

---

## Recorriendo la trayectoria

Una vez definida la lista de puntos, podemos recorrerla mediante un bucle.

```python
import time

for punto in trayectoria:
    sim.setObjectPosition(target, -1, punto)
    time.sleep(2)
```

Cada dos segundos el **Target** se desplazará al siguiente punto.

El solucionador de cinemática inversa calculará automáticamente la nueva configuración de las seis articulaciones.

Desde el punto de vista del programador, únicamente estamos modificando las coordenadas cartesianas.

---

### Trayectorias suaves

En aplicaciones reales no se trabaja con movimientos bruscos entre puntos aislados.

Los controladores industriales generan trayectorias continuas para conseguir desplazamientos suaves, precisos y seguros.

Aunque CoppeliaSim simplifica gran parte de este proceso, es importante comprender que el robot no "salta" entre posiciones.

El movimiento se realiza siguiendo una trayectoria continua calculada por el controlador.

::: teacher
content:

Puedes demostrar este comportamiento desplazando lentamente el **Target** con el ratón mientras la simulación está en marcha.

El alumnado observará cómo todas las articulaciones del UR3 se coordinan automáticamente para seguir el movimiento.

:::

---

## Un ejemplo de aplicación industrial

Imagina una estación de inspección de calidad.

El UR3 debe situar una cámara sobre cuatro zonas diferentes de una pieza.

Cada una de esas posiciones puede almacenarse como un punto de una trayectoria.

El programa únicamente recorrerá la lista de coordenadas.

No será necesario calcular en ningún momento el ángulo de las articulaciones.

Este enfoque simplifica enormemente el desarrollo de aplicaciones industriales.

::: figure
image: ../assets/cap19/fig19_12.png
caption: Recorrido del UR3 siguiendo una trayectoria cartesiana para inspeccionar distintos puntos de una pieza.
:::

---

### Preparados para manipular objetos

Con todo lo aprendido en este capítulo ya somos capaces de:

- comprender la cinemática directa e inversa;
- trabajar con sistemas de referencia;
- utilizar los objetos **Tip** y **Target**;
- mover el efector final mediante coordenadas cartesianas;
- programar trayectorias entre varios puntos.

En el próximo capítulo utilizaremos estas técnicas para realizar una de las tareas más habituales de un robot industrial: **recoger una pieza, transportarla y depositarla en otra posición**.

Será el inicio de nuestras primeras aplicaciones completas de manipulación con el **UR3**.

---

## 19.7 Práctica guiada: Moviendo el efector final mediante cinemática inversa

En esta práctica aplicarás todos los conceptos aprendidos durante el capítulo para controlar el **efector final del UR3** utilizando coordenadas cartesianas.

El objetivo consiste en comprobar cómo CoppeliaSim calcula automáticamente el movimiento de las seis articulaciones mediante cinemática inversa.

::: practice
title: Primeros movimientos cartesianos del UR3

difficulty: Media

time: 60 minutos

content:

Realiza las siguientes actividades:

1. Abre la escena del UR3 utilizada durante este capítulo.
2. Ejecuta la simulación.
3. Localiza los objetos **Tip** y **Target** en el árbol de la escena.
4. Mueve manualmente el **Target** utilizando el manipulador de traslación.
5. Observa cómo el UR3 adapta automáticamente la posición de todas sus articulaciones.
6. Obtén el *handle* del **Target** desde Python.
7. Lee sus coordenadas cartesianas mediante `sim.getObjectPosition()`.
8. Modifica la posición del **Target** desde Python utilizando `sim.setObjectPosition()`.
9. Programa una trayectoria formada por cuatro puntos diferentes.
10. Comprueba que el efector final sigue correctamente la trayectoria definida.

Al finalizar la práctica deberás ser capaz de mover el efector final del UR3 sin calcular manualmente los ángulos de sus articulaciones.

:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Cinemática | Relación entre las articulaciones del robot y la posición del efector final. |
| Cinemática directa | Calcula la posición del efector final a partir de las articulaciones. |
| Cinemática inversa | Calcula las articulaciones necesarias para alcanzar una posición determinada. |
| Efector final | Herramienta situada en el extremo del brazo robótico. |
| Tip | Objeto que representa la posición real del efector final. |
| Target | Objeto que define la posición objetivo del efector final. |
| Coordenadas cartesianas | Sistema formado por los ejes X, Y y Z utilizado para definir posiciones. |
| Orientación | Rotación del efector final respecto a los ejes X, Y y Z. |
| Trayectoria cartesiana | Sucesión ordenada de posiciones que debe recorrer el efector final. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Comprender qué es la cinemática aplicada a un robot industrial.
- ✅ Diferenciar la cinemática directa de la cinemática inversa.
- ✅ Interpretar los sistemas de coordenadas utilizados por el UR3.
- ✅ Comprender la función de los objetos **Tip** y **Target**.
- ✅ Leer y modificar posiciones cartesianas desde Python.
- ✅ Mover el efector final sin calcular manualmente los ángulos de las articulaciones.
- ✅ Programar trayectorias cartesianas sencillas.

A partir de este momento ya puedes controlar el **UR3** utilizando el mismo enfoque empleado en la mayoría de las aplicaciones industriales actuales.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre la cinemática directa y la cinemática inversa?
2. ¿Qué representa el objeto **Tip**?
3. ¿Cuál es la función del objeto **Target**?
4. ¿Qué información contienen las coordenadas X, Y y Z?
5. ¿Por qué resulta más sencillo programar el **Target** que las seis articulaciones?
6. ¿Qué diferencia existe entre posición y orientación?
7. ¿Qué ventajas ofrece trabajar mediante trayectorias cartesianas?

Si puedes responder correctamente a todas ellas, estás preparado para comenzar a manipular objetos mediante el UR3.

---

## Reto

::: challenge
title: Diseñando una trayectoria de inspección

content:

Programa una trayectoria formada por cinco posiciones cartesianas diferentes.

El efector final deberá:

- desplazarse desde una posición inicial;
- recorrer los cinco puntos definidos;
- regresar finalmente al punto de partida.

Como ampliación, modifica únicamente la coordenada **Z** para comprobar cómo cambia la altura del efector final manteniendo constantes las coordenadas **X** e **Y**.

Observa cuidadosamente cómo la cinemática inversa adapta automáticamente la posición de todas las articulaciones.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Comprender el funcionamiento de la cinemática inversa.
- Familiarizar al alumnado con los objetos **Tip** y **Target**.
- Introducir la programación mediante coordenadas cartesianas.
- Preparar las primeras aplicaciones de manipulación industrial.

**Material necesario**

- Ordenadores con CoppeliaSim y Python configurados.
- Escena del UR3 utilizada durante la Parte IV.
- Proyector para realizar demostraciones.

**Consejos metodológicos**

Antes de programar desde Python, permite que el alumnado desplace el **Target** manualmente.

La respuesta inmediata del robot facilita enormemente la comprensión del funcionamiento de la cinemática inversa y ayuda a establecer una relación directa entre las coordenadas cartesianas y el movimiento del efector final.

:::

---

## Próximo capítulo

Hasta ahora el **UR3** únicamente ha aprendido a desplazarse por el espacio.

En el siguiente capítulo comenzará a realizar tareas útiles.

Aprenderás a controlar una pinza, aproximarte correctamente a una pieza, recogerla, transportarla y depositarla en una nueva posición, desarrollando las primeras operaciones de **pick & place**.

Este será el primer capítulo completamente orientado a aplicaciones industriales y supondrá el paso definitivo desde el control del robot hacia la **manipulación automática de objetos**.
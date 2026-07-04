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
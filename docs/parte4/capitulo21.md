::: chapter-cover
number: 21
title: Proyecto industrial completo con el UR3
time: 8 horas
level: ★★★★★ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Diseñar una célula robotizada utilizando CoppeliaSim.
- Integrar un UR3 con sensores y una cinta transportadora.
- Coordinar el movimiento del robot con la llegada de piezas.
- Desarrollar un ciclo automático completo de manipulación.
- Organizar una aplicación industrial mediante programación modular en Python.
- Comprender la estructura general de una célula robotizada similar a las utilizadas en la industria.

:::

# Capítulo 21 · Proyecto industrial completo con el UR3

## Del robot aislado a la célula robotizada

En el capítulo anterior aprendimos a controlar el **UR3** para realizar operaciones de **pick & place**.

El robot era capaz de recoger una pieza, transportarla y depositarla en otra posición.

Sin embargo, en una fábrica real el robot rara vez trabaja de forma aislada.

Habitualmente forma parte de una instalación mucho más amplia en la que intervienen otros elementos, como cintas transportadoras, sensores, cámaras de visión artificial y sistemas de control.

Todos estos dispositivos colaboran para realizar un proceso automático de forma coordinada.

En este capítulo construiremos una célula robotizada inspirada en una instalación industrial real, integrando el **UR3** con otros componentes para desarrollar un proceso completo de manipulación.

::: figure
image: ../assets/cap21/fig21_1.png
caption: Célula robotizada formada por un UR3, una cinta transportadora y un puesto de depósito.
:::

::: teacher
content:

Antes de comenzar el proyecto, muestra al alumnado fotografías o vídeos de células robotizadas reales.

El objetivo es que identifiquen los distintos elementos que las componen y comprendan que el robot constituye únicamente una parte del sistema de automatización.

:::

---

## 21.1 Arquitectura de la célula robotizada

La aplicación que desarrollaremos durante este capítulo estará formada por cuatro elementos principales.

- Un **UR3**, encargado de manipular las piezas.
- Una **cinta transportadora**, que suministrará los objetos.
- Un **sensor de presencia**, que detectará la llegada de cada pieza.
- Una **zona de depósito**, donde el robot dejará los objetos una vez manipulados.

Aunque se trata de una célula simplificada, reproduce la estructura utilizada en numerosas aplicaciones industriales de clasificación, empaquetado y alimentación de máquinas.

::: figure
image: ../assets/cap21/fig21_2.png
caption: Componentes principales de la célula robotizada desarrollada en este capítulo.
:::

---

### El flujo de trabajo

La secuencia general de funcionamiento será la siguiente:

1. La cinta transportadora desplaza una pieza hasta la zona de trabajo.
2. El sensor detecta la presencia del objeto.
3. El UR3 espera la confirmación del sensor.
4. El robot recoge la pieza mediante la pinza.
5. La transporta hasta la zona de depósito.
6. El ciclo vuelve a comenzar con la siguiente pieza.

Este comportamiento reproduce el funcionamiento de muchas células robotizadas utilizadas en procesos de producción automatizados.

---

### Un proyecto integrador

Este capítulo no introduce únicamente nuevos componentes.

Su principal objetivo consiste en integrar todos los conocimientos adquiridos durante la Parte IV.

A lo largo del proyecto utilizaremos:

- control de articulaciones;
- cinemática inversa;
- coordenadas cartesianas;
- objetos **Tip** y **Target**;
- control de la pinza;
- trayectorias seguras;
- programación modular;
- ciclos automáticos.

Al finalizar el capítulo habrás construido una aplicación muy próxima a las que pueden encontrarse en un entorno industrial real.

::: common-error
content:

Antes de comenzar a programar, asegúrate de que todos los elementos de la célula están correctamente posicionados.

Una mala ubicación de la cinta transportadora o de la zona de depósito puede impedir que el UR3 alcance las piezas o provocar colisiones durante la manipulación.

:::
# Parte IV. Robótica industrial y manipulación

En las partes anteriores aprendimos a utilizar CoppeliaSim, a controlar robots móviles y a dotarlos de percepción mediante sensores y visión artificial.

Ha llegado el momento de dar un paso más y adentrarnos en uno de los campos más importantes de la automatización moderna: **la robótica industrial**.

En esta parte trabajaremos con el robot colaborativo **Universal Robots UR3**, uno de los brazos robóticos más utilizados en entornos educativos e industriales. Aprenderemos cómo está construido, cómo controlar sus articulaciones, cómo mover su efector final mediante coordenadas cartesianas y cómo programar operaciones de manipulación utilizando Python.

A medida que avancemos, integraremos pinzas, sensores, cintas transportadoras y sistemas de visión artificial para construir una célula robotizada inspirada en aplicaciones reales de automatización industrial.

El objetivo no será únicamente mover un robot, sino comprender cómo se coordinan todos los elementos de una instalación automática para resolver problemas similares a los que pueden encontrarse en fábricas, centros logísticos y sistemas de producción actuales.

::: part-cover
number: IV
title: Robótica industrial y manipulación
subtitle: Brazos robóticos, cinemática y automatización con CoppeliaSim y Python
:::

---

## Capítulos de esta parte

### Capítulo 17. Introducción a la robótica industrial

Primer contacto con el robot **UR3** y con los conceptos fundamentales de la robótica industrial.

Aprenderás qué es un robot industrial, cuáles son sus principales aplicaciones, cómo está estructurado un brazo robótico y cómo cargarlo y explorar sus componentes dentro de CoppeliaSim.

---

### Capítulo 18. Control de articulaciones

Comenzaremos a programar el UR3 desde Python.

Obtendremos los *handles* de sus articulaciones, aprenderemos a mover cada eje de forma independiente, controlar velocidades y sincronizar movimientos para realizar los primeros programas sobre un robot industrial.

---

### Capítulo 19. Cinemática directa e inversa

Uno de los capítulos más importantes del libro.

Descubrirás cómo mover el efector final mediante coordenadas cartesianas utilizando los objetos **Target** y **Tip**, comprendiendo de forma intuitiva los principios de la cinemática directa e inversa sin necesidad de recurrir a desarrollos matemáticos complejos.

---

### Capítulo 20. Manipulación de objetos

El UR3 comenzará a realizar tareas propias de una aplicación industrial.

Aprenderás a controlar una pinza paralela, desarrollar operaciones de **Pick & Place**, programar trayectorias seguras y construir ciclos automáticos de manipulación utilizando Python.

---

### Capítulo 21. Proyecto industrial completo

Como cierre de la parte desarrollarás una célula robotizada completa inspirada en una instalación industrial real.

Integrarás un **UR3**, una cinta transportadora, sensores de presencia, una cámara de visión artificial y una pinza para crear un sistema capaz de detectar, clasificar y manipular piezas de forma completamente automática.

Este proyecto reunirá todos los conocimientos adquiridos durante la Parte IV y servirá como puente hacia la integración de sistemas robóticos que abordaremos en la siguiente parte del libro.

---

## Lo que aprenderás

Al finalizar esta parte serás capaz de:

- Comprender la estructura y el funcionamiento de un robot industrial.
- Programar el robot colaborativo **UR3** utilizando Python.
- Controlar articulaciones y movimientos cartesianos.
- Aplicar los conceptos fundamentales de la cinemática.
- Desarrollar operaciones completas de **Pick & Place**.
- Coordinar robots con pinzas, sensores y cintas transportadoras.
- Integrar visión artificial en aplicaciones de manipulación.
- Diseñar y programar una célula robotizada inspirada en una instalación industrial real.

---

La robótica industrial constituye uno de los pilares de la automatización moderna.

Los conocimientos adquiridos en esta parte te permitirán comprender cómo trabajan los robots utilizados actualmente en la industria y te prepararán para el siguiente paso: **la integración con sistemas externos, protocolos industriales y tecnologías de la Industria 4.0**, que estudiaremos en la **Parte V**.
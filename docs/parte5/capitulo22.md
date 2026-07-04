::: chapter-cover
number: 22
title: Comunicación entre CoppeliaSim y aplicaciones externas
time: 4 horas
level: ⭐⭐⭐☆☆ (Intermedio)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender cómo se comunica CoppeliaSim con aplicaciones externas.
- Diferenciar una arquitectura cliente-servidor de una aplicación monolítica.
- Entender el funcionamiento de la API remota de CoppeliaSim.
- Identificar el flujo de intercambio de información entre Python y el simulador.
- Preparar el entorno para desarrollar aplicaciones distribuidas.
:::

# Capítulo 22 · Comunicación entre CoppeliaSim y aplicaciones externas

## ¿Por qué comunicar CoppeliaSim con otros programas?

Hasta ahora hemos trabajado con CoppeliaSim como una aplicación prácticamente autónoma.

Hemos creado escenas, añadido robots, programado comportamientos y utilizado sensores y cámaras para resolver diferentes problemas de robótica.

Sin embargo, en un entorno industrial real un robot nunca trabaja de forma aislada.

Forma parte de un sistema mucho más amplio donde intercambia información continuamente con otros dispositivos y aplicaciones.

Por ejemplo, un robot puede recibir órdenes desde un sistema de planificación, enviar el estado de una operación a una base de datos, consultar un PLC para conocer el estado de una máquina o transmitir imágenes a un servidor encargado de realizar visión artificial.

En otras palabras, el robot es únicamente uno de los elementos que forman parte de una arquitectura distribuida.

Precisamente esa será la finalidad de esta parte del libro.

Aprenderemos a integrar CoppeliaSim dentro de aplicaciones reales utilizando Python como lenguaje de comunicación.

Comenzaremos intercambiando información con programas sencillos y, progresivamente, construiremos sistemas similares a los utilizados actualmente en la Industria 4.0.

::: teacher
content:

Antes de comenzar con la programación conviene insistir en que, a partir de este capítulo, CoppeliaSim dejará de ser una aplicación independiente para convertirse en un componente más de un sistema distribuido.

Este cambio de perspectiva ayuda al alumnado a comprender mejor la arquitectura utilizada en la automatización industrial moderna.
:::

---

## 22.1 ¿Qué significa comunicar dos aplicaciones?

Cuando hablamos de comunicación entre aplicaciones nos referimos al proceso mediante el cual dos programas diferentes intercambian información para colaborar en la resolución de una tarea.

Cada aplicación ejecuta una parte del trabajo y comparte únicamente los datos necesarios.

Este enfoque presenta numerosas ventajas.

Permite distribuir el procesamiento entre distintos equipos, reutilizar aplicaciones ya desarrolladas y facilitar el mantenimiento del sistema.

En nuestro caso tendremos dos protagonistas principales:

- **CoppeliaSim**, encargado de simular el robot y su entorno.
- **Python**, encargado de ejecutar la lógica de control.

Ambos programas podrán ejecutarse en el mismo ordenador o en equipos diferentes conectados mediante una red.

La forma en que intercambian información será prácticamente la misma.

La siguiente figura representa esta arquitectura básica.

::: figure
image: ../assets/cap22/fig22_1.png
caption: Arquitectura básica de comunicación entre una aplicación Python y CoppeliaSim.
:::

Observa que ninguno de los dos programas controla directamente al otro.

Ambos permanecen en ejecución y se comunican mediante mensajes.

Esta filosofía será la base de todos los capítulos de esta parte del libro.

---

### Una analogía sencilla

Podemos imaginar esta comunicación como una conversación telefónica entre dos personas.

Cada una realiza una función distinta.

Una persona hace preguntas.

La otra responde.

Del mismo modo, un programa Python puede solicitar información sobre la posición de un robot y CoppeliaSim responder con las coordenadas correspondientes.

Posteriormente Python puede calcular una nueva trayectoria y enviar otra orden al simulador para mover el robot.

Durante toda la ejecución ambos programas permanecen intercambiando mensajes de forma continua.

Este mecanismo resulta mucho más flexible que integrar toda la lógica dentro de una única aplicación.

::: common-error
content:

Es habitual pensar que Python "controla" completamente CoppeliaSim.

En realidad ambos programas son independientes.

Python únicamente envía solicitudes y procesa las respuestas que recibe del simulador.
:::
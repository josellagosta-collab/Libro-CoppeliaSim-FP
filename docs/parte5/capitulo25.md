::: chapter-cover
number: 25
title: Gemelo digital e Industria 4.0
time: 6 horas
level: ⭐⭐⭐⭐☆ (Avanzado)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Comprender qué es un gemelo digital y cuáles son sus aplicaciones.
- Diferenciar un modelo de simulación de un gemelo digital.
- Comprender cómo sincronizar un sistema físico con CoppeliaSim.
- Identificar los principales componentes de una arquitectura Industria 4.0.
- Preparar el entorno para desarrollar aplicaciones conectadas en tiempo real.

:::

# Capítulo 25 · Gemelo digital e Industria 4.0

## ¿Qué es un gemelo digital?

Durante los capítulos anteriores hemos aprendido a crear simulaciones utilizando CoppeliaSim, controlar robots mediante Python, comunicarnos con aplicaciones externas, integrar ROS 2 y utilizar protocolos industriales como OPC UA.

Sin embargo, todas esas aplicaciones compartían una característica común.

La simulación funcionaba de forma independiente.

En una fábrica moderna esto rara vez ocurre.

Lo habitual es que exista una comunicación continua entre la instalación física y su representación virtual.

A esta representación virtual sincronizada se la conoce como **gemelo digital** (*Digital Twin*).

Un gemelo digital no es únicamente un modelo tridimensional.

Es una copia virtual de un sistema físico que recibe información en tiempo real y reproduce su comportamiento de forma sincronizada.

Gracias a ello es posible supervisar procesos, detectar incidencias, analizar el rendimiento de una instalación e incluso probar modificaciones antes de aplicarlas sobre el sistema real.

La siguiente figura muestra la idea general de un gemelo digital.

::: figure
image: ../assets/cap25/fig25_1.png
caption: Relación entre un sistema físico y su gemelo digital en CoppeliaSim.
:::

---

## ¿Por qué utilizar un gemelo digital?

La utilización de gemelos digitales aporta numerosas ventajas tanto durante el diseño de una instalación como durante su funcionamiento.

Entre las más importantes destacan:

- supervisar el estado de una instalación en tiempo real;
- detectar anomalías antes de que provoquen averías;
- optimizar tiempos de producción;
- analizar datos históricos;
- probar nuevas estrategias sin detener la producción;
- formar a operarios en un entorno completamente seguro.

Estas ventajas explican por qué los gemelos digitales se han convertido en una de las tecnologías más importantes de la Industria 4.0.

::: teacher
content:

Muchos alumnos identifican un gemelo digital con una simulación en 3D.

Es importante insistir desde el principio en que una simulación solo se convierte en un gemelo digital cuando existe una sincronización continua con el sistema físico.

Sin intercambio de información en tiempo real no existe un verdadero gemelo digital.

:::

---

## 25.1 De la simulación al gemelo digital

Podemos entender la evolución de un sistema robótico mediante cuatro niveles de complejidad.

**Nivel 1. Modelo virtual**

Representa únicamente la geometría de la instalación.

No existe ningún tipo de comunicación con el exterior.

**Nivel 2. Simulación**

El modelo incorpora motores, sensores, físicas y programas que permiten reproducir el comportamiento del sistema.

**Nivel 3. Sistema conectado**

La simulación comienza a intercambiar información con aplicaciones externas mediante protocolos como OPC UA, MQTT o ROS 2.

**Nivel 4. Gemelo digital**

La representación virtual permanece sincronizada continuamente con la instalación física.

Los cambios producidos en cualquiera de los dos sistemas pueden reflejarse automáticamente en el otro.

La siguiente figura resume esta evolución.

::: figure
image: ../assets/cap25/fig25_2.png
caption: Evolución desde un modelo virtual hasta un gemelo digital completamente sincronizado.
:::

Observa que un gemelo digital no sustituye a la instalación física.

Ambos sistemas trabajan conjuntamente, compartiendo información y complementándose para mejorar el rendimiento, la supervisión y la toma de decisiones.

::: common-error
content:

Es frecuente utilizar indistintamente los términos **simulación** y **gemelo digital**.

Aunque ambos conceptos están relacionados, no significan lo mismo.

Una simulación puede funcionar completamente desconectada del mundo real.

Un gemelo digital necesita intercambiar información continuamente con la instalación física para mantenerse actualizado.

:::

## 25.2 Arquitectura de un gemelo digital

Un gemelo digital no es una única aplicación.

En realidad, está formado por varios sistemas que colaboran intercambiando información de forma continua.

Cada uno de ellos desempeña una función concreta dentro de la instalación.

Los componentes más habituales son:

- el sistema físico;
- los sensores y actuadores;
- el PLC;
- la red industrial;
- CoppeliaSim;
- aplicaciones desarrolladas en Python;
- una base de datos;
- un panel de supervisión (*dashboard*).

La siguiente figura muestra una arquitectura simplificada de un gemelo digital industrial.

::: figure
image: ../assets/cap25/fig25_3.png
caption: Arquitectura básica de un sistema basado en gemelo digital.
:::

Aunque pueda parecer un sistema complejo, cada elemento realiza una tarea muy concreta.

La comunicación entre todos ellos permite mantener sincronizada la representación virtual con la instalación real.

---

### El sistema físico

El sistema físico constituye el origen de toda la información.

Puede tratarse de:

- una célula robotizada;
- una línea de producción;
- una máquina automática;
- un almacén inteligente;
- un sistema logístico.

En nuestro caso utilizaremos como ejemplo una célula formada por:

- un robot **UR3**;
- una cinta transportadora;
- una cámara industrial;
- un PLC Omron NX102;
- diferentes sensores.

Todos estos dispositivos generan continuamente información sobre el estado del proceso.

---

### El PLC

El PLC continúa siendo el cerebro de la instalación.

Su función consiste en:

- controlar la secuencia automática;
- leer sensores;
- activar actuadores;
- supervisar el funcionamiento del proceso;
- intercambiar información con otros sistemas.

Actualmente los PLC ya no trabajan de forma aislada.

Es habitual que compartan información con aplicaciones desarrolladas en Python, sistemas SCADA, bases de datos y gemelos digitales.

---

### CoppeliaSim

En nuestro sistema, CoppeliaSim actuará como representación virtual de la instalación.

La simulación reproducirá:

- el robot UR3;
- la cinta transportadora;
- las piezas;
- los sensores;
- los movimientos del proceso.

Cada vez que cambie el estado del sistema físico, el gemelo digital actualizará automáticamente su comportamiento.

Del mismo modo, determinadas acciones realizadas sobre la simulación podrán enviarse nuevamente al sistema físico.

Este intercambio bidireccional constituye la esencia de un gemelo digital.

::: teacher
content:

Muchos estudiantes piensan que el simulador sustituye al sistema físico.

Es importante explicar que ambos funcionan simultáneamente y se complementan.

La instalación continúa realizando el trabajo real mientras el gemelo digital supervisa, analiza y ayuda a tomar decisiones.
:::

---

## 25.3 Flujo de información

Una vez conocida la arquitectura general, resulta interesante analizar cómo circula la información.

Podemos dividir el proceso en cinco etapas.

1. Los sensores detectan el estado del sistema.
2. El PLC procesa la información recibida.
3. Los datos se envían al gemelo digital mediante OPC UA u otro protocolo industrial.
4. Python procesa la información y actualiza la simulación.
5. El dashboard muestra el estado del sistema al usuario.

La siguiente figura resume este flujo.

::: figure
image: ../assets/cap25/fig25_4.png
caption: Flujo de información entre el sistema físico y el gemelo digital.
:::

Observa que los datos pueden circular en ambos sentidos.

Por ejemplo, una modificación realizada desde una aplicación de supervisión puede enviarse al PLC, actualizar la simulación y modificar posteriormente el comportamiento de la instalación física.

---

### Información en tiempo real

Para que un gemelo digital resulte útil, la información debe actualizarse continuamente.

Algunos ejemplos son:

- posición del robot;
- velocidad de la cinta transportadora;
- número de piezas procesadas;
- estado de los sensores;
- alarmas activas;
- consumo energético;
- tiempo de ciclo.

Toda esta información permite conocer el estado exacto de la instalación en cada instante.

Gracias a ello es posible detectar incidencias mucho antes de que provoquen una parada de producción.

::: common-error
content:

No toda la información necesita actualizarse cientos de veces por segundo.

Cada variable debe transmitirse con la frecuencia adecuada.

Actualizar datos innecesariamente aumenta el tráfico de red y reduce el rendimiento del sistema sin aportar ninguna ventaja.
:::

---

## ¿Qué aprenderemos a continuación?

Ya conocemos cómo se organiza un gemelo digital y cómo circula la información entre sus diferentes componentes.

En el siguiente apartado construiremos un ejemplo práctico utilizando:

- Python;
- CoppeliaSim;
- OPC UA;
- una base de datos;
- un panel de supervisión.

A partir de ese momento comenzaremos a desarrollar un sistema muy similar a los utilizados actualmente en la Industria 4.0.

## 25.4 Construyendo nuestro primer gemelo digital

Después de conocer la arquitectura general de un gemelo digital, ha llegado el momento de construir una versión simplificada que nos permita comprender cómo interactúan todos sus componentes.

Nuestro objetivo será sincronizar una simulación desarrollada en CoppeliaSim con una aplicación Python que recibirá información desde un PLC mediante OPC UA y almacenará determinados datos en una base de datos PostgreSQL.

Aunque el ejemplo es sencillo, reproduce la estructura utilizada actualmente en numerosas aplicaciones industriales.

La siguiente figura muestra el sistema que construiremos durante este capítulo.

::: figure
image: ../assets/cap25/fig25_5.png
caption: Arquitectura del primer gemelo digital desarrollado en este capítulo.
:::

---

### Componentes del sistema

Nuestro gemelo digital estará formado por los siguientes elementos.

**Instalación física**

Representará una célula robotizada compuesta por:

- un robot UR3;
- una cinta transportadora;
- un PLC Omron NX102;
- sensores de presencia;
- una cámara industrial.

**Servidor OPC UA**

Será el encargado de intercambiar información entre el PLC y la aplicación Python.

A través de él accederemos a variables como:

- estado del robot;
- detección de piezas;
- velocidad de la cinta;
- contador de producción.

**Aplicación Python**

Actuará como elemento central del sistema.

Sus responsabilidades serán:

- leer variables OPC UA;
- actualizar la simulación;
- registrar datos históricos;
- comunicar CoppeliaSim con el resto de la instalación.

**Base de datos PostgreSQL**

Almacenará toda la información relevante del proceso.

Gracias a ello podremos consultar posteriormente:

- tiempos de ciclo;
- número de piezas procesadas;
- alarmas;
- estadísticas de producción.

**CoppeliaSim**

Representará el comportamiento de la instalación en tiempo real.

Cada cambio detectado en el sistema físico se reflejará automáticamente en el modelo virtual.

---

## 25.5 Sincronización de datos

La característica más importante de un gemelo digital consiste en mantener sincronizados ambos mundos.

Cada vez que ocurre un cambio en la instalación física, dicho cambio debe reflejarse en la simulación.

Del mismo modo, determinadas acciones realizadas sobre el modelo virtual pueden enviarse nuevamente al sistema físico.

La siguiente figura resume este proceso.

::: figure
image: ../assets/cap25/fig25_6.png
caption: Sincronización bidireccional entre el sistema físico y el gemelo digital.
:::

---

### Ciclo de sincronización

El funcionamiento general puede resumirse en los siguientes pasos.

1. Un sensor detecta la llegada de una pieza.
2. El PLC actualiza sus variables internas.
3. El servidor OPC UA publica los nuevos valores.
4. La aplicación Python consulta las variables.
5. Python actualiza la simulación en CoppeliaSim.
6. Se registra la información en PostgreSQL.
7. El dashboard muestra el nuevo estado del sistema.

Este ciclo se repite continuamente mientras la instalación permanece en funcionamiento.

En aplicaciones industriales reales este proceso puede ejecutarse decenas o incluso cientos de veces por segundo.

---

### ¿Qué información debe sincronizarse?

No todas las variables de un sistema tienen la misma importancia.

Habitualmente se sincronizan únicamente aquellas que resultan relevantes para la supervisión o el control.

Algunos ejemplos son:

- posición del robot UR3;
- estado de la pinza;
- presencia de piezas;
- velocidad de la cinta transportadora;
- contador de producción;
- alarmas activas;
- modo de funcionamiento;
- tiempos de ciclo.

Seleccionar correctamente estas variables permite reducir el tráfico de red y mejorar el rendimiento del sistema.

::: teacher
content:

Una buena actividad consiste en pedir al alumnado que decida qué variables incluiría en el gemelo digital de una instalación determinada.

Este ejercicio les ayuda a comprender que un gemelo digital no consiste en copiar absolutamente toda la información del sistema físico, sino únicamente aquella que aporta valor para la supervisión, el análisis o la toma de decisiones.

:::

---

## Bases de datos y trazabilidad

Una de las grandes ventajas de un gemelo digital consiste en que toda la información puede almacenarse para su análisis posterior.

Gracias a ello es posible responder preguntas como:

- ¿Cuántas piezas se fabricaron durante un turno?
- ¿Cuál fue el tiempo medio de ciclo?
- ¿Qué alarmas aparecieron durante la producción?
- ¿Cuánto tiempo permaneció detenido el robot?
- ¿Qué porcentaje de piezas resultó defectuoso?

Toda esta información resulta esencial para mejorar continuamente el proceso productivo.

Por este motivo, prácticamente todos los gemelos digitales incorporan una base de datos que registra automáticamente los eventos más importantes.

::: common-error
content:

Registrar absolutamente todos los datos del proceso puede generar bases de datos enormes y difíciles de gestionar.

Conviene almacenar únicamente la información que realmente vaya a utilizarse posteriormente para análisis, mantenimiento o trazabilidad.

:::

---

## Preparando el ejemplo completo

Ya conocemos todos los componentes que intervienen en un gemelo digital.

En el siguiente apartado desarrollaremos una aplicación completa que integrará:

- Python;
- CoppeliaSim;
- OPC UA;
- PostgreSQL;
- un dashboard de supervisión.

Con este ejemplo construiremos un sistema muy próximo a los utilizados actualmente en entornos de Industria 4.0.

## 25.6 Caso práctico: una célula robotizada conectada

En este apartado construiremos un ejemplo simplificado de una célula robotizada conectada.

La instalación estará formada por:

- un robot **UR3**;
- una cinta transportadora;
- un PLC Omron NX102;
- una cámara industrial;
- una aplicación Python;
- una base de datos PostgreSQL;
- un dashboard de supervisión;
- un gemelo digital desarrollado en CoppeliaSim.

Aunque se trata de un ejemplo académico, reproduce la arquitectura utilizada actualmente en numerosas instalaciones industriales.

La siguiente figura muestra el sistema completo.

::: figure
image: ../assets/cap25/fig25_7.png
caption: Arquitectura completa del caso práctico desarrollado en este capítulo.
:::

---

### Funcionamiento del sistema

El funcionamiento puede resumirse en las siguientes etapas.

1. Una pieza llega a la cinta transportadora.
2. El sensor detecta su presencia.
3. El PLC inicia el ciclo automático.
4. La cámara identifica la pieza.
5. Python recibe la información mediante OPC UA.
6. El gemelo digital actualiza la posición del robot UR3.
7. El robot recoge la pieza.
8. La operación queda registrada en PostgreSQL.
9. El dashboard actualiza automáticamente los indicadores de producción.

Todo este proceso se ejecuta de forma prácticamente simultánea.

El usuario únicamente observa que la instalación física y la simulación evolucionan de forma sincronizada.

---

## Sincronizando el robot UR3

Uno de los elementos más importantes del gemelo digital consiste en mantener sincronizada la posición del robot.

Para conseguirlo es suficiente con transmitir periódicamente las variables que describen el estado del manipulador.

Por ejemplo:

- posición de cada articulación;
- estado de la pinza;
- objetivo activo;
- modo de funcionamiento;
- velocidad de movimiento.

Cuando Python recibe estos datos, actualiza inmediatamente el modelo del UR3 en CoppeliaSim.

Si el robot físico inicia un movimiento, el mismo movimiento aparecerá casi instantáneamente en la simulación.

La siguiente figura representa este proceso.

::: figure
image: ../assets/cap25/fig25_8.png
caption: Sincronización del robot UR3 entre la instalación física y CoppeliaSim.
:::

---

### Actualizando el dashboard

Además de sincronizar la simulación, la aplicación Python registra continuamente información en la base de datos.

A partir de esos datos el dashboard puede mostrar indicadores como:

- producción total;
- piezas por minuto;
- tiempo medio de ciclo;
- disponibilidad del robot;
- alarmas activas;
- eficiencia de la instalación.

Estos indicadores permiten conocer el estado de la producción sin necesidad de acceder directamente al PLC.

En aplicaciones reales también es habitual representar:

- gráficas históricas;
- tendencias;
- consumo energético;
- tiempos de parada;
- estadísticas de calidad.

Gracias a esta información los responsables de producción pueden tomar decisiones fundamentadas y detectar problemas antes de que afecten al rendimiento de la instalación.

::: teacher
content:

Si el centro dispone de Node-RED o Grafana, este es un excelente momento para mostrar al alumnado un dashboard real conectado a una base de datos.

De este modo comprobarán que el mismo flujo de información utilizado por el gemelo digital puede emplearse también para construir sistemas de monitorización industrial.

:::

---

## Escalando el sistema

La arquitectura desarrollada durante este capítulo puede ampliarse fácilmente.

Por ejemplo, sería posible incorporar:

- varios robots UR3 trabajando simultáneamente;
- varias cámaras industriales;
- sensores adicionales;
- nuevos PLC;
- servicios en la nube;
- algoritmos de Inteligencia Artificial para mantenimiento predictivo.

La filosofía seguiría siendo exactamente la misma.

Cada nuevo componente intercambiaría información mediante protocolos estandarizados y el gemelo digital continuaría ofreciendo una visión unificada de toda la instalación.

::: common-error
content:

Un gemelo digital no debe limitarse a reproducir una animación atractiva.

Su verdadero valor consiste en proporcionar información útil para supervisar, analizar y optimizar el funcionamiento de la instalación industrial.

:::

---

## Preparando el cierre del capítulo

Ya conocemos todos los elementos necesarios para construir un gemelo digital funcional.

En el siguiente apartado realizaremos un resumen de los conceptos aprendidos, revisaremos las principales ideas del capítulo y desarrollaremos una práctica guiada que integrará todos los conocimientos adquiridos.

## 25.7 Del gemelo digital a la fábrica inteligente

A lo largo de este capítulo hemos comprobado que un gemelo digital va mucho más allá de una simple simulación tridimensional.

Su verdadero valor reside en la capacidad de mantenerse sincronizado con la instalación física, intercambiando información de forma continua y permitiendo supervisar, analizar y optimizar el proceso productivo.

Gracias a la integración de tecnologías como **OPC UA**, **Python**, **CoppeliaSim** y **PostgreSQL**, es posible construir sistemas capaces de representar fielmente el comportamiento de una célula robotizada industrial.

La siguiente figura resume todos los elementos que intervienen en un gemelo digital moderno.

::: figure
image: ../assets/cap25/fig25_9.png
caption: Componentes principales de un gemelo digital aplicado a una célula robotizada.
:::

---

## Hacia la Industria 4.0

Los gemelos digitales constituyen uno de los pilares fundamentales de la denominada **Industria 4.0**.

Su utilización permite conectar el mundo físico con el mundo digital, facilitando tareas como:

- monitorización en tiempo real;
- mantenimiento predictivo;
- optimización de procesos;
- trazabilidad de la producción;
- simulación de mejoras antes de aplicarlas;
- formación de operarios mediante entornos virtuales.

En los próximos años este tipo de soluciones será cada vez más habitual en empresas de cualquier tamaño.

Por este motivo, comprender su funcionamiento representa una competencia especialmente valiosa para cualquier técnico de automatización o robótica.

La siguiente figura representa cómo un gemelo digital se integra dentro del ecosistema de una fábrica inteligente.

::: figure
image: ../assets/cap25/fig25_10.png
caption: El gemelo digital como elemento integrador de una solución de Industria 4.0.
:::

::: teacher
content:

Siempre que sea posible, relaciona estos conceptos con ejemplos reales cercanos al alumnado.

Muchos estudiantes descubren que numerosas empresas de su entorno ya utilizan dashboards, bases de datos, PLC conectados y sistemas de supervisión similares a los estudiados en este capítulo.

Comprender que estas tecnologías forman parte de la industria actual aumenta significativamente su motivación.
:::

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Gemelo digital | Representación virtual sincronizada con un sistema físico. |
| Industria 4.0 | Modelo industrial basado en la conectividad, los datos y la automatización inteligente. |
| Sincronización | Actualización continua entre el sistema físico y el modelo virtual. |
| Dashboard | Aplicación que muestra indicadores e información del proceso en tiempo real. |
| Trazabilidad | Registro histórico de los eventos y operaciones realizadas durante la producción. |
| Monitorización | Supervisión continua del estado de una instalación. |
| PostgreSQL | Base de datos utilizada para almacenar la información del proceso. |
| CoppeliaSim | Simulador empleado como representación virtual de la instalación. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Explicar qué es un gemelo digital y en qué se diferencia de una simulación.
- ✅ Comprender la arquitectura básica de un sistema de Industria 4.0.
- ✅ Identificar los componentes que forman un gemelo digital.
- ✅ Entender cómo sincronizar una instalación física con CoppeliaSim.
- ✅ Valorar la importancia de las bases de datos y los dashboards en la supervisión industrial.
- ✅ Comprender el papel de Python como elemento integrador del sistema.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué diferencia existe entre una simulación y un gemelo digital?
2. ¿Qué papel desempeña CoppeliaSim dentro del sistema?
3. ¿Por qué resulta importante mantener sincronizados el sistema físico y el virtual?
4. ¿Qué información suele almacenarse en una base de datos industrial?
5. ¿Cuál es la utilidad de un dashboard?
6. ¿Qué ventajas aporta un gemelo digital frente a una instalación convencional?
7. ¿Qué tecnologías estudiadas en este capítulo intervienen en una solución de Industria 4.0?

Si puedes responder correctamente a todas ellas, estás preparado para abordar el proyecto integrador del siguiente capítulo.

---

## Práctica guiada

::: practice
title: Diseñando un gemelo digital

difficulty: Alta

time: 75 minutos

content:

Diseña el esquema de un gemelo digital para una célula robotizada formada por un robot UR3 y una cinta transportadora.

La solución deberá incluir:

1. El sistema físico.
2. Un PLC industrial.
3. Comunicación mediante OPC UA.
4. Una aplicación desarrollada en Python.
5. Un modelo virtual en CoppeliaSim.
6. Una base de datos PostgreSQL.
7. Un dashboard de supervisión.

Una vez completado el diseño, explica qué información intercambiaría cada componente con el resto del sistema y justifica tus decisiones.

:::

---

## Reto

::: challenge
title: Imaginando la fábrica del futuro

content:

Investiga una empresa o sector industrial donde el uso de un gemelo digital pueda aportar ventajas.

Elabora una propuesta indicando:

- qué proceso automatizarías;
- qué datos recogerías;
- cómo utilizarías CoppeliaSim como representación virtual;
- qué indicadores mostrarías en el dashboard;
- qué beneficios obtendría la empresa.

Presenta tus conclusiones al resto de la clase y compáralas con las propuestas de tus compañeros.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Entre una y dos sesiones de 55 minutos.

**Objetivos**

- Consolidar los conceptos de gemelo digital e Industria 4.0.
- Relacionar los contenidos del capítulo con aplicaciones industriales reales.
- Preparar al alumnado para el proyecto integrador del siguiente capítulo.

**Material necesario**

- CoppeliaSim EDU 4.10.
- Visual Studio Code.
- Python 3.x.
- PostgreSQL.
- Servidor OPC UA (opcional).
- Proyector para mostrar una arquitectura completa.

**Consejos metodológicos**

Anima al alumnado a diseñar arquitecturas propias en lugar de limitarse a reproducir el ejemplo del libro.

La capacidad para justificar las decisiones de diseño constituye una competencia tan importante como la implementación técnica.

:::

---

## Próximo capítulo

Durante este capítulo hemos aprendido cómo integrar una simulación con una instalación real mediante un gemelo digital.

En el siguiente capítulo desarrollaremos un **proyecto industrial conectado**, en el que reuniremos todos los conocimientos adquiridos en la Parte V para construir una célula robotizada completa basada en un **UR3**, un **PLC**, una **cámara industrial**, **OPC UA**, una **base de datos PostgreSQL**, un **dashboard** y **CoppeliaSim** como gemelo digital.

Será el proyecto integrador que pondrá en práctica todos los conceptos estudiados en esta parte del libro.
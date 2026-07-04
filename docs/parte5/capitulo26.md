::: chapter-cover
number: 26
title: Proyecto industrial conectado
time: 8 horas
level: ⭐⭐⭐⭐⭐ (Proyecto integrador)
:::

::: objectives
title: Objetivos del capítulo
content:

Al finalizar este capítulo serás capaz de:

- Integrar CoppeliaSim dentro de una arquitectura industrial completa.
- Diseñar una célula robotizada conectada mediante Python.
- Comunicar un PLC con un robot industrial utilizando OPC UA.
- Sincronizar un gemelo digital con una instalación física.
- Registrar información en una base de datos PostgreSQL.
- Diseñar un dashboard para supervisar el proceso en tiempo real.
- Comprender el flujo completo de información de una solución de Industria 4.0.

:::

# Capítulo 26 · Proyecto industrial conectado

## Uniendo todas las piezas

A lo largo de este libro hemos ido incorporando nuevas capacidades a nuestros robots.

Primero aprendimos a utilizar CoppeliaSim.

Después controlamos robots móviles mediante Python.

Más adelante incorporamos visión artificial, manipuladores industriales, ROS 2 y protocolos de comunicación como OPC UA.

Ha llegado el momento de integrar todos esos conocimientos en un único proyecto.

Durante este capítulo construiremos una célula robotizada inspirada en una instalación industrial real.

No estudiaremos cada tecnología por separado.

Ahora todas ellas trabajarán conjuntamente formando un único sistema.

La siguiente figura muestra la arquitectura general del proyecto.

::: figure
image: ../assets/cap26/fig26_1.png
caption: Arquitectura general del proyecto industrial conectado desarrollado en este capítulo.
:::

---

## Objetivos del proyecto

El sistema que construiremos será capaz de:

- detectar piezas sobre una cinta transportadora;
- identificar su estado mediante una cámara industrial;
- controlar un robot UR3;
- intercambiar información con un PLC Omron NX102;
- actualizar un gemelo digital en CoppeliaSim;
- registrar la producción en PostgreSQL;
- mostrar indicadores en un dashboard de supervisión.

Aunque el proyecto ha sido simplificado para facilitar su comprensión, reproduce fielmente la arquitectura utilizada en numerosas instalaciones industriales.

Nuestro objetivo no consiste únicamente en programar un robot.

Pretendemos comprender cómo colaboran todos los sistemas que forman parte de una solución moderna de automatización.

::: teacher
content:

Antes de comenzar el proyecto, dedica unos minutos a recordar los contenidos estudiados en los capítulos anteriores.

Resulta muy útil pedir al alumnado que identifique qué tecnologías aparecen en la arquitectura y en qué capítulo fueron presentadas.

De este modo comprenderán que el proyecto constituye la integración de todos los conocimientos adquiridos durante la Parte V.

:::

---

## 26.1 Arquitectura general del sistema

La célula robotizada estará formada por los siguientes componentes.

**Sistema físico**

- Robot colaborativo UR3.
- Cinta transportadora.
- Cámara industrial.
- Sensores de presencia.
- PLC Omron NX102.

**Sistema software**

- Servidor OPC UA.
- Aplicación desarrollada en Python.
- Base de datos PostgreSQL.
- Dashboard de supervisión.
- Gemelo digital implementado con CoppeliaSim.

Cada uno de estos elementos intercambiará información continuamente para mantener sincronizado todo el sistema.

La siguiente figura muestra la relación existente entre ellos.

::: figure
image: ../assets/cap26/fig26_2.png
caption: Componentes principales del proyecto industrial conectado.
:::

---

### El papel de Python

Python actuará como el elemento integrador de toda la arquitectura.

Será el encargado de:

- consultar variables OPC UA;
- comunicarse con CoppeliaSim;
- almacenar información en PostgreSQL;
- actualizar el dashboard;
- coordinar el flujo general del sistema.

En otras palabras, Python funcionará como el "director de orquesta" de toda la instalación.

Este enfoque resulta muy habitual en aplicaciones industriales donde diferentes tecnologías deben colaborar entre sí.

::: common-error
content:

Es frecuente pensar que el PLC debe encargarse de todas las tareas del sistema.

En la práctica, el PLC controla el proceso automático, mientras que aplicaciones desarrolladas en Python suelen asumir funciones de integración, análisis de datos, supervisión y comunicación con otros sistemas.

:::

## 26.2 Preparando la escena en CoppeliaSim

Todo proyecto industrial comienza con el diseño de la instalación.

En nuestro caso construiremos una célula robotizada que represente una pequeña línea de producción automatizada.

La escena estará formada por los siguientes elementos:

- un robot colaborativo **UR3**;
- una cinta transportadora;
- una cámara de visión artificial;
- sensores de presencia;
- un área de recogida de piezas;
- un área de clasificación;
- varios objetos que simularán las piezas de producción.

La siguiente figura muestra la distribución general de la escena.

::: figure
image: ../assets/cap26/fig26_3.png
caption: Distribución de los elementos principales de la célula robotizada.
:::

---

### Organización del espacio de trabajo

Antes de comenzar a programar conviene organizar correctamente todos los elementos.

Una distribución ordenada facilita el mantenimiento de la escena y reduce la posibilidad de errores durante el desarrollo.

Una posible organización sería:

- situar el robot UR3 en el centro de trabajo;
- colocar la cinta transportadora frente al robot;
- instalar la cámara sobre la cinta para observar las piezas;
- ubicar los sensores al inicio y al final del recorrido;
- reservar una zona para depositar las piezas clasificadas.

Este tipo de distribución reproduce la disposición habitual de numerosas células robotizadas industriales.

---

### Nombrando correctamente los objetos

A medida que aumenta el número de elementos de la escena resulta imprescindible utilizar nombres descriptivos.

Por ejemplo:

```text
UR3
Conveyor
Camera_Top
Sensor_Input
Sensor_Output
Box_Red
Box_Blue
PLC_Tag
```

Evita utilizar nombres genéricos como:

```text
Shape0
Shape1
Dummy3
Object7
```

Una nomenclatura clara simplifica enormemente la programación y facilita el trabajo colaborativo.

::: teacher
content:

Dedica unos minutos a revisar junto al alumnado el árbol de la escena.

Una estructura ordenada desde el principio evitará muchos problemas cuando el proyecto aumente de tamaño.

:::

---

## 26.3 Integrando los sensores

Una vez creada la escena, el siguiente paso consiste en incorporar los sensores que permitirán detectar el estado del proceso.

En este proyecto utilizaremos dos tipos de sensores.

### Sensores de presencia

Su función será detectar la llegada de una pieza a la cinta transportadora.

Cada vez que una pieza atraviese el área de detección, el sensor activará una señal que será enviada al PLC.

### Cámara industrial

La cámara permitirá identificar las piezas antes de que el robot las manipule.

En capítulos anteriores aprendimos a obtener imágenes desde Python y a procesarlas utilizando OpenCV.

Ahora reutilizaremos esos conocimientos dentro de una arquitectura mucho más amplia.

La siguiente figura muestra la posición recomendada para los sensores de la instalación.

::: figure
image: ../assets/cap26/fig26_4.png
caption: Ubicación de los sensores y de la cámara industrial dentro de la célula robotizada.
:::

---

### Flujo de información

El funcionamiento será el siguiente:

1. Una pieza entra en la cinta transportadora.
2. El sensor de entrada detecta su presencia.
3. La cámara captura una imagen.
4. Python procesa la información recibida.
5. El PLC decide la operación que debe realizar el robot.
6. El UR3 recoge la pieza.
7. El sensor de salida confirma que la operación ha finalizado correctamente.

Este flujo servirá como base para todas las prácticas desarrolladas durante el resto del capítulo.

::: common-error
content:

No sitúes los sensores demasiado cerca del robot o de la zona de recogida.

Una mala ubicación puede provocar detecciones repetidas o impedir que el sistema identifique correctamente el paso de las piezas.

:::

---

## Preparando la integración

La escena ya contiene todos los elementos físicos necesarios para comenzar a trabajar.

En la siguiente entrega desarrollaremos la aplicación Python que coordinará toda la instalación, estableceremos la comunicación mediante OPC UA y sincronizaremos el gemelo digital con la célula robotizada en CoppeliaSim.

## 26.4 Desarrollando la aplicación de integración

Una vez preparada la célula robotizada, necesitamos una aplicación que coordine el intercambio de información entre todos los componentes del sistema.

En nuestro proyecto esta tarea recaerá sobre una aplicación desarrollada en **Python**, que actuará como elemento central de la arquitectura.

Su función será:

- comunicarse con el PLC mediante OPC UA;
- intercambiar información con CoppeliaSim;
- registrar datos en PostgreSQL;
- actualizar el dashboard;
- supervisar el estado general de la instalación.

La siguiente figura representa esta arquitectura.

::: figure
image: ../assets/cap26/fig26_5.png
caption: Python como núcleo de integración del sistema industrial.
:::

---

### Organización de la aplicación

Aunque el proyecto podría desarrollarse en un único programa, resulta mucho más recomendable dividir la aplicación en diferentes módulos.

Una posible organización sería la siguiente:

```text
proyecto_industrial/

├── main.py
├── opcua_client.py
├── coppeliasim.py
├── database.py
├── dashboard.py
├── config.py
└── utils.py
```

Cada módulo tendrá una responsabilidad claramente definida.

Por ejemplo:

- `opcua_client.py` gestionará la comunicación con el PLC.
- `coppeliasim.py` actualizará el gemelo digital.
- `database.py` almacenará la información en PostgreSQL.
- `dashboard.py` preparará los datos para su visualización.
- `config.py` contendrá todos los parámetros de configuración del sistema.

Esta organización facilita el mantenimiento y permite ampliar el proyecto sin necesidad de modificar todo el código.

---

### El ciclo principal

El funcionamiento general de la aplicación seguirá siempre la misma secuencia.

```python
while True:

    leer_variables_plc()

    actualizar_coppeliasim()

    guardar_datos()

    actualizar_dashboard()

    esperar_siguiente_ciclo()
```

Aunque este ejemplo es muy sencillo, representa el comportamiento básico de numerosos sistemas industriales.

El ciclo se repite continuamente mientras la instalación permanece en funcionamiento.

---

## 26.5 Registrando la información

Uno de los aspectos más importantes de cualquier sistema industrial consiste en registrar los eventos más relevantes.

Gracias a ello es posible realizar posteriormente tareas de:

- trazabilidad;
- análisis de producción;
- mantenimiento;
- control de calidad;
- generación de informes.

La siguiente figura muestra el flujo seguido por los datos hasta llegar a la base de datos.

::: figure
image: ../assets/cap26/fig26_6.png
caption: Flujo de almacenamiento de la información en PostgreSQL.
:::

---

### ¿Qué información almacenaremos?

En este proyecto registraremos, entre otros, los siguientes datos:

- fecha y hora de cada operación;
- identificador de la pieza;
- posición del robot UR3;
- resultado de la inspección visual;
- estado del PLC;
- tiempo de ciclo;
- incidencias detectadas.

Toda esta información permitirá reconstruir posteriormente el comportamiento completo de la instalación.

---

### Preparando el dashboard

El último paso consistirá en mostrar la información de forma clara para el operario.

El dashboard podrá incluir indicadores como:

- producción total;
- piezas correctas;
- piezas rechazadas;
- tiempo medio de ciclo;
- disponibilidad del robot;
- estado del PLC;
- alarmas activas.

No es necesario que el operario conozca el funcionamiento interno del sistema.

Su objetivo consiste únicamente en disponer de información útil para supervisar el proceso y tomar decisiones.

::: teacher
content:

Aprovecha este apartado para explicar la diferencia entre almacenar datos y mostrar información.

La base de datos guarda todos los eventos del proceso, mientras que el dashboard presenta únicamente aquellos indicadores que resultan útiles para el usuario.

Este concepto aparece constantemente en aplicaciones reales de Industria 4.0.

:::

---

## Diseñando una aplicación escalable

El proyecto desarrollado en este capítulo ha sido simplificado para facilitar su comprensión.

Sin embargo, la arquitectura propuesta permite crecer fácilmente.

Por ejemplo, podríamos incorporar:

- varios robots UR3;
- diferentes PLC;
- varias cámaras industriales;
- múltiples líneas de producción;
- nuevos dashboards;
- algoritmos de Inteligencia Artificial.

La filosofía seguiría siendo exactamente la misma.

Cada nuevo componente se integraría reutilizando la infraestructura de comunicación ya desarrollada.

::: common-error
content:

Evita escribir toda la aplicación en un único archivo Python.

Dividir el proyecto en módulos independientes facilita enormemente el mantenimiento, la depuración y la reutilización del código.

:::

---

## Preparando la integración final

En la siguiente entrega pondremos en funcionamiento todo el sistema.

Comprobaremos cómo la información circula entre el PLC, Python, PostgreSQL y CoppeliaSim, verificando que el gemelo digital permanece sincronizado con la instalación física y concluyendo el proyecto integrador de la Parte V.

## 26.6 Integración y puesta en marcha del sistema

Después de desarrollar cada uno de los componentes de forma independiente, ha llegado el momento de integrarlos en una única aplicación.

El objetivo consiste en comprobar que todos los elementos intercambian información correctamente y que el gemelo digital permanece sincronizado con la instalación física.

Durante esta fase verificaremos que:

- el PLC transmite correctamente sus variables mediante OPC UA;
- Python recibe y procesa la información;
- CoppeliaSim actualiza el estado del robot UR3;
- PostgreSQL registra los eventos del proceso;
- el dashboard refleja el estado de la producción en tiempo real.

La siguiente figura resume la integración completa del sistema.

::: figure
image: ../assets/cap26/fig26_7.png
caption: Integración completa de la célula robotizada y del gemelo digital.
:::

---

### Secuencia completa de funcionamiento

Cuando el sistema entra en funcionamiento, los diferentes componentes colaboran siguiendo una secuencia perfectamente coordinada.

1. Una pieza entra en la cinta transportadora.
2. El sensor detecta su presencia.
3. El PLC inicia el ciclo automático.
4. La cámara captura una imagen de la pieza.
5. Python recibe la información mediante OPC UA.
6. Se decide la operación que realizará el robot UR3.
7. CoppeliaSim reproduce el movimiento en el gemelo digital.
8. PostgreSQL almacena el evento.
9. El dashboard actualiza los indicadores de producción.
10. El sistema queda preparado para procesar la siguiente pieza.

Todo este proceso se ejecuta de forma automática y prácticamente en tiempo real.

---

### Verificando el funcionamiento

Antes de considerar finalizada la instalación es recomendable comprobar que cada uno de los componentes responde correctamente.

Algunas verificaciones habituales son:

- comprobar que el PLC publica las variables esperadas;
- verificar que Python recibe correctamente los datos;
- confirmar que el robot virtual reproduce el movimiento del robot físico;
- revisar que PostgreSQL almacena los registros;
- comprobar que el dashboard actualiza los indicadores sin retrasos apreciables.

Estas comprobaciones permiten detectar errores de configuración antes de poner el sistema en producción.

---

## 26.7 Validación del gemelo digital

Una vez integrada la aplicación, el siguiente paso consiste en validar que el gemelo digital representa fielmente el comportamiento de la instalación.

No basta con observar que el robot se mueve.

Es necesario comprobar que todos los elementos permanecen sincronizados.

Por ejemplo:

- la posición del robot;
- el estado de la pinza;
- las piezas presentes sobre la cinta;
- los sensores;
- los contadores de producción;
- las alarmas.

La siguiente figura representa el proceso de validación del gemelo digital.

::: figure
image: ../assets/cap26/fig26_8.png
caption: Validación de la sincronización entre la instalación física y el gemelo digital.
:::

---

### Indicadores de validación

Para comprobar que el sistema funciona correctamente podemos utilizar indicadores como:

- tiempo medio de sincronización;
- número de eventos registrados;
- porcentaje de actualizaciones correctas;
- tiempo de respuesta del sistema;
- disponibilidad del robot;
- tiempo de ciclo.

Estos indicadores permiten evaluar objetivamente el rendimiento de la instalación.

En proyectos industriales reales también es habitual registrar métricas relacionadas con la calidad del producto, el consumo energético o la eficiencia global de la línea de producción.

::: teacher
content:

Una buena práctica consiste en introducir intencionadamente pequeños errores durante la demostración.

Por ejemplo, detener el servidor OPC UA o desconectar temporalmente la base de datos.

El alumnado comprobará cómo afecta cada incidencia al funcionamiento global del sistema y comprenderá mejor la importancia de cada componente.

:::

---

## Preparando el cierre del proyecto

Con la integración completada ya disponemos de una célula robotizada totalmente funcional.

En la siguiente y última entrega realizaremos el cierre del capítulo mediante un resumen de los conceptos aprendidos, una práctica guiada, un reto final y una reflexión sobre el papel de este tipo de arquitecturas en la Industria 4.0.

::: common-error
content:

Un sistema puede parecer que funciona correctamente aunque alguno de sus componentes no esté sincronizado.

Antes de dar por finalizado un proyecto, verifica siempre que la información mostrada por el dashboard coincide con la registrada en la base de datos y con el comportamiento observado en CoppeliaSim.

:::

## 26.8 Síntesis del proyecto

Después de desarrollar cada uno de los módulos por separado, ha llegado el momento de observar el sistema completo funcionando como una única aplicación.

Nuestra célula robotizada integra:

- un robot colaborativo **UR3**;
- una cámara industrial;
- una cinta transportadora;
- un PLC Omron NX102;
- un servidor OPC UA;
- una aplicación desarrollada en Python;
- una base de datos PostgreSQL;
- un dashboard de supervisión;
- un gemelo digital implementado con CoppeliaSim.

Cada uno de estos componentes desempeña una función específica.

Sin embargo, únicamente cuando trabajan de forma coordinada es posible construir una solución propia de la Industria 4.0.

La siguiente figura resume la arquitectura completa del proyecto.

::: figure
image: ../assets/cap26/fig26_9.png
caption: Arquitectura final del proyecto industrial conectado.
:::

---

## Beneficios obtenidos

La arquitectura desarrollada durante este proyecto proporciona numerosas ventajas.

Entre ellas destacan:

- supervisión continua del proceso;
- sincronización entre el sistema físico y el gemelo digital;
- trazabilidad completa de la producción;
- almacenamiento histórico de información;
- detección temprana de incidencias;
- posibilidad de analizar el rendimiento de la instalación;
- facilidad para ampliar el sistema incorporando nuevos dispositivos.

Estas características representan algunos de los principios fundamentales de la Industria 4.0.

::: teacher
content:

Durante la demostración final resulta especialmente interesante modificar una variable desde el PLC o desde Python y comprobar cómo el cambio aparece inmediatamente reflejado en CoppeliaSim y en el dashboard.

Esta actividad ayuda al alumnado a comprender que el verdadero valor de un gemelo digital reside en la sincronización continua entre el mundo físico y el virtual.

:::

---

## Evolución futura del proyecto

Aunque el proyecto desarrollado en este capítulo es completamente funcional, podría ampliarse fácilmente incorporando nuevas capacidades.

Por ejemplo:

- algoritmos de Inteligencia Artificial para mantenimiento predictivo;
- visión artificial basada en aprendizaje profundo;
- robots colaborativos adicionales;
- servicios en la nube;
- integración con sistemas ERP y MES;
- monitorización remota mediante dispositivos móviles.

La arquitectura propuesta ha sido diseñada precisamente para facilitar este tipo de ampliaciones.

La figura siguiente resume el recorrido completo de la información dentro de una solución de Industria 4.0 como la desarrollada a lo largo de este capítulo.

En ella puede apreciarse cómo los datos fluyen desde la instalación física hasta el gemelo digital, la base de datos y el dashboard, generando un ciclo continuo de supervisión, análisis y mejora del proceso.

::: figure
image: ../assets/cap26/fig26_10.png
caption: Flujo completo de información en una solución de Industria 4.0 basada en CoppeliaSim.
:::

Este esquema sintetiza el objetivo principal de la Parte V: comprender que un robot industrial no trabaja de forma aislada, sino integrado dentro de un ecosistema de comunicaciones, aplicaciones software y herramientas de supervisión que colaboran para optimizar la producción.

---

## Conceptos clave

::: table
caption: Conceptos fundamentales del capítulo.
content:

| Concepto | Definición breve |
|-----------|------------------|
| Proyecto industrial conectado | Sistema que integra robots, PLC, comunicaciones y aplicaciones software. |
| Gemelo digital | Representación virtual sincronizada con una instalación física. |
| OPC UA | Protocolo industrial para el intercambio de información. |
| Dashboard | Aplicación utilizada para supervisar indicadores del proceso. |
| PostgreSQL | Base de datos empleada para registrar la información del sistema. |
| Trazabilidad | Registro histórico de los eventos de producción. |
| Python | Lenguaje encargado de integrar todos los componentes del sistema. |
| CoppeliaSim | Simulador utilizado como representación virtual de la instalación. |

:::

---

## En este capítulo has aprendido

Al finalizar este capítulo ya eres capaz de:

- ✅ Diseñar una arquitectura industrial completa.
- ✅ Integrar un robot UR3 con un PLC mediante OPC UA.
- ✅ Sincronizar un gemelo digital con una instalación física.
- ✅ Registrar información en PostgreSQL.
- ✅ Diseñar un dashboard de supervisión.
- ✅ Comprender el funcionamiento global de una solución de Industria 4.0.

---

## Autoevaluación

Comprueba si puedes responder correctamente a las siguientes preguntas.

1. ¿Qué función desempeña Python dentro del sistema?
2. ¿Qué ventajas ofrece un gemelo digital?
3. ¿Qué papel desempeña PostgreSQL?
4. ¿Qué información suele mostrar un dashboard?
5. ¿Por qué resulta útil utilizar OPC UA?
6. ¿Qué beneficios aporta registrar la producción?
7. ¿Qué ventajas presenta una arquitectura modular frente a una aplicación monolítica?

Si puedes responder correctamente a todas ellas, has comprendido el funcionamiento general de una célula robotizada conectada.

---

## Práctica guiada

::: practice
title: Construcción de una célula robotizada conectada

difficulty: Alta

time: 120 minutos

content:

Realiza las siguientes tareas.

1. Diseña una escena con un robot UR3 y una cinta transportadora.
2. Configura un servidor OPC UA.
3. Desarrolla una aplicación Python que lea variables del PLC.
4. Actualiza el gemelo digital en CoppeliaSim.
5. Registra los eventos en PostgreSQL.
6. Diseña un dashboard con los principales indicadores.
7. Comprueba la sincronización entre todos los componentes.
8. Documenta la arquitectura desarrollada.
9. Analiza posibles mejoras.
10. Presenta el funcionamiento completo al resto de la clase.

El objetivo consiste en integrar todos los conocimientos adquiridos durante la Parte V.

:::

---

## Reto

::: challenge
title: Diseñando una fábrica inteligente

content:

Imagina que debes automatizar una pequeña línea de producción.

Diseña una arquitectura formada por:

- dos robots UR3;
- una cámara industrial;
- varios sensores;
- un PLC;
- un servidor OPC UA;
- una base de datos PostgreSQL;
- un dashboard;
- un gemelo digital desarrollado en CoppeliaSim.

Elabora un diagrama indicando cómo se comunican todos los componentes y justifica las decisiones adoptadas.

:::

---

## Para el profesor

::: teacher
title: Organización de la sesión

content:

**Duración recomendada**

Dos sesiones de 55 minutos.

**Objetivos**

- Integrar todos los conocimientos desarrollados durante la Parte V.
- Comprender el funcionamiento de una arquitectura Industria 4.0.
- Relacionar simulación, automatización y comunicaciones industriales.

**Material necesario**

- CoppeliaSim EDU 4.10.
- Visual Studio Code.
- Python 3.x.
- PostgreSQL.
- Servidor OPC UA.
- PLC Omron NX102 (opcional).

**Consejos metodológicos**

Valora no solo el funcionamiento técnico del proyecto, sino también la capacidad del alumnado para documentar la arquitectura, justificar sus decisiones de diseño y explicar el flujo de información entre todos los componentes.

:::

---

## Conclusión de la Parte V

Con esta parte del libro has aprendido a comunicar CoppeliaSim con aplicaciones externas, integrar robots industriales con PLC, utilizar protocolos de comunicación industrial, construir gemelos digitales y desarrollar proyectos inspirados en instalaciones reales.

Has dado un paso importante desde la simulación aislada hacia el diseño de sistemas robóticos conectados, sentando las bases necesarias para abordar proyectos profesionales de automatización e Industria 4.0.

---

## Próxima parte

En la **Parte VI · Proyectos completos de robótica** integraremos todos los conocimientos desarrollados a lo largo del libro para construir aplicaciones completas inspiradas en situaciones reales.

Diseñaremos células robotizadas desde cero, desarrollaremos sistemas automáticos de clasificación, combinaremos visión artificial, manipulación, comunicaciones industriales y gemelos digitales, culminando el libro con un proyecto final de alto nivel que reproducirá el funcionamiento de una instalación industrial moderna.
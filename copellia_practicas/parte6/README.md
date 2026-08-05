# Clasificacion de naranjas con CoppeliaSim, PostgreSQL y Grafana

Este capitulo contiene una celula simulada para clasificar naranjas con CoppeliaSim. La escena principal es `clasificacion_naranjas.ttt` y el script Python es `clasificador_naranjas.py`.

## Que hace el script Python

`clasificador_naranjas.py` toma el control de la celula desde Python mediante la API remota ZMQ de CoppeliaSim:

- Desactiva los scripts Lua de control de naranjas, cinta y pinza.
- Restaura la posicion inicial de las 15 naranjas y del robot UR3.
- Controla la cinta transportadora para llevar cada naranja hasta el sensor final.
- Captura imagenes con el `visionSensor`, genera la mascara con OpenCV y calcula el diametro de cada naranja.
- Clasifica cada naranja como `mesa`, `zumo` o `rechazada`.
- Mueve el UR3 con pinza RG2 para recoger cada naranja y depositarla en la caja correspondiente.
- Guarda capturas e imagenes de mascara en `capturas_vision_naranjas`.
- Guarda un resumen local en `diametros_naranjas.csv`.
- Conecta con PostgreSQL 15, crea la base de datos `naranjas` si no existe y actualiza la tabla `datos_naranjas`.

La tabla `datos_naranjas` contiene los acumulados:

- `id_naranja`
- `n_naranjas_procesadas`
- `n_naranjas_mesa`
- `n_naranjas_zumo`
- `n_naranjas_rechazo`

## Panel de Grafana

El sistema esta preparado para visualizar los datos en un panel de Grafana conectado a PostgreSQL. El dashboard debe usar como fuente la base de datos `naranjas` y la tabla `datos_naranjas`.

Grafana se abre en local normalmente en:

```text
http://localhost:3000
```

## Puesta en marcha

1. Abre PostgreSQL 15 y comprueba que el servicio esta iniciado.

2. Abre CoppeliaSim.

3. Carga la escena:

```text
copellia_practicas/parte6/clasificacion_naranjas.ttt
```

4. No ejecutes manualmente los scripts Lua de la escena. El script Python los desactiva al iniciar.

5. Abre una terminal PowerShell en la raiz del proyecto:

```powershell
cd F:\proyectos_SDD\Libro-CoppeliaSim-FP
```

6. Activa el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

7. Ejecuta el script:

```powershell
python .\copellia_practicas\parte6\clasificador_naranjas.py
```

8. Al arrancar, la consola debe mostrar mensajes similares a:

```text
Conectando con PostgreSQL 15.
Conexion con PostgreSQL establecida correctamente.
Base de datos naranjas localizada.
Tabla datos_naranjas preparada.
Conexion con CoppeliaSim establecida.
```

9. Durante la simulacion se mostrara la ventana de OpenCV con la imagen de cada naranja y su mascara. En consola se imprimen el diametro medido, la clasificacion y la actualizacion de PostgreSQL.

10. Abre Grafana en el navegador:

```text
http://localhost:3000
```

11. En Grafana, usa PostgreSQL como origen de datos y conecta con:

```text
Host: localhost:5432
Database: naranjas
User: postgres
Password: la clave local de PostgreSQL configurada en el script
Table: datos_naranjas
```

12. Visualiza en el dashboard los campos acumulados de la tabla:

```sql
SELECT
  id_naranja,
  n_naranjas_procesadas,
  n_naranjas_mesa,
  n_naranjas_zumo,
  n_naranjas_rechazo
FROM datos_naranjas
ORDER BY id_naranja;
```

## Notas

- La simulacion se detiene automaticamente al terminar el ciclo completo.
- Si quieres repetir una prueba limpia, puedes borrar las filas de la tabla desde PostgreSQL antes de ejecutar de nuevo:

```sql
TRUNCATE TABLE datos_naranjas RESTART IDENTITY;
```

- El script espera encontrar `psql.exe` en `C:\Program Files\PostgreSQL\15\bin\psql.exe`.

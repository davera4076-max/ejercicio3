# Ecotech — Panel de Sustentabilidad (SIN base de datos)

Proyecto Django que calcula emisiones de carbono a partir del consumo
eléctrico (kWh) por planta y muestra un panel con totales.
Trabaja 100% en memoria: no usa modelos ni archivo `db.sqlite3`.

## Estructura

```
ecotech/
  manage.py
  ecotech/                 <- paquete del proyecto (settings, urls)
    settings.py            <- configuración general (documentada)
    urls.py                <- rutas principales: / , /panel/ (sin admin)
    wsgi.py / asgi.py      <- puntos de entrada para despliegues
  sustentabilidad/         <- app de negocio
    service.py             <- lógica de cálculo (documentada)
    views.py               <- vista del panel (documentada)
    urls.py                <- ruta de la app ("" -> panel)
    tests.py               <- tests unitarios (documentados)
    models.py / apps.py / admin.py  <- configuración de la app (documentados)
    templates/
      sustentabilidad/panel.html  <- plantilla que usa la vista
```

## Cómo ejecutar

Desde la carpeta donde está `manage.py`:

```powershell
cd "C:\Users\Daniel Vera\Desktop\ecotech\ecotech"

# 1) Tests (verifica que todo funciona)
python manage.py test sustentabilidad -v 2

# 2) Servidor
python manage.py runserver
```

Abrir en el navegador:

- http://127.0.0.1:8000/panel/  (panel principal)
- http://127.0.0.1:8000/        (también panel, es la raíz)

> Sin base de datos no hay `/admin/` ni se usa `migrate`.

## Documentación por evento

Todos los archivos Python tienen docstrings en español que documentan
qué hace cada evento/función, sus parámetros, retorno y errores.

### `service.py`

- `calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4)`
  - Evento básico: convierte kWh en kg CO2.
  - Fórmula: `consumo * factor`. Default 0.4. `0` devuelve `0.0`.
  - Error: `ValueError` si consumo < 0.

- `obtener_metricas_consumo(registros)`
  - Evento de agregación: suma total, acumula por planta
    y encuentra la planta con mayor emisión.
  - Retorna dict: `total_global_emisiones`, `emisiones_por_planta`,
    `planta_mayor_consumo` (None si lista vacía).
  - Planta vacía/`" "` => `"Planta desconocida"`. Planta repetida => se suma.

- Bloque `if __name__ == "__main__":`
  - Solo corre con `python service.py`, no al importar (no rompe tests).

### `views.py`

- `vista_panel_sustentabilidad(request)`
  - Evento HTTP GET (`/` y `/panel/`). Arma registros de ejemplo,
    llama a `obtener_metricas_consumo()`, crea contexto
    (`total_global_emisiones`, `emisiones_por_planta`, `planta_mayor_consumo`)
    y renderiza `sustentabilidad/panel.html`.

### `urls.py` (proyecto y app)

- `ecotech/urls.py`: `admin/`, `""` y `"panel/"` (ambos delegan en la app).
- `sustentabilidad/urls.py`: `""` -> panel, nombre `panel_sustentabilidad`.

### `tests.py`

- `TestCalculoEmisiones.test_calculo_nominal_default`: 100*0.4=40.0
- `TestCalculoEmisiones.test_factor_personalizado`: 250*0.5=125.0
- `TestCalculoEmisiones.test_consumo_cero`: 0 válido
- `TestCalculoEmisiones.test_consumo_negativo`: debe lanzar ValueError
- `TestObtenerMetricasConsumo.test_metricas_con_datos`: total 6180.2,
  Tupungato 3120.2 acumulado, blanco=>desconocida, mayor=Tupungato
- `TestObtenerMetricasConsumo.test_metricas_sin_registros`: [] => ceros/None

### `settings.py` / `apps.py` / `models.py` / `admin.py`

- Documentan qué hace cada configuración. `settings.py` incluye
  `'sustentabilidad'` en `INSTALLED_APPS` (sin esto no funciona).
- `templates/sustentabilidad/panel.html` tiene comentario de cabecera
  que documenta las variables que espera y los filtros usados.

## Datos de ejemplo

```python
[
    {"planta": "Planta Tupungato", "consumo_kwh": 3000.50},
    {"planta": "Planta Tupungato", "consumo_kwh": 4800},
    {"planta": "Planta Tunuyán", "consumo_kwh": 2000},
    {"planta": "Planta San Carlos", "consumo_kwh": 1500},
    {"planta": "Planta San Rafael", "consumo_kwh": 2050},
    {"planta": " ", "consumo_kwh": 2100},
]
```

Resultado esperado:
- Total global: 6180.2 kg CO2
- Planta mayor: Planta Tupungato (3120.2 kg CO2)

## Notas sobre errores comunes

- `can't open file '...manage.py'`: estás parado un nivel arriba.
  Debés estar en la carpeta que CONTIENE manage.py.
- `404 en /panel/` + solo `admin/` en la lista: faltaba incluir la app
  en `ecotech/urls.py` y/o `sustentabilidad/urls.py` vacío.
- `TemplateDoesNotExist: sustentabilidad/panel.html`: la plantilla debe
  estar en `templates/sustentabilidad/panel.html` (carpeta con el
  nombre de la app), no solo en `templates/panel.html`.
- `NameError: consumo is not defined`: la variable es `consumo_kwh`.
- `is 0` en Python es incorrecto para comparar números: usar `==` o `< 0`.

# sustentabilidad/service.py
"""
Lógica de negocio (cálculos) para la app `sustentabilidad`.

Este módulo concentra TODAS las reglas de cálculo, sin depender de Django
(sin base de datos, sin HTTP, sin templates). Así se puede probar con
tests unitarios puros (`python manage.py test sustentabilidad`) y reutilizar
desde vistas, scripts o consola.

Contenido:
- `calcular_emisiones_carbono()`: calcula kg CO2 a partir de kWh.
- `obtener_metricas_consumo()`: agrega consumos por planta y encuentra
la planta con mayor emisión.

Convenciones:
- Consumo siempre en kWh (kilowatt-hora), float o int.
- Factor de emisión por defecto 0.4 kg CO2 por kWh
(puede cambiarse vía parámetro `factor_emision`).
- Planta vacía / espacios en blanco => "Planta desconocida".
- Consumo negativo => ValueError (no tiene sentido físico).
"""

# ---------------------------------------------------------------------------
# Evento / función: cálculo de emisiones
# ---------------------------------------------------------------------------


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """
    Calcula las emisiones de carbono en kg de CO2.

    Evento:
        Se invoca cuando se quiere convertir un consumo energético
        (kWh) en emisiones equivalentes de carbono. Es la unidad
        básica de todo el panel: cualquier métrica mayor se deriva
        de esta función.

    Fórmula:
        emisiones = consumo_kwh * factor_emision

    Parámetros:
        consumo_kwh (float|int): consumo eléctrico en kilowatt-hora.
            Debe ser >= 0. El 0 es válido y devuelve 0.0.
        factor_emision (float, opcional): factor kg CO2 por kWh.
            Por defecto 0.4. Se puede personalizar si cambia
            el mix energético (ej: 0.5 para una fuente más contaminante).

    Retorna:
        float: emisiones en kg CO2.
            Ejemplo: 100 kWh * 0.4 = 40.0 kg CO2.

    Lanza:
        ValueError: si `consumo_kwh < 0`.
            Mensaje: "El consumo en Kwh no puede ser negativo".

    Ejemplos:
        >>> calcular_emisiones_carbono(100)
        40.0
        >>> calcular_emisiones_carbono(250, factor_emision=0.5)
        125.0
        >>> calcular_emisiones_carbono(0)
        0.0
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo en Kwh no puede ser negativo")
    return consumo_kwh * factor_emision


# ---------------------------------------------------------------------------
# Evento / función: agregación de métricas
# ---------------------------------------------------------------------------


def obtener_metricas_consumo(registros):
    """
    Agrega registros de consumo y calcula métricas globales y por planta.

    Evento:
        Se invoca desde la vista `vista_panel_sustentabilidad` (y desde
        tests) para resumir el historial de consumos. Recorre cada
        registro, calcula sus emisiones con `calcular_emisiones_carbono()`,
        suma el total global, acumula por planta y detecta la planta
        con mayor emisión (que equivale a la de mayor consumo,
        ya que el factor es constante).

    Parámetros:
        registros (list[dict]): lista de dicts, cada uno con las claves:
            - "planta" (str, opcional): nombre de la planta.
              Si falta o es "" / " ", se usa "Planta desconocida".
            - "consumo_kwh" (float|int, opcional): consumo en kWh.
              Si falta, se usa 0.0.

    Retorna:
        dict con tres claves:
            - "total_global_emisiones" (float):
              suma de todas las emisiones (kg CO2).
            - "emisiones_por_planta" (dict[str, float]):
              emisiones acumuladas por planta.
              Ej: {"Planta Tupungato": 3120.2, ...}.
            - "planta_mayor_consumo" (str | None):
              nombre de la planta con mayor emisión acumulada,
              o None si `registros` está vacía.

    Casos borde:
        - Lista vacía [] => total 0.0, detalle {}, mayor None.
        - Planta repetida => se suman sus registros (acumulación).
        - Planta en blanco => se agrupa como "Planta desconocida".
        - Consumo negativo en algún registro => ValueError propagate.

    Ejemplo:
        >>> obtener_metricas_consumo([
        ...     {"planta": "Planta Tupungato", "consumo_kwh": 3000.50},
        ...     {"planta": "Planta Tupungato", "consumo_kwh": 4800},
        ...     {"planta": "Planta Tunuyán", "consumo_kwh": 2000},
        ... ])["planta_mayor_consumo"]
        'Planta Tupungato'
    """
    total_global_emisiones = 0.0
    emisiones_por_planta = {}
    planta_mayor_consumo = None
    mayor_emision = -1

    # Paso 1: recorrer registros, calcular emisiones y acumular.
    for registro in registros:
        planta = registro.get("planta", "Planta desconocida")
        # Normalizar planta vacía o solo espacios.
        if not str(planta).strip():
            planta = "Planta desconocida"
        consumo_kwh = registro.get("consumo_kwh", 0.0)

        # Reutiliza la función base -> si consumo < 0 lanza ValueError.
        emisiones = calcular_emisiones_carbono(consumo_kwh)
        total_global_emisiones += emisiones

        if planta not in emisiones_por_planta:
            emisiones_por_planta[planta] = 0.0

        emisiones_por_planta[planta] += emisiones

    # Paso 2: encontrar la planta con mayor emisión acumulada.
    for planta, emisiones in emisiones_por_planta.items():
        if emisiones > mayor_emision:
            mayor_emision = emisiones
            planta_mayor_consumo = planta

    return {
        "total_global_emisiones": total_global_emisiones,
        "emisiones_por_planta": emisiones_por_planta,
        "planta_mayor_consumo": planta_mayor_consumo,
    }


# ---------------------------------------------------------------------------
# Uso manual: python service.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    Demostración ejecutable con `python service.py`.

    No se ejecuta al importar el módulo (importar no debe tener
    efectos secundarios). Solo corre cuando se ejecuta directamente,
    por eso está bajo `if __name__ == "__main__":`.
    """
    registro_historicos = [
        {"planta": "Planta Tupungato", "consumo_kwh": 3000.50},
        {"planta": "Planta Tupungato", "consumo_kwh": 4800},
        {"planta": "Planta Tunuyán", "consumo_kwh": 2000},
        {"planta": "Planta San Carlos", "consumo_kwh": 1500},
        {"planta": "Planta San Rafael", "consumo_kwh": 2050},
        {"planta": " ", "consumo_kwh": 2100},
    ]

    resultado = obtener_metricas_consumo(registro_historicos)
    print("Total global de emisiones de carbono:", resultado["total_global_emisiones"])
    print("Emisiones por planta:", resultado["emisiones_por_planta"])
    print("Planta con mayor consumo (mayor emisión):", resultado["planta_mayor_consumo"])

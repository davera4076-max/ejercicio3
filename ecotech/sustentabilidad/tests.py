# sustentabilidad/tests.py
"""
Tests automatizados para la app `sustentabilidad`.

Se ejecutan con:
    python manage.py test sustentabilidad -v 2

Verifica la lógica de cálculo de emisiones de carbono
definida en `sustentabilidad/service.py`.

Organización:
- `TestCalculoEmisiones`: tests unitarios de `calcular_emisiones_carbono()`.
  Cubre caso nominal, factor personalizado, consumo cero y error negativo.
- `TestObtenerMetricasConsumo`: tests de `obtener_metricas_consumo()`.
  Cubre datos completos, acumulación por planta, planta en blanco
  y lista vacía.

Notas sobre eventos de test:
- Cada método `test_*` es un "evento de prueba" independiente.
- `setUp()` (si existiera) se ejecutaría antes de cada test para
  preparar datos; acá los datos se crean dentro de cada test.
- `assertEqual`, `assertIsNone`, `assertRaises` son aserciones de unittest.
"""

import unittest

from .service import calcular_emisiones_carbono, obtener_metricas_consumo


class TestCalculoEmisiones(unittest.TestCase):
    """
    Eventos de test para `calcular_emisiones_carbono()`.

    Cada método prueba un escenario distinto de la función.
    """

    def test_calculo_nominal_default(self):
        """
        Evento: cálculo nominal con factor por defecto.

        Entrada:  consumo = 100 Kwh, factor = 0.4 (defecto)
        Esperado: 100 * 0.4 = 40.0 kg CO2

        Documenta que el default es 0.4 y que la función
        no requiere pasar el factor.
        """
        resultado = calcular_emisiones_carbono(100)
        self.assertEqual(resultado, 40.0)

    def test_factor_personalizado(self):
        """
        Evento: cálculo con factor de emisión personalizado.

        Entrada:  consumo = 250 Kwh, factor = 0.5
        Esperado: 250 * 0.5 = 125.0 kg CO2

        Documenta el parámetro opcional `factor_emision`.
        """
        resultado = calcular_emisiones_carbono(250, factor_emision=0.5)
        self.assertEqual(resultado, 125.0)

    def test_consumo_cero(self):
        """
        Evento: caso borde, consumo igual a 0.

        Entrada:  consumo = 0 Kwh
        Esperado: 0 * 0.4 = 0.0

        Documenta que 0 es válido y NO debe lanzar excepción.
        (Antes el código usaba `is 0`, que es incorrecto en Python).
        """
        resultado = calcular_emisiones_carbono(0)
        self.assertEqual(resultado, 0)

    def test_consumo_negativo(self):
        """
        Evento: caso de error, consumo negativo.

        Entrada:  consumo = -50 Kwh
        Esperado: lanza ValueError

        Documenta la validación: no puede haber consumo físico negativo.
        Usa `assertRaises` como context manager (forma moderna).
        """
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50)


class TestObtenerMetricasConsumo(unittest.TestCase):
    """
    Eventos de test para `obtener_metricas_consumo()`.

    Verifican la agregación global, por planta y la detección
    de la planta con mayor consumo/emisión.
    """

    def test_metricas_con_datos(self):
        """
        Evento: métricas con datos completos y planta repetida.

        Datos: Tupungato aparece 2 veces (3000.50 + 4800),
        más 4 plantas simples (incluye una en blanco).

        Esperado:
            - Total = (3000.50+4800+2000+1500+2050+2100)*0.4 = 6180.2
            - Tupungato = (3000.50+4800)*0.4 = 3120.2 (acumulación)
            - " " se convierte en "Planta desconocida" = 840.0
            - Mayor consumo = "Planta Tupungato"

        Documenta: acumulación, normalización de nombre y cálculo del máximo.
        """
        registros = [
            {"planta": "Planta Tupungato", "consumo_kwh": 3000.50},
            {"planta": "Planta Tupungato", "consumo_kwh": 4800},
            {"planta": "Planta Tunuyán", "consumo_kwh": 2000},
            {"planta": "Planta San Carlos", "consumo_kwh": 1500},
            {"planta": "Planta San Rafael", "consumo_kwh": 2050},
            {"planta": " ", "consumo_kwh": 2100},
        ]

        resultado = obtener_metricas_consumo(registros)

        # Total global de emisiones.
        self.assertEqual(resultado["total_global_emisiones"], 6180.2)

        # Acumulación de Tupungato (dos registros sumados).
        self.assertEqual(
            resultado["emisiones_por_planta"]["Planta Tupungato"],
            3120.2,
        )

        # Planta en blanco se trata como desconocida.
        self.assertEqual(
            resultado["emisiones_por_planta"]["Planta desconocida"],
            840.0,
        )

        # Planta con mayor emisión (= mayor consumo).
        self.assertEqual(
            resultado["planta_mayor_consumo"],
            "Planta Tupungato",
        )

    def test_metricas_sin_registros(self):
        """
        Evento: caso borde, lista vacía.

        Entrada:  []
        Esperado: total 0.0, detalle {}, mayor consumo None.

        Documenta que la función no falla con entradas vacías.
        """
        resultado = obtener_metricas_consumo([])

        self.assertEqual(resultado["total_global_emisiones"], 0.0)
        self.assertEqual(resultado["emisiones_por_planta"], {})
        self.assertIsNone(resultado["planta_mayor_consumo"])


# Permite ejecutar los tests directamente con:
#   python -m unittest sustentabilidad.tests
# o desde la raíz del proyecto con manage.py test.
if __name__ == "__main__":
    unittest.main()

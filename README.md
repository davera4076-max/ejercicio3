<<<<<<< HEAD
# Ejercicio3

•	Punto A: Auditoría de Algoritmo de Emisiones ( unittest ): A partir de la función calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4) (la cual eleva ValueError si el consumo es negativo), implementa la clase de prueba TestCalculoEmisiones(unittest.TestCase). Diseña los casos de prueba necesarios para validar tanto la exactitud numérica del cálculo ante valores nominales como la correcta elevación de la excepción ante consumos fuera de rango.
•	Punto B: Procesamiento de Métricas y Renderizado Web: Incorpora la función calcular_emisiones_carbono en la función obtener_metricas_consumo(registros), procesando un historial de consumos por planta industrial para determinar el total global de emisiones y la planta de mayor consumo. Por último, diseña la función de vista en Django vista_panel_sustentabilidad(request) que invoque dicho procesamiento y proporcione el diccionario de contexto listo para ser renderizado en la plantilla sustentabilidad/panel.html.

```

## 3. Requisitos

- Python 3.10 o superior
- Solo librería estándar: `json` (no requiere pip install)

## 4. Cómo ejecutar

```bash
python catalogo_ecotech.py
```

**Salida esperada en consola:**

```
Código: PS-001 
Nombre: Panel solar monocristalino 450 W
Precio: 289.9
Stock: 12 
Potencia: 450 W
Eficiencia: 22.5%
----------------------------------------
Código: PS-002 
Nombre: Panel solar policristalino 300 W
Precio: 169.5
Stock: 7 
Potencia: 300 W
Eficiencia: 18.2%
----------------------------------------
Código: INV-001 
Nombre: Inversor híbrido 3000 VA
Precio: 649.0
Stock: 5 
Potencia salida: 3000 W
Tipo onda: Senoidal pura
----------------------------------------
Código: BAT-001 
Nombre: Batería litio 200 Ah 24V
Precio: 899.0
Stock: 4 
Capacidad: 200 Ah
Voltaje: 24 V
Tecnología: LiFePO4
----------------------------------------
Error controlado: El stock no puede ser negativo
Catalogo guardado exitosamente.
```

## 5. Punto A — Dominio del Catálogo y Reglas de Inventario

### 5.1 Excepción personalizada

```python
class StockInvalidoError(Exception):
    pass
```

Se lanza cuando se intenta asignar stock negativo. Permite captura controlada:

```python
try:
    panel1.asignar_stock(-5)
except StockInvalidoError as error:
    print(f"Error controlado: {error}")
# → Error controlado: El stock no puede ser negativo
```

### 5.2 Jerarquía de clases

| Clase | Hereda de | Atributos propios | Método sobrescrito |
| :--- | :--- | :--- | :--- |
| `DispositivoEcologico` | — | `codigo`, `nombre`, `precio`, `stock` | `mostrar_ficha_tecnica()` (base) |
| `PanelSolar` | `DispositivoEcologico` | `potencia_w`, `eficiencia` | `mostrar_ficha_tecnica()` |
| `Inversor` | `DispositivoEcologico` | `potencia_salida_w`, `tipo_onda` | `mostrar_ficha_tecnica()` |
| `Bateria` | `DispositivoEcologico` | `capacidad_ah`, `voltaje_v`, `tecnologia` | `mostrar_ficha_tecnica()` |

**Encapsulamiento:** atributos privados `_codigo`, `_stock`, etc. + propiedades `@property` de solo lectura (`codigo`, `stock`, `potencia_w`, ...).

**Validación centralizada:**

```python
def asignar_stock(self, nuevo_stock):
    if nuevo_stock < 0:
        raise StockInvalidoError("El stock no puede ser negativo")
    self._stock = nuevo_stock
```

Todos los setters passam por este método, incluso el `__init__` (`self._stock = 0` → `self.asignar_stock(stock)`).

**Herencia:** las subclases llaman `super().__init__(codigo, nombre, precio, stock)` y agregan sus atributos.

**Polimorfismo:** una sola lista heterogénea:

```python
productos = [panel1, panel2, inversor1, bateria1]
for p in productos:
    print(p.mostrar_ficha_tecnica())  # cada clase responde distinto
```

## 6. Punto B — Persistencia y Gestión del Catálogo

### 6.1 GestorInventario

```python
GestorInventario().guardar_catalogo_json(productos, "catalogo_ecotech.json")
```

El método:

1. Recorre la lista polimórfica.
2. Crea un dict común (`codigo`, `nombre`, `precio`, `stock`).
3. Detecta el tipo con `isinstance()` y agrega los atributos específicos.
4. Escribe con `json.dump(..., indent=4)`.

### 6.2 Archivo generado `catalogo_ecotech.json`

```json
[
    {
        "codigo": "PS-001",
        "nombre": "Panel solar monocristalino 450 W",
        "precio": 289.9,
        "stock": 12,
        "tipo": "PanelSolar",
        "potencia_w": 450,
        "eficiencia": 22.5
    },
    {
        "codigo": "PS-002",
        "nombre": "Panel solar policristalino 300 W",
        "precio": 169.5,
        "stock": 7,
        "tipo": "PanelSolar",
        "potencia_w": 300,
        "eficiencia": 18.2
    },
    {
        "codigo": "INV-001",
        "nombre": "Inversor híbrido 3000 VA",
        "precio": 649.0,
        "stock": 5,
        "tipo": "Inversor",
        "potencia_salida_w": 3000,
        "tipo_onda": "Senoidal pura"
    },
    {
        "codigo": "BAT-001",
        "nombre": "Batería litio 200 Ah 24V",
        "precio": 899.0,
        "stock": 4,
        "tipo": "Bateria",
        "capacidad_ah": 200,
        "voltaje_v": 24,
        "tecnologia": "LiFePO4"
    }
]
```

### 6.3 Flujo de prueba (bloque `if __name__ == "__main__"`)

1. Crea 2 paneles, 1 inversor y 1 batería.
2. Imprime las 4 fichas técnicas (polimorfismo).
3. Intenta `panel1.asignar_stock(-5)` → captura controlada con `StockInvalidoError`.
4. Exporta los productos válidos a `catalogo_ecotech.json`.

## 7. Nombres de compatibilidad

El código original usaba otros nombres; se incluyen alias:

```python
EquipoEnergetico = DispositivoEcologico
PanelFotovoltaico = PanelSolar
AdministradorCatalogo = GestorInventario
```

Así funciona con cualquier nombre que use el docente.

## 8. Docstrings

Todo el código está documentado con **docstrings Google Style** (módulo, clases, métodos, parámetros, retornos y excepciones) y type hints, para generar documentación automática con `pydoc` o Sphinx.
>>>>>>> 6752afe05a4ffa5deee46a5aa8708d19634ecbb0

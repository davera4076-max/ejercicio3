"""
Módulo: catalogo_ecotech.py
División: Equipamiento Sustentable - EcoTech Solutions

Descripción:
    Gestiona el catálogo de productos ecológicos, valida el inventario
    para impedir stock negativo y persiste el catálogo en formato JSON.

Puntos cubiertos:
    - Punto A: Dominio del Catálogo y Reglas de Inventario (excepción,
      herencia y polimorfismo)
    - Punto B: Persistencia y Gestión del Catálogo (JSON + prueba try/except)

Formato de salida:
    La ficha técnica usa colores ANSI nativos (sin dependencias externas)
    para resaltar relevancia: cabecera, negrita en etiquetas, precio
    destacado en verde y stock en verde (disponible) o amarillo (bajo).

Autor: EcoTech Solutions
Archivo generado: catalogo_ecotech.json
"""

import json
import os
import sys

# Activar colores ANSI en cmd clásico de Windows (en Windows Terminal / PS7 ya vienen activos)
if sys.platform == "win32":
    os.system("")  # noqa: S605 - activa VT processing para ANSI

# Forzar UTF-8 en la consola para poder mostrar =, ☀, , etc.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# =============================================================================
# FORMATO ANSI NATIVO (colores + negrita, sin librerías externas)
# =============================================================================
# códigos: 
#   \033[1m = negrita | \033[0m = reset
#   \033[36m cian | \033[32m verde | \033[33m amarillo | \033[97m blanco brillante
RESET = "\033[0m"
NEGRITA = "\033[1m"
CIAN = "\033[36m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
BLANCO = "\033[97m"


def negrita(texto: str) -> str:
    """Devuelve el texto en negrita."""
    return f"{NEGRITA}{texto}{RESET}"


def color(texto: str, codigo: str) -> str:
    """Devuelve el texto con el color ANSI indicado."""
    return f"{codigo}{texto}{RESET}"


def _cabecera_ficha(titulo: str = "FICHA TÉCNICA") -> str:
    """Línea de separación superior con título (relevancia visual)."""
    return negrita(color(f"\n{'=' * 14} {titulo} {'=' * 14}", CIAN))


def _pie_ficha() -> str:
    """Línea de cierre inferior."""
    return negrita(color("=" * 42, CIAN))


def _formatear_precio(precio: float) -> str:
    """Precio destacado en verde + negrita, ej: $289.90"""
    return negrita(color(f"${precio:.2f}", VERDE))


def _formatear_stock(stock: int) -> str:
    """
    Re­levancia según nivel:
      - stock > 5  -> VERDE (disponible)
      - stock <= 5 -> AMARILLO (stock bajo, conviene reponer)
    """
    if stock <= 5:
        return negrita(color(f"{stock} stock bajo", AMARILLO))
    return negrita(color(f"{stock} disponible", VERDE))


class StockInvalidoError(Exception):
    """
    Excepción personalizada para errores de inventario.

    Se lanza cuando se intenta asignar un stock negativo a un
    DispositivoEcologico. Permite captura controlada con try/except.

    Example:
        >>> raise StockInvalidoError("El stock no puede ser negativo")
    """
    pass


class DispositivoEcologico:
    """
    Clase base para todos los productos ecológicos.

    Encapsula los atributos comunes y centraliza la validación
    de stock mediante asignar_stock().

    Attributes:
        _codigo (str): Código único, ej: "PS-001"
        _nombre (str): Nombre comercial del producto
        _precio (float): Precio de venta
        _stock (int): Cantidad disponible, nunca negativa

    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        """
        Inicializa el dispositivo y valida el stock inicial.

        Args:
            codigo: Identificador único del producto.
            nombre: Nombre del producto.
            precio: Precio unitario.
            stock: Cantidad inicial en inventario.

        Raises:
            StockInvalidoError: Si stock < 0.
        """
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._stock = 0
        self.asignar_stock(stock)  # Validación centralizada

    # --- Encapsulamiento: Properties de solo lectura ---
    @property
    def codigo(self) -> str:
        """str: Código del dispositivo."""
        return self._codigo

    @property
    def nombre(self) -> str:
        """str: Nombre del dispositivo."""
        return self._nombre

    @property
    def precio(self) -> float:
        """float: Precio del dispositivo."""
        return self._precio

    @property
    def stock(self) -> int:
        """int: Stock actual del dispositivo."""
        return self._stock

    def asignar_stock(self, nuevo_stock: int) -> None:
        """
        Asigna un nuevo valor al stock verificando la regla de negocio.

        Args:
            nuevo_stock: Nueva cantidad a asignar.

        Raises:
            StockInvalidoError: Si nuevo_stock es negativo.
        """
        if nuevo_stock < 0:
            raise StockInvalidoError("El stock no puede ser negativo")
        self._stock = nuevo_stock

    def obtener_stock(self) -> int:
        """Retorna el stock actual del dispositivo."""
        return self._stock

    def _lineas_base(self) -> list[str]:
        """
        Líneas comunes con formato (relevancia: negrita en etiquetas,
        nombre en blanco brillante, precio en verde, stock según nivel).
        """
        return [
            f"  {negrita('Código:'):12} {self._codigo}",
            f"  {negrita('Nombre:'):12} {negrita(color(self._nombre, BLANCO))}",
            f"  {negrita('Precio:'):12} {_formatear_precio(self._precio)}",
            f"  {negrita('Stock:'):12} {_formatear_stock(self._stock)}",
        ]

    def mostrar_ficha_tecnica(self) -> str:
        """
        Retorna la ficha técnica básica del dispositivo.

        Returns:
            str: Ficha con formato de relevancia (ANSI).
        """
        lineas = [_cabecera_ficha("FICHA TÉCNICA"), *self._lineas_base(), _pie_ficha()]
        return "\n".join(lineas)


# =============================================================================
# PUNTO A: Clases especializadas (Herencia + Polimorfismo)
# =============================================================================

class PanelSolar(DispositivoEcologico):
    """
    Panel fotovoltaico. Hereda de DispositivoEcologico.

    Attributes:
        _potencia_w (int): Potencia máxima en Watts.
        _eficiencia (float): Eficiencia de conversión en %.

    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int,
                 potencia_w: int, eficiencia: float):
        """
        Args:
            codigo, nombre, precio, stock: Atributos heredados.
            potencia_w: Potencia nominal del panel.
            eficiencia: Eficiencia de conversión energética.
        """
        super().__init__(codigo, nombre, precio, stock)
        self._potencia_w = potencia_w
        self._eficiencia = eficiencia

    @property
    def potencia_w(self) -> int:
        """int: Potencia del panel en Watts."""
        return self._potencia_w

    @property
    def eficiencia(self) -> float:
        """float: Eficiencia del panel en %."""
        return self._eficiencia

    def mostrar_ficha_tecnica(self) -> str:
        """
        Sobrescribe el método base (polimorfismo).

        Agrega potencia_w y eficiencia a la ficha comercial.
        Relevancia: potencia en cian + negrita.

        Returns:
            str: Ficha técnica completa del panel solar.
        """
        lineas = [
            _cabecera_ficha("PANEL SOLAR"),
            *self._lineas_base(),
            f"  {negrita('Potencia:'):12} {negrita(color(f'{self._potencia_w} W', CIAN))}",
            f"  {negrita('Eficiencia:'):12} {self._eficiencia}%",
            _pie_ficha(),
        ]
        return "\n".join(lineas)


class Inversor(DispositivoEcologico):
    """
    Inversor híbrido para sistemas solares.

    Attributes:
        _potencia_salida_w (int): Potencia de salida en Watts.
        _tipo_onda (str): Ej: "Senoidal pura", "Senoidal modificada".
    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int,
                 potencia_salida_w: int, tipo_onda: str):
        """Inicializa el inversor con sus atributos específicos."""
        super().__init__(codigo, nombre, precio, stock)
        self._potencia_salida_w = potencia_salida_w
        self._tipo_onda = tipo_onda

    @property
    def potencia_salida_w(self) -> int:
        """int: Potencia de salida en Watts."""
        return self._potencia_salida_w

    @property
    def tipo_onda(self) -> str:
        """str: Tipo de onda de salida."""
        return self._tipo_onda

    def mostrar_ficha_tecnica(self) -> str:
        """Retorna ficha técnica del inversor (polimorfismo)."""
        lineas = [
            _cabecera_ficha("INVERSOR"),
            *self._lineas_base(),
            f"  {negrita('Potencia:'):12} {negrita(color(f'{self._potencia_salida_w} W', CIAN))}  (salida)",
            f"  {negrita('Tipo onda:'):12} {self._tipo_onda}",
            _pie_ficha(),
        ]
        return "\n".join(lineas)


class Bateria(DispositivoEcologico):
    """
    Batería para almacenamiento de energía.

    Attributes:
        _capacidad_ah (int): Capacidad en Amperios-hora.
        _voltaje_v (int): Voltaje nominal.
        _tecnologia (str): Ej: "LiFePO4", "Plomo-ácido".
    """

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int,
                 capacidad_ah: int, voltaje_v: int, tecnologia: str):
        """Inicializa la batería con sus atributos específicos."""
        super().__init__(codigo, nombre, precio, stock)
        self._capacidad_ah = capacidad_ah
        self._voltaje_v = voltaje_v
        self._tecnologia = tecnologia

    @property
    def capacidad_ah(self) -> int:
        """int: Capacidad en Ah."""
        return self._capacidad_ah

    @property
    def voltaje_v(self) -> int:
        """int: Voltaje nominal."""
        return self._voltaje_v

    @property
    def tecnologia(self) -> str:
        """str: Tecnología de la batería."""
        return self._tecnologia

    def mostrar_ficha_tecnica(self) -> str:
        """Retorna ficha técnica de la batería (polimorfismo)."""
        lineas = [
            _cabecera_ficha("BATERÍA"),
            *self._lineas_base(),
            f"  {negrita('Capacidad:'):12} {negrita(color(f'{self._capacidad_ah} Ah', CIAN))}",
            f"  {negrita('Voltaje:'):12} {self._voltaje_v} V",
            f"  {negrita('Tecnología:'):12} {self._tecnologia}",
            _pie_ficha(),
        ]
        return "\n".join(lineas)


# Alias de compatibilidad con nombres originales del ejercicio
EquipoEnergetico = DispositivoEcologico
PanelFotovoltaico = PanelSolar


# =============================================================================
# PUNTO B: Persistencia y Gestión del Catálogo
# =============================================================================

class GestorInventario:
    """
    Gestiona el inventario y la persistencia en disco.

    La clase recorre una lista polimórfica de dispositivos y serializa
    cada instancia a un diccionario JSON, agregando los atributos
    propios según el tipo detectado con isinstance().
    """

    def guardar_catalogo_json(self, lista_dispositivos: list, ruta_archivo: str) -> None:
        """
        Serializa la lista de dispositivos en un archivo JSON.

        Args:
            lista_dispositivos: Lista de instancias de DispositivoEcologico
                y sus subclases.
            ruta_archivo: Ruta de destino, ej: "catalogo_ecotech.json".

        Comportamiento:
            - Siempre guarda: codigo, nombre, precio, stock, tipo.
            - Si es PanelSolar: agrega potencia_w, eficiencia.
            - Si es Inversor: agrega potencia_salida_w, tipo_onda.
            - Si es Bateria: agrega capacidad_ah, voltaje_v, tecnologia.
        """
        catalogo = []
        for dispositivo in lista_dispositivos:
            producto = {
                "codigo": dispositivo.codigo,
                "nombre": dispositivo.nombre,
                "precio": dispositivo.precio,
                "stock": dispositivo.stock
            }

            # Detección de tipo para persistir atributos específicos
            if isinstance(dispositivo, PanelSolar):
                producto["tipo"] = "PanelSolar"
                producto["potencia_w"] = dispositivo.potencia_w
                producto["eficiencia"] = dispositivo.eficiencia

            elif isinstance(dispositivo, Inversor):
                producto["tipo"] = "Inversor"
                producto["potencia_salida_w"] = dispositivo.potencia_salida_w
                producto["tipo_onda"] = dispositivo.tipo_onda

            elif isinstance(dispositivo, Bateria):
                producto["tipo"] = "Bateria"
                producto["capacidad_ah"] = dispositivo.capacidad_ah
                producto["voltaje_v"] = dispositivo.voltaje_v
                producto["tecnologia"] = dispositivo.tecnologia

            catalogo.append(producto)

        # Persistencia: escribe el catálogo con formato legible
        with open(ruta_archivo, "w", encoding="utf-8") as file:
            json.dump(catalogo, file, indent=4)
        print(f"{VERDE}{RESET} {negrita('Catalogo guardado exitosamente.')}")


AdministradorCatalogo = GestorInventario


# =============================================================================
# Bloque de prueba: captura controlada y exportación
# =============================================================================

if __name__ == "__main__":
    """
    Flujo de prueba solicitado en la consigna:
    1. Creación de instancias válidas.
    2. Intento de asignación de stock erróneo (-5) con captura.
    3. Exportación exitosa a catalogo_ecotech.json.
    """
    try:
        # --- Creación de productos válidos (Punto A) ---
        panel1 = PanelSolar("PS-001", "Panel solar monocristalino 450 W", 289.90, 12, 450, 22.5)
        panel2 = PanelSolar("PS-002", "Panel solar policristalino 300 W", 169.50, 7, 300, 18.2)
        inversor1 = Inversor("INV-001", "Inversor híbrido 3000 VA", 649.00, 5, 3000, "Senoidal pura")
        bateria1 = Bateria("BAT-001", "Batería litio 200 Ah 24V", 899.00, 4, 200, 24, "LiFePO4")

        productos = [panel1, panel2, inversor1, bateria1]

        # Demostración de polimorfismo: mismo método, distinta salida
        for p in productos:
            print(p.mostrar_ficha_tecnica())
            print()

    except StockInvalidoError as error:
        print(f"{AMARILLO} Error controlado:{RESET} {error}")

    # --- Prueba de captura controlada (Punto B) ---
    try:
        panel1.asignar_stock(-5)
    except StockInvalidoError as error:
        print(f"{AMARILLO} Error controlado:{RESET} {error}")

    # --- Exportación exitosa (Punto B) ---
    gestor = GestorInventario()
    gestor.guardar_catalogo_json(productos, "catalogo_ecotech.json")

import pytest

from src.main import (
    aplicar_descuentos_ejemplo,
    crear_catalogo_inicial,
    crear_comedores_ejemplo,
)
from src.services.tienda import TiendaMuebles


@pytest.mark.integration
class TestIntegracionTienda:

    def test_flujo_completo_catalogo_descuento_venta_y_reporte(self):
        tienda = TiendaMuebles("Mueblería Integración")

        crear_catalogo_inicial(tienda)
        crear_comedores_ejemplo(tienda)
        aplicar_descuentos_ejemplo(tienda)

        total_inicial = len(tienda._inventario)
        silla = next(m for m in tienda._inventario if type(m).__name__ == "Silla")

        venta = tienda.realizar_venta(silla, "Lina")
        reporte = tienda.generar_reporte_inventario()

        assert venta["cliente"] == "Lina"
        assert venta["descuento"] == 10.0
        assert len(tienda._inventario) == total_inicial - 1
        assert "REPORTE DE INVENTARIO - Mueblería Integración" in reporte
        assert "DESCUENTOS ACTIVOS:" in reporte
from unittest.mock import patch
import pytest

from src.services.tienda import TiendaMuebles


class Silla:
    def __init__(self, nombre="Silla Clásica", material="Madera", precio=100.0):
        self.nombre = nombre
        self.material = material
        self._precio = precio

    def calcular_precio(self):
        return self._precio


class MuebleErrorPrecio:
    def __init__(self, nombre="Mueble Roto", material="Metal"):
        self.nombre = nombre
        self.material = material

    def calcular_precio(self):
        raise RuntimeError("Error en precio")


class MuebleErrorMaterial:
    nombre = "Raro"

    @property
    def material(self):
        raise RuntimeError("Error leyendo material")

    def calcular_precio(self):
        return 50.0


class ComedorFake:
    def __init__(self, nombre="Comedor 4 Puestos"):
        self.nombre = nombre


class TestTiendaMueblesCompleto:

    @pytest.fixture
    def tienda(self):
        return TiendaMuebles("Mueblería Test")

    def test_init_y_nombre(self, tienda):
        assert tienda.nombre == "Mueblería Test"
        assert tienda._inventario == []
        assert tienda._comedores == []

    def test_agregar_mueble_casos(self, tienda):
        assert tienda.agregar_mueble(None) == "Error: El mueble no puede ser None"

        silla_cero = Silla(precio=0)
        assert (
            tienda.agregar_mueble(silla_cero)
            == "Error: El mueble debe tener un precio válido mayor a 0"
        )

        silla_error = MuebleErrorPrecio()
        assert "Error al calcular precio del mueble:" in tienda.agregar_mueble(
            silla_error
        )

        silla_ok = Silla("Silla Roble", "Madera", 120.0)
        msg = tienda.agregar_mueble(silla_ok)
        assert "agregado exitosamente al inventario" in msg
        assert len(tienda._inventario) == 1

    def test_agregar_comedor_casos(self, tienda):
        assert tienda.agregar_comedor(None) == "Error: El comedor no puede ser None"

        comedor = ComedorFake("Comedor Grande")
        msg = tienda.agregar_comedor(comedor)
        assert "Comedor Grande" in msg
        assert len(tienda._comedores) == 1

    def test_buscar_muebles_por_nombre(self, tienda):
        silla = Silla("Silla Moderna")
        tienda.agregar_mueble(silla)

        assert tienda.buscar_muebles_por_nombre("") == []
        assert tienda.buscar_muebles_por_nombre("   ") == []
        assert tienda.buscar_muebles_por_nombre("moderna") == [silla]
        assert tienda.buscar_muebles_por_nombre("mesa") == []

    def test_filtrar_por_precio_con_negativo_y_error(self, tienda):
        silla_barata = Silla("Silla Barata", precio=50.0)
        silla_cara = Silla("Silla Cara", precio=500.0)
        tienda._inventario = [silla_barata, silla_cara, MuebleErrorPrecio()]

        resultados = tienda.filtrar_por_precio(-10, 100)
        assert resultados == [silla_barata]

    def test_filtrar_por_material_casos(self, tienda):
        silla_madera = Silla("Silla", material="Madera")
        silla_metal = Silla("Mesa", material="Metal")
        tienda._inventario = [silla_madera, silla_metal, MuebleErrorMaterial()]

        assert tienda.filtrar_por_material("") == []
        assert tienda.filtrar_por_material("madera") == [silla_madera]
        assert tienda.filtrar_por_material("vidrio") == []

    def test_aplicar_descuento_casos(self, tienda):
        assert (
            tienda.aplicar_descuento("sillas", 0)
            == "Error: El porcentaje debe estar entre 1 y 100"
        )
        assert (
            tienda.aplicar_descuento("sillas", 150)
            == "Error: El porcentaje debe estar entre 1 y 100"
        )

        msg_plural = tienda.aplicar_descuento("sillas", 20)
        assert "20%" in msg_plural
        assert tienda._descuentos_activos["Silla"] == 0.2

        msg_singular = tienda.aplicar_descuento("mesa", 10)
        assert "10%" in msg_singular
        assert tienda._descuentos_activos["Mesa"] == 0.1

    def test_realizar_venta_casos(self, tienda):
        silla_no = Silla("No está")
        assert tienda.realizar_venta(silla_no) == {
            "error": "El mueble no está disponible en inventario"
        }

        # Venta sin descuento y sin nombre (usa nombre de clase)
        silla_sin_nombre = Silla(nombre="", precio=100.0)
        tienda.agregar_mueble(silla_sin_nombre)
        venta_1 = tienda.realizar_venta(silla_sin_nombre, "Lina")
        assert venta_1["mueble"] == "Silla"
        assert venta_1["descuento"] == 0.0
        assert venta_1["precio_final"] == 100.0

        # Venta con descuento aplicado a la categoría Silla
        silla_con_desc = Silla("Silla Premium", precio=200.0)
        tienda.agregar_mueble(silla_con_desc)
        tienda.aplicar_descuento("sillas", 25)
        venta_2 = tienda.realizar_venta(silla_con_desc, "Carlos")
        assert venta_2["mueble"] == "Silla Premium"
        assert venta_2["descuento"] == 25.0
        assert venta_2["precio_final"] == 150.0
        assert tienda._total_muebles_vendidos == 2
        assert tienda._valor_total_ventas == 250.0

        # Error al calcular precio durante la venta
        mueble_roto = MuebleErrorPrecio()
        tienda._inventario.append(mueble_roto)
        res_err = tienda.realizar_venta(mueble_roto)
        assert "Error al procesar la venta:" in res_err["error"]

    def test_obtener_estadisticas_y_estadisticas_normales_y_con_error_precio(
        self, tienda
    ):
        silla = Silla("Silla 1", precio=100.0)
        tienda._inventario = [silla, MuebleErrorPrecio()]
        tienda.agregar_comedor(ComedorFake())
        tienda.aplicar_descuento("sillas", 10)

        stats_1 = tienda.obtener_estadisticas()
        stats_2 = tienda.estadisticas()

        for stats in (stats_1, stats_2):
            assert stats["total_muebles"] == 2
            assert stats["total_comedores"] == 1
            assert stats["valor_inventario"] == 100.0
            assert stats["tipos_muebles"]["Silla"] == 1
            assert stats["descuentos_activos"] == {"Silla": 0.1}

    def test_obtener_estadisticas_y_estadisticas_excepcion_general(self, tienda):
        tienda._inventario = None

        stats_1 = tienda.obtener_estadisticas()
        stats_2 = tienda.estadisticas()

        for stats in (stats_1, stats_2):
            assert stats["total_muebles"] == 0
            assert stats["valor_inventario"] == 0.0
            assert stats["tipos_muebles"] == {}

    def test_generar_reporte_inventario_casos(self, tienda):
        # Con datos y descuentos activos
        tienda.agregar_mueble(Silla("Silla 1", precio=100.0))
        tienda.aplicar_descuento("sillas", 15)
        reporte = tienda.generar_reporte_inventario()

        assert "=== REPORTE DE INVENTARIO - Mueblería Test ===" in reporte
        assert "- Silla: 1 unidades" in reporte
        assert "DESCUENTOS ACTIVOS:" in reporte
        assert "- Silla: 15.0%" in reporte

        # Cuando obtener_estadisticas no devuelve dict
        with patch.object(tienda, "obtener_estadisticas", return_value="invalido"):
            reporte_fallback = tienda.generar_reporte_inventario()
            assert "Total de muebles: 0" in reporte_fallback
            assert "DESCUENTOS ACTIVOS:" not in reporte_fallback
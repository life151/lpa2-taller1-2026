import pytest

from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla
from src.models.composicion.comedor import Comedor


class TestComedor:

    @pytest.fixture
    def mesa(self):
        return Mesa(
            "Mesa Principal",
            "Madera",
            "Marrón",
            500.0
        )

    @pytest.fixture
    def silla(self):
        return Silla(
            "Silla 1",
            "Madera",
            "Negro",
            100.0
        )

    @pytest.fixture
    def comedor(self, mesa):
        return Comedor("Comedor Familiar", mesa)

    def test_instanciacion(self, comedor):
        assert comedor.nombre == "Comedor Familiar"

    def test_agregar_silla(self, comedor, silla):
        resultado = comedor.agregar_silla(silla)

        assert "agregada exitosamente" in resultado

    def test_quitar_silla_vacio(self, comedor):
        resultado = comedor.quitar_silla()

        assert resultado == "No hay sillas para quitar"

    def test_quitar_silla(self, comedor, silla):
        comedor.agregar_silla(silla)

        resultado = comedor.quitar_silla()

        assert "removida" in resultado

    def test_len(self, comedor, silla):
        comedor.agregar_silla(silla)

        assert len(comedor) == 2

    def test_precio_total(self, comedor, silla):
        comedor.agregar_silla(silla)

        precio = comedor.calcular_precio_total()

        assert precio > 0

    def test_obtener_resumen(self, comedor, silla):
        comedor.agregar_silla(silla)

        resumen = comedor.obtener_resumen()

        assert resumen["nombre"] == "Comedor Familiar"

    def test_materiales_unicos(self, comedor, silla):
        comedor.agregar_silla(silla)

        materiales = comedor._obtener_materiales_unicos()

        assert "Madera" in materiales

    def test_descripcion_completa(self, comedor):
        descripcion = comedor.obtener_descripcion_completa()

        assert "COMEDOR" in descripcion

    def test_str(self, comedor):
        resultado = str(comedor)

        assert "Comedor" in resultado
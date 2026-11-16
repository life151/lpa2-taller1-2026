import pytest

from src.models.concretos.comedor import Comedor
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla


class TestComedorConcreto:

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
            "Silla",
            "Madera",
            "Negro",
            100.0
        )

    @pytest.fixture
    def comedor(self, mesa):
        return Comedor(mesa)

    def test_instanciacion(self, comedor):
        assert comedor.cantidad_sillas() == 0

    def test_agregar_silla(self, comedor, silla):
        comedor.agregar_silla(silla)

        assert comedor.cantidad_sillas() == 1

    def test_quitar_silla(self, comedor, silla):
        comedor.agregar_silla(silla)
        comedor.quitar_silla(silla)

        assert comedor.cantidad_sillas() == 0

    def test_precio_total_vacio(self, comedor):
        precio = comedor.calcular_precio_total()

        assert precio > 0

    def test_precio_total_con_sillas(self, comedor, silla):
        comedor.agregar_silla(silla)
        comedor.agregar_silla(silla)

        precio = comedor.calcular_precio_total()

        assert precio > 0

    def test_descripcion(self, comedor, silla):
        comedor.agregar_silla(silla)

        descripcion = comedor.descripcion()

        assert "Comedor" in descripcion

    def test_cantidad_sillas(self, comedor, silla):
        comedor.agregar_silla(silla)
        comedor.agregar_silla(silla)

        assert comedor.cantidad_sillas() == 2
import pytest
from src.models.concretos.cama import Cama


class TestCama:

    @pytest.fixture
    def cama_basica(self):
        return Cama(
            "Cama Individual",
            "Madera",
            "Blanco",
            500.0
        )

    def test_instanciacion_correcta(self, cama_basica):
        assert cama_basica.nombre == "Cama Individual"
        assert cama_basica.material == "Madera"
        assert cama_basica.color == "Blanco"
        assert cama_basica.precio_base == 500.0

    def test_tamano_default(self, cama_basica):
        assert cama_basica.tamaño == "individual"

    def test_incluye_colchon_default(self, cama_basica):
        assert cama_basica.incluye_colchon is False

    def test_tiene_cabecera_default(self, cama_basica):
        assert cama_basica.tiene_cabecera is False

    def test_setter_tamano_valido(self, cama_basica):
        cama_basica.tamaño = "queen"

        assert cama_basica.tamaño == "queen"

    def test_setter_tamano_invalido(self, cama_basica):
        with pytest.raises(ValueError):
            cama_basica.tamaño = "gigante"

    def test_precio_matrimonial(self):
        cama = Cama(
            "Cama Matrimonial",
            "Madera",
            "Blanco",
            500.0,
            tamaño="matrimonial"
        )

        assert cama.calcular_precio() == 700.0

    def test_precio_queen(self):
        cama = Cama(
            "Cama Queen",
            "Madera",
            "Blanco",
            500.0,
            tamaño="queen"
        )

        assert cama.calcular_precio() == 900.0

    def test_precio_king(self):
        cama = Cama(
            "Cama King",
            "Madera",
            "Blanco",
            500.0,
            tamaño="king"
        )

        assert cama.calcular_precio() == 1100.0

    def test_precio_con_colchon(self):
        cama = Cama(
            "Cama Premium",
            "Madera",
            "Blanco",
            500.0,
            incluye_colchon=True
        )

        assert cama.calcular_precio() == 800.0

    def test_precio_con_cabecera(self):
        cama = Cama(
            "Cama Premium",
            "Madera",
            "Blanco",
            500.0,
            tiene_cabecera=True
        )

        assert cama.calcular_precio() == 600.0

    def test_obtener_descripcion(self, cama_basica):
        descripcion = cama_basica.obtener_descripcion()

        assert "Cama Individual" in descripcion
        assert "Madera" in descripcion
        assert "Blanco" in descripcion
        assert "individual" in descripcion
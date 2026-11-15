import pytest
from src.models.concretos.silla import Silla


class TestSilla:

    @pytest.fixture
    def silla_basica(self):
        return Silla(
            "Silla Básica",
            "Madera",
            "Negro",
            100.0
        )

    def test_instanciacion_correcta(self, silla_basica):
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.color == "Negro"
        assert silla_basica.precio_base == 100.0

    def test_altura_regulable_default(self, silla_basica):
        assert silla_basica.altura_regulable is False

    def test_tiene_ruedas_default(self, silla_basica):
        assert silla_basica.tiene_ruedas is False

    def test_es_silla_oficina_false(self, silla_basica):
        assert silla_basica.es_silla_oficina() is False

    def test_es_silla_oficina_true(self):
        silla = Silla(
            "Silla Oficina",
            "Metal",
            "Negro",
            100.0,
            altura_regulable=True,
            tiene_ruedas=True
        )

        assert silla.es_silla_oficina() is True

    def test_regular_altura_no_regulable(self, silla_basica):
        resultado = silla_basica.regular_altura(60)

        assert resultado == "Esta silla no tiene altura regulable"

    def test_regular_altura_fuera_rango_bajo(self):
        silla = Silla(
            "Silla Oficina",
            "Metal",
            "Negro",
            100.0,
            altura_regulable=True
        )

        resultado = silla.regular_altura(30)

        assert resultado == "La altura debe estar entre 40 y 100 cm"

    def test_regular_altura_fuera_rango_alto(self):
        silla = Silla(
            "Silla Oficina",
            "Metal",
            "Negro",
            100.0,
            altura_regulable=True
        )

        resultado = silla.regular_altura(120)

        assert resultado == "La altura debe estar entre 40 y 100 cm"

    def test_regular_altura_correcta(self):
        silla = Silla(
            "Silla Oficina",
            "Metal",
            "Negro",
            100.0,
            altura_regulable=True
        )

        resultado = silla.regular_altura(70)

        assert resultado == "Altura ajustada a 70 cm"

    def test_obtener_descripcion(self, silla_basica):
        descripcion = silla_basica.obtener_descripcion()

        assert "Silla Básica" in descripcion
        assert "Madera" in descripcion
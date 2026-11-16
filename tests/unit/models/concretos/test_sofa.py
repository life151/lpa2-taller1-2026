import pytest
from src.models.concretos.sofa import Sofa


class TestSofa:

    @pytest.fixture
    def sofa_basico(self):
        return Sofa(
            "Sofá Familiar",
            "Tela",
            "Gris",
            500.0
        )

    def test_instanciacion_correcta(self, sofa_basico):
        assert sofa_basico.nombre == "Sofá Familiar"
        assert sofa_basico.material == "Tela"
        assert sofa_basico.color == "Gris"
        assert sofa_basico.precio_base == 500.0

    def test_tiene_brazos_default(self, sofa_basico):
        assert sofa_basico.tiene_brazos is True

    def test_es_modular_default(self, sofa_basico):
        assert sofa_basico.es_modular is False

    def test_incluye_cojines_default(self, sofa_basico):
        assert sofa_basico.incluye_cojines is False

    def test_calcular_precio_basico(self, sofa_basico):
        precio = sofa_basico.calcular_precio()

        assert precio > 500.0

    def test_calcular_precio_modular(self):
        sofa = Sofa(
            "Sofá Modular",
            "Tela",
            "Negro",
            500.0,
            es_modular=True
        )

        assert sofa.calcular_precio() > 500.0

    def test_calcular_precio_con_cojines(self):
        sofa = Sofa(
            "Sofá Premium",
            "Tela",
            "Azul",
            500.0,
            incluye_cojines=True
        )

        assert sofa.calcular_precio() > 500.0

    def test_calcular_precio_con_todas_las_mejoras(self):
        sofa = Sofa(
            "Sofá Deluxe",
            "Cuero",
            "Negro",
            500.0,
            es_modular=True,
            incluye_cojines=True
        )

        assert sofa.calcular_precio() > 700.0

    def test_obtener_descripcion(self, sofa_basico):
        descripcion = sofa_basico.obtener_descripcion()

        assert "Sofá Familiar" in descripcion
        assert "Tela" in descripcion
        assert "Gris" in descripcion

    def test_descripcion_contiene_precio(self, sofa_basico):
        descripcion = sofa_basico.obtener_descripcion()

        assert "Precio final" in descripcion
import pytest
from src.models.categorias.superficies import Superficie


class SuperficieDePrueba(Superficie):
    """Subclase mínima: llama a super() para ejecutar los métodos abstractos."""

    def calcular_precio(self) -> float:
        super().calcular_precio()
        return self.precio_base * self.calcular_factor_tamaño()

    def obtener_descripcion(self) -> str:
        super().obtener_descripcion()
        return self.obtener_info_superficie()


class TestSuperficie:

    @pytest.fixture
    def superficie(self):
        return SuperficieDePrueba(
            "Mesa", "Madera", "Café", 100.0, 200.0, 100.0, 75.0
        )

    # --- Abstracción ---
    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Superficie("Mesa", "Madera", "Café", 100.0, 200.0, 100.0, 75.0)

    def test_metodos_abstractos_declarados(self):
        assert Superficie.__abstractmethods__ == {
            "calcular_precio",
            "obtener_descripcion",
        }

    def test_subclase_incompleta_no_se_instancia(self):
        class Incompleta(Superficie):
            def calcular_precio(self):
                return 0.0

        with pytest.raises(TypeError):
            Incompleta("A", "M", "C", 1.0, 1.0, 1.0, 1.0)

    # --- Constructor ---
    def test_atributos_heredados(self, superficie):
        assert superficie.nombre == "Mesa"
        assert superficie.material == "Madera"
        assert superficie.color == "Café"
        assert superficie.precio_base == 100.0

    def test_atributos_propios(self, superficie):
        assert superficie.largo == 200.0
        assert superficie.ancho == 100.0
        assert superficie.altura == 75.0

    # --- Setters válidos ---
    def test_setter_largo_valido(self, superficie):
        superficie.largo = 150.0
        assert superficie.largo == 150.0

    def test_setter_ancho_valido(self, superficie):
        superficie.ancho = 90.0
        assert superficie.ancho == 90.0

    def test_setter_altura_valida(self, superficie):
        superficie.altura = 80.0
        assert superficie.altura == 80.0

    # --- Setters inválidos ---
    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_largo_invalido(self, superficie, valor):
        with pytest.raises(ValueError, match="largo"):
            superficie.largo = valor

    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_ancho_invalido(self, superficie, valor):
        with pytest.raises(ValueError, match="ancho"):
            superficie.ancho = valor

    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_altura_invalida(self, superficie, valor):
        with pytest.raises(ValueError, match="altura"):
            superficie.altura = valor

    def test_valores_no_cambian_tras_error(self, superficie):
        with pytest.raises(ValueError):
            superficie.largo = 0
        with pytest.raises(ValueError):
            superficie.ancho = 0
        with pytest.raises(ValueError):
            superficie.altura = 0
        assert superficie.largo == 200.0
        assert superficie.ancho == 100.0
        assert superficie.altura == 75.0

    # --- Área y factor de tamaño ---
    def test_calcular_area(self, superficie):
        assert superficie.calcular_area() == 20000.0

    def test_area_cambia_con_dimensiones(self, superficie):
        superficie.largo = 100.0
        assert superficie.calcular_area() == 10000.0

    def test_factor_tamaño(self, superficie):
        # 1.0 + (20000 / 10000) * 0.05 = 1.10
        assert superficie.calcular_factor_tamaño() == pytest.approx(1.10)

    def test_factor_tamaño_para_10000_cm2(self):
        sup = SuperficieDePrueba("A", "M", "C", 100.0, 100.0, 100.0, 75.0)
        assert sup.calcular_factor_tamaño() == pytest.approx(1.05)

    def test_factor_aumenta_con_el_area(self, superficie):
        antes = superficie.calcular_factor_tamaño()
        superficie.ancho = 200.0
        assert superficie.calcular_factor_tamaño() > antes

    # --- Información ---
    def test_obtener_info_superficie(self, superficie):
        assert superficie.obtener_info_superficie() == (
            "Dimensiones: 200.0x100.0x75.0cm (Área: 20000.0cm²)"
        )

    # --- Métodos abstractos ejecutados desde la subclase ---
    def test_calcular_precio_desde_subclase(self, superficie):
        assert superficie.calcular_precio() == pytest.approx(110.0)

    def test_obtener_descripcion_desde_subclase(self, superficie):
        assert "Dimensiones: 200.0x100.0x75.0cm" in superficie.obtener_descripcion()
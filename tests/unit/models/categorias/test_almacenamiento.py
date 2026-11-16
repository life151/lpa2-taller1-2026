import pytest
from src.models.categorias.almacenamiento import Almacenamiento


class AlmacenamientoDePrueba(Almacenamiento):
    """Subclase mínima: llama a super() para ejecutar los métodos abstractos."""

    def calcular_precio(self) -> float:
        super().calcular_precio()
        return self.precio_base * self.calcular_factor_almacenamiento()

    def obtener_descripcion(self) -> str:
        super().obtener_descripcion()
        return self.obtener_info_almacenamiento()


class TestAlmacenamiento:

    @pytest.fixture
    def almacen(self):
        return AlmacenamientoDePrueba(
            "Estante", "Madera", "Blanco", 100.0, 3, 150.0
        )

    # --- Abstracción ---
    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Almacenamiento("Estante", "Madera", "Blanco", 100.0, 3, 150.0)

    def test_metodos_abstractos_declarados(self):
        assert Almacenamiento.__abstractmethods__ == {
            "calcular_precio",
            "obtener_descripcion",
        }

    def test_subclase_incompleta_no_se_instancia(self):
        class Incompleta(Almacenamiento):
            def calcular_precio(self):
                return 0.0

        with pytest.raises(TypeError):
            Incompleta("A", "B", "C", 1.0, 1, 1.0)

    # --- Constructor y herencia de atributos ---
    def test_atributos_heredados(self, almacen):
        assert almacen.nombre == "Estante"
        assert almacen.material == "Madera"
        assert almacen.color == "Blanco"
        assert almacen.precio_base == 100.0

    def test_atributos_propios(self, almacen):
        assert almacen.num_compartimentos == 3
        assert almacen.capacidad_litros == 150.0

    # --- Setters válidos ---
    def test_setter_num_compartimentos_valido(self, almacen):
        almacen.num_compartimentos = 5
        assert almacen.num_compartimentos == 5

    def test_setter_capacidad_valida(self, almacen):
        almacen.capacidad_litros = 200.0
        assert almacen.capacidad_litros == 200.0

    # --- Setters inválidos ---
    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_num_compartimentos_invalido(self, almacen, valor):
        with pytest.raises(ValueError, match="compartimentos"):
            almacen.num_compartimentos = valor

    @pytest.mark.parametrize("valor", [0, -10.5])
    def test_setter_capacidad_invalida(self, almacen, valor):
        with pytest.raises(ValueError, match="capacidad"):
            almacen.capacidad_litros = valor

    def test_valor_no_cambia_tras_error(self, almacen):
        with pytest.raises(ValueError):
            almacen.num_compartimentos = 0
        assert almacen.num_compartimentos == 3

    # --- Factor de almacenamiento ---
    def test_factor_minimo(self):
        # 1 compartimento y 100 L -> 1.0 + 0 + (100/100)*0.02
        almacen = AlmacenamientoDePrueba("A", "M", "C", 100.0, 1, 100.0)
        assert almacen.calcular_factor_almacenamiento() == pytest.approx(1.02)

    def test_factor_con_varios_compartimentos_y_capacidad(self, almacen):
        # 1.0 + (3-1)*0.05 + (150/100)*0.02 = 1.13
        assert almacen.calcular_factor_almacenamiento() == pytest.approx(1.13)

    def test_factor_aumenta_con_mas_compartimentos(self, almacen):
        antes = almacen.calcular_factor_almacenamiento()
        almacen.num_compartimentos = 6
        assert almacen.calcular_factor_almacenamiento() > antes

    def test_factor_aumenta_con_mayor_capacidad(self, almacen):
        antes = almacen.calcular_factor_almacenamiento()
        almacen.capacidad_litros = 500.0
        assert almacen.calcular_factor_almacenamiento() > antes

    # --- Información ---
    def test_obtener_info_almacenamiento(self, almacen):
        assert almacen.obtener_info_almacenamiento() == (
            "Compartimentos: 3, Capacidad: 150.0L"
        )

    # --- Métodos abstractos ejecutados desde la subclase ---
    def test_calcular_precio_desde_subclase(self, almacen):
        assert almacen.calcular_precio() == pytest.approx(113.0)

    def test_obtener_descripcion_desde_subclase(self, almacen):
        assert "Compartimentos: 3" in almacen.obtener_descripcion()
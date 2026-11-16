import pytest
from src.models.categorias.asientos import Asiento


class AsientoDePrueba(Asiento):
    """Subclase mínima: llama a super() para ejecutar los métodos abstractos."""

    def calcular_precio(self) -> float:
        super().calcular_precio()
        return self.precio_base * self.calcular_factor_comodidad()

    def obtener_descripcion(self) -> str:
        super().obtener_descripcion()
        return self.obtener_info_asiento()


def crear_asiento(capacidad=1, respaldo=True, tapizado=None, precio=100.0):
    return AsientoDePrueba(
        "Asiento", "Madera", "Negro", precio, capacidad, respaldo, tapizado
    )


class TestAsiento:

    @pytest.fixture
    def asiento(self):
        return crear_asiento(capacidad=2, respaldo=True, tapizado="Cuero")

    # --- Abstracción ---
    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Asiento("A", "M", "C", 100.0, 1, True)

    def test_metodos_abstractos_declarados(self):
        assert Asiento.__abstractmethods__ == {
            "calcular_precio",
            "obtener_descripcion",
        }

    def test_subclase_incompleta_no_se_instancia(self):
        class Incompleta(Asiento):
            def calcular_precio(self):
                return 0.0

        with pytest.raises(TypeError):
            Incompleta("A", "M", "C", 1.0, 1, True)

    # --- Constructor ---
    def test_atributos_heredados(self, asiento):
        assert asiento.nombre == "Asiento"
        assert asiento.material == "Madera"
        assert asiento.color == "Negro"
        assert asiento.precio_base == 100.0

    def test_atributos_propios(self, asiento):
        assert asiento.capacidad_personas == 2
        assert asiento.tiene_respaldo is True
        assert asiento.material_tapizado == "Cuero"

    def test_tapizado_por_defecto_es_none(self):
        asiento = AsientoDePrueba("A", "M", "C", 100.0, 1, True)
        assert asiento.material_tapizado is None

    # --- Setters ---
    def test_setter_capacidad_valida(self, asiento):
        asiento.capacidad_personas = 5
        assert asiento.capacidad_personas == 5

    @pytest.mark.parametrize("valor", [0, -1])
    def test_setter_capacidad_invalida(self, asiento, valor):
        with pytest.raises(ValueError, match="capacidad"):
            asiento.capacidad_personas = valor

    def test_capacidad_no_cambia_tras_error(self, asiento):
        with pytest.raises(ValueError):
            asiento.capacidad_personas = 0
        assert asiento.capacidad_personas == 2

    def test_setter_tiene_respaldo(self, asiento):
        asiento.tiene_respaldo = False
        assert asiento.tiene_respaldo is False

    def test_setter_material_tapizado(self, asiento):
        asiento.material_tapizado = "Tela"
        assert asiento.material_tapizado == "Tela"

    # --- Factor de comodidad ---
    def test_factor_sin_extras(self):
        asiento = crear_asiento(capacidad=1, respaldo=False, tapizado=None)
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.0)

    def test_factor_con_respaldo(self):
        asiento = crear_asiento(capacidad=1, respaldo=True, tapizado=None)
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.1)

    def test_factor_con_cuero(self):
        asiento = crear_asiento(capacidad=1, respaldo=False, tapizado="cuero")
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.2)

    def test_factor_con_tela(self):
        asiento = crear_asiento(capacidad=1, respaldo=False, tapizado="tela")
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.1)

    def test_factor_tapizado_no_distingue_mayusculas(self):
        asiento = crear_asiento(capacidad=1, respaldo=False, tapizado="CUERO")
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.2)

    def test_factor_con_tapizado_desconocido_no_suma(self):
        asiento = crear_asiento(capacidad=1, respaldo=False, tapizado="lino")
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.0)

    def test_factor_por_capacidad(self):
        # (3 - 1) * 0.05 = 0.10
        asiento = crear_asiento(capacidad=3, respaldo=False, tapizado=None)
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.1)

    def test_factor_combinado(self, asiento):
        # 1.0 + 0.1 (respaldo) + 0.2 (cuero) + 0.05 (capacidad 2) = 1.35
        assert asiento.calcular_factor_comodidad() == pytest.approx(1.35)

    # --- Información ---
    def test_info_con_tapizado(self, asiento):
        assert asiento.obtener_info_asiento() == (
            "Capacidad: 2 personas, Respaldo: Sí, Tapizado: Cuero"
        )

    def test_info_sin_tapizado_ni_respaldo(self):
        asiento = crear_asiento(capacidad=1, respaldo=False, tapizado=None)
        assert asiento.obtener_info_asiento() == (
            "Capacidad: 1 personas, Respaldo: No"
        )

    # --- Métodos abstractos ejecutados desde la subclase ---
    def test_calcular_precio_desde_subclase(self, asiento):
        assert asiento.calcular_precio() == pytest.approx(135.0)

    def test_obtener_descripcion_desde_subclase(self, asiento):
        assert "Capacidad: 2 personas" in asiento.obtener_descripcion()
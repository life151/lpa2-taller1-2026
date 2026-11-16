import pytest
from src.models.concretos.escritorio import Escritorio


class TestEscritorio:

    @pytest.fixture
    def escritorio_basico(self):
        return Escritorio("Escritorio Oficina", "Madera", "Negro", 400)

    # --- Constructor ---
    def test_instanciacion_correcta(self, escritorio_basico):
        assert escritorio_basico.nombre == "Escritorio Oficina"
        assert escritorio_basico.material == "Madera"
        assert escritorio_basico.color == "Negro"
        assert escritorio_basico.precio_base == 400

    def test_valores_por_defecto(self, escritorio_basico):
        assert escritorio_basico.forma == "rectangular"
        assert escritorio_basico.tiene_cajones is False
        assert escritorio_basico.num_cajones == 0
        assert escritorio_basico.largo == 1.2
        assert escritorio_basico.tiene_iluminacion is False

    def test_atributos_personalizados(self):
        escritorio = Escritorio(
            "Escritorio Gamer", "Metal", "Rojo", 600,
            forma="esquinero", tiene_cajones=True, num_cajones=3,
            largo=1.8, tiene_iluminacion=True,
        )
        assert escritorio.forma == "esquinero"
        assert escritorio.tiene_cajones is True
        assert escritorio.num_cajones == 3
        assert escritorio.largo == 1.8
        assert escritorio.tiene_iluminacion is True

    def test_precio_base_se_convierte_a_entero(self):
        escritorio = Escritorio("E", "M", "C", 400.9)
        assert escritorio.precio_base == 400
        assert isinstance(escritorio.precio_base, int)

    def test_precio_base_none_es_cero(self):
        escritorio = Escritorio("E", "M", "C", None)
        assert escritorio.precio_base == 0

    # --- Cálculo de precio ---
    def test_precio_basico(self, escritorio_basico):
        assert escritorio_basico.calcular_precio() == 400

    def test_precio_con_cajones(self):
        escritorio = Escritorio("E", "M", "C", 400, tiene_cajones=True, num_cajones=3)
        # 400 + 3 * 25 = 475
        assert escritorio.calcular_precio() == 475

    def test_cajones_no_suman_si_tiene_cajones_es_false(self):
        escritorio = Escritorio("E", "M", "C", 400, tiene_cajones=False, num_cajones=5)
        assert escritorio.calcular_precio() == 400

    def test_precio_con_largo_mayor_a_1_5(self):
        escritorio = Escritorio("E", "M", "C", 400, largo=1.6)
        assert escritorio.calcular_precio() == 450

    def test_largo_exactamente_1_5_no_suma(self):
        escritorio = Escritorio("E", "M", "C", 400, largo=1.5)
        assert escritorio.calcular_precio() == 400

    def test_precio_con_iluminacion(self):
        escritorio = Escritorio("E", "M", "C", 400, tiene_iluminacion=True)
        assert escritorio.calcular_precio() == 440

    def test_precio_con_forma_no_rectangular(self):
        escritorio = Escritorio("E", "M", "C", 400, forma="esquinero")
        assert escritorio.calcular_precio() == 430

    def test_precio_con_todo(self):
        escritorio = Escritorio(
            "E", "M", "C", 400,
            forma="esquinero", tiene_cajones=True, num_cajones=2,
            largo=2.0, tiene_iluminacion=True,
        )
        # 400 + 50 (cajones) + 50 (largo) + 40 (luz) + 30 (forma) = 570
        assert escritorio.calcular_precio() == 570

    def test_precio_retorna_entero(self, escritorio_basico):
        assert isinstance(escritorio_basico.calcular_precio(), int)

    # --- Descripción ---
    def test_descripcion_completa(self, escritorio_basico):
        assert escritorio_basico.obtener_descripcion() == (
            "Escritorio 'Escritorio Oficina': Material=Madera, Color=Negro, "
            "Forma=rectangular, Cajones=0, Largo=1.2m, Iluminación=No, "
            "Precio base=$400"
        )

    def test_descripcion_muestra_cajones_si_los_tiene(self):
        escritorio = Escritorio("E", "M", "C", 400, tiene_cajones=True, num_cajones=4)
        assert "Cajones=4" in escritorio.obtener_descripcion()

    def test_descripcion_oculta_cajones_si_no_tiene(self):
        escritorio = Escritorio("E", "M", "C", 400, tiene_cajones=False, num_cajones=4)
        assert "Cajones=0" in escritorio.obtener_descripcion()

    def test_descripcion_con_iluminacion(self):
        escritorio = Escritorio("E", "M", "C", 400, tiene_iluminacion=True)
        assert "Iluminación=Sí" in escritorio.obtener_descripcion()
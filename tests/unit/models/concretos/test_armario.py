import pytest
from src.models.concretos.armario import Armario


class TestArmario:

    @pytest.fixture
    def armario_basico(self):
        return Armario("Armario Clásico", "Madera", "Café", 500)

    # --- Constructor ---
    def test_instanciacion_correcta(self, armario_basico):
        assert armario_basico.nombre == "Armario Clásico"
        assert armario_basico.material == "Madera"
        assert armario_basico.color == "Café"
        assert armario_basico.precio_base == 500

    def test_valores_por_defecto(self, armario_basico):
        assert armario_basico.num_puertas == 2
        assert armario_basico.num_cajones == 0
        assert armario_basico.tiene_espejos is False

    def test_atributos_personalizados(self):
        armario = Armario(
            "Armario Grande", "Roble", "Negro", 800,
            num_puertas=4, num_cajones=3, tiene_espejos=True,
        )
        assert armario.num_puertas == 4
        assert armario.num_cajones == 3
        assert armario.tiene_espejos is True

    def test_precio_base_se_convierte_a_entero(self):
        armario = Armario("A", "M", "C", 500.9)
        assert armario.precio_base == 500
        assert isinstance(armario.precio_base, int)

    def test_precio_base_none_es_cero(self):
        armario = Armario("A", "M", "C", None)
        assert armario.precio_base == 0

    # --- Cálculo de precio ---
    def test_precio_basico(self, armario_basico):
        # 500 + 2 puertas * 50 = 600
        assert armario_basico.calcular_precio() == 600

    def test_precio_por_cada_puerta(self):
        armario = Armario("A", "M", "C", 500, num_puertas=4)
        # 500 + 4 * 50 = 700
        assert armario.calcular_precio() == 700

    def test_precio_sin_puertas(self):
        armario = Armario("A", "M", "C", 500, num_puertas=0)
        assert armario.calcular_precio() == 500

    def test_precio_con_cajones(self):
        armario = Armario("A", "M", "C", 500, num_cajones=3)
        # 500 + 2 * 50 + 3 * 30 = 690
        assert armario.calcular_precio() == 690

    def test_precio_con_espejos(self):
        armario = Armario("A", "M", "C", 500, tiene_espejos=True)
        # 500 + 100 + 100 = 700
        assert armario.calcular_precio() == 700

    def test_precio_con_todo(self):
        armario = Armario(
            "A", "M", "C", 500,
            num_puertas=3, num_cajones=2, tiene_espejos=True,
        )
        # 500 + 150 + 60 + 100 = 810
        assert armario.calcular_precio() == 810

    def test_precio_retorna_entero(self, armario_basico):
        assert isinstance(armario_basico.calcular_precio(), int)

    def test_precio_se_actualiza_al_cambiar_atributos(self, armario_basico):
        armario_basico.num_cajones = 2
        assert armario_basico.calcular_precio() == 660

    # --- Descripción ---
    def test_descripcion_completa(self, armario_basico):
        assert armario_basico.obtener_descripcion() == (
            "Armario 'Armario Clásico': Material=Madera, Color=Café, "
            "Puertas=2, Cajones=0, Espejos=No, Precio base=$500"
        )

    def test_descripcion_con_espejos(self):
        armario = Armario("A", "M", "C", 500, tiene_espejos=True)
        assert "Espejos=Sí" in armario.obtener_descripcion()

    def test_descripcion_muestra_cajones_y_puertas(self):
        armario = Armario("A", "M", "C", 500, num_puertas=3, num_cajones=4)
        descripcion = armario.obtener_descripcion()
        assert "Puertas=3" in descripcion
        assert "Cajones=4" in descripcion
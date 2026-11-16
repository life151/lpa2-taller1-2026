import pytest
from src.models.concretos.cajonera import Cajonera


class TestCajonera:

    @pytest.fixture
    def cajonera_basica(self):
        return Cajonera("Cajonera Clásica", "Madera", "Blanco", 300)

    # --- Constructor ---
    def test_instanciacion_correcta(self, cajonera_basica):
        assert cajonera_basica.nombre == "Cajonera Clásica"
        assert cajonera_basica.material == "Madera"
        assert cajonera_basica.color == "Blanco"
        assert cajonera_basica.precio_base == 300

    def test_valores_por_defecto(self, cajonera_basica):
        assert cajonera_basica.num_cajones == 3
        assert cajonera_basica.tiene_ruedas is False

    def test_atributos_personalizados(self):
        cajonera = Cajonera(
            "Cajonera Móvil", "Metal", "Gris", 400,
            num_cajones=5, tiene_ruedas=True,
        )
        assert cajonera.num_cajones == 5
        assert cajonera.tiene_ruedas is True

    def test_precio_base_se_convierte_a_entero(self):
        cajonera = Cajonera("C", "M", "C", 300.9)
        assert cajonera.precio_base == 300
        assert isinstance(cajonera.precio_base, int)

    def test_precio_base_none_es_cero(self):
        cajonera = Cajonera("C", "M", "C", None)
        assert cajonera.precio_base == 0

    # --- Cálculo de precio ---
    def test_precio_basico(self, cajonera_basica):
        # 300 + 3 cajones * 20 = 360
        assert cajonera_basica.calcular_precio() == 360

    def test_precio_por_cada_cajon(self):
        cajonera = Cajonera("C", "M", "C", 300, num_cajones=5)
        # 300 + 5 * 20 = 400
        assert cajonera.calcular_precio() == 400

    def test_precio_sin_cajones(self):
        cajonera = Cajonera("C", "M", "C", 300, num_cajones=0)
        assert cajonera.calcular_precio() == 300

    def test_precio_con_ruedas(self):
        cajonera = Cajonera("C", "M", "C", 300, tiene_ruedas=True)
        # 300 + 60 + 30 = 390
        assert cajonera.calcular_precio() == 390

    def test_precio_con_todo(self):
        cajonera = Cajonera("C", "M", "C", 300, num_cajones=4, tiene_ruedas=True)
        # 300 + 80 + 30 = 410
        assert cajonera.calcular_precio() == 410

    def test_precio_retorna_entero(self, cajonera_basica):
        assert isinstance(cajonera_basica.calcular_precio(), int)

    def test_precio_se_actualiza_al_cambiar_atributos(self, cajonera_basica):
        cajonera_basica.num_cajones = 1
        assert cajonera_basica.calcular_precio() == 320

    # --- Descripción ---
    def test_descripcion_completa(self, cajonera_basica):
        assert cajonera_basica.obtener_descripcion() == (
            "Cajonera 'Cajonera Clásica': Material=Madera, Color=Blanco, "
            "Cajones=3, Ruedas=No, Precio base=$300"
        )

    def test_descripcion_con_ruedas(self):
        cajonera = Cajonera("C", "M", "C", 300, tiene_ruedas=True)
        assert "Ruedas=Sí" in cajonera.obtener_descripcion()

    def test_descripcion_muestra_cajones(self):
        cajonera = Cajonera("C", "M", "C", 300, num_cajones=6)
        assert "Cajones=6" in cajonera.obtener_descripcion()
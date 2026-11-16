import pytest
from src.models.concretos.sillon import Sillon


class TestSillon:

    @pytest.fixture
    def sillon_basico(self):
        return Sillon("Sillón Clásico", "Madera", "Gris", 600)

    # --- Constructor ---
    def test_instanciacion_correcta(self, sillon_basico):
        assert sillon_basico.nombre == "Sillón Clásico"
        assert sillon_basico.material == "Madera"
        assert sillon_basico.color == "Gris"
        assert sillon_basico.precio_base == 600

    def test_valores_por_defecto(self, sillon_basico):
        assert sillon_basico.capacidad_personas == 2
        assert sillon_basico.tiene_respaldo is True
        assert sillon_basico.material_tapizado is None
        assert sillon_basico.tiene_brazos is True
        assert sillon_basico.es_reclinable is False
        assert sillon_basico.tiene_reposapiés is False

    def test_atributos_personalizados(self):
        sillon = Sillon(
            "Sillón Premium", "Metal", "Negro", 900,
            capacidad_personas=1, tiene_respaldo=False,
            material_tapizado="Cuero", tiene_brazos=False,
            es_reclinable=True, tiene_reposapiés=True,
        )
        assert sillon.capacidad_personas == 1
        assert sillon.tiene_respaldo is False
        assert sillon.material_tapizado == "Cuero"
        assert sillon.tiene_brazos is False
        assert sillon.es_reclinable is True
        assert sillon.tiene_reposapiés is True

    def test_precio_base_se_convierte_a_entero(self):
        sillon = Sillon("S", "M", "C", 600.9)
        assert sillon.precio_base == 600
        assert isinstance(sillon.precio_base, int)

    def test_precio_base_none_es_cero(self):
        sillon = Sillon("S", "M", "C", None)
        assert sillon.precio_base == 0

    # --- Cálculo de precio ---
    def test_precio_basico_incluye_brazos(self, sillon_basico):
        # 600 + 100 (brazos por defecto) = 700
        assert sillon_basico.calcular_precio() == 700

    def test_precio_sin_brazos(self):
        sillon = Sillon("S", "M", "C", 600, tiene_brazos=False)
        assert sillon.calcular_precio() == 600

    def test_precio_con_tapizado(self):
        sillon = Sillon("S", "M", "C", 600, material_tapizado="Tela")
        # 600 + 200 + 100 = 900
        assert sillon.calcular_precio() == 900

    def test_precio_con_reclinable(self):
        sillon = Sillon("S", "M", "C", 600, es_reclinable=True)
        # 600 + 100 + 250 = 950
        assert sillon.calcular_precio() == 950

    def test_precio_con_reposapies(self):
        sillon = Sillon("S", "M", "C", 600, tiene_reposapiés=True)
        # 600 + 100 + 80 = 780
        assert sillon.calcular_precio() == 780

    def test_precio_con_todo(self):
        sillon = Sillon(
            "S", "M", "C", 600,
            material_tapizado="Cuero", tiene_brazos=True,
            es_reclinable=True, tiene_reposapiés=True,
        )
        # 600 + 200 + 100 + 250 + 80 = 1230
        assert sillon.calcular_precio() == 1230

    def test_precio_retorna_entero(self, sillon_basico):
        assert isinstance(sillon_basico.calcular_precio(), int)

    # --- Descripción ---
    def test_descripcion_completa(self, sillon_basico):
        assert sillon_basico.obtener_descripcion() == (
            "Sillón 'Sillón Clásico': Material=Madera, Color=Gris, "
            "Capacidad=2 personas, Tapizado=N/A, Brazos=Sí, Reclinable=No, "
            "Reposapiés=No, Precio base=$600"
        )

    def test_descripcion_muestra_tapizado(self):
        sillon = Sillon("S", "M", "C", 600, material_tapizado="Cuero")
        assert "Tapizado=Cuero" in sillon.obtener_descripcion()

    def test_descripcion_sin_tapizado_muestra_na(self, sillon_basico):
        assert "Tapizado=N/A" in sillon_basico.obtener_descripcion()

    def test_descripcion_reclinable_y_reposapies(self):
        sillon = Sillon("S", "M", "C", 600, es_reclinable=True, tiene_reposapiés=True)
        descripcion = sillon.obtener_descripcion()
        assert "Reclinable=Sí" in descripcion
        assert "Reposapiés=Sí" in descripcion

    def test_descripcion_sin_brazos(self):
        sillon = Sillon("S", "M", "C", 600, tiene_brazos=False)
        assert "Brazos=No" in sillon.obtener_descripcion()
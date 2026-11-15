import pytest
from src.models.concretos.mesa import Mesa


class TestMesa:

    @pytest.fixture
    def mesa_basica(self):
        return Mesa(
            "Mesa Comedor",
            "Madera",
            "Marrón",
            200.0
        )

    def test_instanciacion_correcta(self, mesa_basica):
        assert mesa_basica.nombre == "Mesa Comedor"
        assert mesa_basica.material == "Madera"
        assert mesa_basica.color == "Marrón"
        assert mesa_basica.precio_base == 200.0

    def test_forma_default(self, mesa_basica):
        assert mesa_basica.forma == "rectangular"

    def test_capacidad_default(self, mesa_basica):
        assert mesa_basica.capacidad_personas == 4

    def test_setter_forma_valida(self, mesa_basica):
        mesa_basica.forma = "redonda"

        assert mesa_basica.forma == "redonda"

    def test_setter_forma_invalida(self, mesa_basica):
        with pytest.raises(ValueError):
            mesa_basica.forma = "triangular"

    def test_setter_capacidad_valida(self, mesa_basica):
        mesa_basica.capacidad_personas = 8

        assert mesa_basica.capacidad_personas == 8

    def test_setter_capacidad_invalida(self, mesa_basica):
        with pytest.raises(ValueError):
            mesa_basica.capacidad_personas = 0

    def test_calcular_precio_basico(self, mesa_basica):
        precio = mesa_basica.calcular_precio()

        assert precio > 0

    def test_calcular_precio_forma_especial(self):
        mesa = Mesa(
            "Mesa Redonda",
            "Madera",
            "Marrón",
            200.0,
            forma="redonda"
        )

        assert mesa.calcular_precio() > 200.0

    def test_obtener_descripcion(self, mesa_basica):
        descripcion = mesa_basica.obtener_descripcion()

        assert "Mesa Comedor" in descripcion
        assert "Madera" in descripcion
        assert "rectangular" in descripcion
import pytest
from src.models.mueble import Mueble


class MueblePrueba(Mueble):
    """Clase auxiliar para probar Mueble."""

    def calcular_precio(self):
        return self.precio_base

    def obtener_descripcion(self):
        return self.nombre


class TestMueble:

    def test_es_clase_abstracta(self):
        with pytest.raises(TypeError):
            Mueble("Mesa", "Madera", "Negro", 100.0)

    def test_tiene_metodos_abstractos(self):
        assert hasattr(Mueble, "calcular_precio")
        assert hasattr(Mueble, "obtener_descripcion")

        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__

    def test_getters(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        assert mueble.nombre == "Mesa"
        assert mueble.material == "Madera"
        assert mueble.color == "Negro"
        assert mueble.precio_base == 100.0

    def test_setter_nombre(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        mueble.nombre = "Silla"

        assert mueble.nombre == "Silla"

    def test_nombre_vacio(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        with pytest.raises(ValueError):
            mueble.nombre = ""

    def test_material_vacio(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        with pytest.raises(ValueError):
            mueble.material = ""

    def test_color_vacio(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        with pytest.raises(ValueError):
            mueble.color = ""

    def test_precio_negativo(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        with pytest.raises(ValueError):
            mueble.precio_base = -10

    def test_str(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        assert str(mueble) == "Mesa de Madera en color Negro"

    def test_repr(self):
        mueble = MueblePrueba(
            "Mesa",
            "Madera",
            "Negro",
            100.0
        )

        resultado = repr(mueble)

        assert "Mesa" in resultado
        assert "Madera" in resultado
        assert "Negro" in resultado
        assert "100.0" in resultado
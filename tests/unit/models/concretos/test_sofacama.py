import pytest
from src.models.concretos.sofacama import SofaCama


class TestSofaCama:

    @pytest.fixture
    def sofacama_basico(self):
        return SofaCama(
            "Sofá Cama",
            "Tela",
            "Gris",
            1000.0
        )

    def test_instanciacion_correcta(self, sofacama_basico):
        assert sofacama_basico.nombre == "Sofá Cama"
        assert sofacama_basico.material == "Tela"
        assert sofacama_basico.color == "Gris"

    def test_modo_inicial(self, sofacama_basico):
        assert sofacama_basico.modo_actual == "sofa"

    def test_convertir_a_cama(self, sofacama_basico):
        resultado = sofacama_basico.convertir_a_cama()

        assert "convertido a cama" in resultado
        assert sofacama_basico.modo_actual == "cama"

    def test_convertir_a_cama_dos_veces(self, sofacama_basico):
        sofacama_basico.convertir_a_cama()

        resultado = sofacama_basico.convertir_a_cama()

        assert resultado == "El sofá-cama ya está en modo cama"

    def test_convertir_a_sofa(self, sofacama_basico):
        sofacama_basico.convertir_a_cama()

        resultado = sofacama_basico.convertir_a_sofa()

        assert "convertida a sofá" in resultado
        assert sofacama_basico.modo_actual == "sofa"

    def test_convertir_a_sofa_dos_veces(self, sofacama_basico):
        resultado = sofacama_basico.convertir_a_sofa()

        assert resultado == "El sofá-cama ya está en modo sofá"

    def test_capacidad_total(self, sofacama_basico):
        capacidades = sofacama_basico.obtener_capacidad_total()

        assert "como_sofa" in capacidades
        assert "como_cama" in capacidades

    def test_calcular_precio(self, sofacama_basico):
        precio = sofacama_basico.calcular_precio()

        assert precio > 1000.0

    def test_descripcion(self, sofacama_basico):
        descripcion = sofacama_basico.obtener_descripcion()

        assert "Sofá-Cama" in descripcion
        assert "Tela" in descripcion
        assert "Gris" in descripcion

    def test_str(self, sofacama_basico):
        resultado = str(sofacama_basico)

        assert "Sofá-cama" in resultado
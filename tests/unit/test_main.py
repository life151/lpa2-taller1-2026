from unittest.mock import MagicMock, patch

from src.main import (
    aplicar_descuentos_ejemplo,
    crear_catalogo_inicial,
    crear_comedores_ejemplo,
    main,
    mostrar_estadisticas_iniciales,
)
from src.services.tienda import TiendaMuebles


class TestMain:

    def test_crear_catalogo_inicial(self):
        tienda = TiendaMuebles("Tienda Test")
        crear_catalogo_inicial(tienda)

        assert len(tienda._inventario) == 17

    def test_crear_comedores_ejemplo(self):
        tienda = TiendaMuebles("Tienda Test")
        crear_comedores_ejemplo(tienda)

        assert len(tienda._comedores) == 2

    def test_aplicar_descuentos_ejemplo(self):
        tienda = TiendaMuebles("Tienda Test")
        aplicar_descuentos_ejemplo(tienda)

        assert tienda._descuentos_activos["Silla"] == 0.10
        assert tienda._descuentos_activos["Mesa"] == 0.15
        assert tienda._descuentos_activos["Sofa"] == 0.20

    def test_mostrar_estadisticas_iniciales_con_y_sin_datos(self, capsys):
        tienda = TiendaMuebles("Tienda Test")
        mostrar_estadisticas_iniciales(tienda)
        salida_vacia = capsys.readouterr().out
        assert "Total de muebles: 0" in salida_vacia

        crear_catalogo_inicial(tienda)
        mostrar_estadisticas_iniciales(tienda)
        salida_llena = capsys.readouterr().out
        assert "Total de muebles: 17" in salida_llena
        assert "Silla:" in salida_llena

    @patch("builtins.input", return_value="")
    @patch("src.main.MenuTienda")
    def test_main_flujo_exitoso(self, mock_menu_cls, mock_input, capsys):
        mock_menu = MagicMock()
        mock_menu_cls.return_value = mock_menu

        main()

        mock_menu.ejecutar.assert_called_once()
        salida = capsys.readouterr().out
        assert "Programa finalizado" in salida

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    @patch("src.main.mostrar_estadisticas_iniciales")
    @patch("src.main.aplicar_descuentos_ejemplo")
    @patch("src.main.crear_comedores_ejemplo")
    @patch("src.main.crear_catalogo_inicial")
    @patch("src.main.MenuTienda")
    def test_main_keyboard_interrupt(
        self,
        mock_menu_cls,
        mock_cat,
        mock_com,
        mock_desc,
        mock_stats,
        mock_input,
        capsys,
    ):
        main()

        salida = capsys.readouterr().out
        assert "Programa interrumpido por el usuario" in salida
        assert "Programa finalizado" in salida

    @patch("src.main.TiendaMuebles", side_effect=RuntimeError("Fallo crítico"))
    def test_main_error_inesperado(self, mock_tienda, capsys):
        main()

        salida = capsys.readouterr().out
        assert "Error inesperado: Fallo crítico" in salida
        assert "Programa finalizado" in salida
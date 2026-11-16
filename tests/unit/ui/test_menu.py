from unittest.mock import MagicMock, patch
import pytest
from rich.panel import Panel
from rich.table import Table

from src.ui.menu import MenuTienda


class TestMenuTienda:

    @pytest.fixture
    def tienda_mock(self):
        tienda = MagicMock()
        tienda.nombre = "Mueblería Python"
        tienda._inventario = []
        tienda._comedores = []
        return tienda

    @pytest.fixture
    def menu(self, tienda_mock):
        m = MenuTienda(tienda_mock)
        m.console = MagicMock()
        return m

    @pytest.fixture
    def mueble_mock(self):
        mueble = MagicMock()
        mueble.nombre = "Silla Moderna"
        mueble.material = "Madera"
        mueble.color = "Nogal"
        mueble.calcular_precio.return_value = 150.0
        mueble.obtener_descripcion.return_value = "Silla de madera nogal"
        return mueble

    def test_init_menu(self, tienda_mock):
        menu = MenuTienda(tienda_mock)

        assert menu.tienda is tienda_mock
        assert menu.running is True
        assert menu.console is not None

    def test_mostrar_catalogo_completo_vacio(self, menu):
        menu.tienda._inventario = []
        menu.mostrar_catalogo_completo()

        menu.console.print.assert_called_once_with(
            "[yellow]No hay muebles en el inventario.[/yellow]"
        )

    def test_mostrar_catalogo_completo_con_muebles(self, menu, mueble_mock):
        menu.tienda._inventario = [mueble_mock]
        menu.mostrar_catalogo_completo()

        menu.console.print.assert_called_once()
        assert isinstance(menu.console.print.call_args[0][0], Table)

    def test_mostrar_catalogo_completo_con_error_en_precio(self, menu, mueble_mock):
        mueble_mock.calcular_precio.side_effect = Exception("Error de precio")
        menu.tienda._inventario = [mueble_mock]
        menu.mostrar_catalogo_completo()

        menu.console.print.assert_called_once()
        assert isinstance(menu.console.print.call_args[0][0], Table)

    @patch("src.ui.menu.Prompt.ask", return_value="   ")
    def test_buscar_muebles_termino_vacio(self, mock_prompt, menu):
        menu.buscar_muebles_interactivo()

        menu.console.print.assert_called_with("[red]Término de búsqueda vacío.[/red]")
        menu.tienda.buscar_muebles_por_nombre.assert_not_called()

    @patch("src.ui.menu.time.sleep")
    @patch("src.ui.menu.Prompt.ask", return_value="Mesa")
    def test_buscar_muebles_sin_resultados(self, mock_prompt, mock_sleep, menu):
        menu.tienda.buscar_muebles_por_nombre.return_value = []
        menu.buscar_muebles_interactivo()

        menu.tienda.buscar_muebles_por_nombre.assert_called_once_with("Mesa")
        menu.console.print.assert_called_with(
            "[yellow]No se encontraron muebles que contengan 'Mesa'.[/yellow]"
        )

    @patch("src.ui.menu.time.sleep")
    @patch("src.ui.menu.Prompt.ask", return_value="Silla")
    def test_buscar_muebles_con_resultados(
        self, mock_prompt, mock_sleep, menu, mueble_mock
    ):
        menu.tienda.buscar_muebles_por_nombre.return_value = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu.buscar_muebles_interactivo()

        menu._mostrar_lista_muebles.assert_called_once_with([mueble_mock])

    @patch("src.ui.menu.IntPrompt.ask", side_effect=[500, 100])
    def test_filtrar_por_precio_min_mayor_que_max(self, mock_int, menu):
        menu.filtrar_por_precio_interactivo()

        menu.console.print.assert_any_call(
            "[red]Error: El precio mínimo no puede ser mayor al máximo.[/red]"
        )
        menu.tienda.filtrar_por_precio.assert_not_called()

    @patch("src.ui.menu.time.sleep")
    @patch("src.ui.menu.IntPrompt.ask", side_effect=[0, 0])
    def test_filtrar_por_precio_sin_limite_sin_resultados(
        self, mock_int, mock_sleep, menu
    ):
        menu.tienda.filtrar_por_precio.return_value = []
        menu.filtrar_por_precio_interactivo()

        menu.tienda.filtrar_por_precio.assert_called_once_with(0, float("inf"))
        menu.console.print.assert_any_call(
            "[yellow]No hay muebles en el rango $0 - $inf.[/yellow]"
        )

    @patch("src.ui.menu.time.sleep")
    @patch("src.ui.menu.IntPrompt.ask", side_effect=[100, 300])
    def test_filtrar_por_precio_con_resultados(
        self, mock_int, mock_sleep, menu, mueble_mock
    ):
        menu.tienda.filtrar_por_precio.return_value = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu.filtrar_por_precio_interactivo()

        menu.tienda.filtrar_por_precio.assert_called_once_with(100, 300)
        menu._mostrar_lista_muebles.assert_called_once_with([mueble_mock])

    @patch("src.ui.menu.Prompt.ask", return_value="")
    def test_filtrar_por_material_vacio(self, mock_prompt, menu):
        menu.filtrar_por_material_interactivo()

        menu.console.print.assert_called_with(
            "[red]Material no puede estar vacío.[/red]"
        )

    @patch("src.ui.menu.time.sleep")
    @patch("src.ui.menu.Prompt.ask", return_value="vidrio")
    def test_filtrar_por_material_sin_resultados(self, mock_prompt, mock_sleep, menu):
        menu.tienda.filtrar_por_material.return_value = []
        menu.filtrar_por_material_interactivo()

        menu.console.print.assert_called_with(
            "[yellow]No hay muebles de material 'vidrio'.[/yellow]"
        )

    @patch("src.ui.menu.time.sleep")
    @patch("src.ui.menu.Prompt.ask", return_value="madera")
    def test_filtrar_por_material_con_resultados(
        self, mock_prompt, mock_sleep, menu, mueble_mock
    ):
        menu.tienda.filtrar_por_material.return_value = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu.filtrar_por_material_interactivo()

        menu._mostrar_lista_muebles.assert_called_once_with([mueble_mock])

    def test_mostrar_comedores_vacio(self, menu):
        menu.tienda._comedores = []
        menu.mostrar_comedores()

        menu.console.print.assert_called_once_with(
            "[yellow]No hay comedores disponibles.[/yellow]"
        )

    def test_mostrar_comedores_con_elementos(self, menu):
        comedor = MagicMock()
        comedor.obtener_descripcion_completa.return_value = "Comedor 4 puestos"
        menu.tienda._comedores = [comedor]
        menu.mostrar_comedores()

        menu.console.print.assert_called_once()
        assert isinstance(menu.console.print.call_args[0][0], Panel)

    def test_realizar_venta_sin_inventario(self, menu):
        menu.tienda._inventario = []
        menu.realizar_venta_interactiva()

        menu.console.print.assert_called_once_with(
            "[red]No hay muebles disponibles para venta.[/red]"
        )

    @patch("src.ui.menu.Confirm.ask", return_value=False)
    @patch("src.ui.menu.IntPrompt.ask", return_value=1)
    def test_realizar_venta_cancelada(self, mock_int, mock_confirm, menu, mueble_mock):
        menu.tienda._inventario = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu.realizar_venta_interactiva()

        menu.console.print.assert_any_call("[yellow]Venta cancelada.[/yellow]")
        menu.tienda.realizar_venta.assert_not_called()

    @patch("src.ui.menu.Prompt.ask", return_value="Lina")
    @patch("src.ui.menu.Confirm.ask", return_value=True)
    @patch("src.ui.menu.IntPrompt.ask", return_value=1)
    def test_realizar_venta_con_error(
        self, mock_int, mock_confirm, mock_prompt, menu, mueble_mock
    ):
        menu.tienda._inventario = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu.tienda.realizar_venta.return_value = {"error": "Mueble no disponible"}
        menu.realizar_venta_interactiva()

        menu.console.print.assert_any_call("[red]Error: Mueble no disponible[/red]")

    @patch("src.ui.menu.Prompt.ask", return_value="Lina")
    @patch("src.ui.menu.Confirm.ask", return_value=True)
    @patch("src.ui.menu.IntPrompt.ask", return_value=1)
    def test_realizar_venta_exitosa(
        self, mock_int, mock_confirm, mock_prompt, menu, mueble_mock
    ):
        menu.tienda._inventario = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu._mostrar_comprobante_venta = MagicMock()
        resultado = {"cliente": "Lina", "total": 150.0}
        menu.tienda.realizar_venta.return_value = resultado
        menu.realizar_venta_interactiva()

        menu.tienda.realizar_venta.assert_called_once_with(mueble_mock, "Lina")
        menu._mostrar_comprobante_venta.assert_called_once_with(resultado)

    @patch("src.ui.menu.IntPrompt.ask", side_effect=ValueError("Entrada inválida"))
    def test_realizar_venta_seleccion_invalida(self, mock_int, menu, mueble_mock):
        menu.tienda._inventario = [mueble_mock]
        menu._mostrar_lista_muebles = MagicMock()
        menu.realizar_venta_interactiva()

        menu.console.print.assert_any_call("[red]Selección inválida.[/red]")

    @patch("src.ui.menu.time.sleep")
    def test_mostrar_estadisticas_completas(self, mock_sleep, menu):
        menu.tienda.obtener_estadisticas.return_value = {
            "total_muebles": 10,
            "total_comedores": 2,
            "valor_inventario": 2500.0,
            "ventas_realizadas": 4,
            "descuentos_activos": {"madera": 10},
            "total_muebles_vendidos": 4,
            "valor_total_ventas": 900.0,
            "tipos_muebles": {"Silla": 6, "Mesa": 4},
        }
        menu.mostrar_estadisticas()

        assert isinstance(menu.console.print.call_args_list[0][0][0], Table)
        menu.console.print.assert_any_call("\n[cyan]Distribución por tipos:[/cyan]")

    @patch("src.ui.menu.time.sleep")
    def test_mostrar_estadisticas_no_dict(self, mock_sleep, menu):
        menu.tienda.obtener_estadisticas.return_value = None
        menu.mostrar_estadisticas()

        assert isinstance(menu.console.print.call_args_list[0][0][0], Table)

    @patch("src.ui.menu.Confirm.ask", return_value=False)
    @patch("src.ui.menu.time.sleep")
    def test_generar_reporte_sin_guardar(self, mock_sleep, mock_confirm, menu):
        menu.tienda.generar_reporte_inventario.return_value = "Contenido del reporte"
        menu.generar_reporte_interactivo()

        assert isinstance(menu.console.print.call_args_list[0][0][0], Panel)

    @patch("src.ui.menu.Confirm.ask", return_value=True)
    @patch("src.ui.menu.time.sleep")
    def test_generar_reporte_guardado_exitoso(
        self, mock_sleep, mock_confirm, menu, tmp_path
    ):
        archivo = tmp_path / "reporte.txt"
        menu.tienda.generar_reporte_inventario.return_value = "Reporte OK"
        with patch("src.ui.menu.Prompt.ask", return_value=str(archivo)):
            menu.generar_reporte_interactivo()

        assert archivo.read_text(encoding="utf-8") == "Reporte OK"
        menu.console.print.assert_any_call(
            f"[green]Reporte guardado en {archivo}[/green]"
        )

    @patch("builtins.open", side_effect=OSError("Permiso denegado"))
    @patch("src.ui.menu.Prompt.ask", return_value="reporte.txt")
    @patch("src.ui.menu.Confirm.ask", return_value=True)
    @patch("src.ui.menu.time.sleep")
    def test_generar_reporte_error_al_guardar(
        self, mock_sleep, mock_confirm, mock_prompt, mock_open, menu
    ):
        menu.tienda.generar_reporte_inventario.return_value = "Reporte OK"
        menu.generar_reporte_interactivo()

        menu.console.print.assert_any_call(
            "[red]Error al guardar: Permiso denegado[/red]"
        )

    @patch("src.ui.menu.IntPrompt.ask", side_effect=[1, 20])
    def test_aplicar_descuentos_exitoso(self, mock_int, menu):
        menu.tienda.aplicar_descuento.return_value = "Descuento aplicado a silla"
        menu.aplicar_descuentos_interactivo()

        menu.tienda.aplicar_descuento.assert_called_once_with("silla", 20)
        menu.console.print.assert_any_call("[green]Descuento aplicado a silla[/green]")

    @patch("src.ui.menu.IntPrompt.ask", side_effect=ValueError("Entrada inválida"))
    def test_aplicar_descuentos_seleccion_invalida(self, mock_int, menu):
        menu.aplicar_descuentos_interactivo()

        menu.console.print.assert_any_call("[red]Selección inválida.[/red]")

    @pytest.mark.parametrize("numerada", [False, True])
    def test_mostrar_lista_muebles_validos(self, menu, mueble_mock, numerada):
        menu._mostrar_lista_muebles([mueble_mock], numerada=numerada)

        menu.console.print.assert_called_once()
        assert isinstance(menu.console.print.call_args[0][0], Table)

    @pytest.mark.parametrize("numerada", [False, True])
    def test_mostrar_lista_muebles_con_error(self, menu, mueble_mock, numerada):
        mueble_mock.calcular_precio.side_effect = Exception("Error")
        menu._mostrar_lista_muebles([mueble_mock], numerada=numerada)

        menu.console.print.assert_called_once()
        assert isinstance(menu.console.print.call_args[0][0], Table)

    def test_mostrar_lista_muebles_vacia(self, menu):
        menu._mostrar_lista_muebles([], numerada=False)

        menu.console.print.assert_called_once()
        assert isinstance(menu.console.print.call_args[0][0], Table)

    def test_mostrar_comprobante_venta(self, menu):
        venta = {
            "cliente": "Lina",
            "mueble": "Silla Moderna",
            "precio_original": 200.0,
            "descuento": 10.0,
            "precio_final": 180.0,
        }
        menu._mostrar_comprobante_venta(venta)

        menu.console.print.assert_called_once()
        panel_impreso = menu.console.print.call_args[0][0]
        assert isinstance(panel_impreso, Panel)
        assert panel_impreso.title == "Venta Exitosa"

    def test_mostrar_banner(self, menu):
        menu.mostrar_banner()

        assert menu.console.print.call_count == 2
        assert isinstance(menu.console.print.call_args_list[0][0][0], Panel)

    @patch("src.ui.menu.IntPrompt.ask", side_effect=[ValueError("Invalido"), 4])
    def test_mostrar_menu_principal_reintento_y_valido(self, mock_int, menu):
        opcion = menu.mostrar_menu_principal()

        assert opcion == 4
        menu.console.print.assert_any_call(
            "[red]Opción inválida. Intenta de nuevo.[/red]"
        )

    @patch("builtins.input")
    def test_ejecutar_salir_inmediato(self, mock_input, menu):
        menu.mostrar_banner = MagicMock()
        menu.mostrar_menu_principal = MagicMock(return_value=0)
        menu.ejecutar()

        menu.console.clear.assert_called_once()
        menu.mostrar_banner.assert_called_once()
        menu.console.print.assert_any_call("[red]¡Hasta luego! 👋[/red]")
        assert menu.running is False
        mock_input.assert_not_called()

    @pytest.mark.parametrize(
        "opcion,metodo_esperado",
        [
            (1, "mostrar_catalogo_completo"),
            (2, "buscar_muebles_interactivo"),
            (3, "filtrar_por_precio_interactivo"),
            (4, "filtrar_por_material_interactivo"),
            (5, "mostrar_comedores"),
            (6, "realizar_venta_interactiva"),
            (7, "mostrar_estadisticas"),
            (8, "generar_reporte_interactivo"),
            (9, "aplicar_descuentos_interactivo"),
        ],
    )
    @patch("builtins.input", return_value="")
    def test_ejecutar_opciones_menu(self, mock_input, menu, opcion, metodo_esperado):
        menu.mostrar_banner = MagicMock()
        menu.mostrar_menu_principal = MagicMock(side_effect=[opcion, 0])
        setattr(menu, metodo_esperado, MagicMock())
        menu.ejecutar()

        getattr(menu, metodo_esperado).assert_called_once()
        assert menu.running is False
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="")
    def test_ejecutar_opcion_no_reconocida(self, mock_input, menu):
        menu.mostrar_banner = MagicMock()
        menu.mostrar_menu_principal = MagicMock(side_effect=[99, 0])
        menu.ejecutar()

        assert menu.running is False
        mock_input.assert_called_once()

    def test_ejecutar_keyboard_interrupt(self, menu):
        menu.mostrar_banner = MagicMock()
        menu.mostrar_menu_principal = MagicMock(side_effect=KeyboardInterrupt())
        menu.ejecutar()

        menu.console.print.assert_any_call(
            "\n[red]Operación cancelada por el usuario.[/red]"
        )
        assert menu.running is False

    @patch("builtins.input", return_value="")
    def test_ejecutar_error_inesperado(self, mock_input, menu):
        menu.mostrar_banner = MagicMock()
        menu.mostrar_menu_principal = MagicMock(
            side_effect=[RuntimeError("Fallo"), 0]
        )
        menu.ejecutar()

        menu.console.print.assert_any_call("[red]Error inesperado: Fallo[/red]")
        mock_input.assert_called_once()
        assert menu.running is False
        
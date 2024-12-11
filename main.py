import flet as ft
import asyncio
import time
import requests
import json

#criando acesso ao banco de dados

# Tela de Loading
def loading_screen(page: ft.Page):
    page.appbar.visible=False
    loading_image = ft.Image(
        src="AppAT/assets/loading.png",  # Caminho da imagem
        width=500,
        height=250,
        opacity= 0,
        fit=ft.ImageFit.CONTAIN,
    )

    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

    loading_status = ft.Text(
        value="",  
        size=20,
        color="black",  # Ajuste a cor conforme o tema
        text_align=ft.TextAlign.CENTER
    )

    def animate_loading():
        for i in range(51):
            loading_image.opacity= i/50
            page.update()
            time.sleep(0.2)

    async def check_status():
        loading_status.value = 'Iniciando...'
        await asyncio.sleep(1)
        loading_status.value = 'Vericando Conexão...'
        await asyncio.sleep(2)
        def is_internet_connected(url="http://www.google.com", timeout=5):
            try:
                response = requests.get(url, timeout=timeout)
                return response.status_code == 200
            except requests.ConnectionError:
                return False
        if is_internet_connected():
            loading_status.value = 'Atualizando Informações...'
            page.update()
            #verificar código de atualização.
            await asyncio.sleep(2)
            loading_status.value = "Concluído!"
            page.update()
            await asyncio.sleep(2)
            if page.controls:
                page.controls[0] = HomeScreen(page)
            else:
                page.add(HomeScreen())
            page.update()

        else:
            loading_status.value = 'Falha na Conexão'
    
    # Adiciona a imagem à página
    page.add(
        ft.Column(
            [loading_image, ft.Row([pr, loading_status], alignment=ft.MainAxisAlignment.CENTER)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )
    page.run_task(check_status)
    animate_loading()


# Tela Principal (Home Screen)
class HomeScreen(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.appbar.visible=True

        if page.controls:
            page.clean()

        page.add(
            ft.Container(
                    margin=ft.Margin(20, 0, 60, 0),
                    content=ft.Row(
                        [
                            ft.IconButton(ft.icons.ARROW_BACK_ROUNDED),
                            ft.Text('Linhas', theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                            ft.Container() 
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            ft.Image("AppAT/assets/arotec.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: Arotec(),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                            ),
                        ft.Container(
                            ft.Image("AppAT/assets/struers1.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: print('teste'),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    )
                            ),
                        ft.Container(
                            ft.Image("AppAT/assets/foerster.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: print('teste'),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    )
                            ),
                        ft.Container(
                            ft.Image("AppAT/assets/Evident.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: print('teste'),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    )
                            )
                    ],
                    height=180,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border_radius=ft.border_radius.all(16),
                height=200,
                margin=ft.Margin(0,50,0,0)
            )
        )

        # Conteúdo da Home Screen
        def Arotec():
            page.clean()
            page.add(
                ft.Container(
                    margin=ft.Margin(20, 0, 60, 40),
                    content=ft.Row(
                        [
                            ft.IconButton(ft.icons.ARROW_BACK_ROUNDED, on_click=lambda e: HomeScreen(page)),
                            ft.Text('Máquinas', theme_style=ft.TextThemeStyle.HEADLINE_SMALL), 
                            ft.Container()
                            ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),
                ft.Container(
                    content=ft.ListView([
                        ft.FilledTonalButton('Cortadoras', style=ft.ButtonStyle(text_style=ft.TextStyle(size=20))),
                        ft.FilledTonalButton('Embutidoras', style=ft.ButtonStyle(text_style=ft.TextStyle(size=20))),
                        ft.FilledTonalButton('Politrizes e Lixadeiras', style=ft.ButtonStyle(text_style=ft.TextStyle(size=20))),
                    ],
                    spacing=20,
                    width=600,
                    ),
                    alignment=ft.alignment.center,
                ),
                # ft.Container(
                #     content=ft.Row(),
                #     bgcolor=ft.colors.BLUE,
                #     expand=True,
                #     margin=ft.Margin(0,20,0,0)
                # )
            )

# Função principal do aplicativo
def main(page: ft.Page):
    page.title = "App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.spacing = 0
    page.window.width = 1000
    page.window.height=600

    page.appbar = ft.AppBar(
        bgcolor=ft.colors.ON_INVERSE_SURFACE,
        leading=ft.Image('AppAT/assets/logo.png'),
        leading_width=120,
        center_title=True,
        actions=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.IconButton(ft.icons.SEARCH_SHARP, on_click=lambda e: search_btn(), on_blur=lambda e: close_search()),
                        ft.IconButton(ft.icons.MENU),
                    ]
                ),
                margin=ft.Margin(0,0,10,0)
            ),
        ],
    )

    def handle_dismissal(e):
        page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.control.selected_index}"))

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.Text('Menu', text_align=ft.TextAlign.CENTER),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                selected_icon_content=ft.Icon(ft.icons.BUILD),
                icon_content=ft.Icon(ft.icons.BUILD_OUTLINED),
                label="Troubleshooting",
            ),
            ft.NavigationDrawerDestination(
                selected_icon_content=ft.Icon(ft.icons.DRIVE_FILE_MOVE_ROUNDED),
                icon_content=ft.Icon(ft.icons.DRIVE_FILE_MOVE_OUTLINED),
                label="Manuais",
            ),
        ],
    )

    def close_search(e=None):
        # Remove o campo de busca e restaura o título original
        page.appbar.title = None
        page.update()
    
    def search_btn():
        page.appbar.title = ft.TextField(
            autofocus=True,
            on_blur=lambda e: close_search(),
            height=35,
            width=500,
            content_padding=ft.padding.symmetric(vertical=5, horizontal=10)
            # cursor_height=15
        )
        page.update()

    # page.window.title_bar_hidden = True
    # page.window.icon = caminho para arquivo .ico

    page.bgcolor = ft.colors.ON_PRIMARY

    # Inicializa com a tela de Loading
    HomeScreen(page)

# Executa o aplicativo
ft.app(target=main)

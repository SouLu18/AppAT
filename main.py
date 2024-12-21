import flet as ft
import asyncio
import time
import requests
import json

class Loading(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(page)

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

                ### CÓDIGO PARA VERIFICAR ATUALIZAÇÕES ###

                await asyncio.sleep(2)
                loading_status.value = "Iniciando"
                page.update()
                await asyncio.sleep(2)
                LoginScreen(page)

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

class LoginScreen(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.bgcolor = ft.colors.ON_PRIMARY_CONTAINER
        page.bottom_appbar = ft.BottomAppBar(
            ft.Row(
                [
                    ft.Text('v1.0')
                ]
            ),
            height=50
        )

        link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
        requisicao = requests.get(f'{link}/Logins/.json')
        dic_re = requisicao.json()
    
        if page.controls:
            page.clean()

        self.user = ft.TextField(on_submit=lambda e: login(), autofocus=True)
        password = ft.TextField(on_submit=lambda e: login(), password=True, can_reveal_password=True)
        alerta = ft.AlertDialog(
            content=ft.Column(
                [
                    ft.Text('Acesso negado', size=18),
                    ft.Text('Verifique as credenciais e tente novamente')
                ],
                height=40
            ),
            actions=[ft.TextButton('OK', on_click=lambda e: page.close(alerta), autofocus=True)],
        )
        
        page.add(
            ft.Container(
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(content=ft.Text('Login', text_align=ft.TextAlign.END, size=32, color='#35588e'), margin=ft.Margin(0,10,0,0)),
                            ft.Container(content=ft.Divider()),
                            ft.Column([ft.Text('Usuário', color='#35588e', size=16), self.user]),
                            ft.Column([ft.Text('Senha', color='#35588e', size=16), password]),
                            ft.Checkbox('Continuar logado'),
                            ft.Container(content=ft.ElevatedButton('Logar'), margin=ft.Margin(0,0,0,10))
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    margin=ft.Margin(20,0,20,0),
                ),
                width=400,
                bgcolor=ft.colors.ON_INVERSE_SURFACE,
                border_radius=16
            )
        )

        def login():
            if self.user.value == 'arotec':
                if password.value == dic_re['Default']['password']:
                    HomeScreen(page, self.user.value)
                else:
                    page.open(alerta)
            elif self.user.value == 'admin':
                if password.value == dic_re['ADM']['password']:
                    HomeScreen(page, self.user.value)
                else:
                    page.open(alerta)
            else:
                page.open(alerta)

class HomeScreen(ft.Container):
    def __init__(self, page: ft.Page, user):
        super().__init__(page)
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.bgcolor = ft.colors.ON_PRIMARY
        self.user = user

        if page.controls:
            page.clean()

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
                            ft.IconButton(ft.icons.MENU, on_click=lambda e: open_drawer()),
                        ]
                    ),
                    margin=ft.Margin(0,0,10,0)
                ),
            ],
        )

        page.add(
            ft.Container(
                    margin=ft.Margin(20, 0, 60, 0),
                    content=ft.Row(
                        [
                            ft.IconButton(ft.icons.ARROW_BACK_ROUNDED),
                            ft.TextButton(content=ft.Text("Linhas", size=22)),
                            ft.Container() 
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),
            ft.Divider(),
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            ft.Image("AppAT/assets/arotec.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: Arotec(page, user), padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                            ),
                        ft.Container(
                            ft.Image("AppAT/assets/struers.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: print('teste'), padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                            ),
                        ft.Container(
                            ft.Image("AppAT/assets/foerster.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: print('teste'), padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    )
                            ),
                        ft.Container(
                            ft.Image("AppAT/assets/evident.png"), width=140, height=160, 
                            bgcolor=ft.colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: print('teste'), padding=ft.padding.all(10),
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
                expand=True,
                alignment=ft.alignment.center
            )
        )

        page.update()

        def close_search(e=None):
            page.appbar.title = None
            page.update()
    
        def search_btn():
            search=ft.TextField(
                autofocus=True,
                on_blur=lambda e: close_search(),
                height=35,
                width=500,
                # on_submit=lambda e: searching(search.value),
                content_padding=ft.padding.symmetric(vertical=5, horizontal=10)
            )
            page.appbar.title = search
            page.update()

        def open_drawer():
            end_drawer = ft.NavigationDrawer(
                position=ft.NavigationDrawerPosition.END,
                selected_index=-1,
                on_change=lambda e: on_selected(e, end_drawer),
                controls=[
                    ft.Container(height=12),
                    ft.Text('Menu', text_align='center'),
                    ft.Divider(thickness=2),
                    ft.NavigationDrawerDestination(
                        icon_content=ft.Icon(ft.icons.SETTINGS),
                        label="Configurações",
                    ),
                    ft.Container(height=12),
                    ft.NavigationDrawerDestination(
                        icon_content=ft.Icon(ft.icons.DOWNLOAD),
                        label="Downloads",
                    ),
                    ft.Container(height=12),
                    ft.NavigationDrawerDestination(
                        icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
                        label="Sair",
                    ),
                ],
            )
            page.open(end_drawer)

        def on_selected(e, menu):
            if e.control.selected_index == 0:
                print("Configurações clicado!")
            elif e.control.selected_index == 1:
                print("Downloads clicado!")
            elif e.control.selected_index == 2:
                page.close(menu)
                LoginScreen(page)

class Arotec(ft.Container):
    def __init__(self, page: ft.Page, user):
        super().__init__(page)
        self.user = user
        page.clean()
        page.add(
            ft.Container(
                margin=ft.Margin(20, 0, 60, 0),
                content=ft.Row(
                    [
                        ft.IconButton(ft.icons.ARROW_BACK_ROUNDED, on_click=lambda e: HomeScreen(page, self.user)),
                        ft.Row(
                            [
                                ft.TextButton(content=ft.Text("Arotec", size=22), on_click=lambda e: HomeScreen(page, self.user)),
                                ft.TextButton(content=ft.Text("Máquinas", size=22), disabled=True),
                            ],
                        ),
                        ft.Container()
                        ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ),
            ft.Divider(),
            ft.Container(
                margin=ft.Margin(0,0,0,0),
                content=ft.Column(
                    [
                        ft.ListView([
                                ft.FilledTonalButton('Cortadoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE ,text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0,-1)), on_click=lambda e: self.equip_list(page, 'Cortadoras')),
                                ft.FilledTonalButton('Embutidoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0,-1)), on_click=lambda e: self.equip_list(page, 'Embutidoras')),
                                ft.FilledTonalButton('Politrizes e Lixadeiras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0,-1)), on_click=lambda e: self.equip_list(page, 'Politriz e Lixadeira')),
                            ],
                            spacing=20,
                            width=600,
                            ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
                image=ft.DecorationImage(src='AppAT/assets/loading.png', opacity=0.1)
            ),
        )

    ###ADICIONAR LAYOUTS###
    # card_equip = 
    # card_comp =
    # card_problem = 
    
    def equip_list(self, page, equip):



def main(page: ft.Page):
    page.title = "AppAT"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 0
    page.bgcolor = ft.colors.ON_PRIMARY
    page.window.maximized = True

    Loading(page)

    

ft.app(target=main)
 
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
        if page.appbar:
            page.appbar = None

        while page.controls != []:
            page.controls.pop()

        link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
        requisicao = requests.get(f'{link}/Logins/.json')
        dict_re = requisicao.json()
    
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
                if password.value == dict_re['Default']['password']:
                    HomeScreen(page, self.user.value)
                else:
                    page.open(alerta)
            elif self.user.value == 'admin':
                if password.value == dict_re['ADM']['password']:
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
                        icon_content=ft.Icon(ft.icons.STAR),
                        label="Favoritos",
                    ),
                    # ft.Container(height=12),
                    # ft.NavigationDrawerDestination(
                    #     icon_content=ft.Icon(ft.icons.TEXT_SNIPPET),
                    #     label="Relatório",
                    # ),
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
                print("Favoritos clicado!")
            # elif e.control.selected_index == 3:
            #     print("Relatório clicado!")
            elif e.control.selected_index == 3:
                page.close(menu)
                LoginScreen(page)

class Arotec(ft.Container):
    def __init__(self, page: ft.Page, user):
        super().__init__(page)
        self.user = user
        page.clean()
        self.cont_way = ft.Container(
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
        )
        page.add(
            self.cont_way,
            ft.Divider(),
            ft.Container(
                margin=ft.Margin(0,0,0,0),
                content=ft.Column(
                    [
                        ft.ListView([
                                ft.FilledTonalButton('Cortadoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE ,text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0, 0)), on_click=lambda e: self.equip_list(page, 'Cortadoras')),
                                ft.FilledTonalButton('Embutidoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0, 0)), on_click=lambda e: self.equip_list(page, 'Embutidoras')),
                                ft.FilledTonalButton('Politrizes e Lixadeiras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0, 0)), on_click=lambda e: self.equip_list(page, 'Politriz e Lixadeira')),
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
        self.link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
        self.list_opt = ft.ListView(spacing=10, padding=0, divider_thickness=1, expand=True)
        self.button_add = ft.Container(
            margin=ft.Margin(90,10,0,0),
            content=ft.Row(
                [
                    ft.ElevatedButton(icon=ft.icons.ADD, text='Adicionar Máquina')
                ]
            ),
        )
    
    def equip_list(self, page, maquinas):
        requisicao = requests.get(f'{self.link}/Equipamentos/.json')
        dict_requisicao = requisicao.json()
        dict_mach = dict_requisicao[f'{maquinas}']
        self.list_opt.controls.clear()
        self.list_opt.divider_thickness = 1

        for id in dict_mach:
            mach_row = ft.Row(
                [
                    ft.Icon(ft.icons.ARROW_RIGHT),
                    ft.TextButton(content=ft.Text(f'{id}'), on_click=lambda e, id=id: self.selected_maq(page, maquinas, id)),
                    ft.Container(expand=True),
                    ft.IconButton(ft.icons.DOWNLOAD),
                    ft.PopupMenuButton(items=[
                        ft.PopupMenuItem('Editar', ft.icons.EDIT, on_click=lambda e, id=id: edit(id)),
                        ft.PopupMenuItem('Favoritos', ft.icons.STAR_BORDER_OUTLINED),
                        ft.PopupMenuItem('Delete', ft.icons.DELETE, on_click=lambda e, id=id: delete(id))
                    ])
                ]
            )
            if self.user != 'admin':
                mach_row.controls[4].items.pop()
            self.list_opt.controls.append(mach_row)

        while len(page.controls) > 2: 
            page.controls.pop()
        
        while len(self.cont_way.content.controls[1].controls) > 2:
            self.cont_way.content.controls[1].controls.pop()

        self.cont_way.content.controls[0].on_click = lambda e: Arotec(page, self.user)
        self.cont_way.content.controls[1].controls[1].disabled = False
        self.cont_way.content.controls[1].controls[1].on_click = lambda e: Arotec(page, self.user)
        self.cont_way.content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{maquinas}', size=22), disabled=True)) #adicionando a trilha
        self.button_add.content.controls[0].on_click=lambda e: new_model(page, maquinas) # função button add
        self.button_add.content.controls[0].text = 'Adicionar Máquina'
        page.add(
            self.button_add,
            ft.Container(
                margin=ft.Margin(20,25,20,20),
                content=self.list_opt,
                expand=True
            ),
        ) # adicionando container com lista de opções.

        def edit(id):
            def save():
                dlg.actions.clear()
                if self.edit.value in dict_mach:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.icons.WARNING),ft.Text('Máquina já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                else:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    old_path = f'{self.link}/Equipamentos/{maquinas}/{id}/'
                    new_path = f'{self.link}/Equipamentos/{maquinas}/{self.edit.value}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    self.equip_list(page, maquinas)


            self.edit = ft.TextField(label='Máquina', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.edit,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

        def delete(id):
            emoji = '\u26A0'
            alerta = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Você realmente deseja apagar {id}?"),
                    content=ft.ResponsiveRow([ 
                                ft.Text(f'{emoji} Não será possível recuperar os dados apagados', size=14, col={"sm": 5, "md": 10, "xl": 10}, )
                            ]),
                    actions=[
                        ft.TextButton("Yes", on_click=lambda e: yes_no('yes')),
                        ft.TextButton("No", on_click=lambda e: yes_no('no')),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            page.open(alerta)
            def yes_no(answer):
                if answer == 'yes':
                    page.close(alerta)
                    link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
                    requests.delete(f'{link}/Equipamentos/{maquinas}/{id}.json')
                    self.equip_list(page, maquinas)
                else:
                    page.close(alerta)

        def new_model(page, mach):
            def save():
                dlg.actions.clear()
                if self.name.value in dict_mach:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.icons.WARNING),ft.Text('Máquina já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                else:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    dados = {"status": "vazio"}
                    requests.put(f'{self.link}/Equipamentos/{mach}/{self.name.value}/Problemas.json', data=json.dumps(dados))
                    page.close(dlg)
                    self.equip_list(page, mach)
                

            self.name = ft.TextField(label='Nome da Máquina', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.name,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)
            
    def selected_maq(self, page, maq, model):
        requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/Problemas.json')
        dict_problem = requisicao.json()
        self.list_opt.divider_thickness = 0
        self.list_opt.controls.clear()

        for id in dict_problem:
            if id == 'status':
                pass
            else:
                comp_row = ft.Container(
                    ft.Row(
                        [
                            ft.Icon(ft.icons.ARROW_RIGHT),
                            ft.Text(f'{id}', size=20),
                            ft.Container(expand=True),
                            ft.IconButton(ft.icons.DOWNLOAD),
                            ft.PopupMenuButton(items=[
                                ft.PopupMenuItem('Editar', ft.icons.EDIT, on_click= lambda e, id=id: edit(id)),
                                ft.PopupMenuItem('Deletar', ft.icons.DELETE, on_click=lambda e, id=id: delete(id)),
                            ])
                        ]
                    ),
                    bgcolor=ft.colors.ON_INVERSE_SURFACE,
                    border_radius=16,
                    on_click= lambda e, id=id: self.selected_comp(page, maq,model,id)
                )
                if self.user != 'admin':
                    comp_row.content.controls[4].items.pop()
                self.list_opt.controls.append(comp_row)
        
        while len(page.controls) > 2: 
            page.controls.pop()
        
        while len(self.cont_way.content.controls[1].controls) > 3:
            self.cont_way.content.controls[1].controls.pop()

        page.controls[0].content.controls[0].on_click = lambda e: self.equip_list(page, maq)
        page.controls[0].content.controls[1].controls[2].on_click = lambda e: self.equip_list(page, maq)
        self.cont_way.content.controls[1].controls[-1].disabled = False,
        self.cont_way.content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{model}', size=22), disabled=True)) #adicionando a trilha
        self.button_add.content.controls[0].text = 'Adicionar Componente'
        self.button_add.content.controls[0].on_click=lambda e: new_comp() # função button add

        page.add(
            self.button_add,
            ft.Container(
                margin=ft.Margin(20,20,20,20),
                content=self.list_opt,
                expand=True
            )  
        )

        def edit(id):
            def save():
                dlg.actions.clear()
                if self.edit.value in dict_problem:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                else:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    old_path = f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{id}/'
                    new_path = f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{self.edit.value}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    self.selected_maq(page, maq, model)


            self.edit = ft.TextField(label='Componente', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.edit,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

        def delete(id):
            emoji = '\u26A0'
            alerta = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Você realmente deseja apagar {id}?"),
                    content=ft.ResponsiveRow([ 
                                ft.Text(f'{emoji} Não será possível recuperar os dados apagados', size=14, col={"sm": 5, "md": 10, "xl": 10}, )
                            ]),
                    actions=[
                        ft.TextButton("Sim", on_click=lambda e: yes_no('yes')),
                        ft.TextButton("Não", on_click=lambda e: yes_no('no')),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            page.open(alerta)
            def yes_no(answer):
                if answer == 'yes':
                    page.close(alerta)
                    requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{id}.json')
                    page.controls[0].content.controls[1].controls.pop()
                    self.selected_maq(page, maq, model)
                else:
                    page.close(alerta)

        def new_comp():
            def save():
                dlg.actions.clear()
                if self.edit.value in dict_problem:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                else:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    dados = {'vazio': 'vazio'}
                    requests.put(f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{self.comp.value}/.json', data=json.dumps(dados))
                    page.close(dlg)
                    page.controls[0].content.controls[1].controls.pop()
                    self.selected_maq(page, maq, model)

            self.comp = ft.TextField(label='Componente', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.comp,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)
        
    def selected_comp(self, page, maq, model, comp):
        requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{comp}.json')
        dict_trouble = requisicao.json()
        self.list_opt.controls.clear()
        self.list_opt.spacing=20

        for problem in dict_trouble:
            problem_details = dict_trouble[problem]
            if isinstance(problem_details, dict):
                descricao = problem_details.get('descrição', 'Descrição não encontrada')
                solucao = problem_details.get('solução', 'Solução não encontrada')
            else:
                continue
            cont_problem = ft.Container(
                ft.Column(
                    [
                        # Texto principal
                        ft.Row([ft.Text(f'{problem}', size=20)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
                        ft.Divider(),
                        
                        # Container com Row ajustável
                        ft.Container(
                            margin=ft.Margin(20, 5, 20, 10),
                            content=ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(f'Detalhes', size=20),
                                            ft.Container(
                                                ft.Column(
                                                    controls=[
                                                        ft.Text(f'{descricao}', size=18, max_lines=6, overflow='ellipsis'),
                                                        ft.Divider(),
                                                        ft.Row([
                                                            ft.IconButton('open_in_new', on_click=lambda e, item=descricao: open_view(item)), 
                                                            ft.IconButton('edit')
                                                            ])
                                                    ] if self.user == 'admin' else [
                                                        ft.Text(f'{descricao}', size=18, max_lines=6, overflow='ellipsis'),
                                                        ft.Divider(),
                                                        ft.Row([ft.IconButton('open_in_new', on_click=lambda e, item=descricao: open_view(item))])
                                                    ],
                                                    spacing=0
                                                ),
                                                border=ft.border.all(color='black'),
                                                border_radius=ft.border_radius.all(8),
                                                padding=10,
                                                expand=True
                                            )
                                        ],
                                        expand=True,
                                        horizontal_alignment='center'
                                    ),
                                    ft.Container(),
                                    ft.Column(
                                        [
                                            ft.Text(f'Solução', size=20),
                                            ft.Container(
                                                ft.Column(
                                                    controls= [
                                                        ft.Text(f'{solucao}', size=18, max_lines=6, overflow='ellipsis'),
                                                        ft.Divider(),
                                                        ft.Row(
                                                            controls=[
                                                                ft.IconButton('open_in_new', on_click=lambda e, solucao=solucao: open_view(solucao)), 
                                                                ft.IconButton('edit')
                                                            ] if self.user == 'admin' else [
                                                                ft.IconButton('open_in_new', on_click=lambda e, solucao=solucao: open_view(solucao))
                                                            ]
                                                        )
                                                    ] if solucao != 'Adicionar Soluções' else [
                                                        ft.TextButton(
                                                            content=ft.Row(
                                                                [ft.Icon('add'),ft.Text(f'{solucao}', size=18, text_align='center')]
                                                            )
                                                        )
                                                    ],
                                                    spacing=0
                                                ),
                                                border=ft.border.all(color='black'),
                                                border_radius=ft.border_radius.all(8),
                                                padding=10,
                                                expand=True
                                            )
                                        ],
                                        expand=True,
                                        horizontal_alignment='center'
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=True,
                                vertical_alignment='start'
                            )
                        ),
                        ft.Container(
                            content =ft.Row(
                                controls = [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT, 
                                        on_click=lambda e, problem=problem: edit(problem)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE, 
                                        on_click=lambda e, problem=problem: delete(problem)
                                    ),
                                    ft.Container(expand=True),
                                    ft.Icon('check_circle')
                                ] if solucao != 'Adicionar Soluções' else [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT, 
                                        on_click=lambda e, problem=problem: edit(problem)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE, 
                                        on_click=lambda e, problem=problem: delete(problem)
                                    ),
                                    ft.Container(expand=True),
                                    ft.Icon('QUESTION_MARK')
                                ],
                                alignment='spaceBetween'
                            ) if self.user == 'admin' else ft.Row(
                                controls = [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT, 
                                        on_click=lambda e, problem=problem: edit(problem)
                                    ),
                                    ft.Icon('check_circle')
                                ] if solucao != 'Adicionar Soluções' else [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT, 
                                        on_click=lambda e, problem=problem: edit(problem)
                                    ),
                                    ft.Icon('QUESTION_MARK')
                                ],
                                alignment='spaceBetween'
                            ),
                            margin=ft.Margin(20, 0, 20, 5)
                        )
                    ],
                    expand=True,  # Expande a coluna para ocupar o espaço disponível
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0
                ),
                border_radius=16,
                bgcolor='oninversesurface',
                padding=ft.Padding(top=20, left=0, right=0, bottom=0),
            )
            self.list_opt.controls.append(cont_problem)

        comp_row = ft.Container(
            ft.Row(
                [
                    ft.Icon(ft.icons.ARROW_RIGHT, rotate = ft.Rotate(angle=3.14159 / 2)),
                    ft.Text(f'{comp}', size=20),
                    ft.Container(expand=True),
                    ft.IconButton(ft.icons.DOWNLOAD),
                    ft.PopupMenuButton(items=[
                        ft.PopupMenuItem('Favoritos', ft.icons.STAR_BORDER_OUTLINED),
                        ft.PopupMenuItem('Editar', ft.icons.EDIT, on_click= lambda e, comp=comp: edit_comp(comp)),
                        ft.PopupMenuItem('Deletar', ft.icons.DELETE, on_click=lambda e, comp=comp: delete_comp(comp)),
                    ])
                ]
            ),
            margin=ft.Margin(5,15,5,5),
            bgcolor=ft.colors.ON_INVERSE_SURFACE,
            border_radius=16,
            on_click= lambda e: self.selected_maq(page, maq, model)
        )
        if self.user != 'admin':
            comp_row.content.controls[4].items.pop()
            comp_row.content.controls[4].items.pop()

        def edit_comp(id):
            def save():
                dlg.actions.clear()
                requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/Problemas.json')
                dict_problem = requisicao.json()
                if self.edit.value in dict_problem:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                else:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    old_path = f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{id}/'
                    new_path = f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{self.edit.value}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    self.selected_maq(page, maq, model)


            self.edit = ft.TextField(label='Componente', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.edit,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

        def delete_comp(id):
            emoji = '\u26A0'
            alerta = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Você realmente deseja apagar {id}?"),
                    content=ft.ResponsiveRow([ 
                                ft.Text(f'{emoji} Não será possível recuperar os dados apagados', size=14, col={"sm": 5, "md": 10, "xl": 10}, )
                            ]),
                    actions=[
                        ft.TextButton("Sim", on_click=lambda e: yes_no('yes')),
                        ft.TextButton("Não", on_click=lambda e: yes_no('no')),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            page.open(alerta)
            def yes_no(answer):
                if answer == 'yes':
                    requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{id}.json')
                    page.close(alerta)
                    self.selected_maq(page, maq, model)
                else:
                    page.close(alerta)

        while len(page.controls) > 2: 
            page.controls.pop()
        
        #reiniciando a trilha de caminhos
        while len(self.cont_way.content.controls[1].controls) > 4:
            self.cont_way.content.controls[1].controls.pop()
                
        self.cont_way.content.controls[0].on_click = lambda e: self.selected_maq(page, maq, model)
        self.cont_way.content.controls[1].controls[3].on_click = lambda e: self.selected_maq(page, maq, model)
        self.cont_way.content.controls[1].controls[-1].disabled = False,
        self.cont_way.content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{comp}', size=22), disabled=True)) #adicionando a trilha
        self.button_add.content.controls[0].text = 'Adicionar Problemas'
        self.button_add.content.controls[0].on_click=lambda e: new_problem() # função button add
        self.match = False

        page.add(
            self.button_add,
            comp_row,
            ft.Container(
                self.list_opt,
                margin=ft.Margin(20,15,20,0),
                expand=True
            )
        )

        def new_problem():
            def save():
                counter = 1
                original_value = descricao.value
                while descricao.value in dict_trouble:
                    parts = descricao.value.split("_")
                    if len(parts) > 1 and parts[-1].isdigit():
                        descricao.value = "_".join(parts[:-1])
                    else:
                        descricao.value = original_value
                    descricao.value = f"{descricao.value}_{counter}"
                    counter += 1
                        
                if not descricao.value.strip():
                    descricao.error_text='Adicione uma descrição'
                    descricao.focus()
                elif not detail.value.strip():
                    detail.focus()
                elif not resolution.value.strip():
                    resolution.value='Adicionar Soluções'
                else:
                    dlg.content.clean()
                    dlg.actions.clear()
                    dlg.content.controls.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Registrando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    dados = {'descrição': f'{detail.value}', 'solução': f'{resolution.value}'}
                    requests.put(f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{comp}/{descricao.value}.json', data=json.dumps(dados))
                    page.close(dlg)
                    self.selected_comp(page, maq, model, comp)
            descricao = ft.TextField(label='Descrição', border_radius=16, on_submit=lambda e: save(), autofocus=True)
            detail = ft.TextField(label='Detalhes do erro', border_radius=16, on_submit=lambda e: save(), multiline=True, height=50,)
            resolution = ft.TextField(label='Solução', border_radius=16, on_submit=lambda e: save(), multiline=True, height=50)

            dlg = ft.AlertDialog(
                content=ft.Column(
                    [
                        descricao,
                        detail,
                        resolution,
                    ],
                    spacing=8,
                    tight=True,
                ),
                actions=[ft.FilledButton(text="Salvar", on_click=lambda e: save())],
                on_dismiss=lambda e: save()
            )
            page.open(dlg)

        def delete(item):
            emoji = '\u26A0'
            alerta = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Você realmente deseja apagar {item}?"),
                    content=ft.ResponsiveRow([ 
                                ft.Text(f'{emoji} Não será possível recuperar os dados apagados', size=14, col={"sm": 5, "md": 10, "xl": 10}, )
                            ]),
                    actions=[
                        ft.TextButton("Sim", on_click=lambda e: yes_no('yes')),
                        ft.TextButton("Não", on_click=lambda e: yes_no('no')),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            page.open(alerta)

            def yes_no(answer):
                if answer == 'yes':
                    requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{comp}/{item}.json')
                    self.selected_comp(page, maq, model, comp)
                page.close(alerta)
            
        def edit(item):
            def save():
                dlg.actions.clear()
                if self.edit.value in dict_trouble:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.icons.WARNING),ft.Text('Problema já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                else:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    old_path = f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{comp}/{item}/'
                    new_path = f'{self.link}/Equipamentos/{maq}/{model}/Problemas/{comp}/{self.edit.value}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    self.selected_comp(page, maq, model, comp)


            self.edit = ft.TextField(label='Descrição', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.edit,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

        def open_view(item):
            dlg = ft.AlertDialog(
                content=ft.Column(
                    [
                        ft.Text(f'{item}', size=20, max_lines=20),
                    ],
                    spacing=8,
                    scroll=True,
                ),
                actions_padding=10,
            )
            page.open(dlg)





def main(page: ft.Page):
    page.title = "AppAT"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.ON_PRIMARY
    page.window.maximized = True

    Loading(page)

    

ft.app(target=main)
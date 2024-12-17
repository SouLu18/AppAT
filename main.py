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
        page.appbar.visible=False
        page.bgcolor = ft.colors.ON_PRIMARY_CONTAINER

        link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
        requisicao = requests.get(f'{link}/Logins/.json')
        dic_re = requisicao.json()
    
        if page.controls:
            page.clean()

        user = ft.TextField(on_submit=lambda e: login())
        password = ft.TextField(on_submit=lambda e: login(), password=True, can_reveal_password=True)
        alerta = ft.AlertDialog(
            content=ft.Column(
                [
                    ft.Text('Acesso negado', size=18),
                    ft.Text('Verifique as credenciais e tente novamente')
                ],
                height=20
            )
        )
        
        page.add(
            ft.Container(
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(content=ft.Text('Login', text_align=ft.TextAlign.END, size=32, color='#35588e'), margin=ft.Margin(0,10,0,0)),
                            ft.Container(content=ft.Divider()),
                            ft.Column([ft.Text('Usuário', color='#35588e', size=16), user]),
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
            if user.value == 'arotec':
                if password.value == dic_re['Default']['password']:
                    HomeScreen(page, user.value)
                else:
                    page.open(alerta)
            elif user.value == 'admin':
                if password.value == dic_re['ADM']['password']:
                    HomeScreen(page, user.value)
            else:
                page.open(alerta)
                    


class HomeScreen(ft.Container):
    def __init__(self, page: ft.Page, user):
        super().__init__()
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.bgcolor = ft.colors.ON_PRIMARY
        page.appbar.visible=True
        self.user = user

        if page.controls:
            page.clean()

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
                expand=True,
                alignment=ft.alignment.center
            )
        )

        # Conteúdo da Home Screen
        def Arotec():
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
                                    ft.FilledTonalButton('Cortadoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE ,text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0,-1)), on_click=lambda e: equip_list('Cortadoras')),
                                    ft.FilledTonalButton('Embutidoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0,-1)), on_click=lambda e: equip_list('Embutidoras')),
                                    ft.FilledTonalButton('Politrizes e Lixadeiras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0,-1)), on_click=lambda e: equip_list('Politriz e Lixadeira')),
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
        
        def equip_list(maquinas):
            link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
            requisicao = requests.get(f'{link}/Equipamentos/.json')
            dic_requisicao = requisicao.json()
            dic_mach = dic_requisicao[f'{maquinas}']

            self.list_mach = ft.ListView(spacing=10, padding=0, divider_thickness=1, expand=True)

            for id in dic_mach:
                if self.user == 'admin':
                    self.list_mach.controls.append(
                        ft.Row(
                            [
                                ft.Icon(ft.icons.ARROW_RIGHT),
                                ft.TextButton(content=ft.Text(f'{id}'), on_click=lambda e, id=id: selected_maq(page, maquinas, id)),
                                ft.Container(expand=True),
                                ft.IconButton(ft.icons.DOWNLOAD),
                                ft.PopupMenuButton(items=[
                                    ft.PopupMenuItem('Editar', ft.icons.EDIT, on_click=lambda e, id=id: edit(id)),
                                    ft.PopupMenuItem('Delete', ft.icons.DELETE, on_click=lambda e, id=id: delete(id))
                                ])
                            ]
                        )
                    )
                else:
                    self.list_mach.controls.append(
                        ft.Row(
                            [
                                ft.Icon(ft.icons.ARROW_RIGHT),
                                ft.TextButton(content=ft.Text(f'{id}'), on_click=lambda e, id=id: selected_maq(page, maquinas, id)),
                                ft.Container(expand=True),
                                ft.IconButton(ft.icons.DOWNLOAD),
                                ft.PopupMenuButton(items=[
                                    ft.PopupMenuItem('Editar', ft.icons.EDIT, on_click=lambda e, id=id: edit(id)),
                                    ft.PopupMenuItem('Delete', ft.icons.DELETE, on_click=lambda e, id=id: delete(id), disabled=True)
                                ])
                            ]
                        )
                    )

            def edit(id):
                def save():
                    dlg.actions.clear()
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    old_path = f'{link}/Equipamentos/{maquinas}/{id}/'
                    new_path = f'{link}/Equipamentos/{maquinas}/{self.edit.value}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    equip_list(maquinas)


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
                        equip_list(maquinas)
                    else:
                        page.close(alerta)
                        
            page.clean()
            page.add(
                ft.Container(
                    margin=ft.Margin(20, 0, 60, 0),
                    content=ft.Row(
                        [
                            ft.IconButton(ft.icons.ARROW_BACK_ROUNDED, on_click=lambda e: Arotec()),
                            ft.Row(
                                [
                                    ft.TextButton(content=ft.Text("Arotec", size=22), on_click=lambda e: HomeScreen(page, self.user)),
                                    ft.TextButton(content=ft.Text("Máquinas", size=22), on_click=lambda e: Arotec()),
                                    ft.TextButton(content=ft.Text(f'{maquinas}', size=22), disabled=True),
                                ],
                            ),
                            ft.Container()
                            ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),
                ft.Divider(),
                ft.Container(
                    margin=ft.Margin(90,10,0,0),
                    content=ft.Row(
                        [
                            ft.ElevatedButton(icon=ft.icons.ADD, text='Adicionar Máquina', on_click=lambda e: new_model(page, maquinas))
                        ]
                    ),
                ),
                ft.Container(
                    margin=ft.Margin(20,25,20,20),
                    content=self.list_mach,
                    expand=True
                ),
            )

        def selected_maq(page, maq, model):
            link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
            requisicao = requests.get(f'{link}/Equipamentos/{maq}/{model}/Problemas.json')
            dic_problem = requisicao.json()

            self.list_problem = ft.ListView(spacing=10, padding=0, expand=True)
            for id in dic_problem:
                if id == 'status':
                    pass
                else:
                    if self.user == 'admin':
                        self.list_problem.controls.append(
                            ft.Container(
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
                                on_click= lambda e, id=id: selected_comp(maq,model,id)
                            )
                        )
                    else:
                        self.list_problem.controls.append(
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.ARROW_RIGHT),
                                        ft.Text(f'{id}', size=20),
                                        ft.Container(expand=True),
                                        ft.IconButton(ft.icons.DOWNLOAD),
                                        ft.PopupMenuButton(items=[
                                            ft.PopupMenuItem('Editar', ft.icons.EDIT, on_click= lambda e, id=id: edit(id)),
                                            ft.PopupMenuItem('Deletar', ft.icons.DELETE, on_click=lambda e, id=id: delete(id), disabled=True),
                                        ])
                                    ]
                                ),
                                bgcolor=ft.colors.ON_INVERSE_SURFACE,
                                border_radius=16,
                                on_click= lambda e, id=id: selected_comp(maq,model,id)
                            )
                        )

            page.controls[0].content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{model}', size=22), disabled=True))
            page.controls[0].content.controls[0].on_click = lambda e: equip_list(maq)
            page.controls[0].content.controls[1].controls[2].disabled = False
            page.controls[0].content.controls[1].controls[2].on_click = lambda e: equip_list(maq)
            page.controls[2].content.controls[0].text = 'Adicionar Componente'
            page.controls[2].content.controls[0].on_click = lambda e: new_category()
            del page.controls[-1]
            page.add(
                ft.Container(
                    margin=ft.Margin(20,20,20,20),
                    content=self.list_problem,
                    expand=True
                )  
            )                

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
                        requests.delete(f'{link}/Equipamentos/{maq}/{model}/Problemas/{id}.json')
                        page.controls[0].content.controls[1].controls.pop()
                        selected_maq(page, maq, model)
                    else:
                        page.close(alerta)

            def edit(id):
                def save():
                    dlg.actions.clear()
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    old_path = f'{link}/Equipamentos/{maq}/{model}/Problemas/{id}/'
                    new_path = f'{link}/Equipamentos/{maq}/{model}/Problemas/{self.edit.value}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    page.controls[0].content.controls[1].controls.pop()
                    selected_maq(page, maq, model)


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

            def new_category():
                def save():
                    dlg.actions.clear()
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
                    dados = {'vazio': 'vazio'}
                    requests.put(f'{link}/Equipamentos/{maq}/{model}/Problemas/{self.category.value}/.json', data=json.dumps(dados))
                    page.close(dlg)
                    page.controls[0].content.controls[1].controls.pop()
                    selected_maq(page, maq, model)

                self.category = ft.TextField(label='Componente', border_radius=16, on_submit=lambda e: save(), autofocus=True)

                dlg = ft.AlertDialog(
                    actions=[
                        ft.Column(
                            [
                                self.category,
                                ft.FilledButton(text="Salvar", on_click=lambda e: save())
                            ],
                            spacing=8
                        ),
                    ],
                    actions_padding=10,
                )
                page.open(dlg)


        def selected_comp(maq, model, comp):

            def reload_problems():
                # Limpa a interface
                exp_list.controls.clear()
                page.update()

                # Recarrega os dados do Firebase
                link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
                requisicao = requests.get(f'{link}/Equipamentos/{maq}/{model}/Problemas/{comp}.json')
                dic_trouble = requisicao.json()

                # Reconstrói a lista
                for problem in dic_trouble:
                    problem_details = dic_trouble[problem]
                    if isinstance(problem_details, dict):
                        descricao = problem_details.get('descrição', 'Descrição não encontrada')
                        solucao = problem_details.get('solução', 'Solução não encontrada')
                    else:
                        continue

                    exp_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                        [
                            ft.Row([ft.Text(f'{problem}')]),
                            ft.Divider(),
                            ft.Row(
                                [
                                    ft.Column([ft.Text(f'Detalhes'), ft.Container(ft.Text(f'{descricao}'), border= ft.border.all(color='black'), border_radius=ft.border_radius.all(8), padding=10 )]),
                                    ft.Container(),
                                    ft.Column([ft.Text(f'Solução'), ft.Container(ft.Text(f'{solucao}'), border= ft.border.all(color='black'), border_radius=ft.border_radius.all(8), padding=10)]),
                                    ft.Container(expand=True),
                                    ft.IconButton(icon=ft.icons.DELETE, on_click= lambda e, problem = problem: delete(problem)),
                                    ft.IconButton(icon=ft.icons.EDIT)
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            )
                        ]
                        ),
                        border_radius=16,
                        bgcolor=ft.colors.ON_INVERSE_SURFACE
                    )
                )
                page.update()

            def back():
                del page.controls[0].content.controls[1].controls[4]
                del page.controls[0].content.controls[1].controls[3]
                del page.controls[-1]
                selected_maq(page, maq, model)

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
                page.update()

                def yes_no(answer):
                    if answer == 'yes':
                        requests.delete(f'{link}/Equipamentos/{maq}/{model}/Problemas/{comp}/{item}.json')
                        reload_problems()
                    page.close(alerta)
                    page.update()
            
            def new_problem():
                def save():
                    dlg.actions.clear()
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Registrando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
                    dados = {'descrição': f'{detail.value}', 'solução': f'{resolution.value}'}
                    requests.put(f'{link}/Equipamentos/{maq}/{model}/Problemas/{comp}/{descricao.value}.json', data=json.dumps(dados))
                    page.close(dlg)
                    reload_problems()

                descricao = ft.TextField(label='Descrição', border_radius=16, on_submit=lambda e: save(), autofocus=True)
                detail = ft.TextField(label='Detalhes do erro', border_radius=16, on_submit=lambda e: save())
                resolution = ft.TextField(label='Solução', border_radius=16, on_submit=lambda e: save())

                dlg = ft.AlertDialog(
                    actions=[
                        ft.Column(
                            [
                                descricao,
                                detail,
                                resolution,
                                ft.FilledButton(text="Salvar", on_click=lambda e: save())
                            ],
                            spacing=8
                        ),
                    ],
                    actions_padding=10,
                )
                page.open(dlg)
                page.update()

            page.controls[0].content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{comp}', size=22), disabled=True))
            page.controls[0].content.controls[0].on_click = lambda e: back()
            page.controls[0].content.controls[1].controls[3].disabled = False
            page.controls[0].content.controls[1].controls[3].on_click = lambda e: back()
            page.controls[2].content.controls[0].text = 'Adicionar Problemas'
            link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
            requisicao = requests.get(f'{link}/Equipamentos/{maq}/{model}/Problemas/{comp}.json')
            dic_trouble = requisicao.json()
            page.controls[2].content.controls[0].on_click = lambda e: new_problem()
            page.update()

            del page.controls[-1]
            self.match = False

            for cont in self.list_problem.controls:
                if cont.content.controls[1].value == comp:
                    self.match = True
                    cont.margin=ft.Margin(5,15,5,5)
                    cont.content.controls[0].rotate = ft.Rotate(angle=3.14159 / 2)
                    page.add(cont)
            page.update()

            exp_list = ft.ListView(spacing=20)

            if self.match:
                page.add(
                    ft.Container(
                        exp_list,
                        expand=True,
                        margin=ft.Margin(20,15,20,0),
                    )
                )       

            for problem in dic_trouble:
                problem_details = dic_trouble[problem]
                if isinstance(problem_details, dict):
                    descricao = problem_details.get('descrição', 'Descrição não encontrada')
                    solucao = problem_details.get('solução', 'Solução não encontrada')
                else:
                    continue

                exp_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                        [
                            ft.Container(),
                            ft.Row([ft.Text(f'{problem}', size=20)], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END),
                            ft.Divider(),
                            ft.Container(
                                margin=ft.Margin(20,10,20,10),
                                content=ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Column(
                                                            [
                                                                ft.Text(f'Detalhes', size=20), 
                                                                ft.Container(
                                                                    ft.Text(f'{descricao}', size=18), 
                                                                    border= ft.border.all(color='black'), 
                                                                    border_radius=ft.border_radius.all(8), 
                                                                    padding=10
                                                                )
                                                            ],
                                                            width=400
                                                        ),
                                                        ft.Container(width=20),
                                                        ft.Column(
                                                            [
                                                                ft.Text(f'Solução', size=20), 
                                                                ft.Container(
                                                                    ft.Text(f'{solucao}', size=18), 
                                                                    border= ft.border.all(color='black'), 
                                                                    border_radius=ft.border_radius.all(8), 
                                                                    padding=10
                                                                )
                                                            ],
                                                            width=400
                                                        ),
                                                    ]
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.IconButton(icon=ft.icons.DELETE, on_click= lambda e, problem = problem: delete(problem)),
                                                        ft.IconButton(icon=ft.icons.EDIT)
                                                    ],
                                                    height=40
                                                )
                                            ]
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                )
                            )
                        ]
                        ),
                        border_radius=16,
                        bgcolor=ft.colors.ON_INVERSE_SURFACE
                    )
                )
            page.update()     

            
        
        def add_list(maq, model):                    
            link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
            requisicao = requests.get(f'{link}/Equipamentos/{maq}/{model}/Problemas.json')
            dic_options = requisicao.json()

            self.list_options = ft.ListView(divider_thickness=1, expand=True)
            for id in dic_options:
                self.list_options.controls.append(
                    ft.Row(
                        [
                            ft.Icon(ft.icons.ARROW_RIGHT),
                            ft.TextButton(content=ft.Text(f'{id}', size=20), on_click= lambda e: add_list(maq, model)),
                            ft.Container(expand=True),
                            ft.PopupMenuButton()
                        ]
                    )
                )
            page.add(
                ft.Container(
                    margin=ft.Margin(60,0,0,0),
                    content=self.list_options,
                    expand=True
                )  
            )
            
        
        def new_model(page, mach):
            def save():
                dlg.actions.clear()
                dlg.actions.append(
                    ft.Container(
                        ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center
                    )
                )
                page.update()
                link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
                dados = {"status": "vazio"}
                requests.put(f'{link}/Equipamentos/{mach}/{self.name.value}/Problemas.json', data=json.dumps(dados))
                page.close(dlg)
                equip_list(mach)
                

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

# Função principal do aplicativo
def main(page: ft.Page):
    page.title = "App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.spacing = 0
    # page.window.max_width= 1500
    # page.window.max_height=1300

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

    page.bottom_appbar = ft.BottomAppBar(
        ft.Row(
            [
                ft.Text('v1.0')
            ]
        ),
        height=50
    )

    def handle_dismissal(e):
        page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.control.selected_index}"))

    def open_drawer():
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
        page.add(drawer)

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
    HomeScreen(page, 'admin')

# Executa o aplicativo
ft.app(target=main)

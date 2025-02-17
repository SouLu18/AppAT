import flet as ft
import os
import asyncio
import time
import requests
import json
import subprocess
import zipfile
import sys
# import sqlite3

class Loading(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        loading_image = ft.Image(
            src="assets/loading.png",  # Caminho da imagem
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
        page.bgcolor = ft.Colors.ON_PRIMARY_CONTAINER
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
        
        CONFIG_FILE = "config.json"
        def save_login_state(stay_logged_in, username=None):
            data = {
                "stay_logged_in": stay_logged_in,
                "username": username if stay_logged_in else None
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)

        page.add(
            ft.Container(
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(content=ft.Text('Login', text_align=ft.TextAlign.END, size=32, color='#35588e'), margin=ft.Margin(0,10,0,0)),
                            ft.Column([ft.Text('Usuário', color='#35588e', size=16), self.user]),
                            ft.Column([ft.Text('Senha', color='#35588e', size=16), password]),
                            ft.Checkbox(
                                'Continuar logado', 
                                on_change = lambda e: save_login_state(e.control.value, self.user.value),
                                ),
                            ft.Container(content=ft.ElevatedButton('Logar', on_click=lambda e: login()), margin=ft.Margin(0,0,0,10))
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    margin=ft.Margin(20,0,20,0),
                ),
                width=400,
                bgcolor=ft.Colors.ON_INVERSE_SURFACE,
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

class Updating(ft.Container):
    def __init__(self, page: ft.Page, ver):
        super().__init__(page)

        update = ft.AlertDialog(
                title=ft.Text("Atualização de software"),
                content=ft.Text(f"Uma nova versão está disponível v{ver}.\nGostaria de atualizar?"),
                actions=[
                    ft.TextButton("Não", on_click=lambda e: page.close(update)),
                    ft.TextButton("Sim", on_click=lambda e: atualizar_app()),
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        page.open(update)
        
        def atualizar_app():

            update.content.value = 'O aplicativo precisará reiniciar após o download.\nContinuar o processo?'
            update.actions[1].on_click = lambda e: continuar()
            page.update()

            def continuar():
                update.content=ft.Column(
                    [
                        ft.ProgressRing(),
                        ft.Text("Baixando atualização"),
                        ft.ProgressBar(visible=False)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True
                )
                update.actions=None
                page.update()

                URL_DOWNLOAD = "https://github.com/SouLu18/AppAT/releases/latest/download/windows.zip"
                ZIP_PATH = "windows.zip"
                EXTRACT_FOLDER = "update" 

                resposta = requests.get(URL_DOWNLOAD, stream=True)

                if resposta.status_code == 200:
                    tamanho_total = int(resposta.headers.get('content-length', 0))
                    bytes_baixados = 0
                    with open(ZIP_PATH, "wb") as f:
                        for chunk in resposta.iter_content(chunk_size=1024):
                            f.write(chunk)
                            bytes_baixados += len(chunk)
                            progresso = bytes_baixados / tamanho_total if tamanho_total else 0
                            update.content.controls[2].visible = True
                            update.content.controls[2].value = progresso
                            update.content.controls[1].value = f"Baixando... {int(progresso * 100)}%"
                            page.update()
                    update.content.controls[1].value = f"Download finalizado!"
                    update.content.controls[2].visible = False
                    page.update()
                else:
                    update.content.controls[1].value = f"Erro ao baixar o arquivo: {resposta.status_code}"
                    page.update()
                
                os.makedirs(EXTRACT_FOLDER, exist_ok=True)
                update.content.controls[1].value = f"Extraindo arquivos"
                page.update()
                with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
                    zip_ref.extractall(EXTRACT_FOLDER)

                os.remove(ZIP_PATH)

                update.content.controls[1].value = f"Movendo arquivos.\nReinicie o aplicativo após a finalização."
                page.update()
                time.sleep(2)
                
                extract_path = os.path.abspath(EXTRACT_FOLDER)
                temp_bat = os.path.join(os.environ['TEMP'], 'remover.bat')
                current_folder = os.path.dirname(os.path.dirname(sys.executable))
                exe_name = 'AppAT.exe'

                bat_content = f'''
                    @echo off
                    timeout /t 5 /nobreak > nul
                    echo Substituindo a pasta antiga...

                    :: Finaliza qualquer instância do AppAT.exe
                    taskkill /f /im "AppAT.exe" > nul 2>&1

                    :: Aguarda até que o processo desapareça completamente
                    :CHECK
                    tasklist | findstr /i "AppAT.exe" > nul
                    if not errorlevel 1 (
                        echo Aguardando fechamento do AppAT.exe...
                        timeout /t 2 /nobreak > nul
                        goto CHECK
                    )

                    :: Exclui completamente a pasta "windows"
                    rmdir /s /q "{current_folder}\\windows"

                    :: Copia a nova pasta "windows" para dentro de current_folder
                    xcopy /e /i /h /y "{extract_path}" "{current_folder}"

                    :: Remove a pasta de extração após a cópia
                    rmdir /s /q "{extract_path}"l
                    
                    exit
                '''

                with open(temp_bat, 'w') as bat_file:
                    bat_file.write(bat_content)
                
                os.system(f'start "" "{temp_bat}"')

class HomeScreen(ft.Container):
    def __init__(self, page: ft.Page, user):
        super().__init__(page)
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.bgcolor = ft.Colors.ON_PRIMARY
        self.user = user
        self.arotec_screen = Arotec(page, self.user)

        ver_local = '1.0.2'
        ver = requests.get('https://appat-5805e-default-rtdb.firebaseio.com/versão.json')

        page.bottom_appbar = ft.BottomAppBar(
            ft.Row(
                [
                    ft.Text(f'v{ver_local}'),
                    ft.Text('© 2025 Arotec', size=16),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            height=50
        )

        if page.controls:
            page.clean()

        page.appbar = ft.AppBar(
            bgcolor=ft.Colors.ON_INVERSE_SURFACE,
            leading=ft.Image('assets/logo.png'),
            leading_width=120,
            center_title=True,
            actions=[
                ft.Container(
                    content=ft.Row(
                        [
                            ft.IconButton(ft.Icons.SEARCH_SHARP, on_click=lambda e: search_btn(), on_blur=lambda e: close_search(), disabled=True),
                            ft.IconButton(ft.Icons.MENU, on_click=lambda e: open_drawer(), tooltip='menu'),
                        ]
                    ),
                    margin=ft.Margin(0,0,10,0)
                ),
            ],
        )

        if ver.status_code == 200:
            if ver_local != ver.json():
                bottom = page.bottom_appbar.content
                bottom.controls[0] = ft.OutlinedButton(
                    content= ft.Row(
                        [
                            ft.Text(f'v{ver_local}', size=16),
                            ft.Icon(ft.Icons.DOWNLOADING_ROUNDED, color='blue', size=20)
                        ],
                        spacing=2
                    ),
                    tooltip='atualização disponível',
                    on_click=lambda e: Updating(page, ver.json())
                )

        page.add(
            ft.Container(
                    margin=ft.Margin(20, 0, 60, 0),
                    content=ft.Row(
                        [
                            ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED),
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
                            ft.Image("assets/arotec.png"), width=140, height=160, 
                            bgcolor=ft.Colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, on_click=lambda e: self.arotec_screen.first_page(page), padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.Colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                            ),
                        ft.Container(
                            ft.Image("assets/struers.png"), width=140, height=160, 
                            bgcolor=ft.Colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.Colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    ),
                            ),
                        ft.Container(
                            ft.Image("assets/foerster.png"), width=140, height=160, 
                            bgcolor=ft.Colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.Colors.BLUE_GREY_100,
                                        offset=ft.Offset(0, 0),
                                        blur_style=ft.ShadowBlurStyle.OUTER,
                                    )
                            ),
                        ft.Container(
                            ft.Image("assets/evident.png"), width=140, height=160, 
                            bgcolor=ft.Colors.ON_PRIMARY, border_radius= ft.border_radius.all(16),
                            ink=True, padding=ft.padding.all(10),
                            shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color=ft.Colors.BLUE_GREY_100,
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
            ),
        )

        page.update()

        def close_search(e=None):
            page.appbar.title = None
            page.update()
        
        def searching(word):
            self.link = 'https://appat-5805e-default-rtdb.firebaseio.com/'
            requisicao = requests.get(f'{self.link}/Equipamentos/.json')
            dic_requisicao = requisicao.json()
            search_list = ft.ListView(spacing=15)

            results = search_in_dict(dic_requisicao, word)
            if results:
                search_list.controls.clear()
                page.controls.clear()
                page.add(
                    ft.Container(
                        margin=ft.Margin(20, 0, 60, 0),
                        content=ft.Row(
                            [
                                ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED, on_click=lambda e: HomeScreen(page, user)),
                                ft.TextButton(content=ft.Text("Pesquisa", size=22)),
                                ft.Container() 
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ),
                    ft.Divider(),
                    ft.Container(content=search_list, margin=ft.Margin(20,5,20,0), expand=True, alignment=ft.alignment.center)
                )
                for result in results:
                    search_list.controls.append(
                        ft.Container(
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.ARROW_RIGHT),
                                    ft.Text(f'{result}', size=18),
                                    ft.Container()
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                height=40
                            ),
                            on_click=lambda e, result=result: go_to(result),
                            bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                            border_radius=16
                        )
                    )
                page.update()
                    
            else:
                snack_bar = ft.SnackBar(
                    content=ft.Text("Nenhum resultado encontrado!"),
                    duration=2000,
                )
                page.open(snack_bar)
        
        def search_in_dict(data, word, path=None, results=None):
            if path is None:
                path = []
            if results is None:
                results = []
            word = word.lower()
            if isinstance(data, dict):
                for key, value in data.items():
                    if word in str(key).lower():
                        results.append(" - ".join(path + [key]))
                    search_in_dict(value, word, path + [key], results)
            elif isinstance(data, list):
                for index, value in enumerate(data):
                    search_in_dict(value, word, path + [f"[{index}]"], results)
            else:
                if word in str(data).lower():
                    results.append(" - ".join(path))

            return results
    
        def go_to(string):
            screen = Arotec(page, self.user)
            sections = [section.strip() for section in string.split(" - ")]
            maq = sections[0] if len(sections) >= 1 else None
            model = sections[1] if len(sections) >= 2 else None
            comp = sections[3] if len(sections) >=4 else None

            if comp:
                pass
            elif model:
                screen.selected_maq(page, maq, model)
            else:
                screen.equip_list(page, maq)


    
        def search_btn():
            search=ft.TextField(
                autofocus=True,
                on_blur=lambda e: close_search(),
                height=35,
                width=500,
                on_submit=lambda e: searching(search.value) if search.value != '' else None,
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
                        icon=ft.Icon(ft.Icons.SETTINGS),
                        label="Configurações",
                    ),
                    ft.Container(height=12),
                    ft.NavigationDrawerDestination(
                        icon=ft.Icon(ft.Icons.DOWNLOAD),
                        label="Downloads",
                    ),
                    ft.Container(height=12),
                    ft.NavigationDrawerDestination(
                        icon=ft.Icon(ft.Icons.STAR),
                        label="Favoritos",
                    ),
                    # ft.Container(height=12),
                    # ft.NavigationDrawerDestination(
                    #     icon=ft.Icon(ft.Icons.TEXT_SNIPPET),
                    #     label="Relatório",
                    # ),
                    ft.Container(height=12),
                    ft.NavigationDrawerDestination(
                        icon=ft.Icon(ft.Icons.DOOR_BACK_DOOR),
                        label="Sair",
                    ),
                ],
            )
            page.open(end_drawer)

        def on_selected(e, menu):
            if e.control.selected_index == 0:
                pass
            elif e.control.selected_index == 1:
                pass
            elif e.control.selected_index == 2:
                pass
            # elif e.control.selected_index == 3:
            #     print("Relatório clicado!")
            elif e.control.selected_index == 3:
                page.close(menu)
                save_login_state(False, None)
                LoginScreen(page)  

        def save_login_state(stay_logged_in, username=None):
            CONFIG_FILE = "config.json"
            data = {
                "stay_logged_in": stay_logged_in,
                "username": username if stay_logged_in else None
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)          

class Arotec(ft.Container):
    def __init__(self, page: ft.Page, user):
        super().__init__(page)
        self.user = user
        page.controls.clear()
        self.cont_way = ft.Container(
            margin=ft.Margin(20, 0, 60, 0),
            content=ft.Row(
                [
                    ft.IconButton(ft.Icons.ARROW_BACK_ROUNDED, on_click=lambda e: HomeScreen(page, self.user)),
                    ft.Row(
                        [
                            ft.TextButton(content=ft.Text("Arotec", size=22), on_click=lambda e: HomeScreen(page, self.user)),
                            ft.TextButton(content=ft.Text("Máquinas", size=22), disabled=True, on_click=lambda e: self.first_page(page)),
                        ],
                    ),
                    ft.ProgressRing(opacity=0, width=20, height=20, stroke_width=2),
                    ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        self.link = 'https://appat-5805e-default-rtdb.firebaseio.com/AROTEC'
        self.list_opt = ft.ListView(spacing=10, padding=0, divider_thickness=1, expand=True)
        self.button_add = ft.Container(
            margin=ft.Margin(130,10,150,0),
            content=ft.Row(
                [
                    ft.ElevatedButton(icon=ft.Icons.ADD, content=ft.Text('Adicionar Máquina', text_align='center'), width=250)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
        )

    # def download(self, page, maq=None, model=None, comp=None):
    #     status = ft.AlertDialog(
    #         actions=[
    #             ft.Container(
    #                 ft.Column([ft.ProgressRing(), ft.Text('Baixando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    #                 alignment=ft.alignment.center
    #             )
    #         ],
    #         actions_padding=ft.Padding(0,5,0,0)
    #     )
    #     page.open(status)
    #     connection = sqlite3.connect("assets/equipment.db")
    #     cursor = connection.cursor()
    #     link = 'https://appat-5805e-default-rtdb.firebaseio.com'
    #     if not comp:
    #         requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/Componentes.json')
    #         dict_requisicao = requisicao.json()
    #         for componente, subdicionarios in dict_requisicao.items():
    #             for problema, detalhes in subdicionarios.items():
    #                 if problema == 'vazio':
    #                     continue
    #                 cursor.execute('''
    #                 INSERT INTO AROTEC (maquina, modelo, componente, problema, detalhe, solução)
    #                 VALUES (?,?,?,?,?,?)
    #                 ''', (f'{maq}', f'{model}', f'{componente}', f'{problema}', f'{detalhes['descrição']}', f'{detalhes["solução"]}'))
    #     else:
    #         requisicao = requests.get(f'{link}/Equipamentos/{maq}/{model}/Componentes/{comp}.json')
    #         dict_requisicao = requisicao.json()
    #         for problema, detalhes in dict_requisicao.items():
    #             if problema == 'vazio':
    #                 continue
    #             cursor.execute('''
    #             INSERT INTO AROTEC (maquina, modelo, componente, problema, detalhe, solução)
    #             VALUES (?,?,?,?,?,?)
    #             ''', (f'{maq}', f'{model}', f'{comp}', f'{problema}', f'{detalhes['descrição']}', f'{detalhes["solução"]}'))
    #     connection.commit()
    #     connection.close()
    #     if comp:
    #         self.selected_comp(page, maq, model, comp)
    #         page.close(status)
    #     elif model:
    #         self.equip_list(page, maq)
    #         page.close(status)


    # def verificacao(self, maq, model=None):
    #     connection = sqlite3.connect("assets/equipment.db")
    #     cursor = connection.cursor()
    #     if model != None:
    #         query = """
    #             SELECT componente, COUNT(*) as quantidade
    #             FROM AROTEC
    #             GROUP BY componente
    #         """      
    #     elif maq and model == None:
    #         query = '''
    #             SELECT modelo, componente, COUNT(problema)
    #             FROM AROTEC
    #             GROUP BY modelo, componente
    #         '''
    #     cursor.execute(query)
    #     db_contagem_comp = {}
    #     if model != None:
    #         db_contagem_comp = {linha[0]: linha[1] for linha in cursor.fetchall()}
    #     elif maq and model == None:
    #         for row in cursor.fetchall():
    #             modelo, componente, count = row
    #             if modelo not in db_contagem_comp:
    #                 db_contagem_comp[modelo] = 0
    #             db_contagem_comp[modelo] += count
    #     cursor.close()
    #     connection.close

    #     contagem_comp = {}
    #     if model != None:
    #         results = requests.get(f'{self.link}/Equipamentos/{maq}/{model}.json')
    #         data = results.json()
    #         if data == None:
    #             return 'back'
    #         total_itens = 0
    #         for componente, detalhes in data.items():
    #             contagem_comp = {chave: len(valor) for chave, valor in detalhes.items()}
    #     elif maq and model == None:
    #         results = requests.get(f'{self.link}/Equipamentos/{maq}.json')                                   
    #         data = results.json()
    #         for key, valor  in data.items():
    #             componentes = valor.get('Componentes', {})
    #             total_itens = 0
    #             for componente, detalhes in componentes.items():
    #                 if detalhes == {'vazio': 'vazio'}:
    #                     continue
    #                 total_itens += len(detalhes)
    #             contagem_comp[key] = total_itens
            
    #     itens_iguais = []
    #     for key, valor in contagem_comp.items():
    #         if key in db_contagem_comp and valor == db_contagem_comp[key]:
    #             itens_iguais.append(key)
        
    #     return itens_iguais

    def first_page(self, page):
        while len(self.cont_way.content.controls[1].controls) > 2:
            self.cont_way.content.controls[1].controls.pop()

        while len(self.button_add.content.controls) > 1:
            self.button_add.content.controls.pop()

        self.cont_way.content.controls[1].controls[-1].disabled =True
        self.cont_way.content.controls[0].on_click = lambda e: HomeScreen(page, self.user)
        page.controls.clear()
        page.add(
            self.cont_way,
            ft.Divider(),
            ft.Container(
                margin=ft.Margin(0,0,0,0),
                content=ft.Column(
                    [
                        ft.ListView([
                                ft.FilledTonalButton('Cortadoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.Colors.WHITE ,text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0, 0)), on_click=lambda e: self.equip_list(page, 'Cortadoras')),
                                ft.FilledTonalButton('Embutidoras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.Colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0, 0)), on_click=lambda e: self.equip_list(page, 'Embutidoras')),
                                ft.FilledTonalButton('Politrizes e Lixadeiras', style=ft.ButtonStyle(bgcolor='#35588e' ,color=ft.Colors.WHITE, text_style=ft.TextStyle(size=20), alignment=ft.Alignment(0, 0)), on_click=lambda e: self.equip_list(page, 'Politrizes e Lixadeiras')),
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
                image=ft.DecorationImage(src='assets/loading.png', opacity=0.1)
            ),
        )
    
    def equip_list(self, page, maquinas):
        self.cont_way.content.controls[2].opacity = 1
        page.update()
        requisicao = requests.get(f'{self.link}/Equipamentos/.json')
        if requisicao.status_code == 200:
            self.cont_way.content.controls[2].opacity = 0
            page.update()
        dict_requisicao = requisicao.json()
        dict_mach = dict_requisicao[f'{maquinas}']
        self.list_opt.controls.clear()
        self.list_opt.divider_thickness = 1
        self.list_opt.spacing = 10
        # self.list_downloaded = self.verificacao(maquinas)

        for id in dict_mach:
            if id == 'valid' or id == 'categorias':
                continue
            mach_row = ft.Row(
                [
                    ft.Icon(ft.Icons.ARROW_RIGHT),
                    ft.TextButton(f'{id}', on_click=lambda e, id=id: self.categories(page, maquinas, id)),
                    ft.Container(expand=True),
                    # ft.IconButton(
                    #     icon=ft.Icons.DOWNLOAD if id not in self.list_downloaded else ft.Icons.DOWNLOAD_DONE_OUTLINED,
                    #     on_click=lambda e, maquinas=maquinas, id=id: self.download(page, maquinas, id),
                    #     tooltip='Download' if id not in self.list_downloaded else 'Download realizado',
                    #     disabled= True if id in self.list_downloaded else False
                    # ),
                    ft.PopupMenuButton(items=[
                        ft.PopupMenuItem('Editar', ft.Icons.EDIT, on_click=lambda e, id=id: edit(id)),
                        ft.PopupMenuItem('Favoritos', ft.Icons.STAR_BORDER_OUTLINED),
                        # ft.PopupMenuItem('Delete', ft.Icons.DELETE, on_click=lambda e, id=id: delete(id))
                    ])
                ]
            )
            # if self.user != 'admin':
            #     mach_row.controls[3].items.pop()
            self.list_opt.controls.append(mach_row)

        
        while len(self.cont_way.content.controls[1].controls) > 2:
            self.cont_way.content.controls[1].controls.pop()

        while len(self.button_add.content.controls) > 1:
            self.button_add.content.controls.pop()

        self.cont_way.content.controls[0].on_click = lambda e: self.first_page(page)
        self.cont_way.content.controls[1].controls[1].disabled = False
        self.cont_way.content.controls[1].controls[1].on_click = lambda e: self.first_page(page)
        self.cont_way.content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{maquinas}', size=22), disabled=True)) #adicionando a trilha
        self.button_add.content.controls[0].on_click=lambda e: new_model(page, maquinas) # função button add
        self.button_add.content.controls[0].text = 'Adicionar Máquina'
        page.controls.clear()
        page.add(
            self.cont_way,
            ft.Divider(),
            self.button_add,
            ft.Container(
                margin=ft.Margin(20,25,20,20),
                content=self.list_opt,
                expand=True
            ),
        )

        def edit(id):
            def save():
                dlg.actions.clear()
                if self.edit.value == '':
                    dlg.content = ft.Column(
                        [
                            ft.Row(
                                [ft.IconButton('close', on_click= lambda e: page.close(dlg))], 
                                alignment=ft.MainAxisAlignment.END
                            ),
                            ft.Text(f'⚠️\nAlteração mal sucedida.\nAdicione o nome da máquina e tente novamente.', text_align='center', size=18),
                        ],
                        tight=True,
                        spacing=0
                    )
                    dlg.content_padding = 20
                    page.update()
                    return
                if self.edit.value in dict_mach:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.Icons.WARNING),ft.Text('Máquina já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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
                    new_path = f'{self.link}/Equipamentos/{maquinas}/{self.edit.value.upper()}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    self.equip_list(page, maquinas)
                    page.close(dlg)


            self.edit = ft.TextField(label='Máquina', border_radius=16, on_submit=lambda e: save(), autofocus=True, value=f'{id}')

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.edit,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

        # def delete(id):
        #     emoji = '\u26A0'
        #     alerta = ft.AlertDialog(
        #             modal=True,
        #             title=ft.Text(f"Você realmente deseja apagar {id}?"),
        #             content=ft.ResponsiveRow([ 
        #                         ft.Text(f'{emoji} Não será possível recuperar os dados apagados', size=14, col={"sm": 5, "md": 10, "xl": 10}, )
        #                     ]),
        #             actions=[
        #                 ft.TextButton("Yes", on_click=lambda e: yes_no('yes')),
        #                 ft.TextButton("No", on_click=lambda e: yes_no('no')),
        #             ],
        #             actions_alignment=ft.MainAxisAlignment.END,
        #         )
        #     page.open(alerta)
        #     def yes_no(answer):
        #         if answer == 'yes':
        #             alerta.title = None
        #             alerta.actions = None
        #             alerta.content.controls = [
        #                 ft.Column(
        #                     [ft.ProgressRing(), ft.Text('Apagando')], 
        #                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #                     tight=True
        #                 ),
        #             ]
        #             page.update()
        #             link = 'https://appat-5805e-default-rtdb.firebaseio.com/AROTEC'
        #             requests.delete(f'{link}/Equipamentos/{maquinas}/{id}.json')
        #             self.equip_list(page, maquinas)
        #             page.close(alerta)
        #         else:
        #             page.close(alerta)

        def new_model(page, mach):
            def save():
                dlg.actions.clear()
                if self.name.value.upper() in dict_mach:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.Icons.WARNING),ft.Text('Máquina já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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
                    dados = {"status": "vazio"}
                    requests.put(f'{self.link}/Equipamentos/{mach}/{self.name.value.upper()}/componentes.json', data=json.dumps(dados))
                    requests.put(f'{self.link}/Equipamentos/{mach}/{self.name.value.upper()}/erros.json', data=json.dumps(dados))
                    self.equip_list(page, mach)
                    page.close(dlg)
                

            self.name = ft.TextField(label='Nome da Máquina', border_radius=16, on_submit=lambda e: save(), autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.name,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)
    
    def categories(self, page, maq, model):
        self.cont_way.content.controls[2].opacity = 1
        page.update()
        requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/categorias.json')
        self.dict_category = requisicao.json()
        if requisicao.status_code == 200:
            self.cont_way.content.controls[2].opacity = 0
            page.update()

        if len(page.controls) == 0:
            page.add(self.cont_way, ft.Divider())

        while len(page.controls) > 2: 
            page.controls.pop()

        while len(self.cont_way.content.controls[1].controls) > 2:
            self.cont_way.content.controls[1].controls.pop()

        try:
            self.cont_way.content.controls[0].on_click = lambda e: self.equip_list(page, maq)
            self.cont_way.content.controls[1].controls[2].on_click = lambda e: self.equip_list(page, maq)
            self.cont_way.content.controls[1].controls[-1].disabled = False
        except IndexError:
            self.cont_way.content.controls[1].controls[-1].disabled = False
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{maq}', size=22), on_click = lambda e: self.equip_list(page, maq)),
                )
            self.cont_way.content.controls[0].on_click = lambda e: self.equip_list(page, maq)

        self.opt_category = ft.Dropdown(
            options=[
                ft.dropdown.Option(f'   {item}')
                for item in self.dict_category
            ],
            label='Categoria de Erros', border_radius=20,
            max_menu_height = 200, filled=None,
            bgcolor='#ffffff', border_color= '#ffffff',
            on_click=lambda e: dropdown_change(e)
        )

        page.add(
            ft.Container(
                bgcolor='#35588e',
                content= ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(f'{model.upper()}', size=100, 
                                        color='#ffffff', theme_style=ft.TextThemeStyle.DISPLAY_LARGE
                                ),
                                ft.Container(
                                    ft.Image("assets/arotec.png", color='#ffffff'),
                                    border_radius=50, width=100,
                                    padding=5, margin=ft.Margin(10,40,0,0)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Text(f'   Selecione o erro apresentado', size=15, 
                                color='#ffffff', theme_style=ft.TextThemeStyle.DISPLAY_LARGE
                        ),
                        self.opt_category,
                        ft.Container(height=15),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    text="Abrir lista de erros completa ", width=210, height=40, bgcolor='#ffffff',
                                    on_click= lambda e: complet_list()
                                ),
                                ft.ElevatedButton(
                                    text="Prosseguir", width=100, height=40, bgcolor='#ffffff',
                                    on_click=lambda e: prosseguir()
                                )
                            ],
                            
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                expand=True,
                padding=ft.Padding(150,0,150,0),
            )
        )

        page.update()

        def dropdown_change(e):
            if e.control.value == None:
                e.control.label = ''
            e.control.label = ''
            e.page.update()
        
        def prosseguir():
            if self.opt_category.value == None:
                return
            else:
                category = self.opt_category.value.strip()
                self.issue(page, maq, model, category)

        def complet_list():
            self.issue(page, maq, model)
            
        
    def issue(self, page, maq, model, category=None, comp=None):
        self.cont_way.content.controls[2].opacity = 1
        page.update()
        requisicao_categ = requests.get(f'{self.link}/Equipamentos/{maq}/categorias.json')
        requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/erros.json')
        self.dict_issue = requisicao.json()
        self.dict_category = requisicao_categ.json()
        if category:
            self.categ_id = self.dict_category[category].strip("'\"")
        self.componentes_list = requests.get(f'{self.link}/Componentes.json').json()
        self.comp_list = []
        if requisicao.status_code == 200:
            self.cont_way.content.controls[2].opacity = 0
            page.update()
        self.list_opt.divider_thickness = 0
        self.list_opt.spacing = 30
        self.list_opt.controls.clear()

        try:
            for chave, valores in self.dict_issue.items():
                componente_id = valores['componente_id']
                self.comp_list.append(componente_id)
        except TypeError:
            pass

        if self.dict_issue == None:
            self.equip_list(page, maq)
            return
        
        for id in self.dict_issue.keys():
            if id == 'status':
                pass
            elif category and self.dict_issue[id]['categoria'] != int(self.categ_id):
                continue
            else:
                issue_row = ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(width=50),
                                    ft.TextButton(content=ft.Text(f'{id}', size=20, text_align='start'), on_click=lambda e, id = id: self.issue_content(page, maq, model, id, category)),
                                    ft.Container(expand=True),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Container(width=63), 
                                    ft.Text(
                                        value = self.dict_issue[id]['descricao'], size=16,
                                        expand=True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                                        no_wrap=True
                                    ),
                                ],
                                width=700
                            )
                        ],
                        spacing=0
                    ),
                )
                comp_name = self.componentes_list[self.dict_issue[id]['componente_id']]['nome']
                if comp and comp_name != comp:
                    continue
                elif comp and comp_name == comp:
                    self.list_opt.controls.append(issue_row)
                else:
                    self.list_opt.controls.append(issue_row)        

        if len(page.controls) == 0:
            page.add(self.cont_way, ft.Divider())
        
        while len(page.controls) > 2: 
            page.controls.pop()
        
        while len(self.cont_way.content.controls[1].controls) > 3:
            self.cont_way.content.controls[1].controls.pop()

        try:
            self.cont_way.content.controls[0].on_click = lambda e: self.categories(page, maq, model)
            self.cont_way.content.controls[1].controls[2].on_click = lambda e: self.equip_list(page, maq)
            self.cont_way.content.controls[1].controls[-1].disabled = False,
            self.cont_way.content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{model}', size=22), on_click = lambda e: self.categories(page, maq, model))) #adicionando a trilha
            self.button_add.content.controls[0].text = 'Adicionar Erro'
            self.button_add.content.controls[0].on_click=lambda e: new_issue() # função button add
            if len(self.button_add.content.controls) < 2:
                if comp:
                    self.button_add.content.controls.append(ft.ElevatedButton(text=f'{comp}', icon=ft.Icons.FILTER_ALT_OFF_ROUNDED, width=250, on_click=lambda e: self.issue(page, maq, model, category)))
                else:
                    self.button_add.content.controls.append(ft.ElevatedButton(text='Filtrar por Componentes', icon=ft.Icons.FILTER_ALT, width=250, on_click=lambda e: self.selected_maq(page, maq, model, category)))
            else:
                if comp:
                    self.button_add.content.controls.pop()
                    self.button_add.content.controls.append(ft.ElevatedButton(text=f'{comp}', icon=ft.Icons.FILTER_ALT_OFF_ROUNDED, width=250, on_click=lambda e: self.issue(page, maq, model, category)))
                else:
                    if len(self.button_add.content.controls) > 2:
                        self.button_add.content.controls.pop()
                        self.button_add.content.controls.pop()
                        self.button_add.content.controls.append(ft.ElevatedButton(text='Filtrar por Componentes', icon=ft.Icons.FILTER_ALT, width=250, on_click=lambda e: self.selected_maq(page, maq, model, category)))
                    else:
                        self.button_add.content.controls[1].text = 'Filtrar por Componentes'
                        self.button_add.content.controls[1].icon = ft.Icons.FILTER_ALT
                        self.button_add.content.controls[1].on_click=lambda e: self.selected_maq(page, maq, model, category)
        except IndexError:
            self.cont_way.content.controls[1].controls[-1].disabled = False
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{maq}', size=22), on_click = lambda e: self.equip_list(page, maq)),
                )
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{model}', size=22), on_click = lambda e: self.categories(page, maq, model))
            )
            self.cont_way.content.controls[0].on_click = lambda e: self.categories(page, maq, model)
            self.button_add.content.controls[0].text = 'Adicionar Erro'
            self.button_add.content.controls[0].on_click=lambda e: new_issue() # função button add
            if len(self.button_add.content.controls) < 2:
                self.button_add.content.controls.append(ft.ElevatedButton(text='Filtrar por Componentes', icon=ft.Icons.FILTER_ALT, width=250, on_click=lambda e: self.selected_maq(page, maq, model, category)))
            else:
                self.button_add.content.controls[1].text = 'Filtrar por Componentes'
                self.button_add.content.controls[1].icon = ft.Icons.FILTER_ALT
                self.button_add.content.controls[1].on_click=lambda e: self.selected_maq(page, maq, model, category)

        page.add(
            self.button_add,
            ft.Row(
                [
                    ft.Container(
                        bgcolor="#35588e",
                        content=ft.Row(
                            [
                                ft.Text(f'{category}' if category != None else 'Erros', size=24, color='#ffffff', theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            width=300
                        ),
                        border_radius= ft.BorderRadius(16,0,0,16),
                        margin=ft.Margin(130,0,150,0),
                    ),
                ],
                alignment='center'
            ),
            ft.Container(
                margin=ft.Margin(80,30,0,0),
                content=self.list_opt,
                expand=True
            ),
        )

        def new_issue(error=None, title=None):
            self.componentes_maq = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/componentes.json').json()

            self.componentes_list = requests.get(f'{self.link}/Componentes.json').json()
            self.comp_list_name = []

            for id in self.componentes_maq:
                if not id or id == 'status':
                    continue
                componente_nome = self.componentes_list[id]['nome']
                self.comp_list_name.append(componente_nome)

            self.last_id = len(self.comp_list_name)
                               
            def save():
                if self.comp.value == None:
                    self.comp.value = 'vazio'
                error_list = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/erros.json').json()
                indice = next(
                    (i for i, componente in enumerate(self.componentes_list) if componente and componente.get('nome') == self.comp.value),
                    None
                )
                if 'status' in error_list:
                    error_list.pop('status')
                counter = 1
                original_value = self.title.value
                while self.title.value.capitalize() in error_list:

                    parts = self.title.value.split("_")
                    if len(parts) > 1 and parts[-1].isdigit():
                        self.title.value = "_".join(parts[:-1])
                    else:
                        self.title.value = original_value
                    self.title.value = f"{self.title.value}_{counter}"
                    counter += 1

                if self.problem.content.value == '' or self.title.value == '':
                    return
                dlg.actions.clear()
                dlg.actions.append(
                    ft.Container(
                        ft.Column([ft.ProgressRing(), ft.Text('Salvando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center
                    )
                )
                page.update()
                if category:
                    dados = {'descricao' : self.problem.content.value, 'categoria':int(self.categ_id), 'componente_id': indice, 'solução': 'Adicionar Solução'}
                else:
                    dados = {'descricao' : self.problem.content.value, 'categoria': self.categ.value, 'componente_id': indice, 'solução': 'Adicionar Solução'}
                requests.put(f'{self.link}/Equipamentos/{maq}/{model}/erros/{self.title.value.capitalize()}.json', data=json.dumps(dados))
                if 'status' in self.dict_issue:
                    requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/erros/status.json')
                page.close(dlg)
                page.controls[0].content.controls[1].controls.pop()
                self.issue(page, maq, model, category)

            def new_comp():
                def saving():
                    new_dlg.actions.clear()
                    if self.comp_name.value in self.comp_list_name:
                        new_dlg.actions.append(
                            ft.Container(
                                ft.Column([ft.Icon(ft.Icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                alignment=ft.alignment.center
                            )
                        )
                        page.update()
                    else:
                        new_dlg.actions.append(
                            ft.Container(
                                ft.Column([ft.ProgressRing(), ft.Text('Salvando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                alignment=ft.alignment.center
                            )
                        )
                        page.update()
                        dados = {'nome': f'{self.comp_name.value}', 'fabricante': f'{self.comp_fab.value}'}
                        id_data = {f'{self.last_id}': len(self.componentes_list)}
                        requests.put(f'{self.link}/Componentes/{len(self.componentes_list)}.json', data=json.dumps(dados))
                        requests.patch(f'{self.link}/Equipamentos/{maq}/{model}/componentes.json', data= json.dumps(id_data))
                        if 'status' in self.componentes_maq:
                            requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/componentes/status.json')
                        new_issue(self.problem.content.value, self.title.value)

                self.comp_name = ft.TextField(label='Componente', border_radius=16, autofocus=True)
                self.comp_fab = ft.TextField(label='Fabricante', border_radius=16)
                               

                new_dlg = ft.AlertDialog(
                    actions=[
                        ft.Column(
                            [
                                self.comp_name,
                                self.comp_fab,
                                ft.FilledButton(text="Salvar", on_click=lambda e: saving())
                            ],
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.END
                        ),
                    ],
                    actions_padding=10,
                )
                page.open(new_dlg)
            
            self.title = ft.TextField(label='Título', border_radius=16, value=title)
            # self.crm_link = ft.TextField(label='CRM Link', border_radius=16, value=title)
            self.comp = ft.Dropdown(
                options=[
                    ft.dropdown.Option(f'{item}')
                    for item in self.comp_list_name
                ],
                label='Componente', border_radius=16,
                max_menu_height = 200, filled=None
            )
            self.problem = ft.Container(
                ft.TextField(
                    label='Detalhes do erro:', border_radius=16, 
                    multiline=True, expand=True, border_color=ft.Colors.TRANSPARENT, value=error
                    ),
                width=500,
                height=100,
                padding=ft.Padding(0,15,0,0),
                border=ft.border.all(1, 'black'),
                border_radius=16
            )
            self.categ = ft.Dropdown(
                    options=[
                        ft.dropdown.Option(f'   {item}')
                        for item in self.dict_category
                    ],
                    label='Categoria do erro', border_radius=16,
                    max_menu_height = 200, filled=None,
                )

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.title,
                            self.problem,
                            self.comp,
                            ft.Container(height=5),
                            ft.Row(
                                [   
                                    ft.FilledButton(text="Novo Componente", width=150, on_click=lambda e: new_comp()),
                                    ft.Container(),
                                    ft.FilledButton(text="Salvar", on_click=lambda e: save(), width=150),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND
                            ),
                            ft.Container(height=10)
                        ]if category
                        else [
                            self.title,
                            self.problem,
                            self.categ,
                            self.comp,
                            ft.Container(height=5),
                            ft.Row(
                                [   
                                    ft.FilledButton(text="Novo Componente", width=150, on_click=lambda e: new_comp()),
                                    ft.Container(),
                                    ft.FilledButton(text="Salvar", on_click=lambda e: save(), width=150),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND
                            ),
                            ft.Container(height=10)
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

    def issue_content(self, page, maq, model, issue, categ):
        self.cont_way.content.controls[2].opacity = 1
        page.update()

        while len(page.controls) > 2: 
            page.controls.pop()
        try:
            self.cont_way.content.controls[1].controls[3].disabled = False
            self.cont_way.content.controls[0].on_click = lambda e: self.issue(page, maq, model, categ)
            self.cont_way.content.controls[1].controls[3].on_click = lambda e: self.issue(page, maq, model, categ)
            self.cont_way.content.controls[1].controls[2].on_click = lambda e: self.equip_list(page, maq)
        except IndexError:
            self.cont_way.content.controls[1].controls[-1].disabled = False
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{maq}', size=22), on_click = lambda e: self.equip_list(page, maq)),
                )
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{model}', size=22), disabled=False)
            )            
            self.cont_way.content.controls[0].on_click = lambda e: self.issue(page, maq, model, categ)
        
        self.componentes_list = requests.get(f'{self.link}/Componentes.json').json()
        requisicao = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/erros/{issue}.json')
        dict_issue = requisicao.json()
        issue_des = dict_issue['descricao']
        issue_sol = dict_issue['solução']
        comp_issue = dict_issue['componente_id']
        comp_name = self.componentes_list[comp_issue]['nome']
        comp_fab = self.componentes_list[comp_issue]['fabricante']

        if requisicao.status_code == 200:
            self.cont_way.content.controls[2].opacity = 0
            page.update()

        sol_widget = ft.Container(
            content=(
                ft.Text(issue_sol, size=14, selectable=True) 
            ),
            bgcolor=ft.Colors.ON_INVERSE_SURFACE,
            padding=ft.Padding(10, 10, 10, 10),
            border_radius=16,
            width=1000
        ) if issue_sol != 'Adicionar Solução' else ft.ElevatedButton(content=ft.Text(issue_sol, size=14), bgcolor=ft.Colors.ON_INVERSE_SURFACE, on_click=lambda e: add_solution(issue))
        
        comp_widget = ft.Container(
                content = ft.Text(f'{comp_name.capitalize()} / {comp_fab.capitalize()}', size=14, selectable=True),
                bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                padding=ft.Padding(10,10,10,10),
                border_radius=16,
                width=250
            ) if comp_name != 'vazio' else ft.ElevatedButton(
                text="Adicionar Componente",
                bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                on_click=lambda e: add_comp()
            )
        
        page.add(
            ft.Row(
                [
                    ft.Container(
                        bgcolor="#35588e",
                        content=ft.Row(
                            [
                                ft.Text(f'{categ}', size=24, color='#ffffff', theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
                            ],
                            alignment = ft.MainAxisAlignment.CENTER,
                            width=300
                        ),
                        border_radius= ft.BorderRadius(16,0,0,16),
                        margin=ft.Margin(150,20,150,20),
                        on_click= lambda e: self.issue(page, maq, model, categ)
                    ),
                ],
                alignment='center'
            ),
            ft.Row([ft.Text(f'{issue}', size=22, color='#35588e')], alignment='center')
            )

        page.add(
            ft.Container(
                margin=ft.Margin(300,10,300,0),
                content=ft.Column(
                    [
                        # ft.Row([ft.Text(f'{issue}', size=22, color='#35588e')], alignment='center'),
                        ft.Container(height=15),
                        ft.Row([ft.Text('Detalhes do Erro:', size=16, color='black')]),
                        ft.Container(
                            content=ft.Text(issue_des, size=14, selectable=True),
                            bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                            padding=ft.Padding(10,10,10,10),
                            border_radius=16,
                            width=1000
                        ),
                        ft.Container(height=15),
                        ft.Text('Solução:', size=16),
                        sol_widget,
                        ft.Container(height=15),
                        ft.Text('Componente:', size=16),
                        comp_widget,
                    ],
                    spacing=5,
                    scroll=True,
                    expand=True,
                ),
            )
        )

        page.update()
        
        def add_solution(issue, text=''):
            def exit():
                try:
                    if self.save:
                        return
                except AttributeError:
                    pass
                def handle_click():
                    page.close(close_dlg)
                    add_solution(issue, self.add.content.value)
                close_dlg = ft.AlertDialog(
                    content=ft.Text(
                        f'⚠️Atenção⚠️\nTodos as informações inseridas serão perdidas.\nDeseja continuar?',
                        text_align='center', 
                        size=18
                    ),
                    actions = [
                        ft.TextButton("Não", on_click=lambda e: handle_click()),
                        ft.TextButton("Sim", on_click=lambda e: page.close(close_dlg)),
                    ],
                    content_padding = ft.Padding(20,20,20,10)
                )
                page.open(
                    close_dlg
                )
            def save():
                if self.add.content.value == '':
                    self.add.content.focus()
                else:  
                    dlg.actions.clear()
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.ProgressRing(), ft.Text('Salvando alteração')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center
                        )
                    )
                    page.update()
                    path = f'{self.link}/Equipamentos/{maq}/{model}/erros/{issue}'
                    data = {'solução': self.add.content.value}
                    requests.patch(f"{path}.json", json=data)
                    self.save = True
                    page.close(dlg)
                    self.issue_content(page, maq, model, issue, categ)

            self.add = ft.Container(
                ft.TextField(
                    label='Solução:', border_radius=16, on_submit=lambda e: save(), 
                    multiline=True, expand=True, border_color=ft.Colors.TRANSPARENT, 
                    value=text
                ),
                width=500,
                height=100,
                padding=ft.Padding(0,15,0,0),
                border=ft.border.all(1, 'black'),
                border_radius=16
            )

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.add,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                on_dismiss= lambda e: exit(),
                actions_padding=10,
            )
            page.open(dlg)

        def add_comp():
            def save():
                for id in self.componentes_maq:
                    if not id or id == 'status':
                        continue
                    componente_nome = self.componentes_list[id]['nome']
                    if componente_nome == self.comp.value:
                        comp_id = id
                        break

                requests.patch(f'{self.link}/Equipamentos/{maq}/{model}/erros/{issue}.json', data=json.dumps({'componente_id': comp_id}))
                page.close(dlg)
                self.issue_content(page, maq, model, issue, categ)
            
            self.componentes_list = requests.get(f'{self.link}/Componentes.json').json()
            self.componentes_maq = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/componentes.json').json()
            self.comp_list_name = []

            for id in self.componentes_maq:
                if not id or id == 'status':
                    continue
                componente_nome = self.componentes_list[id]['nome']
                self.comp_list_name.append(componente_nome)

            self.last_id = len(self.comp_list_name)

            self.comp = ft.Dropdown(
                options=[
                    ft.dropdown.Option(f'{item}')
                    for item in self.comp_list_name
                ],
                label='Componente' if len(self.componentes_maq) >= 1 else 'Sem componentes na lista',
                border_radius=16,
                max_menu_height = 200, filled=None
            )
            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.comp,
                            ft.Row(
                                [   
                                    ft.FilledButton(text="Novo Componente", width=150, on_click=lambda e: new_comp()),
                                    ft.Container(width=10),
                                    ft.FilledButton(text="Salvar", on_click=lambda e: save(), width=150),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND
                            )
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)

            def new_comp():
                def saving():
                    new_dlg.actions.clear()
                    if self.comp_name.value in self.comp_list_name:
                        new_dlg.actions.append(
                            ft.Container(
                                ft.Column([ft.Icon(ft.Icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                alignment=ft.alignment.center
                            )
                        )
                        page.update()
                    else:
                        new_dlg.actions.append(
                            ft.Container(
                                ft.Column([ft.ProgressRing(), ft.Text('Salvando')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                alignment=ft.alignment.center
                            )
                        )
                        page.update()
                        dados = {'nome': f'{self.comp_name.value}', 'fabricante': f'{self.comp_fab.value}'}
                        id_data = {f'{self.last_id}': len(self.componentes_list)}
                        requests.put(f'{self.link}/Componentes/{len(self.componentes_list)}.json', data=json.dumps(dados))
                        requests.patch(f'{self.link}/Equipamentos/{maq}/{model}/componentes.json', data= json.dumps(id_data))
                        if 'status' in self.componentes_maq:
                            requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/componentes/status.json')
                        add_comp()

                self.comp_name = ft.TextField(label='Componente', border_radius=16, autofocus=True)
                self.comp_fab = ft.TextField(label='Fabricante', border_radius=16)

                new_dlg = ft.AlertDialog(
                    actions=[
                        ft.Column(
                            [
                                self.comp_name,
                                self.comp_fab,
                                ft.FilledButton(text="Salvar", on_click=lambda e: saving())
                            ],
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.END
                        ),
                    ],
                    actions_padding=10,
                )
                page.open(new_dlg)
            
    def selected_maq(self, page, maq, model, categ):
        self.componentes_maq = requests.get(f'{self.link}/Equipamentos/{maq}/{model}/componentes.json').json()
        self.componentes_list = requests.get(f'{self.link}/Componentes.json').json()
        self.comp_list_name = []

        for id in self.componentes_maq:
            if not id or id == 'vazio':
                continue
            componente_nome = self.componentes_list[int(id)]['nome']
            self.comp_list_name.append(componente_nome)


        self.list_opt.divider_thickness = 0
        self.list_opt.controls.clear()
        self.list_opt.spacing = 10
        # self.list_downloaded = self.verificacao(maq, model)

        # if self.list_downloaded == 'back':
        #     self.equip_list(page, maq) 
        
        for id in self.comp_list_name:
            if id == 'status':
                pass
            else:
                comp_row = ft.Container(
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ARROW_RIGHT),
                            ft.Text(f'{id}', size=20),
                            ft.Container(expand=True),
                            # ft.IconButton(
                            #     icon=ft.Icons.DOWNLOAD if id not in self.list_downloaded else ft.Icons.DOWNLOAD_DONE_OUTLINED,
                            #     on_click=lambda e, maquinas=maq, id=id: self.download(page, maquinas, id),
                            #     tooltip='Download' if id not in self.list_downloaded else 'Download realizado',
                            #     disabled= True if id in self.list_downloaded else False
                            # ),
                            # ft.PopupMenuButton(items=[
                            #     ft.PopupMenuItem('Favoritos', ft.Icons.STAR_BORDER_OUTLINED),
                            #     ft.PopupMenuItem('Editar', ft.Icons.EDIT, on_click= lambda e, id=id: edit(id)),
                            #     ft.PopupMenuItem('Deletar', ft.Icons.DELETE, on_click=lambda e, id=id: delete(id)),
                            # ])
                        ]
                    ),
                    bgcolor=ft.Colors.ON_INVERSE_SURFACE,
                    border_radius=16,
                    on_click= lambda e, id=id: self.issue(page, maq,model,categ,id)
                )
                # if self.user != 'admin':
                #     comp_row.content.controls[3].items.pop()
                self.list_opt.controls.append(comp_row)

        if len(page.controls) == 0:
            page.add(self.cont_way, ft.Divider())
        
        while len(page.controls) > 2: 
            page.controls.pop()
        
        while len(self.cont_way.content.controls[1].controls) > 3:
            self.cont_way.content.controls[1].controls.pop()

        try:
            self.cont_way.content.controls[0].on_click = lambda e: self.equip_list(page, maq)
            self.cont_way.content.controls[1].controls[2].on_click = lambda e: self.equip_list(page, maq)
            self.cont_way.content.controls[1].controls[-1].disabled = False,
            self.cont_way.content.controls[1].controls.append(ft.TextButton(content=ft.Text(f'{model}', size=22))) #adicionando a trilha
            self.button_add.content.controls[0].text = 'Adicionar Componente'
            self.button_add.content.controls[0].on_click=lambda e: new_comp() # função button add
            self.button_add.content.controls[1].text = 'Cancelar Filtro'
            self.button_add.content.controls[1].icon = ft.Icons.FILTER_ALT_OFF_ROUNDED
            self.button_add.content.controls[1].on_click=lambda e: self.issue(page, maq, model, categ)
        except IndexError:
            self.cont_way.content.controls[1].controls[-1].disabled = False
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{maq}', size=22), on_click = lambda e: self.equip_list(page, maq)),
                )
            self.cont_way.content.controls[1].controls.append(
                ft.TextButton(content=ft.Text(f'{model}', size=22))
            )
            self.cont_way.content.controls[0].on_click = lambda e: self.equip_list(page, maq)
            self.button_add.content.controls[0].text = 'Adicionar Componente'
            self.button_add.content.controls[0].on_click=lambda e: new_comp() # função button add
            self.button_add.content.controls[1].text = 'Cancelar Filtro'
            self.button_add.content.controls[1].icon = ft.Icons.FILTER_ALT_OFF_ROUNDED
            self.button_add.content.controls[1].on_click=lambda e: self.issue(page, maq, model, categ)

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
                if self.edit.value == '':
                    dlg.content = ft.Column(
                        [
                            ft.Row(
                                [ft.IconButton('close', on_click= lambda e: page.close(dlg))], 
                                alignment=ft.MainAxisAlignment.END
                            ),
                            ft.Text(f'⚠️\nAlteração mal sucedida.\nAdicione o nome do componente e tente novamente.', text_align='center', size=18),
                        ],
                        tight=True,
                        spacing=0
                    )
                    dlg.content_padding = 20
                    page.update()
                    return
                if self.edit.value in self.comp_list_name:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.Icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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
                    old_path = f'{self.link}/Equipamentos/{maq}/{model}/Componentes/{id}/'
                    new_path = f'{self.link}/Equipamentos/{maq}/{model}/Componentes/{self.edit.value.upper()}/'
                    response = requests.get(f"{old_path}.json")
                    data = response.json()
                    requests.put(f"{new_path}.json", data=json.dumps(data))
                    requests.delete(f"{old_path}.json")
                    page.close(dlg)
                    self.selected_maq(page, maq, model, categ)


            self.edit = ft.TextField(label='Componente', border_radius=16, on_submit=lambda e: save(), autofocus=True, value=f'{id}')

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.edit,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END
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
                    requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/Componentes/{id}.json')
                    page.controls[0].content.controls[1].controls.pop()
                    self.selected_maq(page, maq, model, categ)
                    page.close(alerta)
                else:
                    page.close(alerta)

        def new_comp():
            def save():
                dlg.actions.clear()
                if self.comp.value in self.comp_list_name:
                    dlg.actions.append(
                        ft.Container(
                            ft.Column([ft.Icon(ft.Icons.WARNING),ft.Text('Componente já existente')], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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

                    dados = {'nome': f'{self.comp.value.capitalize()}', 'fabricante': f'{self.fab.value.capitalize()}'}
                    dados_id = {f'{len(self.componentes_maq)}': len(self.componentes_list)}
                    requests.put(f'{self.link}/Componentes/{len(self.componentes_list)}.json', data=json.dumps(dados))
                    requests.patch(f'{self.link}/Equipamentos/{maq}/{model}/componentes.json', data=json.dumps(dados_id))
                    if 'status' in self.comp_list_name:
                        requests.delete(f'{self.link}/Equipamentos/{maq}/{model}/componentes/status.json')
                    page.close(dlg)
                    page.controls[0].content.controls[1].controls.pop()
                    self.selected_maq(page, maq, model, categ)

            self.comp = ft.TextField(label='Componente', border_radius=16, autofocus=True)
            self.fab = ft.TextField(label='Fabricante', border_radius=16, autofocus=True)

            dlg = ft.AlertDialog(
                actions=[
                    ft.Column(
                        [
                            self.comp,
                            self.fab,
                            ft.FilledButton(text="Salvar", on_click=lambda e: save())
                        ],
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.END
                    ),
                ],
                actions_padding=10,
            )
            page.open(dlg)


def main(page: ft.Page):
    page.title = "AppAT"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 0
    page.bgcolor = "rgba(224, 226, 229, 0.91)"
    page.window.maximized = True
    page.theme_mode = ft.ThemeMode.LIGHT

    CONFIG_FILE = "config.json"

    def load_login_state():
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"stay_logged_in": False, "username": None}
        else:
            return {"stay_logged_in": False, "username": None}
    
    login_state = load_login_state()
    if not login_state["stay_logged_in"]:
        Loading(page)
    else:
        HomeScreen(page, login_state["username"])


if __name__ == "__main__":
    ft.app(target=main,  assets_dir="assets")

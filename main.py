import flet as ft
from usuario import (
    criar_tabela_usuarios,
    cadastrar_usuario,
    validar_login,
    verificar_usuario_existente,
    recuperar_senha,
    verificar_resposta_secreta
)
from personagem import Personagem
from database import criar_tabela_personagens, inserir_personagem, obter_personagens, deletar_personagem
import sqlite3

def main(page: ft.Page):
    # =============================================
    # 0. CONFIGURAÇÕES INICIAIS
    # =============================================
    criar_tabela_usuarios()
    criar_tabela_personagens()
    
    page.title = "Projeto RPG"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Constantes
    PONTOS_TOTAIS = Personagem.PONTOS_TOTAIS
    CORES_CABELO = {
        "Preto": "#000000",
        "Castanho": "#A52A2A",
        "Loiro": "#F5DEB3",
        "Ruivo": "#FF4500",
        "Grisalho": "#c0c0c0",
        "Branco": "#FFFFFF",
        "Azul": "#0000FF"
    }
    
    CORES_OLHOS = {
        "Castanho": "#8B4513",
        "Azul": "#1E90FF",
        "Verde": "#2E8B57",
        "Preto": "#000000",
        "Cinza": "#808080",
        "Vermelho": "#FF0000"
    }

    PERGUNTAS_SECRETAS = [
        "Nome do seu primeiro pet",
        "Cidade onde nasceu",
        "Nome do seu melhor amigo de infância",
        "Modelo do seu primeiro carro",
        "Nome da sua primeira professora"
    ]

    # =============================================
    # 1. SISTEMA DE PERSONAGENS (DEFINIDO PRIMEIRO)
    # =============================================
    def navegar_para_criacao(usuario_logado):
        page.controls.clear()
        current_user = usuario_logado

        def carregar_personagens():
            personagens = obter_personagens(current_user)
            if personagens:
                return ft.Column(
                    controls=[
                        ft.ListTile(
                            title=ft.Text(p[2]),  # Nome do personagem
                            subtitle=ft.Text(f"Força: {p[9]}, Int: {p[11]}, Car: {p[12]}"),
                            on_click=lambda e, p=p: mostrar_ficha(p)
                        ) for p in personagens
                    ],
                    spacing=10
                )
            return ft.Text("Nenhum personagem criado ainda.")

        def mostrar_tela_principal(e=None):
            page.controls.clear()
            page.add(
                ft.Column([
                    ft.Text(f"Bem-vindo, {current_user}!", size=24, weight="bold"),
                    ft.Text("Meus Personagens", size=20),
                    carregar_personagens(),
                    ft.ElevatedButton(
                        "Criar Novo Personagem",
                        on_click=mostrar_formulario_criacao,
                        width=300,
                        color=ft.colors.GREEN
                    ),
                    ft.ElevatedButton(
                        "Sair",
                        on_click=lambda _: mostrar_login(),
                        width=300,
                        color=ft.colors.RED
                    )
                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        def mostrar_ficha(personagem_db):
            def deletar_e_voltar(e):
                deletar_personagem(personagem_db[0])  # ID do personagem
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"{personagem_db[2]} deletado com sucesso!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED,
                    duration=3000
                )
                page.snack_bar.open = True
                page.update()
                mostrar_tela_principal()

            page.controls.clear()
            page.add(
                ft.Column([
                    ft.Text("Ficha do Personagem", size=24, weight="bold"),
                    ft.Text(f"Nome: {personagem_db[2]}"),
                    ft.Text(f"Raça: {personagem_db[3]}"),
                    ft.Text(f"Sexo: {personagem_db[4]}"),
                    ft.Text(f"Cor da pele: {personagem_db[5]}"),
                    ft.Text(f"Tamanho do cabelo: {personagem_db[6]}"),
                    ft.Row([
                        ft.Text("Cor do cabelo: "),
                        ft.Container(width=20, height=20, bgcolor=personagem_db[7], border=ft.border.all(1)),
                        ft.Text(personagem_db[7])
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        ft.Text("Cor dos olhos: "),
                        ft.Container(width=20, height=20, bgcolor=personagem_db[8], border=ft.border.all(1)),
                        ft.Text(personagem_db[8])
                    ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(f"Força: {personagem_db[9]}"),
                    ft.Text(f"Destreza: {personagem_db[10]}"),
                    ft.Text(f"Inteligência: {personagem_db[11]}"),
                    ft.Text(f"Carisma: {personagem_db[12]}"),
                    ft.Row([
                        ft.ElevatedButton("Voltar", on_click=lambda _: mostrar_tela_principal()),
                        ft.ElevatedButton("Novo Personagem", on_click=mostrar_formulario_criacao, color=ft.colors.GREEN),
                        ft.ElevatedButton("Deletar", on_click=deletar_e_voltar, color=ft.colors.RED),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        def mostrar_formulario_criacao(e=None):
            page.controls.clear()

            # Componentes do formulário
            nome = ft.TextField(label="Nome do personagem", width=300)
            raca = ft.Dropdown(
                label="Raça",
                options=[
                    ft.dropdown.Option("Humano"),
                    ft.dropdown.Option("Elfo"),
                    ft.dropdown.Option("Anão"),
                    ft.dropdown.Option("Halfling"),
                ],
                width=300
            )
            sexo = ft.Dropdown(
                label="Sexo",
                options=[
                    ft.dropdown.Option("Masculino"),
                    ft.dropdown.Option("Feminino"),
                    ft.dropdown.Option("Outro"),
                ],
                width=300
            )
            
            # Seção de APARÊNCIA
            cor_pele = ft.TextField(label="Cor da pele", width=300)
            tamanho_cabelo = ft.TextField(label="Tamanho do cabelo", width=300)
            
            # Dropdowns para cores
            dropdown_cabelo = ft.Dropdown(
                label="Cor do Cabelo",
                options=[ft.dropdown.Option(cor) for cor in CORES_CABELO.keys()],
                width=300,
                value="Preto"
            )
            
            dropdown_olhos = ft.Dropdown(
                label="Cor dos Olhos",
                options=[ft.dropdown.Option(cor) for cor in CORES_OLHOS.keys()],
                width=300,
                value="Castanho"
            )

            # Visualização das cores
            preview_cabelo = ft.Container(
                width=30,
                height=30,
                bgcolor=CORES_CABELO["Preto"],
                border_radius=15,
                border=ft.border.all(1, ft.colors.BLACK))
            
            preview_olhos = ft.Container(
                width=30,
                height=30,
                bgcolor=CORES_OLHOS["Castanho"],
                border_radius=15,
                border=ft.border.all(1, ft.colors.BLACK))
            
            # Textos dinâmicos para as cores
            texto_cor_cabelo = ft.Text("Preto")
            texto_cor_olhos = ft.Text("Castanho")

            def atualizar_preview(e):
                cor_cabelo = dropdown_cabelo.value
                preview_cabelo.bgcolor = CORES_CABELO[cor_cabelo]
                texto_cor_cabelo.value = cor_cabelo
                
                cor_olhos = dropdown_olhos.value
                preview_olhos.bgcolor = CORES_OLHOS[cor_olhos]
                texto_cor_olhos.value = cor_olhos
                
                page.update()

            dropdown_cabelo.on_change = atualizar_preview
            dropdown_olhos.on_change = atualizar_preview

            # Seção de ATRIBUTOS
            forca_slider = ft.Slider(
                min=0, 
                max=10, 
                divisions=10, 
                label="{value}", 
                width=300
            )
            
            destreza_slider = ft.Slider(
                min=0, 
                max=10, 
                divisions=10, 
                label="{value}", 
                width=300
            )

            inteligencia_slider = ft.Slider(
                min=0, 
                max=10, 
                divisions=10, 
                label="{value}", 
                width=300
            )
            
            carisma_slider = ft.Slider(
                min=0, 
                max=10, 
                divisions=10, 
                label="{value}", 
                width=300
            )
            
            pontos_info = ft.Text("Pontos restantes: 25")

            # Controle de pontos
            TOTAL_PONTOS = 25
            pontos_usados = 0
            
            def atualizar_pontos(e):
                nonlocal pontos_usados

                forca = max(0, forca_slider.value)
                destreza = max(0, destreza_slider.value)
                inteligencia = max(0, inteligencia_slider.value)
                carisma = max(0, carisma_slider.value)

                if e.control == forca_slider and forca != forca_slider.value:
                    forca_slider.value = forca
                elif e.control == destreza_slider and destreza != destreza_slider.value:
                    inteligencia_slider.value = inteligencia
                elif e.control == inteligencia_slider and inteligencia != inteligencia_slider.value:
                    inteligencia_slider.value = inteligencia
                elif e.control == carisma_slider and carisma != carisma_slider.value:
                    carisma_slider.value = carisma

                novo_total = forca + destreza + inteligencia + carisma

                if novo_total > TOTAL_PONTOS:
                    excesso = novo_total - TOTAL_PONTOS
                    e.control.value = max(0, e.control.value - excesso)

                pontos_usados = forca_slider.value + destreza_slider.value + inteligencia_slider.value + carisma_slider.value
                pontos_info.value = f"Pontos restantes: {TOTAL_PONTOS - pontos_usados}"
                page.update()

            forca_slider.on_change = atualizar_pontos
            destreza_slider.on_change = atualizar_pontos
            inteligencia_slider.on_change = atualizar_pontos
            carisma_slider.on_change = atualizar_pontos

            def criar_personagem(e):
                try:
                    if not nome.value:
                        raise ValueError("O nome do personagem é obrigatório")
                    if not raca.value:
                        raise ValueError("A raça do personagem é obrigatória")
                    if not sexo.value:
                        raise ValueError("O sexo do personagem é obrigatório")
                    
                    pontos_usados = (forca_slider.value + destreza_slider.value + 
                                    inteligencia_slider.value + carisma_slider.value)
                    if pontos_usados > TOTAL_PONTOS:
                        raise ValueError(f"Pontos excedidos! Você usou {pontos_usados} de {TOTAL_PONTOS} disponíveis")

                    personagem = Personagem(
                        nome=nome.value,
                        raca=raca.value,
                        sexo=sexo.value,
                        cor_pele=cor_pele.value if cor_pele.value else "Não especificado",
                        tamanho_cabelo=tamanho_cabelo.value if tamanho_cabelo.value else "Não especificado"
                    )
                    
                    # Define atributos adicionais
                    personagem.cor_cabelo = CORES_CABELO[dropdown_cabelo.value]
                    personagem.cor_olhos = CORES_OLHOS[dropdown_olhos.value]
                    personagem.forca = int(forca_slider.value)
                    personagem.destreza = int(destreza_slider.value)
                    personagem.inteligencia = int(inteligencia_slider.value)
                    personagem.carisma = int(carisma_slider.value)

                    inserir_personagem(current_user, personagem)
                    
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Personagem criado com sucesso!", color=ft.colors.WHITE),
                        bgcolor=ft.colors.GREEN,
                        duration=3000
                    )
                    page.snack_bar.open = True
                    page.update()
                    
                    mostrar_tela_principal()
                    
                except Exception as e:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f"Erro: {str(e)}", color=ft.colors.WHITE),
                        bgcolor=ft.colors.RED,
                        duration=4000
                    )
                    page.snack_bar.open = True
                    page.update()
                    print(f"Erro detalhado: {str(e)}")

            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Criar Novo Personagem", size=24, weight="bold"),
                        nome,
                        raca,
                        sexo,
                        
                        ft.Text("Aparência", size=18, weight="bold"),
                        cor_pele,
                        tamanho_cabelo,
                        
                        ft.Row([
                            ft.Column([
                                dropdown_cabelo,
                                ft.Row([
                                    preview_cabelo,
                                    texto_cor_cabelo
                                ], spacing=10)
                            ]),
                            ft.Column([
                                dropdown_olhos,
                                ft.Row([
                                    preview_olhos,
                                    texto_cor_olhos
                                ], spacing=10)
                            ])
                        ], spacing=20),
                        
                        ft.Text("Força:", weight="bold"),
                        forca_slider,
                        
                        ft.Text("Destreza:", weight="bold"),
                        destreza_slider,

                        ft.Text("Inteligência:", weight="bold"),
                        inteligencia_slider,
                        
                        ft.Text("Carisma:", weight="bold"),
                        carisma_slider,
                        
                        pontos_info,
                        
                        ft.ElevatedButton(
                            "Criar Personagem",
                            on_click=criar_personagem,
                            width=300,
                            color=ft.colors.GREEN
                        ),
                        ft.ElevatedButton(
                            "Cancelar",
                            on_click=mostrar_tela_principal,
                            width=300,
                            color=ft.colors.RED
                        )
                    ],
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                    ),
                    padding=ft.padding.only(bottom=40)
                )
            )
            page.update()

        mostrar_tela_principal()

    # =============================================
    # 2. TELAS DE AUTENTICAÇÃO
    # =============================================
    def mostrar_login():
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        usuario_input = ft.TextField(label="Usuário", width=300)
        senha_input = ft.TextField(label="Senha", password=True, width=300)
        mensagem = ft.Text("", color=ft.Colors.RED_400)

        def entrar(e):
            if validar_login(usuario_input.value, senha_input.value):
                navegar_para_criacao(usuario_input.value)
            else:
                mensagem.value = "Credenciais inválidas"
                page.update()

        layout = ft.Column(
            [
                ft.Text("Login", size=24, weight="bold"),
                usuario_input,
                senha_input,
                ft.Row(
                    [
                        ft.ElevatedButton("Entrar", on_click=entrar, width=150),
                        ft.TextButton("Registrar", on_click=lambda e: mostrar_registro(), width=150)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                ft.TextButton("Esqueci minha senha", 
                            on_click=lambda e: mostrar_recuperacao_senha(),
                            style=ft.ButtonStyle(color=ft.colors.BLUE)),
                mensagem
            ],
            spacing=20,
            width=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(ft.Container(content=layout, alignment=ft.alignment.center))
        page.update()

    def mostrar_registro():
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        nome_completo = ft.TextField(label="Nome Completo", width=300)
        usuario = ft.TextField(label="Usuário", width=300)
        senha = ft.TextField(label="Senha", password=True, width=300)
        confirmar_senha = ft.TextField(label="Confirmar Senha", password=True, width=300)
        pergunta_secreta = ft.Dropdown(
            label="Pergunta Secreta",
            options=[ft.dropdown.Option(p) for p in PERGUNTAS_SECRETAS],
            width=300
        )
        resposta_secreta = ft.TextField(
            label="Resposta Secreta", 
            password=True, 
            width=300
        )
        mensagem = ft.Text("", color=ft.Colors.RED_400)

        def registrar(e):
            if senha.value != confirmar_senha.value:
                mensagem.value = "As senhas não coincidem"
            elif len(senha.value) < 6:
                mensagem.value = "A senha deve ter pelo menos 6 caracteres"
            elif not pergunta_secreta.value or not resposta_secreta.value:
                mensagem.value = "Preencha a pergunta e resposta secreta"
            else:
                if cadastrar_usuario(
                    nome_completo.value, 
                    usuario.value, 
                    senha.value, 
                    pergunta_secreta.value,
                    resposta_secreta.value
                ):
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Cadastro realizado com sucesso!"),
                        bgcolor=ft.Colors.GREEN
                    )
                    page.snack_bar.open = True
                    mostrar_login()
                else:
                    mensagem.value = "Usuário já existe"
            page.update()

        layout = ft.Column(
            [
                ft.Text("Registro", size=24, weight="bold"),
                nome_completo,
                usuario,
                senha,
                confirmar_senha,
                pergunta_secreta,
                resposta_secreta,
                ft.ElevatedButton("Cadastrar", on_click=registrar, width=300),
                ft.TextButton("Já tem conta? Faça login", on_click=lambda e: mostrar_login()),
                mensagem
            ],
            spacing=20,
            width=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(ft.Container(content=layout, alignment=ft.alignment.center))
        page.update()

    def mostrar_recuperacao_senha():
        page.controls.clear()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        usuario = ft.TextField(label="Seu usuário", width=300)
        mensagem = ft.Text("", color=ft.Colors.RED_400)

        def verificar_usuario(e):
            if verificar_usuario_existente(usuario.value):
                with sqlite3.connect("usuarios.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT pergunta_secreta FROM usuarios WHERE usuario = ?', (usuario.value,))
                    resultado = cursor.fetchone()
                    if resultado:
                        mostrar_verificacao_resposta(usuario.value, resultado[0])
            else:
                mensagem.value = "Usuário não encontrado"
                page.update()

        layout = ft.Column(
            [
                ft.Text("Recuperar Senha", size=24, weight="bold"),
                ft.Text("Digite seu usuário para ver sua pergunta secreta"),
                usuario,
                ft.ElevatedButton("Verificar", on_click=verificar_usuario, width=300),
                ft.TextButton("Voltar ao login", on_click=lambda e: mostrar_login()),
                mensagem
            ],
            spacing=20,
            width=400,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(ft.Container(content=layout, alignment=ft.alignment.center))
        page.update()

    def mostrar_verificacao_resposta(usuario: str, pergunta: str):
        page.controls.clear()
        
        resposta_input = ft.TextField(
            label=f"Responda: {pergunta}", 
            password=True, 
            width=300
        )
        mensagem = ft.Text("", color=ft.Colors.RED_400)

        def verificar_resposta(e):
            if verificar_resposta_secreta(usuario, resposta_input.value):
                mostrar_nova_senha(usuario)
            else:
                mensagem.value = "Resposta incorreta"
                page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Verificação de Segurança", size=24, weight="bold"),
                    resposta_input,
                    ft.ElevatedButton("Verificar Resposta", on_click=verificar_resposta, width=300),
                    ft.TextButton("Voltar", on_click=lambda e: mostrar_login()),
                    mensagem
                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        )
        page.update()

    def mostrar_nova_senha(usuario: str):
        page.controls.clear()
        
        nova_senha = ft.TextField(label="Nova senha", password=True, width=300)
        confirmar_senha = ft.TextField(label="Confirmar nova senha", password=True, width=300)
        mensagem = ft.Text("", color=ft.Colors.RED_400)

        def redefinir(e):
            if nova_senha.value != confirmar_senha.value:
                mensagem.value = "As senhas não coincidem"
            elif len(nova_senha.value) < 6:
                mensagem.value = "A senha deve ter pelo menos 6 caracteres"
            else:
                if recuperar_senha(usuario, nova_senha.value):
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("Senha redefinida com sucesso!"),
                        bgcolor=ft.Colors.GREEN
                    )
                    page.snack_bar.open = True
                    mostrar_login()
                else:
                    mensagem.value = "Erro ao redefinir senha"
            page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Redefinir Senha", size=24, weight="bold"),
                    nova_senha,
                    confirmar_senha,
                    ft.ElevatedButton("Redefinir Senha", on_click=redefinir, width=300),
                    ft.TextButton("Cancelar", on_click=lambda e: mostrar_login()),
                    mensagem
                ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.alignment.center
            )
        )
        page.update()

    # =============================================
    # 3. INICIALIZAÇÃO
    # =============================================
    mostrar_login()

ft.app(target=main)
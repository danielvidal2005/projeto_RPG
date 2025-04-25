# Projeto RPG

## Descrição

Este projeto é uma aplicação simples para a criação de personagens de RPG. As principais funcionalidades incluem:

- Cadastro e login de usuários
- Recuperação de senha
- Criação de personagens personalizados com limite de pontos para atributos
- Armazenamento dos dados com SQLite
- Interface gráfica com Flet (Python)

## Tecnologias Utilizadas

- Python
- anyio==4.9.0
- arrow==1.3.0
- bcrypt==4.3.0
- binaryornot==0.4.4
- blinker==1.9.0
- certifi==2025.1.31
- chardet==5.2.0
- charset-normalizer==3.4.1
- click==8.1.8
- cookiecutter==2.6.0
- flet==0.27.6
- flet-cli==0.27.6
- flet-desktop==0.27.6
- h11==0.14.0
- httpcore==1.0.8
- httpx==0.28.1
- idna==3.10
- itsdangerous==2.2.0
- Jinja2==3.1.6
- markdown-it-py==3.0.0
- MarkupSafe==3.0.2
- mdurl==0.1.2
- oauthlib==3.2.2
- packaging==25.0
- Pygments==2.19.1
- pypng==0.20220715.0
- python-dateutil==2.9.0.post0
- python-slugify==8.0.4
- PyYAML==6.0.2
- qrcode==7.4.2
- repath==0.9.0
- requests==2.32.3
- rich==14.0.0
- six==1.17.0
- sniffio==1.3.1
- SQLAlchemy==2.0.40
- text-unidecode==1.3
- toml==0.10.2
- types-python-dateutil==2.9.0.20241206
- typing_extensions==4.13.2
- urllib3==2.4.0
- watchdog==4.0.2
- Werkzeug==3.1.3

## Como Rodar o Projeto

1. Clone o repositório:

    ```bash
    git clone https://github.com/danielvidal2005/projeto_RPG.git
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # no Linux/MacOS
    .\.venv\Scripts\activate  # no Windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Navegue até a pasta do código-fonte e execute o projeto:

    ```bash
    cd src
    python main.py
    ```

## Autor

- **Nome**: Daniel Vidal
- **Email**: [danielvidal2005@gmail.com](mailto:danielvidal2005@gmail.com)
- **GitHub**: [https://github.com/danielvidal2005](https://github.com/danielvidal2005)

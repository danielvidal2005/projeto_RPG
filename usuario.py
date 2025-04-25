import sqlite3
import bcrypt

def criar_tabela_usuarios():
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                pergunta_secreta TEXT NOT NULL,
                resposta_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def cadastrar_usuario(nome_completo: str, usuario: str, senha: str, pergunta_secreta: str, resposta_secreta: str) -> bool:
    try:
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        resposta_hash = bcrypt.hashpw(resposta_secreta.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        with sqlite3.connect("usuarios.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios 
                (nome_completo, usuario, senha_hash, pergunta_secreta, resposta_hash) 
                VALUES (?, ?, ?, ?, ?)
            ''', (nome_completo, usuario, senha_hash, pergunta_secreta, resposta_hash))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {str(e)}")
        return False

def validar_login(usuario: str, senha: str) -> bool:
    """Verifica as credenciais do usuário"""
    try:
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT senha_hash FROM usuarios WHERE usuario = ?', (usuario,))
            resultado = cursor.fetchone()

        if resultado:
            senha_hash = resultado[0].encode('utf-8')
            return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)
        return False
        
    except Exception as e:
        print(f"Erro ao validar login: {str(e)}")
        return False

def verificar_usuario_existente(usuario: str) -> bool:
    """Verifica se um nome de usuário já está cadastrado"""
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM usuarios WHERE usuario = ?', (usuario,))
        return cursor.fetchone() is not None
    

def recuperar_senha(usuario: str, nova_senha: str) -> bool:
    """Atualiza a senha de um usuário existente"""
    try:
        senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        with sqlite3.connect("usuarios.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE usuarios SET senha_hash = ?
            WHERE usuario = ?
            ''', (senha_hash, usuario))
            conn.commit()
            return cursor.rowcount > 0
            
    except Exception as e:
        print(f"Erro ao recuperar senha: {str(e)}")
        return False
    
def verificar_resposta_secreta(usuario: str, resposta: str) -> bool:
    """Verifica se a resposta secreta está correta"""
    with sqlite3.connect('usuarios.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT resposta_hash FROM usuarios WHERE usuario = ?', (usuario,))
        resultado = cursor.fetchone()
        if resultado:
            return bcrypt.checkpw(resposta.encode('utf-8'), resultado[0].encode('utf-8'))
        return False
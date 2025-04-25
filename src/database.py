import sqlite3
from personagem import Personagem

def criar_tabela_personagens():
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                nome TEXT NOT NULL,
                raca TEXT NOT NULL,
                sexo TEXT NOT NULL,
                cor_pele TEXT NOT NULL,
                tamanho_cabelo TEXT NOT NULL,
                cor_cabelo TEXT NOT NULL,
                cor_olhos TEXT NOT NULL,
                forca INTEGER NOT NULL,
                destreza INTEGER NOT NULL,
                inteligencia INTEGER NOT NULL,
                carisma INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuario (id)
            )
        ''')
        conn.commit()

def inserir_personagem(usuario, personagem):
    try:
        with sqlite3.connect("usuarios.db") as conn:
            cursor = conn.cursor()
            
            # Obtém ID do usuário
            cursor.execute('SELECT id FROM usuarios WHERE usuario = ?', (usuario,))
            usuario_id = cursor.fetchone()
            
            if not usuario_id:
                print("Usuário não encontrado!")
                return False
                
            usuario_id = usuario_id[0]
            
            # Insere personagem
            cursor.execute('''
                INSERT INTO personagens (
                    usuario_id, nome, raca, sexo, cor_pele, tamanho_cabelo,
                    cor_cabelo, cor_olhos, forca, destreza, inteligencia, carisma
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                usuario_id,
                personagem.nome,
                personagem.raca,
                personagem.sexo,
                personagem.cor_pele,
                personagem.tamanho_cabelo,
                personagem.cor_cabelo,
                personagem.cor_olhos,
                personagem.forca,
                personagem.destreza,
                personagem.inteligencia,
                personagem.carisma
            ))
            
            conn.commit()
            print("Personagem inserido com sucesso!")
            return True
            
    except sqlite3.Error as e:
        print(f"Erro ao inserir personagem: {str(e)}")
        return False

def obter_personagens(usuario_logado):
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM personagens 
            WHERE usuario_id = (
                SELECT id FROM usuarios 
                WHERE usuario = ?
            )
        ''', (usuario_logado,))
        return cursor.fetchall()
    
def deletar_personagem(id_personagem):
    with sqlite3.connect("usuarios.db") as conn:
        cursor = conn.cursor()
        query = "DELETE FROM personagens WHERE id = ?"
        cursor.execute(query, (id_personagem,))
        conn.commit()


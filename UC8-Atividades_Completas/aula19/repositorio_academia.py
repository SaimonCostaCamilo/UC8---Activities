"""Repositório SQLite da demonstração A19 (dados fictícios)."""
from pathlib import Path
import sqlite3

class RepositorioAcademia:
    def __init__(self, caminho):
        self.caminho = Path(caminho).expanduser().resolve()
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._inicializar()

    def conectar(self):
        return sqlite3.connect(self.caminho)

    def _inicializar(self):
        with self.conectar() as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0)
                );
                CREATE TABLE IF NOT EXISTS planos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0),
                    valor_centavos INTEGER NOT NULL CHECK(valor_centavos >= 0)
                );
                CREATE TABLE IF NOT EXISTS matriculas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    plano_id INTEGER NOT NULL,
                    data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

    @staticmethod
    def _nome(nome):
        nome = str(nome).strip()
        if not nome:
            raise ValueError('Informe um nome.')
        return nome

    def adicionar_aluno(self, nome):
        with self.conectar() as con:
            cur = con.execute('INSERT INTO alunos(nome) VALUES (?)', (self._nome(nome),))
            return cur.lastrowid

    def adicionar_plano(self, nome, valor_centavos):
        nome = self._nome(nome)
        if type(valor_centavos) is not int or valor_centavos < 0:
            raise ValueError('Valor do plano inválido; informe centavos inteiros não negativos.')
        with self.conectar() as con:
            cur = con.execute('INSERT INTO planos(nome, valor_centavos) VALUES (?, ?)', (nome, valor_centavos))
            return cur.lastrowid

    def adicionar_matricula(self, aluno_id, plano_id):
        if type(aluno_id) is not int or aluno_id <= 0 or type(plano_id) is not int or plano_id <= 0:
            raise ValueError('IDs devem ser inteiros positivos.')
        with self.conectar() as con:
            if not con.execute('SELECT 1 FROM alunos WHERE id=?', (aluno_id,)).fetchone():
                raise ValueError(f'Aluno ID {aluno_id} não encontrado.')
            if not con.execute('SELECT 1 FROM planos WHERE id=?', (plano_id,)).fetchone():
                raise ValueError(f'Plano ID {plano_id} não encontrado.')
            cur = con.execute('INSERT INTO matriculas(aluno_id, plano_id) VALUES (?, ?)', (aluno_id, plano_id))
            return cur.lastrowid

    def excluir_aluno(self, codigo):
        if type(codigo) is not int or codigo <= 0:
            raise ValueError('ID do aluno deve ser inteiro positivo.')
        with self.conectar() as con:
            if con.execute('SELECT 1 FROM matriculas WHERE aluno_id=?', (codigo,)).fetchone():
                raise ValueError('Aluno possui matrícula vinculada; exclusão bloqueada.')
            return con.execute('DELETE FROM alunos WHERE id=?', (codigo,)).rowcount == 1

    def excluir_plano(self, codigo):
        if type(codigo) is not int or codigo <= 0:
            raise ValueError('ID do plano deve ser inteiro positivo.')
        with self.conectar() as con:
            if con.execute('SELECT 1 FROM matriculas WHERE plano_id=?', (codigo,)).fetchone():
                raise ValueError('Plano possui matrícula vinculada; exclusão bloqueada.')
            return con.execute('DELETE FROM planos WHERE id=?', (codigo,)).rowcount == 1

    def listar_alunos(self):
        with self.conectar() as con:
            return con.execute('SELECT id, nome FROM alunos ORDER BY id').fetchall()

    def listar_planos(self):
        with self.conectar() as con:
            return con.execute('SELECT id, nome, valor_centavos FROM planos ORDER BY id').fetchall()

    def listar_matriculas(self):
        with self.conectar() as con:
            return con.execute('''SELECT m.id, m.aluno_id, a.nome, m.plano_id, p.nome
                FROM matriculas m JOIN alunos a ON a.id=m.aluno_id
                JOIN planos p ON p.id=m.plano_id ORDER BY m.id''').fetchall()

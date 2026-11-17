"""Repositório A20: persistência SQLite com FK e ON DELETE RESTRICT."""
from pathlib import Path
import sqlite3
from vinculos import validar_vinculos, pode_excluir_aluno

class RepositorioRelacional:
    def __init__(self, caminho):
        self.caminho=Path(caminho).expanduser().resolve()
        self.caminho.parent.mkdir(parents=True,exist_ok=True)
        self._inicializar()

    def conectar(self):
        con=sqlite3.connect(self.caminho)
        con.execute('PRAGMA foreign_keys = ON')
        return con

    def _inicializar(self):
        with self.conectar() as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT CHECK(id > 0),
                    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0)
                );
                CREATE TABLE IF NOT EXISTS planos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT CHECK(id > 0),
                    nome TEXT NOT NULL CHECK(length(trim(nome)) > 0),
                    valor_centavos INTEGER NOT NULL CHECK(valor_centavos >= 0)
                );
                CREATE TABLE IF NOT EXISTS matriculas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT CHECK(id > 0),
                    aluno_id INTEGER NOT NULL,
                    plano_id INTEGER NOT NULL,
                    data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(aluno_id) REFERENCES alunos(id) ON DELETE RESTRICT,
                    FOREIGN KEY(plano_id) REFERENCES planos(id) ON DELETE RESTRICT
                );
            """)

    @staticmethod
    def _id(valor, rotulo):
        if type(valor) is not int or valor <= 0: raise ValueError(f'{rotulo} deve ser inteiro positivo.')
        return valor

    @staticmethod
    def _nome(valor):
        valor=str(valor).strip()
        if not valor: raise ValueError('Informe um nome.')
        return valor

    def adicionar_aluno(self,nome):
        with self.conectar() as con: return con.execute('INSERT INTO alunos(nome) VALUES(?)',(self._nome(nome),)).lastrowid

    def adicionar_plano(self,nome,valor_centavos):
        if type(valor_centavos) is not int or valor_centavos < 0: raise ValueError('Valor inválido.')
        with self.conectar() as con: return con.execute('INSERT INTO planos(nome,valor_centavos) VALUES(?,?)',(self._nome(nome),valor_centavos)).lastrowid

    def adicionar_matricula(self,aluno_id,plano_id):
        aluno_id=self._id(aluno_id,'ID do aluno'); plano_id=self._id(plano_id,'ID do plano')
        alunos={r[0]:r[1] for r in self.listar_alunos()}
        planos={r[0]:r[1] for r in self.listar_planos()}
        matriculas=[{'id':r[0],'aluno_id':r[1],'plano_id':r[3]} for r in self.listar_matriculas()]
        validar_vinculos(alunos,planos,matriculas+[{'id':max([m['id'] for m in matriculas],default=0)+1,'aluno_id':aluno_id,'plano_id':plano_id}])
        try:
            with self.conectar() as con:
                return con.execute('INSERT INTO matriculas(aluno_id,plano_id) VALUES(?,?)',(aluno_id,plano_id)).lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Vínculo recusado pelo SQLite: {erro}') from erro

    def excluir_aluno(self,codigo):
        codigo=self._id(codigo,'ID do aluno')
        matriculas=[{'id':r[0],'aluno_id':r[1],'plano_id':r[3]} for r in self.listar_matriculas()]
        if not pode_excluir_aluno(codigo,matriculas): raise ValueError('Aluno possui matrícula vinculada; exclusão bloqueada.')
        try:
            with self.conectar() as con: return con.execute('DELETE FROM alunos WHERE id=?',(codigo,)).rowcount==1
        except sqlite3.IntegrityError as erro: raise ValueError(f'Exclusão bloqueada por integridade referencial: {erro}') from erro

    def excluir_plano(self,codigo):
        codigo=self._id(codigo,'ID do plano')
        try:
            with self.conectar() as con: return con.execute('DELETE FROM planos WHERE id=?',(codigo,)).rowcount==1
        except sqlite3.IntegrityError as erro: raise ValueError('Plano possui matrícula vinculada; exclusão bloqueada.') from erro

    def listar_alunos(self):
        with self.conectar() as con:return con.execute('SELECT id,nome FROM alunos ORDER BY id').fetchall()
    def listar_planos(self):
        with self.conectar() as con:return con.execute('SELECT id,nome,valor_centavos FROM planos ORDER BY id').fetchall()
    def listar_matriculas(self):
        with self.conectar() as con:return con.execute('''SELECT m.id,m.aluno_id,a.nome,m.plano_id,p.nome FROM matriculas m JOIN alunos a ON a.id=m.aluno_id JOIN planos p ON p.id=m.plano_id ORDER BY m.id''').fetchall()

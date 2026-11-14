"""Repositório SQLite da Aula 14. Importar este módulo não cria o banco."""
from contextlib import closing
from pathlib import Path
import sqlite3

from pagamento import preco_para_centavos


def validar_nome(nome):
    """Retorna o nome sem espaços externos; rejeita valores vazios e não textuais."""
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("Informe um nome de produto/cliente.")
    nome = nome.strip()
    if len(nome) > 120:
        raise ValueError("O nome deve ter no máximo 120 caracteres.")
    return nome


def validar_id(codigo):
    """Converte um identificador em inteiro positivo, sem aceitar bool."""
    if isinstance(codigo, bool):
        raise ValueError("O ID deve ser um inteiro positivo.")
    try:
        valor = int(codigo)
    except (TypeError, ValueError) as erro:
        raise ValueError("O ID deve ser um inteiro positivo.") from erro
    if str(codigo).strip() not in (str(valor), f"+{valor}") or valor <= 0:
        raise ValueError("O ID deve ser um inteiro positivo.")
    return valor


def validar_preco(preco):
    """Converte preço digitado para centavos inteiros e exige valor positivo."""
    centavos = preco_para_centavos(preco)
    if centavos <= 0:
        raise ValueError("O preço deve ser maior que zero.")
    return centavos


class RepositorioSqlite:
    """Persistência local de produtos e clientes em um único arquivo SQLite."""

    def __init__(self, caminho):
        if caminho is None or not str(caminho).strip():
            raise ValueError("Informe o caminho do banco SQLite.")
        self.caminho = Path(caminho).expanduser().resolve()

    def conectar(self):
        """Abre uma conexão; quem chama deve fechá-la (preferencialmente com closing)."""
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        conexao = sqlite3.connect(str(self.caminho), timeout=10)
        conexao.row_factory = sqlite3.Row
        return conexao

    def iniciar(self):
        """Cria tabelas ausentes sem apagar registros já existentes."""
        sql_produtos = """CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco_centavos INTEGER NOT NULL CHECK(preco_centavos > 0)
        )"""
        sql_clientes = """CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )"""
        with closing(self.conectar()) as con:
            try:
                con.execute(sql_produtos)
                con.execute(sql_clientes)
                con.commit()
            except Exception:
                con.rollback()
                raise
        return True

    def adicionar_produto(self, nome, preco):
        nome_validado = validar_nome(nome)
        preco_centavos = validar_preco(preco)
        sql = "INSERT INTO produtos (nome, preco_centavos) VALUES (?, ?)"
        with closing(self.conectar()) as con:
            try:
                cursor = con.execute(sql, (nome_validado, preco_centavos))
                codigo = cursor.lastrowid
                con.commit()
            except Exception:
                con.rollback()
                raise
        return {"id": codigo, "nome": nome_validado, "preco_centavos": preco_centavos}

    def listar_produtos(self):
        with closing(self.conectar()) as con:
            linhas = con.execute(
                "SELECT id, nome, preco_centavos FROM produtos ORDER BY id"
            ).fetchall()
        return [dict(linha) for linha in linhas]

    def adicionar_cliente(self, nome):
        nome_validado = validar_nome(nome)
        with closing(self.conectar()) as con:
            try:
                cursor = con.execute(
                    "INSERT INTO clientes (nome) VALUES (?)", (nome_validado,)
                )
                codigo = cursor.lastrowid
                con.commit()
            except Exception:
                con.rollback()
                raise
        return {"id": codigo, "nome": nome_validado}

    def listar_clientes(self):
        with closing(self.conectar()) as con:
            linhas = con.execute(
                "SELECT id, nome FROM clientes ORDER BY id"
            ).fetchall()
        return [dict(linha) for linha in linhas]


    def editar_produto(self, codigo, nome, preco):
        codigo = validar_id(codigo)
        nome_validado = validar_nome(nome)
        preco_centavos = validar_preco(preco)
        with closing(self.conectar()) as con:
            try:
                cursor = con.execute(
                    "UPDATE produtos SET nome = ?, preco_centavos = ? WHERE id = ?",
                    (nome_validado, preco_centavos, codigo),
                )
                con.commit()
                return cursor.rowcount == 1
            except Exception:
                con.rollback()
                raise

    def excluir_produto(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if confirmado is not True:
            return False
        with closing(self.conectar()) as con:
            try:
                cursor = con.execute("DELETE FROM produtos WHERE id = ?", (codigo,))
                con.commit()
                return cursor.rowcount == 1
            except Exception:
                con.rollback()
                raise

    def editar_cliente(self, codigo, nome):
        codigo = validar_id(codigo)
        nome_validado = validar_nome(nome)
        with closing(self.conectar()) as con:
            try:
                cursor = con.execute(
                    "UPDATE clientes SET nome = ? WHERE id = ?", (nome_validado, codigo)
                )
                con.commit()
                return cursor.rowcount == 1
            except Exception:
                con.rollback()
                raise

    def excluir_cliente(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if confirmado is not True:
            return False
        with closing(self.conectar()) as con:
            try:
                cursor = con.execute("DELETE FROM clientes WHERE id = ?", (codigo,))
                con.commit()
                return cursor.rowcount == 1
            except Exception:
                con.rollback()
                raise

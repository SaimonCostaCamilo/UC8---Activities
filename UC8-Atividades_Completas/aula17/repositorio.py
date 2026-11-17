"""Persistência SQLite da A17: cadastros e vendas com itens atômicos."""
from contextlib import closing
from pathlib import Path
import sqlite3
from pagamento import preco_para_centavos, calcular_pagamento


def validar_nome(nome):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("Informe um nome de produto/cliente.")
    nome = nome.strip()
    if len(nome) > 120:
        raise ValueError("O nome deve ter no máximo 120 caracteres.")
    return nome


def validar_id(codigo):
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
    centavos = preco_para_centavos(preco)
    if centavos <= 0:
        raise ValueError("O preço deve ser maior que zero.")
    return centavos


class RepositorioSqlite:
    """Repositório local; cada conexão ativa chaves estrangeiras."""
    def __init__(self, caminho):
        if caminho is None or not str(caminho).strip():
            raise ValueError("Informe o caminho do banco SQLite.")
        self.caminho = Path(caminho).expanduser().resolve()

    def conectar(self):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(str(self.caminho), timeout=10)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def iniciar(self):
        comandos = [
            """CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco_centavos INTEGER NOT NULL CHECK(preco_centavos > 0)
            )""",
            """CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                cliente_nome TEXT NOT NULL,
                data_hora TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now','localtime')),
                forma_pagamento TEXT NOT NULL,
                subtotal_centavos INTEGER NOT NULL CHECK(subtotal_centavos > 0),
                total_pagamento_centavos INTEGER NOT NULL CHECK(total_pagamento_centavos > 0),
                FOREIGN KEY(cliente_id) REFERENCES clientes(id) ON UPDATE RESTRICT ON DELETE RESTRICT
            )""",
            """CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                nome_produto TEXT NOT NULL,
                preco_unitario_centavos INTEGER NOT NULL CHECK(preco_unitario_centavos > 0),
                quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                subtotal_centavos INTEGER NOT NULL CHECK(subtotal_centavos > 0),
                FOREIGN KEY(venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
                FOREIGN KEY(produto_id) REFERENCES produtos(id) ON UPDATE RESTRICT ON DELETE RESTRICT
            )""",
        ]
        with closing(self.conectar()) as con:
            try:
                for sql in comandos:
                    con.execute(sql)
                con.commit()
            except Exception:
                con.rollback()
                raise
        return True

    def adicionar_produto(self, nome, preco):
        nome, centavos = validar_nome(nome), validar_preco(preco)
        with closing(self.conectar()) as con:
            try:
                cur = con.execute("INSERT INTO produtos(nome,preco_centavos) VALUES(?,?)", (nome, centavos))
                con.commit()
                return {"id": cur.lastrowid, "nome": nome, "preco_centavos": centavos}
            except Exception:
                con.rollback(); raise

    def listar_produtos(self):
        with closing(self.conectar()) as con:
            return [dict(r) for r in con.execute("SELECT id,nome,preco_centavos FROM produtos ORDER BY id")]

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        with closing(self.conectar()) as con:
            try:
                cur = con.execute("INSERT INTO clientes(nome) VALUES(?)", (nome,))
                con.commit()
                return {"id": cur.lastrowid, "nome": nome}
            except Exception:
                con.rollback(); raise

    def listar_clientes(self):
        with closing(self.conectar()) as con:
            return [dict(r) for r in con.execute("SELECT id,nome FROM clientes ORDER BY id")]

    def editar_produto(self, codigo, nome, preco):
        codigo, nome, centavos = validar_id(codigo), validar_nome(nome), validar_preco(preco)
        with closing(self.conectar()) as con:
            try:
                cur = con.execute("UPDATE produtos SET nome=?,preco_centavos=? WHERE id=?", (nome,centavos,codigo))
                con.commit(); return cur.rowcount == 1
            except Exception:
                con.rollback(); raise

    def excluir_produto(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if confirmado is not True: return False
        with closing(self.conectar()) as con:
            try:
                cur = con.execute("DELETE FROM produtos WHERE id=?", (codigo,))
                con.commit(); return cur.rowcount == 1
            except Exception:
                con.rollback(); raise

    def editar_cliente(self, codigo, nome):
        codigo, nome = validar_id(codigo), validar_nome(nome)
        with closing(self.conectar()) as con:
            try:
                cur = con.execute("UPDATE clientes SET nome=? WHERE id=?", (nome,codigo))
                con.commit(); return cur.rowcount == 1
            except Exception:
                con.rollback(); raise

    def excluir_cliente(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if confirmado is not True: return False
        with closing(self.conectar()) as con:
            try:
                cur = con.execute("DELETE FROM clientes WHERE id=?", (codigo,))
                con.commit(); return cur.rowcount == 1
            except Exception:
                con.rollback(); raise

    def iniciar_vendas(self):
        """Garante o esquema de vendas sem apagar cadastros ou histórico."""
        return self.iniciar()

    def registrar_venda(self, cliente_id, itens, forma):
        """Insere cabeçalho e todos os itens na MESMA transação SQLite."""
        cliente_id = validar_id(cliente_id)
        if not isinstance(itens, (list, tuple)) or not itens:
            raise ValueError("A venda precisa conter ao menos um item.")
        if forma not in ("Dinheiro", "PIX", "Débito", "Crédito 1x"):
            raise ValueError("Forma de pagamento inválida.")
        # Normalização e soma feitas antes da escrita, mas conferência do catálogo
        # acontece dentro da transação para evitar usar preço/nome obsoletos.
        normalizados = []
        soma = 0
        for pos, item in enumerate(itens, 1):
            if not isinstance(item, dict):
                raise ValueError(f"Item {pos} inválido.")
            pid = validar_id(item.get("codigo", item.get("produto_id")))
            qtd = item.get("quantidade")
            if isinstance(qtd, bool) or not isinstance(qtd, int) or qtd <= 0:
                raise ValueError(f"Quantidade inválida no item {pos}.")
            nome = validar_nome(item.get("nome"))
            preco = item.get("preco_unitario", item.get("preco_unitario_centavos"))
            if isinstance(preco, bool) or not isinstance(preco, int) or preco <= 0:
                raise ValueError(f"Preço inválido no item {pos}.")
            subtotal = item.get("subtotal", preco * qtd)
            if isinstance(subtotal, bool) or not isinstance(subtotal, int) or subtotal != preco * qtd:
                raise ValueError(f"Subtotal divergente no item {pos}.")
            normalizados.append({"produto_id": pid, "nome": nome, "preco": preco, "quantidade": qtd, "subtotal": subtotal})
            soma += subtotal
        pagamento = calcular_pagamento(f"{soma // 100},{soma % 100:02d}", forma)
        total_pagamento = int(pagamento["total"] * 100)

        with closing(self.conectar()) as con:
            try:
                with con:
                    con.execute("BEGIN IMMEDIATE")
                    cliente = con.execute("SELECT id,nome FROM clientes WHERE id=?", (cliente_id,)).fetchone()
                    if cliente is None:
                        raise ValueError(f"Cliente ID {cliente_id} não existe. Atualize a seleção.")
                    for item in normalizados:
                        produto = con.execute("SELECT nome,preco_centavos FROM produtos WHERE id=?", (item["produto_id"],)).fetchone()
                        if produto is None:
                            raise ValueError(f"Produto ID {item['produto_id']} não existe mais. Revise a montagem.")
                        if produto["nome"] != item["nome"] or produto["preco_centavos"] != item["preco"]:
                            raise ValueError(f"O produto ID {item['produto_id']} mudou no catálogo. Atualize e revise o item antes de confirmar.")
                    cur = con.execute(
                        "INSERT INTO vendas(cliente_id,cliente_nome,forma_pagamento,subtotal_centavos,total_pagamento_centavos) VALUES(?,?,?,?,?)",
                        (cliente_id, cliente["nome"], forma, soma, total_pagamento),
                    )
                    venda_id = cur.lastrowid
                    for item in normalizados:
                        con.execute(
                            "INSERT INTO itens_venda(venda_id,produto_id,nome_produto,preco_unitario_centavos,quantidade,subtotal_centavos) VALUES(?,?,?,?,?,?)",
                            (venda_id, item["produto_id"], item["nome"], item["preco"], item["quantidade"], item["subtotal"]),
                        )
                # O contexto faz commit somente após o último item.
            except Exception:
                con.rollback()
                raise
        return {
            "id": venda_id, "cliente_id": cliente_id, "cliente_nome": cliente["nome"],
            "forma_pagamento": forma, "subtotal_centavos": soma,
            "total_pagamento_centavos": total_pagamento, "itens": [dict(i) for i in normalizados],
        }

    def listar_vendas(self):
        with closing(self.conectar()) as con:
            vendas = [dict(r) for r in con.execute("SELECT id,cliente_id,cliente_nome,data_hora,forma_pagamento,subtotal_centavos,total_pagamento_centavos FROM vendas ORDER BY id DESC")]
            for venda in vendas:
                itens = con.execute("SELECT produto_id AS codigo,nome_produto AS nome,preco_unitario_centavos AS preco_unitario,quantidade,subtotal_centavos AS subtotal FROM itens_venda WHERE venda_id=? ORDER BY id", (venda["id"],)).fetchall()
                venda["itens"] = [dict(i) for i in itens]
        return vendas

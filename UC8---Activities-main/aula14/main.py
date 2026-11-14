"""Interface A14: cadastro persistente de produtos (SQLite) e pedido em memória."""
import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from pathlib import Path

from modelos import Pedido, Produto, formatar
from repositorio import RepositorioSqlite


class AplicacaoA14:
    def __init__(self, janela, repositorio=None):
        self.janela = janela
        self.janela.title("A14 — Produtos persistidos com SQLite")
        self.janela.geometry("900x650")
        self.janela.minsize(700, 520)
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(1, weight=1)
        caminho_db = Path(__file__).resolve().parent / "dados" / "mercado.db"
        self.repositorio = repositorio or RepositorioSqlite(caminho_db)
        self.repositorio.iniciar()
        self.pedido = Pedido()  # Carrinho permanece em memória nesta aula.
        self.produtos = []
        self._montar_interface()
        self.atualizar_lista_produtos()
        self.atualizar_pedido()

    def _montar_interface(self):
        base = ttk.Frame(self.janela, padding=12)
        base.grid(row=0, column=0, sticky="nsew")
        base.columnconfigure(0, weight=1)
        base.rowconfigure(1, weight=1)

        ttk.Label(base, text="A14 — Cadastro de produtos", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        cadastro = ttk.LabelFrame(base, text="Novo produto — gravação SQLite", padding=10)
        cadastro.grid(row=1, column=0, sticky="nsew")
        cadastro.columnconfigure(1, weight=1)
        ttk.Label(cadastro, text="Nome:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.campo_nome = ttk.Entry(cadastro)
        self.campo_nome.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(cadastro, text="Preço (ex.: 7,50):").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.campo_preco = ttk.Entry(cadastro)
        self.campo_preco.grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        ttk.Button(cadastro, text="Salvar produto", command=self.salvar_produto).grid(
            row=2, column=1, sticky="e", padx=4, pady=6
        )

        area = ttk.LabelFrame(base, text="Produtos cadastrados no banco", padding=8)
        area.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)
        self.tabela_produtos = ttk.Treeview(
            area, columns=("id", "nome", "preco"), show="headings", height=7, selectmode="browse"
        )
        for coluna, titulo, largura in (
            ("id", "ID", 70), ("nome", "Produto", 450), ("preco", "Preço", 140)
        ):
            self.tabela_produtos.heading(coluna, text=titulo)
            self.tabela_produtos.column(coluna, width=largura, anchor="w" if coluna == "nome" else "center")
        self.tabela_produtos.grid(row=0, column=0, sticky="nsew")
        barra = ttk.Scrollbar(area, orient="vertical", command=self.tabela_produtos.yview)
        barra.grid(row=0, column=1, sticky="ns")
        self.tabela_produtos.configure(yscrollcommand=barra.set)
        ttk.Button(area, text="Adicionar selecionado ao pedido", command=self.adicionar_ao_pedido).grid(
            row=1, column=0, sticky="w", pady=7
        )

        pedido = ttk.LabelFrame(base, text="Pedido atual — mantido em memória", padding=8)
        pedido.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
        pedido.columnconfigure(0, weight=1)
        self.tabela_pedido = ttk.Treeview(
            pedido, columns=("id", "nome", "qtd", "subtotal"), show="headings", height=5
        )
        for col, titulo, width in (("id", "ID", 60), ("nome", "Produto", 400), ("qtd", "Qtd.", 70), ("subtotal", "Subtotal", 130)):
            self.tabela_pedido.heading(col, text=titulo)
            self.tabela_pedido.column(col, width=width, anchor="w" if col == "nome" else "center")
        self.tabela_pedido.grid(row=0, column=0, sticky="ew")
        ttk.Label(pedido, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=(7, 0))
        linha_qtd = ttk.Frame(pedido)
        linha_qtd.grid(row=2, column=0, sticky="ew")
        self.campo_qtd = ttk.Entry(linha_qtd, width=8)
        self.campo_qtd.insert(0, "1")
        self.campo_qtd.pack(side="left")
        ttk.Button(linha_qtd, text="Atualizar selecionado", command=self.atualizar_quantidade).pack(side="left", padx=5)
        ttk.Button(linha_qtd, text="Remover selecionado", command=self.remover_item).pack(side="left", padx=5)
        self.lbl_total = ttk.Label(pedido, text="Total do pedido: R$ 0,00", font=("Segoe UI", 11, "bold"))
        self.lbl_total.grid(row=3, column=0, sticky="e", pady=6)

        self.aviso = ttk.Label(base, text="Pronto. Os produtos permanecem no SQLite após fechar o programa.", wraplength=850)
        self.aviso.grid(row=4, column=0, sticky="w", pady=(8, 0))

    def atualizar_lista_produtos(self):
        registros = self.repositorio.listar_produtos()
        self.produtos = [Produto(str(r["id"]), r["nome"], r["preco_centavos"]) for r in registros]
        for item in self.tabela_produtos.get_children():
            self.tabela_produtos.delete(item)
        for produto in self.produtos:
            self.tabela_produtos.insert(
                "", "end", iid=produto.codigo,
                values=(produto.codigo, produto.nome, formatar(produto.preco_centavos)),
            )

    def salvar_produto(self):
        # Os campos só são limpos e a listagem só é atualizada depois do commit.
        nome = self.campo_nome.get()
        preco = self.campo_preco.get()
        try:
            registro = self.repositorio.adicionar_produto(nome, preco)
            self.atualizar_lista_produtos()
        except (ValueError, OSError, RuntimeError, sqlite3.Error) as erro:
            messagebox.showerror("Não foi possível salvar", str(erro), parent=self.janela)
            self.aviso.configure(text="Falha ao gravar. Os campos foram preservados para correção.")
            return
        self.campo_nome.delete(0, tk.END)
        self.campo_preco.delete(0, tk.END)
        self.campo_nome.focus_set()
        self.aviso.configure(text=f"Produto #{registro['id']} gravado e confirmado no banco.")

    def _produto_selecionado(self):
        selecionados = self.tabela_produtos.selection()
        if not selecionados:
            raise ValueError("Selecione um produto na lista.")
        codigo = selecionados[0]
        for produto in self.produtos:
            if produto.codigo == codigo:
                return produto
        raise ValueError("O produto selecionado não está mais disponível. Atualize a lista.")

    def adicionar_ao_pedido(self):
        try:
            produto = self._produto_selecionado()
            self.pedido.adicionar(produto, self.campo_qtd.get())
            self.atualizar_pedido()
            self.aviso.configure(text=f"{produto.nome} adicionado ao pedido em memória.")
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Pedido", str(erro), parent=self.janela)

    def atualizar_quantidade(self):
        try:
            selecionados = self.tabela_pedido.selection()
            if not selecionados:
                raise ValueError("Selecione um item do pedido.")
            self.pedido.atualizar(selecionados[0], self.campo_qtd.get())
            self.atualizar_pedido()
        except (ValueError, RuntimeError, KeyError) as erro:
            messagebox.showerror("Pedido", str(erro), parent=self.janela)

    def remover_item(self):
        try:
            selecionados = self.tabela_pedido.selection()
            if not selecionados:
                raise ValueError("Selecione um item do pedido.")
            self.pedido.remover(selecionados[0])
            self.atualizar_pedido()
        except (ValueError, RuntimeError, KeyError) as erro:
            messagebox.showerror("Pedido", str(erro), parent=self.janela)

    def atualizar_pedido(self):
        for item in self.tabela_pedido.get_children():
            self.tabela_pedido.delete(item)
        for linha in self.pedido.linhas():
            self.tabela_pedido.insert(
                "", "end", iid=linha["codigo"],
                values=(linha["codigo"], linha["nome"], linha["quantidade"], formatar(linha["subtotal"])),
            )
        self.lbl_total.configure(text=f"Total do pedido: {formatar(self.pedido.total_centavos())}")


def criar_janela(repositorio=None):
    janela = tk.Tk()
    AplicacaoA14(janela, repositorio=repositorio)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

"""A15 — CRUD de produtos por ID, início de clientes e pedido em memória."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import sqlite3

from modelos import Pedido, Produto, formatar
from repositorio import RepositorioSqlite


class AplicacaoA15:
    def __init__(self, janela, repositorio=None):
        self.janela = janela
        janela.title("A15 — CRUD de produtos e clientes")
        janela.geometry("960x760")
        janela.minsize(720, 600)
        janela.columnconfigure(0, weight=1)
        janela.rowconfigure(0, weight=1)
        caminho = Path(__file__).resolve().parent / "dados" / "mercado.db"
        self.repo = repositorio or RepositorioSqlite(caminho)
        self.repo.iniciar()
        self.pedido = Pedido()  # permanece em memória
        self.produtos = []
        self.modo = "novo"
        self._montar()
        self.atualizar_produtos()
        self.atualizar_clientes()
        self.atualizar_pedido()

    def _montar(self):
        base = ttk.Frame(self.janela, padding=12)
        base.grid(sticky="nsew")
        base.columnconfigure(0, weight=1)
        base.rowconfigure(1, weight=1)
        ttk.Label(base, text="A15 — Cadastro, edição e exclusão", font=("Segoe UI", 16, "bold")).grid(sticky="w")
        self.abas = ttk.Notebook(base)
        self.abas.grid(row=1, column=0, sticky="nsew", pady=8)
        produtos = ttk.Frame(self.abas, padding=10)
        clientes = ttk.Frame(self.abas, padding=10)
        self.abas.add(produtos, text="Produtos")
        self.abas.add(clientes, text="Clientes")
        produtos.columnconfigure(1, weight=1)
        ttk.Label(produtos, text="Nome:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.campo_nome = ttk.Entry(produtos)
        self.campo_nome.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(produtos, text="Preço (ex.: 12,50):").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.campo_preco = ttk.Entry(produtos)
        self.campo_preco.grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        acoes = ttk.Frame(produtos)
        acoes.grid(row=2, column=0, columnspan=2, sticky="w", pady=6)
        ttk.Button(acoes, text="Novo", command=self.novo_produto).pack(side="left", padx=3)
        ttk.Button(acoes, text="Salvar", command=self.salvar_produto).pack(side="left", padx=3)
        ttk.Button(acoes, text="Editar selecionado", command=self.carregar_edicao).pack(side="left", padx=3)
        ttk.Button(acoes, text="Excluir selecionado", command=self.excluir_produto).pack(side="left", padx=3)
        ttk.Label(produtos, text="Selecione pela identidade (ID); ordenar a tabela não altera o alvo.").grid(row=3, column=0, columnspan=2, sticky="w")
        self.tabela = ttk.Treeview(produtos, columns=("id","nome","preco"), show="headings", selectmode="browse", height=10)
        for col, label, width in (("id","ID",75),("nome","Produto",430),("preco","Preço",130)):
            self.tabela.heading(col, text=label, command=lambda c=col: self.ordenar(c))
            self.tabela.column(col, width=width, anchor="w" if col=="nome" else "center")
        self.tabela.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=6)
        produtos.rowconfigure(4, weight=1)
        produtos.columnconfigure(0, weight=0)
        produtos.bind("<<TreeviewSelect>>", self._selecionou)

        clientes.columnconfigure(1, weight=1)
        ttk.Label(clientes, text="Nome fictício do cliente:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.campo_cliente = ttk.Entry(clientes)
        self.campo_cliente.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Button(clientes, text="Cadastrar cliente", command=self.salvar_cliente).grid(row=1, column=1, sticky="w", padx=4, pady=5)
        self.tabela_clientes = ttk.Treeview(clientes, columns=("id","nome"), show="headings", height=12)
        self.tabela_clientes.heading("id", text="ID")
        self.tabela_clientes.heading("nome", text="Cliente")
        self.tabela_clientes.column("id", width=80, anchor="center")
        self.tabela_clientes.column("nome", width=500)
        self.tabela_clientes.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=8)
        clientes.rowconfigure(2, weight=1)

        pedido = ttk.LabelFrame(base, text="Pedido atual — somente em memória", padding=8)
        pedido.grid(row=2, column=0, sticky="ew")
        pedido.columnconfigure(0, weight=1)
        self.tabela_pedido = ttk.Treeview(pedido, columns=("id","nome","qtd","subtotal"), show="headings", height=4)
        for c, t, w in (("id","ID",60),("nome","Produto",400),("qtd","Qtd.",70),("subtotal","Subtotal",130)):
            self.tabela_pedido.heading(c, text=t); self.tabela_pedido.column(c, width=w, anchor="w" if c=="nome" else "center")
        self.tabela_pedido.grid(row=0, column=0, sticky="ew")
        linha = ttk.Frame(pedido); linha.grid(row=1, column=0, sticky="w", pady=5)
        ttk.Label(linha, text="Quantidade:").pack(side="left")
        self.campo_qtd = ttk.Entry(linha, width=6); self.campo_qtd.insert(0,"1"); self.campo_qtd.pack(side="left", padx=4)
        ttk.Button(linha, text="Adicionar produto selecionado", command=self.adicionar_pedido).pack(side="left", padx=4)
        ttk.Button(linha, text="Remover item", command=self.remover_item).pack(side="left", padx=4)
        self.lbl_total = ttk.Label(pedido, text="Total: R$ 0,00", font=("Segoe UI", 10, "bold"))
        self.lbl_total.grid(row=2, column=0, sticky="e")
        self.aviso = ttk.Label(base, text="Pronto. Dados fictícios persistem no SQLite.", wraplength=900)
        self.aviso.grid(row=3, column=0, sticky="w", pady=8)

    def _selecionou(self, _event=None):
        if self.modo == "novo": return
        sel = self.tabela.selection()
        if not sel: return
        rid = sel[0]
        registro = next((p for p in self.repo.listar_produtos() if str(p["id"]) == rid), None)
        if registro:
            self.campo_nome.delete(0, tk.END); self.campo_nome.insert(0, registro["nome"])
            self.campo_preco.delete(0, tk.END); self.campo_preco.insert(0, f'{registro["preco_centavos"]//100},{registro["preco_centavos"]%100:02d}')

    def novo_produto(self):
        self.modo = "novo"
        self.tabela.selection_remove(self.tabela.selection())
        self.campo_nome.delete(0, tk.END); self.campo_preco.delete(0, tk.END)
        self.aviso.configure(text="Modo Novo: Salvar criará outro ID.")
        self.campo_nome.focus_set()

    def carregar_edicao(self):
        sel = self.tabela.selection()
        if not sel:
            messagebox.showwarning("Editar produto", "Selecione um produto pelo ID.", parent=self.janela); return
        rid = sel[0]
        registro = next((p for p in self.repo.listar_produtos() if str(p["id"]) == rid), None)
        if registro is None:
            messagebox.showerror("Produto não encontrado", "O ID selecionado não existe mais. Atualize a lista.", parent=self.janela); return
        self.modo = "editar"
        self.campo_nome.delete(0, tk.END); self.campo_nome.insert(0, registro["nome"])
        self.campo_preco.delete(0, tk.END); self.campo_preco.insert(0, f'{registro["preco_centavos"]//100},{registro["preco_centavos"]%100:02d}')
        self.aviso.configure(text=f"Editando produto #{rid}. Salvar atualizará o mesmo ID.")

    def salvar_produto(self):
        nome, preco = self.campo_nome.get(), self.campo_preco.get()
        sel = self.tabela.selection()
        try:
            if self.modo == "editar":
                if not sel: raise ValueError("A seleção da edição foi perdida. Selecione novamente ou clique em Novo.")
                rid = int(sel[0])
                if not self.repo.editar_produto(rid, nome, preco):
                    raise ValueError(f"O produto ID {rid} não existe mais; nenhum cadastro foi criado.")
                mensagem = f"Produto #{rid} atualizado; nenhuma linha nova foi criada."
            else:
                registro = self.repo.adicionar_produto(nome, preco)
                mensagem = f"Produto #{registro['id']} cadastrado."
            self.atualizar_produtos()
        except (ValueError, sqlite3.Error, OSError) as erro:
            messagebox.showerror("Não foi possível salvar", str(erro), parent=self.janela)
            self.aviso.configure(text="Falha: dados persistidos e campos foram preservados para correção.")
            return
        self.novo_produto()
        self.aviso.configure(text=mensagem)

    def excluir_produto(self):
        sel = self.tabela.selection()
        if not sel:
            messagebox.showwarning("Excluir produto", "Selecione um produto antes de excluir.", parent=self.janela); return
        rid = int(sel[0])
        registro = next((p for p in self.repo.listar_produtos() if p["id"] == rid), None)
        if registro is None:
            messagebox.showerror("Produto não encontrado", "O ID não existe mais. Atualize a lista.", parent=self.janela); return
        if not messagebox.askyesno("Confirmar exclusão", f'Excluir o produto #{rid} — {registro["nome"]}?', parent=self.janela):
            self.aviso.configure(text=f"Exclusão do produto #{rid} cancelada; banco e lista preservados."); return
        try:
            if not self.repo.excluir_produto(rid, confirmado=True):
                raise ValueError("O produto não foi encontrado; nada foi removido.")
            self.atualizar_produtos()
            self.novo_produto()
            self.aviso.configure(text=f"Produto #{rid} excluído.")
        except (ValueError, sqlite3.Error) as erro:
            messagebox.showerror("Falha na exclusão", str(erro), parent=self.janela)

    def ordenar(self, coluna):
        if coluna == "preco":
            mapa = {str(p["id"]): p["preco_centavos"] for p in self.produtos}
            pares = [(mapa.get(i, 0), i) for i in self.tabela.get_children("")]
        else:
            pares = [(self.tabela.set(i, coluna), i) for i in self.tabela.get_children("")]
        pares.sort(key=lambda x: (int(x[0]) if coluna == "id" or coluna == "preco" else x[0].casefold()))
        if getattr(self, "_ordem_desc", None) == coluna:
            pares.reverse(); self._ordem_desc = None
        else: self._ordem_desc = coluna
        for pos, (_, iid) in enumerate(pares): self.tabela.move(iid, "", pos)

    def atualizar_produtos(self):
        self.produtos = self.repo.listar_produtos()
        for i in self.tabela.get_children(): self.tabela.delete(i)
        for p in self.produtos:
            self.tabela.insert("", "end", iid=str(p["id"]), values=(p["id"],p["nome"],formatar(p["preco_centavos"])))

    def salvar_cliente(self):
        try:
            r = self.repo.adicionar_cliente(self.campo_cliente.get())
            self.atualizar_clientes()
        except (ValueError, sqlite3.Error, OSError) as erro:
            messagebox.showerror("Cliente", str(erro), parent=self.janela); return
        self.campo_cliente.delete(0, tk.END)
        self.aviso.configure(text=f'Cliente fictício #{r["id"]} cadastrado e listado.')

    def atualizar_clientes(self):
        for i in self.tabela_clientes.get_children(): self.tabela_clientes.delete(i)
        for c in self.repo.listar_clientes():
            self.tabela_clientes.insert("", "end", iid=str(c["id"]), values=(c["id"],c["nome"]))

    def adicionar_pedido(self):
        try:
            sel = self.tabela.selection()
            if not sel: raise ValueError("Selecione um produto.")
            r = next((p for p in self.repo.listar_produtos() if str(p["id"]) == sel[0]), None)
            if r is None: raise ValueError("Produto não encontrado.")
            self.pedido.adicionar(Produto(str(r["id"]), r["nome"], r["preco_centavos"]), self.campo_qtd.get())
            self.atualizar_pedido()
            self.aviso.configure(text=f'{r["nome"]} adicionado ao pedido em memória.')
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Pedido", str(erro), parent=self.janela)

    def remover_item(self):
        sel = self.tabela_pedido.selection()
        if not sel: messagebox.showwarning("Pedido", "Selecione um item do pedido.", parent=self.janela); return
        try: self.pedido.remover(sel[0]); self.atualizar_pedido()
        except (ValueError, RuntimeError, KeyError) as erro: messagebox.showerror("Pedido", str(erro), parent=self.janela)

    def atualizar_pedido(self):
        for i in self.tabela_pedido.get_children(): self.tabela_pedido.delete(i)
        for l in self.pedido.linhas():
            self.tabela_pedido.insert("", "end", iid=l["codigo"], values=(l["codigo"],l["nome"],l["quantidade"],formatar(l["subtotal"])))
        self.lbl_total.configure(text=f"Total: {formatar(self.pedido.total_centavos())}")


def criar_janela(repositorio=None):
    janela = tk.Tk()
    AplicacaoA15(janela, repositorio)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

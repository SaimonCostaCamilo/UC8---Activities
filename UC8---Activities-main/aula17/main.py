"""A17 — Sorveteria integrada: cadastros persistentes e venda transacional."""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from modelos import Pedido, Produto, formatar
from repositorio import RepositorioSqlite
from controller import CadastroController
from relatorios import exportar_csv


class AplicacaoA17:
    def __init__(self, janela, repositorio=None):
        self.janela = janela
        janela.title("A17 — Sorveteria integrada")
        janela.geometry("1080x780")
        janela.minsize(850, 650)
        janela.columnconfigure(0, weight=1)
        janela.rowconfigure(0, weight=1)
        caminho = Path(__file__).resolve().parent / "dados" / "sorveteria.db"
        self.repo = repositorio or RepositorioSqlite(caminho)
        self.repo.iniciar()
        self.controller = CadastroController(self.repo)
        self.pedido = Pedido()  # montagem nunca é persistida antes da confirmação
        self.comprovante = None
        self.produtos_cache = []
        self.clientes_cache = []
        self.produto_edicao = None
        self.cliente_edicao = None
        self._montar()
        self.atualizar_produtos()
        self.atualizar_clientes()
        self.atualizar_pedido()
        self.atualizar_vendas()

    def _montar(self):
        base = ttk.Frame(self.janela, padding=12)
        base.grid(sticky="nsew")
        base.columnconfigure(0, weight=1)
        base.rowconfigure(1, weight=1)
        ttk.Label(base, text="SORVETERIA — Gestão de cadastros e vendas", font=("Segoe UI", 17, "bold")).grid(row=0, column=0, sticky="w")
        self.abas = ttk.Notebook(base)
        self.abas.grid(row=1, column=0, sticky="nsew", pady=10)
        self.tab_produtos = ttk.Frame(self.abas, padding=10)
        self.tab_clientes = ttk.Frame(self.abas, padding=10)
        self.tab_venda = ttk.Frame(self.abas, padding=10)
        self.tab_historico = ttk.Frame(self.abas, padding=10)
        self.abas.add(self.tab_venda, text="Nova venda")
        self.abas.add(self.tab_produtos, text="Produtos / sabores")
        self.abas.add(self.tab_clientes, text="Clientes")
        self.abas.add(self.tab_historico, text="Vendas confirmadas")
        self._montar_venda()
        self._montar_produtos()
        self._montar_clientes()
        self._montar_historico()
        self.aviso = ttk.Label(base, text="Pronto. Cadastros e vendas confirmadas ficam no SQLite; montagem fica na memória.", wraplength=1000)
        self.aviso.grid(row=2, column=0, sticky="w", pady=(8, 0))

    def _montar_produtos(self):
        f = self.tab_produtos
        f.columnconfigure(1, weight=1); f.rowconfigure(2, weight=1)
        ttk.Label(f, text="Nome do produto / sabor:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.campo_nome = ttk.Entry(f); self.campo_nome.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(f, text="Preço (ex.: 6,50):").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.campo_preco = ttk.Entry(f); self.campo_preco.grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        a = ttk.Frame(f); a.grid(row=1, column=2, sticky="e")
        ttk.Button(a, text="Novo", command=self.novo_produto).pack(side="left", padx=2)
        ttk.Button(a, text="Salvar", command=self.salvar_produto).pack(side="left", padx=2)
        ttk.Button(a, text="Excluir", command=self.excluir_produto).pack(side="left", padx=2)
        self.tabela_produtos = ttk.Treeview(f, columns=("id", "nome", "preco"), show="headings", selectmode="browse")
        for c, t, w in (("id", "ID", 70), ("nome", "Produto / sabor", 520), ("preco", "Preço", 140)):
            self.tabela_produtos.heading(c, text=t); self.tabela_produtos.column(c, width=w, anchor="center" if c != "nome" else "w")
        self.tabela_produtos.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=8)
        self.tabela_produtos.bind("<<TreeviewSelect>>", self._selecionou_produto)
        ttk.Label(f, text="A exclusão de produto já utilizado em venda é bloqueada pelo vínculo do banco.").grid(row=3, column=0, columnspan=3, sticky="w")

    def _montar_clientes(self):
        f = self.tab_clientes
        f.columnconfigure(1, weight=1); f.rowconfigure(2, weight=1)
        ttk.Label(f, text="Nome do cliente:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.campo_cliente = ttk.Entry(f); self.campo_cliente.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        a = ttk.Frame(f); a.grid(row=0, column=2, sticky="e")
        ttk.Button(a, text="Novo", command=self.novo_cliente).pack(side="left", padx=2)
        ttk.Button(a, text="Salvar", command=self.salvar_cliente).pack(side="left", padx=2)
        ttk.Button(a, text="Excluir", command=self.excluir_cliente).pack(side="left", padx=2)
        self.tabela_clientes = ttk.Treeview(f, columns=("id", "nome"), show="headings", selectmode="browse")
        self.tabela_clientes.heading("id", text="ID"); self.tabela_clientes.heading("nome", text="Cliente")
        self.tabela_clientes.column("id", width=80, anchor="center"); self.tabela_clientes.column("nome", width=600)
        self.tabela_clientes.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=8)
        self.tabela_clientes.bind("<<TreeviewSelect>>", self._selecionou_cliente)
        ttk.Label(f, text="Clientes vinculados a vendas não podem ser excluídos.").grid(row=3, column=0, columnspan=3, sticky="w")

    def _montar_venda(self):
        f = self.tab_venda
        f.columnconfigure(0, weight=1); f.columnconfigure(1, weight=1); f.rowconfigure(2, weight=1)
        ttk.Label(f, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.combo_cliente = ttk.Combobox(f, state="readonly", width=45)
        self.combo_cliente.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=4)
        ttk.Button(f, text="Atualizar clientes", command=self.atualizar_clientes).grid(row=1, column=1, sticky="w", pady=4)
        ttk.Label(f, text="Catálogo atual (selecione um produto):").grid(row=2, column=0, sticky="nw", pady=(8, 2))
        ttk.Label(f, text="Montagem do pedido — permanece em memória até a confirmação:").grid(row=2, column=1, sticky="nw", pady=(8, 2))
        self.lista_catalogo = ttk.Treeview(f, columns=("id", "nome", "preco"), show="headings", height=9, selectmode="browse")
        for c, t, w in (("id", "ID", 55), ("nome", "Produto", 230), ("preco", "Preço", 90)):
            self.lista_catalogo.heading(c, text=t); self.lista_catalogo.column(c, width=w, anchor="center" if c != "nome" else "w")
        self.lista_catalogo.grid(row=3, column=0, sticky="nsew", padx=(0, 8))
        lado = ttk.Frame(f); lado.grid(row=3, column=1, sticky="nsew")
        lado.columnconfigure(0, weight=1); lado.rowconfigure(0, weight=1)
        self.tabela_pedido = ttk.Treeview(lado, columns=("id", "nome", "qtd", "subtotal"), show="headings", height=9, selectmode="browse")
        for c, t, w in (("id", "ID", 50), ("nome", "Produto", 200), ("qtd", "Qtd.", 55), ("subtotal", "Subtotal", 100)):
            self.tabela_pedido.heading(c, text=t); self.tabela_pedido.column(c, width=w, anchor="center" if c != "nome" else "w")
        self.tabela_pedido.grid(row=0, column=0, columnspan=4, sticky="nsew")
        ttk.Label(lado, text="Quantidade:").grid(row=1, column=0, sticky="w", pady=6)
        self.campo_qtd = ttk.Entry(lado, width=7); self.campo_qtd.insert(0, "1"); self.campo_qtd.grid(row=1, column=1, sticky="w", padx=4)
        ttk.Button(lado, text="Adicionar", command=self.adicionar_pedido).grid(row=1, column=2, padx=3)
        ttk.Button(lado, text="Remover", command=self.remover_item).grid(row=1, column=3, padx=3)
        ttk.Button(lado, text="Revisar preços do carrinho", command=self.revisar_pedido).grid(row=2, column=0, columnspan=2, sticky="w", pady=4)
        self.lbl_total = ttk.Label(lado, text="Subtotal: R$ 0,00", font=("Segoe UI", 11, "bold"))
        self.lbl_total.grid(row=2, column=2, columnspan=2, sticky="e")
        ttk.Label(f, text="Pagamento:").grid(row=4, column=0, sticky="w", pady=(10, 2))
        self.combo_pagamento = ttk.Combobox(f, state="readonly", values=("Dinheiro", "PIX", "Débito", "Crédito 1x"), width=18)
        self.combo_pagamento.set("PIX"); self.combo_pagamento.grid(row=5, column=0, sticky="w")
        a = ttk.Frame(f); a.grid(row=5, column=1, sticky="e")
        ttk.Button(a, text="Atualizar catálogo", command=self.atualizar_produtos).pack(side="left", padx=3)
        ttk.Button(a, text="Prévia", command=self.mostrar_previa).pack(side="left", padx=3)
        ttk.Button(a, text="Confirmar e gravar venda", command=self.finalizar_venda).pack(side="left", padx=3)
        ttk.Button(a, text="Novo pedido", command=self.novo_pedido).pack(side="left", padx=3)
        ttk.Button(f, text="Exportar comprovante CSV", command=self.exportar_comprovante).grid(row=6, column=1, sticky="e", pady=8)

    def _montar_historico(self):
        f = self.tab_historico; f.columnconfigure(0, weight=1); f.rowconfigure(1, weight=1)
        ttk.Label(f, text="Vendas confirmadas e recuperadas do banco SQLite:").grid(row=0, column=0, sticky="w")
        self.tabela_vendas = ttk.Treeview(f, columns=("id", "data", "cliente", "forma", "subtotal", "total"), show="headings")
        for c, t, w in (("id", "Venda", 65), ("data", "Data/hora", 160), ("cliente", "Cliente", 220), ("forma", "Pagamento", 130), ("subtotal", "Subtotal", 120), ("total", "Total pago", 120)):
            self.tabela_vendas.heading(c, text=t); self.tabela_vendas.column(c, width=w, anchor="center" if c != "cliente" else "w")
        self.tabela_vendas.grid(row=1, column=0, sticky="nsew", pady=8)
        ttk.Button(f, text="Recarregar histórico", command=self.atualizar_vendas).grid(row=2, column=0, sticky="e")

    def _erro(self, titulo, erro):
        messagebox.showerror(titulo, str(erro), parent=self.janela)
        self.aviso.configure(text=f"Falha: {erro}. A montagem/campos foram preservados para correção.")

    def _selecionou_produto(self, _=None):
        sel = self.tabela_produtos.selection()
        if not sel: return
        r = next((p for p in self.produtos_cache if str(p["id"]) == sel[0]), None)
        if r:
            self.produto_edicao = r["id"]
            self.campo_nome.delete(0, tk.END); self.campo_nome.insert(0, r["nome"])
            self.campo_preco.delete(0, tk.END); self.campo_preco.insert(0, f'{r["preco_centavos"]//100},{r["preco_centavos"]%100:02d}')

    def _selecionou_cliente(self, _=None):
        sel = self.tabela_clientes.selection()
        if not sel: return
        r = next((c for c in self.clientes_cache if str(c["id"]) == sel[0]), None)
        if r:
            self.cliente_edicao = r["id"]
            self.campo_cliente.delete(0, tk.END); self.campo_cliente.insert(0, r["nome"])

    def novo_produto(self):
        self.produto_edicao = None; self.tabela_produtos.selection_remove(self.tabela_produtos.selection())
        self.campo_nome.delete(0, tk.END); self.campo_preco.delete(0, tk.END); self.campo_nome.focus_set()

    def salvar_produto(self):
        try:
            r = self.controller.salvar("produto", self.campo_nome.get(), self.campo_preco.get(), self.produto_edicao)
            self.atualizar_produtos(); self.novo_produto()
            self.aviso.configure(text=f'Produto #{r["id"]} salvo. Atualize/revise o carrinho se ele já estiver em montagem.')
        except (ValueError, sqlite3.Error, OSError) as e: self._erro("Produto", e)

    def excluir_produto(self):
        if self.produto_edicao is None: messagebox.showwarning("Produto", "Selecione um produto.", parent=self.janela); return
        if not messagebox.askyesno("Excluir", "Confirma a exclusão deste produto?", parent=self.janela): return
        try:
            if not self.controller.excluir("produto", self.produto_edicao, True): raise ValueError("Produto não encontrado.")
            self.atualizar_produtos(); self.novo_produto()
        except (ValueError, sqlite3.Error, OSError) as e: self._erro("Exclusão bloqueada", e)

    def atualizar_produtos(self):
        self.produtos_cache = self.controller.listar("produto")
        for tabela in (getattr(self, "tabela_produtos", None), getattr(self, "lista_catalogo", None)):
            if tabela is None: continue
            for i in tabela.get_children(): tabela.delete(i)
            for p in self.produtos_cache:
                tabela.insert("", "end", iid=str(p["id"]), values=(p["id"], p["nome"], formatar(p["preco_centavos"])))
        if hasattr(self, "aviso"): self.aviso.configure(text="Catálogo recarregado do banco. Confira os itens que já estavam na montagem.")

    def novo_cliente(self):
        self.cliente_edicao = None; self.tabela_clientes.selection_remove(self.tabela_clientes.selection())
        self.campo_cliente.delete(0, tk.END); self.campo_cliente.focus_set()

    def salvar_cliente(self):
        try:
            r = self.controller.salvar("cliente", self.campo_cliente.get(), codigo=self.cliente_edicao)
            self.atualizar_clientes(); self.novo_cliente(); self.aviso.configure(text=f'Cliente #{r["id"]} salvo.')
        except (ValueError, sqlite3.Error, OSError) as e: self._erro("Cliente", e)

    def excluir_cliente(self):
        if self.cliente_edicao is None: messagebox.showwarning("Cliente", "Selecione um cliente.", parent=self.janela); return
        if not messagebox.askyesno("Excluir", "Confirma a exclusão deste cliente?", parent=self.janela): return
        try:
            if not self.controller.excluir("cliente", self.cliente_edicao, True): raise ValueError("Cliente não encontrado.")
            self.atualizar_clientes(); self.novo_cliente()
        except (ValueError, sqlite3.Error, OSError) as e: self._erro("Exclusão bloqueada", e)

    def atualizar_clientes(self):
        self.clientes_cache = self.controller.listar("cliente")
        if hasattr(self, "tabela_clientes"):
            for i in self.tabela_clientes.get_children(): self.tabela_clientes.delete(i)
            for c in self.clientes_cache: self.tabela_clientes.insert("", "end", iid=str(c["id"]), values=(c["id"], c["nome"]))
        if hasattr(self, "combo_cliente"):
            self.combo_cliente["values"] = [f'{c["id"]} — {c["nome"]}' for c in self.clientes_cache]
            if self.combo_cliente.get() not in self.combo_cliente["values"]: self.combo_cliente.set("")

    def adicionar_pedido(self):
        sel = self.lista_catalogo.selection()
        if not sel: messagebox.showwarning("Pedido", "Selecione um produto do catálogo.", parent=self.janela); return
        p = next((x for x in self.produtos_cache if str(x["id"]) == sel[0]), None)
        if not p: self.atualizar_produtos(); return
        try:
            self.pedido.adicionar(Produto(str(p["id"]), p["nome"], p["preco_centavos"]), self.campo_qtd.get())
            self.atualizar_pedido(); self.aviso.configure(text=f'{p["nome"]} adicionado à montagem em memória.')
        except (ValueError, RuntimeError) as e: self._erro("Pedido", e)

    def remover_item(self):
        sel = self.tabela_pedido.selection()
        if not sel: messagebox.showwarning("Pedido", "Selecione um item.", parent=self.janela); return
        try: self.pedido.remover(sel[0]); self.atualizar_pedido()
        except (ValueError, RuntimeError, KeyError) as e: self._erro("Pedido", e)

    def revisar_pedido(self):
        catalogo = {str(p["id"]): p for p in self.controller.listar("produto")}
        ausentes, alterados = [], []
        for linha in self.pedido.linhas():
            atual = catalogo.get(str(linha["codigo"]))
            if atual is None: ausentes.append(linha["codigo"]); continue
            if atual["nome"] != linha["nome"] or atual["preco_centavos"] != linha["preco_unitario"]:
                self.pedido.substituir_produto(Produto(str(atual["id"]), atual["nome"], atual["preco_centavos"]))
                alterados.append(atual["nome"])
        self.atualizar_produtos(); self.atualizar_pedido()
        if ausentes:
            self.aviso.configure(text=f"Produtos removidos do catálogo: {ausentes}. Remova-os da montagem antes de confirmar. Itens restantes foram revisados.")
        elif alterados:
            self.aviso.configure(text=f"Itens atualizados com os dados atuais: {', '.join(alterados)}. Confira o novo subtotal antes de confirmar.")
        else: self.aviso.configure(text="Montagem conferida: nomes e preços correspondem ao catálogo atual.")

    def atualizar_pedido(self):
        for i in self.tabela_pedido.get_children(): self.tabela_pedido.delete(i)
        for l in self.pedido.linhas(): self.tabela_pedido.insert("", "end", iid=str(l["codigo"]), values=(l["codigo"], l["nome"], l["quantidade"], formatar(l["subtotal"])))
        self.lbl_total.configure(text=f"Subtotal: {formatar(self.pedido.total_centavos())}")

    def mostrar_previa(self):
        if not self.pedido.linhas(): messagebox.showwarning("Prévia", "Adicione itens antes de abrir a prévia.", parent=self.janela); return
        from pagamento import calcular_pagamento
        forma = self.combo_pagamento.get()
        valor = self.pedido.total_centavos()
        previa = calcular_pagamento(f"{valor//100},{valor%100:02d}", forma)
        self.versao_previa = self.pedido.versao
        messagebox.showinfo("Prévia da venda", f"Itens: {len(self.pedido.linhas())}\nSubtotal: {formatar(valor)}\nPagamento: {forma}\nTotal: {formatar(int(previa['total'] * 100))}\n\nA prévia vale para a montagem atual.", parent=self.janela)

    def finalizar_venda(self):
        cliente_txt = self.combo_cliente.get().strip()
        if not cliente_txt:
            messagebox.showwarning("Venda", "Selecione um cliente cadastrado antes de confirmar.", parent=self.janela); return
        cliente_id = int(cliente_txt.split(" — ", 1)[0])
        forma = self.combo_pagamento.get()
        versao = getattr(self, "versao_previa", None)
        if versao != self.pedido.versao:
            messagebox.showwarning("Prévia desatualizada", "Abra uma nova prévia e confira a montagem antes de confirmar.", parent=self.janela); return
        if not messagebox.askyesno("Confirmar venda", "Gravar a venda e todos os itens no banco? A montagem só será encerrada após sucesso.", parent=self.janela): return
        try:
            comprovante = self.controller.registrar_venda(cliente_id, self.pedido, forma, True, versao)
            self.comprovante = comprovante
            self.atualizar_vendas()
            self.aviso.configure(text=f'Venda #{comprovante["venda_id"]} gravada com todos os itens. Total pago: {formatar(comprovante["total_pagamento_centavos"])}.')
            messagebox.showinfo("Venda confirmada", f'Venda #{comprovante["venda_id"]} registrada.\nCliente: {comprovante["cliente_nome"]}\nSubtotal: {formatar(comprovante["total_centavos"])}\nTotal pago: {formatar(comprovante["total_pagamento_centavos"])}', parent=self.janela)
        except (ValueError, RuntimeError, sqlite3.Error, OSError) as e: self._erro("Venda não gravada", e)

    def novo_pedido(self):
        if self.pedido.estado == "montagem" and self.pedido.linhas():
            if not messagebox.askyesno("Novo pedido", "Descartar a montagem atual que ainda não foi confirmada?", parent=self.janela): return
        self.pedido.novo(); self.versao_previa = None; self.atualizar_pedido(); self.aviso.configure(text="Nova montagem em memória iniciada.")

    def exportar_comprovante(self):
        if not self.comprovante: messagebox.showwarning("CSV", "Não há comprovante confirmado nesta sessão.", parent=self.janela); return
        caminho = filedialog.asksaveasfilename(parent=self.janela, defaultextension=".csv", filetypes=(("CSV", "*.csv"),), initialfile=f'venda-{self.comprovante["venda_id"]}.csv')
        if not caminho: return
        try:
            exportar_csv(self.comprovante, caminho)
            self.aviso.configure(text=f"Comprovante exportado: {caminho}")
            messagebox.showinfo("CSV", "Comprovante confirmado exportado com sucesso.", parent=self.janela)
        except (ValueError, OSError) as e: self._erro("Exportação CSV", e)

    def atualizar_vendas(self):
        if not hasattr(self, "tabela_vendas"): return
        for i in self.tabela_vendas.get_children(): self.tabela_vendas.delete(i)
        for v in self.controller.listar("venda"):
            self.tabela_vendas.insert("", "end", iid=str(v["id"]), values=(v["id"], v["data_hora"], v["cliente_nome"], v["forma_pagamento"], formatar(v["subtotal_centavos"]), formatar(v["total_pagamento_centavos"])))


def criar_janela(repositorio=None):
    janela = tk.Tk(); AplicacaoA17(janela, repositorio); return janela

if __name__ == "__main__":
    criar_janela().mainloop()

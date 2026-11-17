# A13 — Pizzaria: comprovante CSV e simulação de perfis
import copy
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from decimal import Decimal

from modelos import Pedido, Produto, formatar
from pagamento import calcular_pagamento, FATORES
from relatorios import exportar_csv
from perfis import SessaoDemo


class AplicacaoVendas:
    def __init__(self, janela, catalogo=None, nome_aplicacao="Mercado"):
        self.janela = janela
        self.nome_aplicacao = nome_aplicacao
        self.janela.title(f"A13 — {nome_aplicacao}: Relatórios e Perfis")
        self.janela.geometry("980x700")
        self.janela.minsize(780, 580)
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)

        self.pedido = Pedido()
        self.sessao = SessaoDemo()
        self.comprovante_exportacao = None

        self.produtos_catalogo = catalogo or [
            Produto("M01", "Arroz 5 kg", 2890),
            Produto("M02", "Feijão 1 kg", 890),
            Produto("M03", "Leite integral 1 L", 549),
            Produto("M04", "Óleo de soja 900 ml", 699),
            Produto("M05", "Açúcar 1 kg", 479),
        ]
        self._criar_menu()
        self._criar_interface()

    def _criar_menu(self):
        barra = tk.Menu(self.janela)
        menu_sessao = tk.Menu(barra, tearoff=False)
        menu_sessao.add_command(label="Entrar na simulação", command=self.acao_entrar)
        menu_sessao.add_command(label="Sair do perfil", command=self.acao_sair)
        menu_sessao.add_separator()
        menu_sessao.add_command(label="Configurações (Administração)", command=self.abrir_configuracoes, state="disabled")
        self.menu_configuracoes = menu_sessao
        barra.add_cascade(label="Perfil demonstrativo", menu=menu_sessao)
        barra.add_command(label="Sair do programa", command=self.janela.destroy)
        self.janela.config(menu=barra)

    def _criar_interface(self):
        base = ttk.Frame(self.janela, padding=12)
        base.grid(row=0, column=0, sticky="nsew")
        base.columnconfigure(0, weight=1)
        base.rowconfigure(2, weight=1)

        ttk.Label(
            base,
            text=f"{self.nome_aplicacao} — venda, comprovante CSV e perfis",
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        perfil = ttk.LabelFrame(base, text="Simulação de identificação e perfil (não é autenticação real)", padding=9)
        perfil.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        perfil.columnconfigure(1, weight=1)
        ttk.Label(perfil, text="Nome fictício:").grid(row=0, column=0, padx=4, sticky="w")
        self.entry_nome = ttk.Entry(perfil, width=22)
        self.entry_nome.grid(row=0, column=1, padx=4, sticky="ew")
        ttk.Label(perfil, text="Perfil:").grid(row=0, column=2, padx=4, sticky="w")
        self.combo_perfil = ttk.Combobox(
            perfil, values=list(SessaoDemo.PERFIS_VALIDOS), state="readonly", width=18
        )
        self.combo_perfil.grid(row=0, column=3, padx=4)
        self.combo_perfil.current(0)
        ttk.Button(perfil, text="Entrar", command=self.acao_entrar).grid(row=0, column=4, padx=4)
        ttk.Button(perfil, text="Sair", command=self.acao_sair).grid(row=0, column=5, padx=4)
        self.lbl_sessao = ttk.Label(perfil, text="Nenhuma sessão demonstrativa ativa.")
        self.lbl_sessao.grid(row=1, column=0, columnspan=6, sticky="w", padx=4, pady=(7, 0))

        venda = ttk.LabelFrame(base, text="Montagem e finalização da venda", padding=10)
        venda.grid(row=2, column=0, sticky="nsew")
        venda.columnconfigure(0, weight=1)
        venda.rowconfigure(2, weight=1)

        controles = ttk.Frame(venda)
        controles.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        controles.columnconfigure(1, weight=1)
        ttk.Label(controles, text="Produto:").grid(row=0, column=0, padx=4)
        self.combo_produtos = ttk.Combobox(
            controles,
            values=[f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in self.produtos_catalogo],
            state="readonly",
        )
        self.combo_produtos.grid(row=0, column=1, sticky="ew", padx=4)
        if self.produtos_catalogo:
            self.combo_produtos.current(0)
        ttk.Label(controles, text="Qtd:").grid(row=0, column=2, padx=4)
        self.entry_qtd = ttk.Entry(controles, width=7)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.grid(row=0, column=3, padx=4)
        ttk.Button(controles, text="Adicionar", command=self.acao_adicionar).grid(row=0, column=4, padx=4)

        colunas = ("codigo", "nome", "preco", "quantidade", "subtotal")
        self.tree = ttk.Treeview(venda, columns=colunas, show="headings", selectmode="browse", height=9)
        titulos = {
            "codigo": "ID", "nome": "Produto", "preco": "Preço unit.",
            "quantidade": "Qtd.", "subtotal": "Subtotal",
        }
        larguras = {"codigo": 80, "nome": 360, "preco": 130, "quantidade": 80, "subtotal": 140}
        for coluna in colunas:
            self.tree.heading(coluna, text=titulos[coluna])
            self.tree.column(coluna, width=larguras[coluna], anchor="w" if coluna == "nome" else "center")
        self.tree.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(venda, orient="vertical", command=self.tree.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        acoes = ttk.Frame(venda)
        acoes.grid(row=3, column=0, sticky="ew", pady=8)
        ttk.Button(acoes, text="Atualizar quantidade", command=self.acao_atualizar).pack(side="left", padx=3)
        ttk.Button(acoes, text="Remover selecionado", command=self.acao_remover).pack(side="left", padx=3)
        ttk.Label(acoes, text="Pagamento:").pack(side="left", padx=(12, 3))
        self.combo_pagamento = ttk.Combobox(acoes, values=list(FATORES.keys()), state="readonly", width=15)
        self.combo_pagamento.pack(side="left", padx=3)
        self.combo_pagamento.current(0)
        ttk.Button(acoes, text="Prévia e confirmar", command=self.acao_previa).pack(side="left", padx=3)
        ttk.Button(acoes, text="Novo pedido", command=self.acao_novo).pack(side="left", padx=3)

        exportar = ttk.LabelFrame(venda, text="Comprovante confirmado", padding=8)
        exportar.grid(row=4, column=0, sticky="ew", pady=(2, 0))
        exportar.columnconfigure(0, weight=1)
        self.lbl_comprovante = ttk.Label(
            exportar,
            text="Nenhum comprovante confirmado nesta sessão.",
            wraplength=760,
        )
        self.lbl_comprovante.grid(row=0, column=0, sticky="w")
        ttk.Button(exportar, text="Exportar comprovante CSV...", command=self.acao_exportar).grid(row=0, column=1, padx=6)

        self.aviso = ttk.Label(base, text="Pronto para iniciar uma venda fictícia.", wraplength=900)
        self.aviso.grid(row=3, column=0, sticky="w", pady=(8, 0))
        self.atualizar_interface()

    def atualizar_interface(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for linha in self.pedido.linhas():
            self.tree.insert(
                "", "end", iid=linha["codigo"],
                values=(
                    linha["codigo"], linha["nome"], formatar(linha["preco_unitario"]),
                    linha["quantidade"], formatar(linha["subtotal"]),
                ),
            )
        self.aviso.configure(
            text=f"Estado: {self.pedido.estado.upper()} | Versão da montagem: {self.pedido.versao} | "
                 f"Total dos itens: {formatar(self.pedido.total_centavos())}"
        )

    def acao_entrar(self):
        try:
            dados = self.sessao.entrar(self.entry_nome.get(), self.combo_perfil.get())
            permitido = self.sessao.pode_configurar()
            self.menu_configuracoes.entryconfigure(
                "Configurações (Administração)", state="normal" if permitido else "disabled"
            )
            self.lbl_sessao.configure(
                text=f"Sessão demonstrativa: {dados['nome']} | Perfil: {dados['perfil']} | "
                     f"Pode configurar: {'Sim' if permitido else 'Não'}"
            )
            self.aviso.configure(text="Perfil selecionado para comparação local. Não houve autenticação real.")
        except ValueError as erro:
            messagebox.showerror("Perfil demonstrativo", str(erro), parent=self.janela)

    def acao_sair(self):
        self.sessao.sair()
        self.menu_configuracoes.entryconfigure("Configurações (Administração)", state="disabled")
        self.lbl_sessao.configure(text="Sessão demonstrativa encerrada. Vendas e relatórios foram preservados.")
        self.aviso.configure(text="Saiu do perfil demonstrativo; nenhum pedido ou arquivo foi apagado.")

    def abrir_configuracoes(self):
        # A autorização é conferida na operação, não apenas na visibilidade do menu.
        if not self.sessao.pode_configurar():
            messagebox.showerror(
                "Acesso demonstrativo", "O perfil atual não pode configurar.", parent=self.janela
            )
            return
        messagebox.showinfo(
            "Configurações", "Ação demonstrativa disponível para Administração.", parent=self.janela
        )

    def _produto_selecionado(self):
        indice = self.combo_produtos.current()
        if indice < 0 or indice >= len(self.produtos_catalogo):
            raise ValueError("Selecione um produto válido.")
        return self.produtos_catalogo[indice]

    def acao_adicionar(self):
        try:
            produto = self._produto_selecionado()
            self.pedido.adicionar(produto, self.entry_qtd.get())
            self.atualizar_interface()
            self.aviso.configure(text=f"Adicionado: {produto.nome}")
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Não foi possível adicionar", str(erro), parent=self.janela)

    def acao_atualizar(self):
        try:
            selecionados = self.tree.selection()
            if not selecionados:
                raise ValueError("Selecione uma linha para atualizar.")
            codigo = selecionados[0]
            self.pedido.atualizar(codigo, self.entry_qtd.get())
            self.atualizar_interface()
            self.aviso.configure(text=f"Quantidade atualizada para {codigo}.")
        except (ValueError, RuntimeError, KeyError) as erro:
            messagebox.showerror("Não foi possível atualizar", str(erro), parent=self.janela)

    def acao_remover(self):
        try:
            selecionados = self.tree.selection()
            if not selecionados:
                raise ValueError("Selecione uma linha para remover.")
            codigo = selecionados[0]
            self.pedido.remover(codigo)
            self.atualizar_interface()
            self.aviso.configure(text=f"Item {codigo} removido. A seleção visual foi atualizada.")
        except (ValueError, RuntimeError, KeyError) as erro:
            messagebox.showerror("Não foi possível remover", str(erro), parent=self.janela)

    def acao_previa(self):
        try:
            if not self.pedido.linhas():
                raise ValueError("Não é possível finalizar uma venda vazia.")
            forma = self.combo_pagamento.get()
            total_itens = self.pedido.total_centavos()
            calculo = calcular_pagamento(str(Decimal(total_itens) / Decimal(100)), forma)
            versao = self.pedido.versao

            previa = tk.Toplevel(self.janela)
            previa.title("Prévia da venda")
            previa.geometry("410x300")
            previa.transient(self.janela)
            previa.grab_set()
            frame = ttk.Frame(previa, padding=16)
            frame.pack(fill="both", expand=True)
            ttk.Label(frame, text="Conferência antes da confirmação", font=("Segoe UI", 11, "bold")).pack(anchor="w")
            ttk.Label(
                frame,
                text=f"Total dos itens: {formatar(total_itens)}\n"
                     f"Forma: {forma}\n"
                     f"Total calculado: R$ {calculo['total']:.2f}\n\n"
                     "Deseja confirmar esta venda?",
                font=("Consolas", 10),
            ).pack(anchor="w", pady=14)
            botoes = ttk.Frame(frame)
            botoes.pack(fill="x", pady=10)

            def cancelar():
                previa.destroy()
                self.aviso.configure(text="Prévia cancelada; a montagem continua intacta.")

            def confirmar():
                try:
                    comprovante = self.pedido.finalizar(
                        forma=forma, confirmado=True, versao_previa=versao
                    )
                    # O total efetivamente calculado fica no retrato exportável.
                    comprovante["total_pagamento_centavos"] = int(
                        (calculo["total"] * Decimal(100)).quantize(Decimal("1"))
                    )
                    self.comprovante_exportacao = copy.deepcopy(comprovante)
                    previa.destroy()
                    self.atualizar_interface()
                    self.lbl_comprovante.configure(
                        text=f"Comprovante confirmado: {len(comprovante['itens'])} item(ns) | "
                             f"Forma: {forma} | Total: R$ {calculo['total']:.2f}. "
                             "Este retrato permanece disponível mesmo ao iniciar outra montagem."
                    )
                    self.aviso.configure(text="Venda confirmada. O comprovante está pronto para exportação.")
                except (ValueError, RuntimeError) as erro:
                    previa.destroy()
                    messagebox.showerror("Falha na confirmação", str(erro), parent=self.janela)
                    self.atualizar_interface()

            btn_cancelar = ttk.Button(botoes, text="Cancelar", command=cancelar)
            btn_cancelar.pack(side="right", padx=4)
            ttk.Button(botoes, text="Confirmar", command=confirmar).pack(side="right", padx=4)
            previa.protocol("WM_DELETE_WINDOW", cancelar)
            previa.bind("<Escape>", lambda evento: cancelar())
            btn_cancelar.focus_set()
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Prévia", str(erro), parent=self.janela)

    def acao_novo(self):
        try:
            if self.pedido.estado == "montagem" and self.pedido.linhas():
                if not messagebox.askyesno(
                    "Novo pedido", "Há uma montagem em andamento. Deseja descartá-la?", parent=self.janela
                ):
                    return
            self.pedido.novo()
            # Não apaga self.comprovante_exportacao: é um retrato já confirmado.
            self.atualizar_interface()
            self.aviso.configure(text="Nova montagem iniciada. O último comprovante confirmado foi preservado.")
        except RuntimeError as erro:
            messagebox.showerror("Novo pedido", str(erro), parent=self.janela)

    def acao_exportar(self):
        if self.comprovante_exportacao is None:
            messagebox.showwarning(
                "Sem comprovante", "Confirme uma venda antes de exportar. Nenhuma venda fictícia será criada.",
                parent=self.janela,
            )
            return
        caminho = filedialog.asksaveasfilename(
            parent=self.janela,
            title="Exportar comprovante CSV",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            self.aviso.configure(text="Exportação cancelada; pedido e arquivo permaneceram inalterados.")
            return
        try:
            destino = exportar_csv(self.comprovante_exportacao, caminho)
            messagebox.showinfo("Exportação concluída", f"Comprovante exportado:\n{destino}", parent=self.janela)
            self.aviso.configure(text=f"CSV exportado: {destino}")
        except (OSError, ValueError) as erro:
            messagebox.showerror("Falha na exportação", str(erro), parent=self.janela)
            self.aviso.configure(text="Falha ao exportar; comprovante e destino anterior foram preservados.")


def criar_janela(catalogo=None, nome_aplicacao="Mercado"):
    janela = tk.Tk()
    AplicacaoVendas(janela, catalogo=catalogo, nome_aplicacao=nome_aplicacao)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

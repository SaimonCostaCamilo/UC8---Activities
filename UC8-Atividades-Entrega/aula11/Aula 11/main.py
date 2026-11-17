# A11: Interface Principal — Pizzaria (Estados, Prévia, Cancelamento e Versão)
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal  # <--- ADICIONE ESTA LINHA AQUI
from modelos import Pedido, Pizza, Bebida, formatar
from pagamento import calcular_pagamento, FATORES

class AppPizzaria:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("A11 — Pizzaria (Estados, Confirmação e Versão)")
        self.janela.geometry("620x520")
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)

        # Inicializa o pedido e produtos fictícios de exemplo
        self.pedido = Pedido()
        self.produtos_catalogo = [
            Pizza("P01", "Pizza Calabresa Média", "Média", 4000),
            Pizza("P02", "Pizza Margherita Grande", "Grande", 5500),
            Bebida("B01", "Guaraná 2L", 1200),
            Bebida("B02", "Água Mineral 500ml", 500)
        ]

        self.criar_widgets()

    def criar_widgets(self):
        base = ttk.Frame(self.janela, padding=12)
        base.grid(row=0, column=0, sticky="nsew")
        base.columnconfigure(0, weight=1)
        base.rowconfigure(3, weight=1)

        # 1. Título e Instruções
        ttk.Label(base, text="Sistema de Pizzaria — Aula 11", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

        # 2. Frame de Ações de Montagem
        frame_montagem = ttk.LabelFrame(base, text=" 1. Montagem do Pedido ", padding=10)
        frame_montagem.grid(row=1, column=0, sticky="ew", pady=4)
        frame_montagem.columnconfigure(1, weight=1)

        ttk.Label(frame_montagem, text="Produto:").grid(row=0, column=0, sticky="w", padx=4)
        self.combo_produtos = ttk.Combobox(frame_montagem, values=[f"{p.codigo} - {p.nome} ({formatar(p.preco_centavos)})" for p in self.produtos_catalogo], state="readonly", width=38)
        self.combo_produtos.grid(row=0, column=1, sticky="ew", padx=4)
        if self.produtos_catalogo:
            self.combo_produtos.current(0)

        ttk.Label(frame_montagem, text="Qtd:").grid(row=0, column=2, sticky="w", padx=4)
        self.entry_qtd = ttk.Entry(frame_montagem, width=6)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.grid(row=0, column=3, padx=4)

        btn_adicionar = ttk.Button(frame_montagem, text="Adicionar", command=self.acao_adicionar)
        btn_adicionar.grid(row=0, column=4, padx=4)

        # 3. Listagem de Itens (Treeview)
        frame_lista = ttk.LabelFrame(base, text=" Itens no Carrinho ", padding=10)
        frame_lista.grid(row=2, column=0, sticky="nsew", pady=4)
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(frame_lista, columns=("cod", "nome", "preco", "qtd", "subtotal"), show="headings", height=6)
        self.tree.heading("cod", text="Cód")
        self.tree.heading("nome", text="Nome do Produto")
        self.tree.heading("preco", text="Preço Unit.")
        self.tree.heading("qtd", text="Qtd")
        self.tree.heading("subtotal", text="Subtotal")
        
        self.tree.column("cod", width=50, anchor="center")
        self.tree.column("nome", width=220, anchor="w")
        self.tree.column("preco", width=90, anchor="e")
        self.tree.column("qtd", width=50, anchor="center")
        self.tree.column("subtotal", width=90, anchor="e")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")

        # 4. Frame de Fechamento / Finalização
        frame_fechamento = ttk.LabelFrame(base, text=" 2. Pagamento e Finalização ", padding=10)
        frame_fechamento.grid(row=3, column=0, sticky="ew", pady=4)
        frame_fechamento.columnconfigure(1, weight=1)

        ttk.Label(frame_fechamento, text="Forma de Pagamento:").grid(row=0, column=0, sticky="w", padx=4)
        self.combo_pagamento = ttk.Combobox(frame_fechamento, values=list(FATORES.keys()), state="readonly", width=20)
        self.combo_pagamento.grid(row=0, column=1, sticky="w", padx=4)
        if FATORES:
            self.combo_pagamento.current(0)

        self.btn_finalizar = ttk.Button(frame_fechamento, text="Abrir Prévia e Finalizar", command=self.acao_abrir_previa)
        self.btn_finalizar.grid(row=0, column=2, padx=4)

        self.btn_novo = ttk.Button(frame_fechamento, text="Novo Pedido", command=self.acao_novo_pedido)
        self.btn_novo.grid(row=0, column=3, padx=4)

        # 5. Rótulo de Status e Mensagens
        self.aviso = ttk.Label(base, text="Pronto para montagem.", foreground="navy", wraplength=580)
        self.aviso.grid(row=4, column=0, sticky="w", pady=(8, 0))

        self.atualizar_interface()

    def atualizar_interface(self):
        """Atualiza a Treeview com os itens atuais do pedido e o estado."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for linha in self.pedido.linhas():
            self.tree.insert("", "end", values=(
                linha["codigo"],
                linha["nome"],
                formatar(linha["preco_unitario"]),
                linha["quantidade"],
                formatar(linha["subtotal"])
            ))

        total_geral = self.pedido.total_centavos()
        self.aviso.configure(text=f"Estado: [{self.pedido.estado.upper()}] | Versão da Montagem: {self.pedido.versao} | Total Atual: {formatar(total_geral)}")

    def acao_adicionar(self):
        try:
            if self.pedido.estado != "montagem":
                raise RuntimeError("O pedido já está finalizado. Inicie um novo pedido.")
            
            sel_idx = self.combo_produtos.current()
            if sel_idx < 0:
                raise ValueError("Selecione um produto válido.")
            
            produto = self.produtos_catalogo[sel_idx]
            texto_qtd = self.entry_qtd.get()
            
            self.pedido.adicionar(produto, texto_qtd)
            self.atualizar_interface()
            self.aviso.configure(text=f"Item {produto.nome} adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro na Adição", str(e))

    def acao_abrir_previa(self):
        """Abre a janela Toplevel de prévia e confirmação com foco em Cancelar."""
        try:
            if not self.pedido._itens:
                raise ValueError("Não é possível gerar prévia de um pedido vazio.")
            
            forma = self.combo_pagamento.get()
            subtotal = self.pedido.total_centavos()
            calculo = calcular_pagamento(str(Decimal(subtotal) / 100), forma)

            # Captura a versão da prévia no momento exato da abertura
            versao_da_previa = self.pedido.versao

            # Criação da janela Toplevel de prévia
            previa_janela = tk.Toplevel(self.janela)
            previa_janela.title("Prévia e Confirmação do Pedido")
            previa_janela.geometry("400x320")
            previa_janela.transient(self.janela)
            previa_janela.grab_set()

            frame_prev = ttk.Frame(previa_janela, padding=16)
            frame_prev.pack(fill="both", expand=True)

            ttk.Label(frame_prev, text="Resumo da Prévia do Pedido", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
            
            detalhes_txt = f"Itens: {len(self.pedido.linhas())}\n" \
                           f"Subtotal: {formatar(calculo['subtotal'] * 100)}\n" \
                           f"Forma: {forma} (Fator: {calculo['fator']})\n" \
                           f"Total Previsto: {formatar(calculo['total'] * 100)}"
            
            ttk.Label(frame_prev, text=detalhes_txt, font=("Consolas", 10)).pack(anchor="w", pady=8)
            ttk.Label(frame_prev, text="Deseja confirmar este pedido?", font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=8)

            btn_frame = ttk.Frame(frame_prev)
            btn_frame.pack(fill="x", pady=16)

            # Ação de Cancelar / Fechar (preserva montagem e itens)
            def cancelar_previa():
                previa_janela.destroy()
                self.aviso.configure(text="Prévia cancelada. A montagem foi preservada.")

            # Ação de Confirmar com validação de versão
            def confirmar_previa():
                try:
                    # Executa a finalização conferindo a versão guardada da prévia
                    self.pedido.finalizar(forma=forma, confirmado=True, versao_previa=versao_da_previa)
                    previa_janela.destroy()
                    self.atualizar_interface()
                    messagebox.showinfo("Sucesso", "Pedido finalizado com sucesso! Comprovante gerado.")
                except Exception as err:
                    previa_janela.destroy()
                    messagebox.showerror("Erro na Confirmação", str(err))
                    self.atualizar_interface()

            # Botões com foco inicial em Cancelar para evitar confirmação acidental por teclado
            btn_cancelar = ttk.Button(btn_frame, text="Cancelar", command=cancelar_previa)
            btn_cancelar.pack(side="right", padx=4)

            btn_confirmar = ttk.Button(btn_frame, text="Confirmar", command=confirmar_previa)
            btn_confirmar.pack(side="right", padx=4)

            # Associa X e Escape à mesma ação de cancelamento
            previa_janela.protocol("WM_DELETE_WINDOW", cancelar_previa)
            previa_janela.bind("<Escape>", lambda e: cancelar_previa())

            # Dando foco inicial ao botão Cancelar
            btn_cancelar.focus_set()

        except Exception as e:
            messagebox.showerror("Erro na Prévia", str(e))

    def acao_novo_pedido(self):
        try:
            # Se houver itens em montagem não finalizada, pede confirmação de descarte
            if self.pedido.estado == "montagem" and self.pedido._itens:
                if not messagebox.askyesno("Novo Pedido", "Há um pedido em montagem. Deseja realmente descartá-lo e iniciar um novo?"):
                    return
            self.pedido.novo()
            self.atualizar_interface()
            self.aviso.configure(text="Novo pedido iniciado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


def criar_janela():
    janela = tk.Tk()
    AppPizzaria(janela)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
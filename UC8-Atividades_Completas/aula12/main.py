# A12 — Mercado: fluxo de pedidos preservado + navegação e catálogo JSON
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from decimal import Decimal

from modelos import Pedido, Produto, formatar
from pagamento import calcular_pagamento, FATORES
from arquivos import ler_catalogo, salvar_catalogo, validar_catalogo


class AplicacaoA12:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Aula 12 — Sistema de Mercado")
        self.janela.geometry("900x650")
        self.janela.minsize(720, 520)
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)

        # Uma única instância do pedido é compartilhada durante a navegação.
        self.pedido = Pedido()
        self.produtos_catalogo = [
            Produto("M01", "Arroz 5 kg", 2890),
            Produto("M02", "Feijão 1 kg", 890),
            Produto("M03", "Leite integral 1 L", 549),
            Produto("M04", "Óleo de soja 900 ml", 699),
            Produto("M05", "Açúcar 1 kg", 479),
        ]
        self.caminho_json = None
        self._criar_menu()
        self._criar_abas()

    def _criar_menu(self):
        barra = tk.Menu(self.janela)
        menu_navegar = tk.Menu(barra, tearoff=False)
        menu_navegar.add_command(label="Pedido", command=lambda: self.notebook.select(self.aba_pedido))
        menu_navegar.add_command(label="Exercício JSON", command=lambda: self.notebook.select(self.aba_json))
        barra.add_cascade(label="Navegar", menu=menu_navegar)
        barra.add_command(label="Sair", command=self.janela.destroy)
        self.janela.config(menu=barra)

    def _criar_abas(self):
        base = ttk.Frame(self.janela, padding=12)
        base.grid(row=0, column=0, sticky="nsew")
        base.columnconfigure(0, weight=1)
        base.rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(base)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.aba_pedido = ttk.Frame(self.notebook, padding=12)
        self.aba_json = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.aba_pedido, text="Pedido")
        self.notebook.add(self.aba_json, text="Exercício JSON")
        self._montar_aba_pedido()
        self._montar_aba_json()

    # ------------------------- ABA PEDIDO (fluxo A11) -------------------------
    def _montar_aba_pedido(self):
        base = self.aba_pedido
        base.columnconfigure(0, weight=1)
        base.rowconfigure(2, weight=1)
        ttk.Label(base, text="Mercado • Produtos, carrinho e pagamento", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

        montagem = ttk.LabelFrame(base, text=" 1. Montagem do Pedido ", padding=10)
        montagem.grid(row=1, column=0, sticky="ew", pady=4)
        montagem.columnconfigure(1, weight=1)
        ttk.Label(montagem, text="Produto:").grid(row=0, column=0, sticky="w", padx=4)
        self.combo_produtos = ttk.Combobox(
            montagem,
            values=[f"{p.codigo} — {p.nome} ({formatar(p.preco_centavos)})" for p in self.produtos_catalogo],
            state="readonly",
        )
        self.combo_produtos.grid(row=0, column=1, sticky="ew", padx=4)
        self.combo_produtos.current(0)
        ttk.Label(montagem, text="Qtd:").grid(row=0, column=2, padx=4)
        self.entry_qtd = ttk.Entry(montagem, width=7)
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.grid(row=0, column=3, padx=4)
        ttk.Button(montagem, text="Adicionar", command=self.acao_adicionar).grid(row=0, column=4, padx=4)

        lista = ttk.LabelFrame(base, text="Itens no Carrinho", padding=8)
        lista.grid(row=2, column=0, sticky="nsew", pady=4)
        lista.columnconfigure(0, weight=1)
        lista.rowconfigure(0, weight=1)
        colunas = ("cod", "nome", "preco", "qtd", "subtotal")
        self.tree = ttk.Treeview(lista, columns=colunas, show="headings", height=7)
        titulos = {"cod": "Cód", "nome": "Nome do Produto", "preco": "Preço Unit.", "qtd": "Qtd", "subtotal": "Subtotal"}
        larguras = {"cod": 65, "nome": 280, "preco": 110, "qtd": 60, "subtotal": 110}
        for coluna in colunas:
            self.tree.heading(coluna, text=titulos[coluna])
            self.tree.column(coluna, width=larguras[coluna], anchor="w" if coluna == "nome" else "center")
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(lista, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        fechamento = ttk.LabelFrame(base, text=" 2. Pagamento e Finalização ", padding=10)
        fechamento.grid(row=3, column=0, sticky="ew", pady=4)
        fechamento.columnconfigure(1, weight=1)
        ttk.Label(fechamento, text="Forma de Pagamento:").grid(row=0, column=0, sticky="w", padx=4)
        self.combo_pagamento = ttk.Combobox(fechamento, values=list(FATORES.keys()), state="readonly", width=20)
        self.combo_pagamento.grid(row=0, column=1, sticky="w", padx=4)
        self.combo_pagamento.current(0)
        ttk.Button(fechamento, text="Abrir Prévia e Finalizar", command=self.acao_abrir_previa).grid(row=0, column=2, padx=4)
        ttk.Button(fechamento, text="Novo Pedido", command=self.acao_novo_pedido).grid(row=0, column=3, padx=4)
        self.aviso = ttk.Label(base, text="Pronto para montagem.", wraplength=820)
        self.aviso.grid(row=4, column=0, sticky="w", pady=(8, 0))
        self.atualizar_interface()

    def atualizar_interface(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for linha in self.pedido.linhas():
            self.tree.insert("", "end", values=(
                linha["codigo"], linha["nome"], formatar(linha["preco_unitario"]),
                linha["quantidade"], formatar(linha["subtotal"]),
            ))
        self.aviso.configure(
            text=f"Estado: [{self.pedido.estado.upper()}] | Versão: {self.pedido.versao} | Total atual: {formatar(self.pedido.total_centavos())}"
        )

    def acao_adicionar(self):
        try:
            if self.pedido.estado != "montagem":
                raise RuntimeError("O pedido já foi finalizado. Inicie um novo pedido.")
            indice = self.combo_produtos.current()
            if indice < 0:
                raise ValueError("Selecione um produto válido.")
            produto = self.produtos_catalogo[indice]
            self.pedido.adicionar(produto, self.entry_qtd.get())
            self.atualizar_interface()
            self.aviso.configure(text=f"Item {produto.nome} adicionado com sucesso!")
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Erro na Adição", str(erro), parent=self.janela)

    def acao_abrir_previa(self):
        try:
            if not self.pedido._itens:
                raise ValueError("Não é possível gerar prévia de um pedido vazio.")
            forma = self.combo_pagamento.get()
            subtotal_centavos = self.pedido.total_centavos()
            calculo = calcular_pagamento(str(Decimal(subtotal_centavos) / 100), forma)
            versao_da_previa = self.pedido.versao

            previa = tk.Toplevel(self.janela)
            previa.title("Prévia e Confirmação do Pedido")
            previa.geometry("420x330")
            previa.transient(self.janela)
            previa.grab_set()
            frame = ttk.Frame(previa, padding=16)
            frame.pack(fill="both", expand=True)
            ttk.Label(frame, text="Resumo da Prévia do Pedido", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
            detalhes = (
                f"Itens: {len(self.pedido.linhas())}\n"
                f"Subtotal: {formatar(int(calculo['subtotal'] * 100))}\n"
                f"Forma: {forma} (Fator: {calculo['fator']})\n"
                f"Total previsto: {formatar(int(calculo['total'] * 100))}"
            )
            ttk.Label(frame, text=detalhes, font=("Consolas", 10)).pack(anchor="w", pady=8)
            ttk.Label(frame, text="Deseja confirmar este pedido?", font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=8)
            botoes = ttk.Frame(frame)
            botoes.pack(fill="x", pady=16)

            def cancelar_previa():
                previa.destroy()
                self.aviso.configure(text="Prévia cancelada. A montagem foi preservada.")

            def confirmar_previa():
                try:
                    comprovante = self.pedido.finalizar(
                        forma=forma, confirmado=True, versao_previa=versao_da_previa
                    )
                    previa.destroy()
                    self.atualizar_interface()
                    messagebox.showinfo(
                        "Pedido finalizado",
                        "Pedido finalizado e comprovante gerado.\n"
                        f"Total dos itens: {formatar(comprovante['total_centavos'])}\n"
                        f"Forma selecionada: {comprovante['forma_pagamento']}\n"
                        f"Total calculado na prévia: {formatar(int(calculo['total'] * 100))}",
                        parent=self.janela,
                    )
                except (ValueError, RuntimeError) as erro:
                    previa.destroy()
                    messagebox.showerror("Erro na Confirmação", str(erro), parent=self.janela)
                    self.atualizar_interface()

            btn_cancelar = ttk.Button(botoes, text="Cancelar", command=cancelar_previa)
            btn_cancelar.pack(side="right", padx=4)
            ttk.Button(botoes, text="Confirmar", command=confirmar_previa).pack(side="right", padx=4)
            previa.protocol("WM_DELETE_WINDOW", cancelar_previa)
            previa.bind("<Escape>", lambda evento: cancelar_previa())
            btn_cancelar.focus_set()
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Erro na Prévia", str(erro), parent=self.janela)

    def acao_novo_pedido(self):
        try:
            if self.pedido.estado == "montagem" and self.pedido._itens:
                if not messagebox.askyesno("Novo Pedido", "Há um pedido em montagem. Deseja descartá-lo e iniciar outro?", parent=self.janela):
                    return
            self.pedido.novo()
            self.atualizar_interface()
            self.aviso.configure(text="Novo pedido iniciado com sucesso.")
        except (ValueError, RuntimeError) as erro:
            messagebox.showerror("Erro", str(erro), parent=self.janela)

    # --------------------------- ABA EXERCÍCIO JSON ---------------------------
    def _montar_aba_json(self):
        aba = self.aba_json
        aba.columnconfigure(0, weight=1)
        aba.rowconfigure(2, weight=1)
        ttk.Label(aba, text="Catálogo fictício em JSON", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Label(aba, text="Cada registro deve conter id, nome e preco_centavos (inteiro positivo em centavos).", wraplength=800).grid(row=1, column=0, sticky="w", pady=(0, 8))
        self.editor_json = tk.Text(aba, height=18, wrap="none", undo=True, font=("Consolas", 10))
        self.editor_json.grid(row=2, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(aba, orient="vertical", command=self.editor_json.yview)
        scroll.grid(row=2, column=1, sticky="ns")
        self.editor_json.configure(yscrollcommand=scroll.set)
        acoes = ttk.Frame(aba)
        acoes.grid(row=3, column=0, sticky="ew", pady=8)
        ttk.Button(acoes, text="Inserir exemplo", command=self.inserir_exemplo).pack(side="left", padx=3)
        ttk.Button(acoes, text="Carregar JSON...", command=self.acao_carregar).pack(side="left", padx=3)
        ttk.Button(acoes, text="Validar texto", command=self.acao_validar).pack(side="left", padx=3)
        ttk.Button(acoes, text="Salvar como...", command=self.acao_salvar).pack(side="left", padx=3)
        self.status_json = ttk.Label(aba, text="Nenhum arquivo carregado. O pedido é independente.", wraplength=800)
        self.status_json.grid(row=4, column=0, sticky="w")

    def inserir_exemplo(self):
        exemplo = [
            {"id": 1, "nome": "Picolé de limão", "preco_centavos": 450},
            {"id": 2, "nome": "Sorvete de chocolate", "preco_centavos": 1200},
            {"id": 3, "nome": "Açaí com morango", "preco_centavos": 1650},
        ]
        self.editor_json.delete("1.0", "end")
        self.editor_json.insert("1.0", json.dumps(exemplo, ensure_ascii=False, indent=4))
        self.status_json.configure(text="Exemplo fictício inserido no editor; nenhum arquivo foi criado.")

    def acao_carregar(self):
        caminho = filedialog.askopenfilename(
            parent=self.janela, title="Carregar catálogo JSON",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            dados = ler_catalogo(caminho)
            texto = json.dumps(dados, ensure_ascii=False, indent=4)
        except (OSError, ValueError) as erro:
            messagebox.showerror("Falha ao carregar", str(erro), parent=self.janela)
            self.status_json.configure(text="Falha na leitura; o texto atual do editor foi preservado.")
            return
        self.editor_json.delete("1.0", "end")
        self.editor_json.insert("1.0", texto)
        self.caminho_json = caminho
        self.status_json.configure(text=f"Catálogo válido carregado: {caminho}. O pedido não foi alterado.")

    def _obter_catalogo_editor(self):
        try:
            dados = json.loads(self.editor_json.get("1.0", "end-1c"))
        except json.JSONDecodeError as erro:
            raise ValueError(f"JSON inválido na linha {erro.lineno}, coluna {erro.colno}.") from erro
        return validar_catalogo(dados)

    def acao_validar(self):
        try:
            dados = self._obter_catalogo_editor()
            self.status_json.configure(text=f"Catálogo válido: {len(dados)} registro(s). Nenhum arquivo foi criado.")
            messagebox.showinfo("Validação", "Estrutura JSON válida.", parent=self.janela)
        except ValueError as erro:
            messagebox.showerror("Catálogo inválido", str(erro), parent=self.janela)

    def acao_salvar(self):
        try:
            dados = self._obter_catalogo_editor()
        except ValueError as erro:
            messagebox.showerror("Catálogo inválido", str(erro), parent=self.janela)
            return
        caminho = filedialog.asksaveasfilename(
            parent=self.janela, title="Salvar catálogo JSON", defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            salvar_catalogo(caminho, dados)
        except (OSError, ValueError) as erro:
            messagebox.showerror("Falha ao salvar", str(erro), parent=self.janela)
            self.status_json.configure(text="Falha na gravação; não foi anunciado sucesso.")
            return
        self.caminho_json = caminho
        self.status_json.configure(text=f"Catálogo salvo com sucesso: {caminho}")
        messagebox.showinfo("Salvamento", "Catálogo salvo com sucesso.", parent=self.janela)


def criar_janela():
    janela = tk.Tk()
    AplicacaoA12(janela)
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

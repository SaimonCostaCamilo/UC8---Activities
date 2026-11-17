# A09: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk
from modelos import Produto, Pedido
from pagamento import calcular_pagamento

def criar_janela():
    janela = tk.Tk()
    janela.title("A09 — minha implementação")
    janela.columnconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    
    pedido = Pedido()
    catalogo_produtos = {
        "P01": Produto("P01", "Sorvete Chocolate", 500),
        "P02": Produto("P02", "Sorvete Morango", 450),
        "P03": Produto("P03", "Açaí Tradicional", 1000),
        "P04": Produto("P04", "Leite Condensado", 300),
    }

    frame_controles = ttk.LabelFrame(base, text="Gerenciar Carrinho", padding=10)
    frame_controles.grid(row=0, column=0, sticky="ew", pady=(0, 10))
    frame_controles.columnconfigure(1, weight=1)
    frame_controles.columnconfigure(3, weight=1)

    ttk.Label(frame_controles, text="Produto:").grid(row=0, column=0, sticky="w", padx=5)
    combo_produto = ttk.Combobox(frame_controles, values=[f"{p.codigo} - {p.nome}" for p in catalogo_produtos.values()], state="readonly")
    combo_produto.grid(row=0, column=1, sticky="ew", padx=5)
    if catalogo_produtos:
        combo_produto.current(0)

    ttk.Label(frame_controles, text="Qtd:").grid(row=0, column=2, sticky="w", padx=5)
    entry_qtd = ttk.Entry(frame_controles, width=8)
    entry_qtd.grid(row=0, column=3, sticky="w", padx=5)
    entry_qtd.insert(0, "1")

    frame_tabela = ttk.Frame(base)
    frame_tabela.grid(row=3, column=0, sticky="nsew", pady=5)
    frame_tabela.columnconfigure(0, weight=1)
    frame_tabela.rowconfigure(0, weight=1)

    colunas = ("codigo", "nome", "preco", "quantidade", "subtotal")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

    tabela.heading("codigo", text="Código")
    tabela.heading("nome", text="Nome do Produto")
    tabela.heading("preco", text="Preço Unit.")
    tabela.heading("quantidade", text="Qtd")
    tabela.heading("subtotal", text="Subtotal")

    tabela.column("codigo", width=70, anchor="center")
    tabela.column("nome", width=200, anchor="w")
    tabela.column("preco", width=90, anchor="e")
    tabela.column("quantidade", width=60, anchor="center")
    tabela.column("subtotal", width=90, anchor="e")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame_acoes = ttk.Frame(base)
    frame_acoes.grid(row=4, column=0, sticky="ew", pady=10)

    frame_pagamento = ttk.LabelFrame(base, text="Prévia de Pagamento", padding=10)
    frame_pagamento.grid(row=5, column=0, sticky="ew", pady=(0, 5))
    frame_pagamento.columnconfigure(1, weight=1)

    ttk.Label(frame_pagamento, text="Forma:").grid(row=0, column=0, sticky="w", padx=5)
    combo_pagamento = ttk.Combobox(frame_pagamento, values=['Dinheiro', 'PIX', 'Débito', 'Crédito 1x'], state="readonly")
    combo_pagamento.grid(row=0, column=1, sticky="ew", padx=5)
    combo_pagamento.current(1)

    lbl_resultado_pagamento = ttk.Label(frame_pagamento, text="Total a pagar: R$ 0,00")
    lbl_resultado_pagamento.grid(row=0, column=2, padx=10)

    aviso = ttk.Label(base, text="Sistema pronto. Selecione um produto e execute uma ação.",foreground="blue", wraplength=500)
    aviso.grid(row=6, column=0, sticky="w", pady=5)
    
    lbl_total = ttk.Label(base, text="Total do Pedido: R$ 0,00")
    lbl_total.grid(row=2, column=0, sticky="e", pady=5)
    
    def atualizar_interface():
        for row in tabela.get_children():
            tabela.delete(row)
        for linha in pedido.linhas():
            codigo = linha[0]
            tabela.insert("", "end", iid=codigo, values=linha)

        total_centavos = pedido.total_centavos()
        reais = total_centavos / 100
        lbl_total.configure(text=f"Total do Pedido: R$ {reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        calcular_previa_pagamento()

    def obter_produto_selecionado_combobox():
        selecao = combo_produto.get()
        if not selecao:
            raise ValueError("Nenhum produto selecionado.")
        codigo = selecao.split(" - ")[0]
        return catalogo_produtos.get(codigo)

    def acao_adicionar():
        try:
            prod = obter_produto_selecionado_combobox()
            txt_qtd = entry_qtd.get()
            pedido.adicionar(prod, txt_qtd)
            atualizar_interface()
            aviso.configure(text=f"Adicionado/Somado: {prod.nome}", foreground="green")
        except Exception as e:
            aviso.configure(text=f"Erro ao adicionar: {e}", foreground="red")

    def acao_atualizar():
        try:
            selecionados = tabela.selection()
            if not selecionados:
                raise ValueError("Selecione uma linha na tabela para atualizar.")
            codigo_iid = selecionados[0]
            txt_qtd = entry_qtd.get()
            pedido.atualizar(codigo_iid, txt_qtd)
            atualizar_interface()
            aviso.configure(text=f"Quantidade atualizada para o item {codigo_iid}.", foreground="green")
        except Exception as e:
            aviso.configure(text=f"Erro ao atualizar: {e}", foreground="red")

    def acao_remover():
        try:
            selecionados = tabela.selection()
            if not selecionados:
                raise ValueError("Selecione uma linha na tabela para remover.")
            codigo_iid = selecionados[0]
            pedido.remover(codigo_iid)
            atualizar_interface()
            aviso.configure(text=f"Item {codigo_iid} removido com sucesso.", foreground="green")
        except Exception as e:
            aviso.configure(text=f"Erro ao remover: {e}", foreground="red")

    def calcular_previa_pagamento():
        try:
            total_centavos = pedido.total_centavos()
            subtotal_str = f"{total_centavos / 100:.2f}"
            forma = combo_pagamento.get()
            resultado = calcular_pagamento(subtotal_str, forma)
            lbl_resultado_pagamento.configure(text=f"Total ({forma}): R$ {resultado['total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        except Exception:
            lbl_resultado_pagamento.configure(text="Erro no cálculo")
    
    def testar():
        # TODO: conectar seu modelo/controller; tratar o erro sem perder dados.
        try:
            prod_teste = list(catalogo_produtos.values())[0]
            pedido.adicionar(prod_teste, "2")
            atualizar_interface()
            aviso.configure(text="Teste de fluxo executado com sucesso! Dados preservados.", foreground="green")
        except Exception as e:
            aviso.configure(text=f"Erro no teste: {e}", foreground="red")

    ttk.Button(base, text="Testar meu fluxo", command=testar).grid(row=1, column=0, pady=8)
    # TODO: organização, rótulos, listagens, ações e foco indicados no roteiro.
    ttk.Button(frame_acoes, text="Adicionar / Somar", command=acao_adicionar).pack(side="left", padx=5)
    ttk.Button(frame_acoes, text="Atualizar Qtd", command=acao_atualizar).pack(side="left", padx=5)
    ttk.Button(frame_acoes, text="Remover Item", command=acao_remover).pack(side="left", padx=5)
    ttk.Button(frame_acoes, text="Calcular Pagamento", command=calcular_previa_pagamento).pack(side="left", padx=5)

    return janela

if __name__ == "__main__":
    criar_janela().mainloop()
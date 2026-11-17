# A10: Integração da interface em Tkinter com o modelo de pedido, pizza e bebida.
import tkinter as tk
from tkinter import ttk, messagebox
from modelos import Pizza, Bebida, Pedido
from pagamento import calcular_pagamento
from modelos import formatar as formatar_preco


def criar_janela():
    janela = tk.Tk()
    janela.title("A10 — Pizzaria: transferir o modelo de pedido")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(3, weight=1)

    # Instância do Pedido e Catálogo Inicial de Produtos
    pedido = Pedido()
    catalogo = {
        "P01": Pizza(codigo="P01", nome="Mussarela", tamanho="Média", preco_centavos=3500),
        "P02": Pizza(codigo="P02", nome="Calabresa", tamanho="Grande", preco_centavos=4500),
        "B01": Bebida(codigo="B01", nome="Refrigerante", preco_centavos=600),
        "B02": Bebida(codigo="B02", nome="Suco Natural", preco_centavos=800)
    }

    # --- Título e Orientação ---
    ttk.Label(base, text="Catálogo e Carrinho da Pizzaria", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

    # --- Painel de Seleção ---
    frame_controles = ttk.LabelFrame(base, text="Adicionar / Atualizar Item", padding=10)
    frame_controles.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    frame_controles.columnconfigure(3, weight=1)

    ttk.Label(frame_controles, text="Produto:").grid(row=0, column=0, sticky="w", padx=4)
    combo_produtos = ttk.Combobox(frame_controles, values=[f"{p.codigo} - {p.nome} ({getattr(p, 'tamanho', 'Bebida')})" for p in catalogo.values()], state="readonly", width=35)
    combo_produtos.grid(row=0, column=1, padx=4)
    if catalogo:
        combo_produtos.current(0)

    ttk.Label(frame_controles, text="Qtd:").grid(row=0, column=2, sticky="w", padx=4)
    entry_qtd = ttk.Entry(frame_controles, width=8)
    entry_qtd.insert(0, "1")
    entry_qtd.grid(row=0, column=3, sticky="w", padx=4)

    # --- Tabela / Listagem (Treeview) ---
    frame_tabela = ttk.Frame(base)
    frame_tabela.grid(row=3, column=0, sticky="nsew", pady=4)
    frame_tabela.columnconfigure(0, weight=1)
    frame_tabela.rowconfigure(0, weight=1)

    colunas = ("codigo", "nome", "preco", "quantidade", "subtotal")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=8)
    tree.heading("codigo", text="Código")
    tree.heading("nome", text="Nome / Tamanho")
    tree.heading("preco", text="Preço Unit.")
    tree.heading("quantidade", text="Qtd")
    tree.heading("subtotal", text="Subtotal")
    
    tree.column("codigo", width=70, anchor="center")
    tree.column("nome", width=180, anchor="w")
    tree.column("preco", width=90, anchor="e")
    tree.column("quantidade", width=60, anchor="center")
    tree.column("subtotal", width=90, anchor="e")
    
    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # --- Rótulo de Total e Avisos ---
    lbl_total = ttk.Label(base, text="Total do Pedido: R$ 0,00", font=("Segoe UI", 11, "bold"))
    lbl_total.grid(row=4, column=0, sticky="e", pady=8)

    aviso = ttk.Label(base, text="Pronto para registrar o pedido.", foreground="gray")
    aviso.grid(row=6, column=0, sticky="w", pady=4)

    # --- Funções de Atualização da Interface ---
    def atualizar_interface():
        for item in tree.get_children():
            tree.delete(item)
        
        for linha in pedido.linhas():
            tree.insert("", "end", values=(
                linha["codigo"],
                linha["nome"],
                formatar_preco(linha["preco_unitario"]),
                linha["quantidade"],
                formatar_preco(linha["subtotal"])
            ))
        
        total_centavos = pedido.total_centavos()
        lbl_total.configure(text=f"Total do Pedido: {formatar_preco(total_centavos)}")

    # --- Callbacks de Ação ---
    def acao_adicionar():
        try:
            sel = combo_produtos.get()
            if not sel:
                raise ValueError("Selecione um produto do catálogo.")
            codigo = sel.split(" - ")[0]
            produto = catalogo[codigo]
            texto_qtd = entry_qtd.get()

            pedido.adicionar(produto, texto_qtd)
            atualizar_interface()
            aviso.configure(text=f"Item {produto.nome} adicionado com sucesso.", foreground="green")
        except Exception as e:
            messagebox.showerror("Erro de Validação", str(e))
            aviso.configure(text=f"Erro: {e}", foreground="red")

    def acao_atualizar():
        try:
            selecionados = tree.selection()
            if not selecionados:
                raise ValueError("Selecione um item na tabela para atualizar a quantidade.")
            
            item_valores = tree.item(selecionados[0], "values")
            codigo = item_valores[0]
            texto_qtd = entry_qtd.get()

            pedido.atualizar(codigo, texto_qtd)
            atualizar_interface()
            aviso.configure(text=f"Quantidade do item {codigo} atualizada.", foreground="green")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            aviso.configure(text=f"Erro: {e}", foreground="red")

    def acao_remover():
        try:
            selecionados = tree.selection()
            if not selecionados:
                raise ValueError("Selecione um item na tabela para remover.")
            
            item_valores = tree.item(selecionados[0], "values")
            codigo = item_valores[0]

            pedido.remover(codigo)
            atualizar_interface()
            aviso.configure(text=f"Item {codigo} removido do pedido.", foreground="green")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            aviso.configure(text=f"Erro: {e}", foreground="red")

    # Exemplo de controles para a escolha do pagamento na interface (main.py)
    frame_pagamento = ttk.LabelFrame(base, text="Finalizar Pagamento", padding=10)
    frame_pagamento.grid(row=5, column=0, sticky="ew", pady=4)

    ttk.Label(frame_pagamento, text="Forma:").pack(side="left", padx=4)

    # Importa as chaves do dicionário de fatores do módulo pagamento.py
    from pagamento import FATORES
    combo_pagamento = ttk.Combobox(frame_pagamento, values=list(FATORES.keys()), state="readonly", width=15)
    combo_pagamento.pack(side="left", padx=4)
    combo_pagamento.current(1)  # Seleciona o PIX por padrão (ou 0 para Dinheiro)

    def acao_pagar_completo():
        try:
            if not pedido.linhas():
                raise ValueError("O pedido está vazio.")
            
            total_centavos = pedido.total_centavos()
            total_reais_str = str(total_centavos / 100)
            
            # Pega a forma selecionada no combobox da tela
            forma_escolhida = combo_pagamento.get()
            
            # Calcula o pagamento usando o contrato do pagamento.py
            valor_final = calcular_pagamento(total_reais_str, forma_escolhida)
            
            messagebox.showinfo("Pagamento Concluído", f"Forma: {forma_escolhida}\nTotal com ajustes: R$ {valor_final}")
            aviso.configure(text=f"Pedido pago via {forma_escolhida}.", foreground="blue")
        except Exception as e:
            messagebox.showerror("Erro no Pagamento", str(e))

    ttk.Button(frame_pagamento, text="Pagar Pedido", command=acao_pagar_completo).pack(side="right", padx=4)

    # --- Botões de Operação ---
    frame_botoes = ttk.Frame(base)
    frame_botoes.grid(row=2, column=0, sticky="ew", pady=4)

    ttk.Button(frame_botoes, text="Adicionar Item", command=acao_adicionar).pack(side="left", padx=2)
    ttk.Button(frame_botoes, text="Atualizar Qtd", command=acao_atualizar).pack(side="left", padx=2)
    ttk.Button(frame_botoes, text="Remover Item", command=acao_remover).pack(side="left", padx=2)
    ttk.Button(frame_botoes, text="Finalizar / Pagar", command=acao_pagar_completo).pack(side="right", padx=2)

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
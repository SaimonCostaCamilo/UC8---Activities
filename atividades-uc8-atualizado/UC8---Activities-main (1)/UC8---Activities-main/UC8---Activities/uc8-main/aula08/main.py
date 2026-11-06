# A08: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk
from decimal import Decimal
from modelos import Produto, Pedido, formatar
from pagamento import calcular_pagamento


def criar_janela():
    janela = tk.Tk()
    janela.title("A08 — minha implementação")
    janela.columnconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    ttk.Label(base, text="Traga seu layout e conecte as responsabilidades desta aula.", wraplength=430).grid(row=0, column=0)
    catalogo = {
        "P01": Produto("P01", "Fruta", 500),
        "P02": Produto("P02", "Leite", 750)
    }
    pedido = Pedido()
    p_teste = Produto("P99", "Pedido Base R$ 100", 10000)
    pedido.adicionar(p_teste, "1")

    frame_form = ttk.Frame(base)
    frame_form.grid(row=1, column=0, pady=8, sticky="ew")
    frame_form.columnconfigure(1, weight=1)

    ttk.Label(frame_form, text="Produto:").grid(row=0, column=0, sticky="w", pady=2)
    opcoes_prod = [f"{p.codigo} - {p.nome} ({formatar(p.preco_centavos)})" for p in catalogo.values()]
    combo_prod = ttk.Combobox(frame_form, values=opcoes_prod, state="readonly")
    combo_prod.grid(row=0, column=1, sticky="ew", padx=4, pady=2)
    if opcoes_prod:
        combo_prod.current(0)

    ttk.Label(frame_form, text="Qtd:").grid(row=1, column=0, sticky="w", pady=2)
    entry_qtd = ttk.Entry(frame_form)
    entry_qtd.grid(row=1, column=1, sticky="ew", padx=4, pady=2)
    entry_qtd.insert(0, "1")

    ttk.Label(frame_form, text="Pagamento:").grid(row=2, column=0, sticky="w", pady=2)
    opcoes_pagamento = ["Dinheiro", "PIX", "Débito", "Crédito 1x"]
    combo_pagamento = ttk.Combobox(frame_form, values=opcoes_pagamento, state="readonly")
    combo_pagamento.grid(row=2, column=1, sticky="ew", padx=4, pady=2)
    combo_pagamento.current(1) 

    aviso = ttk.Label(base, text="Prévia de pagamento pronta para consulta.", wraplength=430)
    aviso.grid(row=3, column=0, pady=8)
    
    def testar():
        # TODO: conectar seu modelo/controller; tratar o erro sem perder dados.
        # TODO: organização, rótulos, listagens, ações e foco indicados no roteiro.
        try:
            total_centavos = pedido.total_centavos()
            subtotal_str = str(Decimal(total_centavos) / 100)

            forma_escolhida = combo_pagamento.get()
            if not forma_escolhida:
                raise ValueError("Selecione uma forma de pagamento válida.")

            resultado = calcular_pagamento(subtotal_str, forma_escolhida)

            sub_f = f"R$ {resultado['subtotal']:.2f}".replace(".", ",")
            tot_f = f"R$ {resultado['total']:.2f}".replace(".", ",")
            desc_f = f"R$ {resultado['desconto']:.2f}".replace(".", ",")

            msg = (f"Forma: {resultado['forma']} | Subtotal: {sub_f} | " f"Desconto: {desc_f} | Total: {tot_f}")
            aviso.configure(text=msg)

        except (ValueError, TypeError, RuntimeError) as e:
            aviso.configure(text=f"Erro: {e}")

        entry_qtd.focus()

    ttk.Button(base, text="Conferir pagamento", command=testar).grid(row=2, column=0, pady=8)

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

"""A03 — complete a lógica e os callbacks do conversor."""
import tkinter as tk
from tkinter import ttk


def calcular(campos, registro):
    # TODO: ler reais e as duas cotações; aceitar vírgula ou ponto decimal.
    # TODO: tratar conversão inválida, reais negativos e cotações <= 0.
    # TODO: dividir reais por cada cotação.
    # TODO: confirmar entradas e os dois resultados somente após validar tudo.

    try:
        valor_real = float(campos["reais"].replace(',', '.'))
        valor_dolar = float(campos["cotacao_dolar"].replace(',', '.'))
        valor_euro = float(campos["cotacao_euro"].replace(',', '.'))
    except ValueError:
        return False,"Erro: Entrada inválida. Por favor, insira números válidos."

    if valor_real <= 0 or valor_dolar <= 0 or valor_euro <= 0:
        return False,"Erro: O valor em reais e as cotações devem ser maiores que zero."

    cotacao_real_dolar = valor_real / valor_dolar
    cotacao_real_euro = valor_real / valor_euro
    registro.append((valor_real, valor_dolar, valor_euro, cotacao_real_dolar, cotacao_real_euro))
    return True,f"""Valores convertidos:
      Reais: {valor_real:.2f} 
      Trumpetas: {cotacao_real_dolar:.2f}
      Euros: {cotacao_real_euro:.2f}"""


def exibir(registro):
    # TODO: tratar ausência de conversão; consultar somente registro.
    # Registros são tratados no calculo e apenas apos validação são inseridos na lista
    # TODO: mostrar entradas usadas e resultados, estes com duas casas.
    return "Complete a função exibir."


def limpar(campos):
    # TODO: esvaziar os três campos; preservar registro e resultados.
    pass


def criar_janela():
    janela = tk.Tk()
    janela.title("Conversor com cotações fictícias — A03")
    janela.columnconfigure(1, weight=1)
    campos = {"reais": "", "cotacao_dolar": "", "cotacao_euro": ""}
    registro = []
    lista_registros = []

    ttk.Label(janela, text="Cotações fictícias manuais; sem consulta à internet.", wraplength=420).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    ttk.Label(janela, text="Valor em reais (R$):").grid(row=1, column=0, padx=12, pady=6, sticky="w")
    entrada_reais = ttk.Entry(janela)
    entrada_reais.grid(row=1, column=1, padx=12, pady=6, sticky="ew")
    ttk.Label(janela, text="R$ por 1 USD:").grid(row=2, column=0, padx=12, pady=6, sticky="w")
    entrada_dolar = ttk.Entry(janela)
    entrada_dolar.grid(row=2, column=1, padx=12, pady=6, sticky="ew")
    ttk.Label(janela, text="R$ por 1 EUR:").grid(row=3, column=0, padx=12, pady=6, sticky="w")
    entrada_euro = ttk.Entry(janela)
    entrada_euro.grid(row=3, column=1, padx=12, pady=6, sticky="ew")

    def ao_calcular():
        # TODO: ler os três Entry, calcular e atualizar aviso/último confirmado.
        campos["reais"] = entrada_reais.get()
        campos["cotacao_dolar"] = entrada_dolar.get()
        campos["cotacao_euro"] = entrada_euro.get()
        
        sucesso,mensagem = calcular(campos,registro)
        if sucesso:
            lista_registros.append(mensagem)
        
        entrada_reais.delete(0,tk.END)
        entrada_euro.delete(0,tk.END)
        entrada_dolar.delete(0, tk.END)
        aviso.configure(text=mensagem)

    def ao_exibir():
        # TODO: consultar somente registro, sem ler as entradas editáveis.
        print("listando registros")
        if not lista_registros:
            aviso.configure(text="Nenhum registro encontrado.")
            return
        texto = "\n".join(
            f"Registro: {registro}"
            for registro in lista_registros
        )
        aviso.configure(text=texto)

    def ao_limpar():
        # TODO: esvaziar campos/Entry e devolver foco; conservar resultado.
        print("Limpando campos")
        entrada_reais.delete(0, tk.END)
        entrada_dolar.delete(0, tk.END)
        entrada_euro.delete(0, tk.END)
        aviso.configure(text="Campos para limpar foram limpos com sucesso")

    ttk.Button(janela, text="Calcular", command=ao_calcular).grid(row=4, column=0, padx=12, pady=8)
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(row=4, column=1, padx=12, pady=8)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=5, column=0, columnspan=2, pady=6)
    aviso = ttk.Label(janela, text="Use vírgula ou ponto decimal, sem milhares.", wraplength=420)
    aviso.grid(row=6, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    entrada_reais.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.title("Um evento")

def responder():
    mensagem.configure(text="O clique chamou a função.")

mensagem = ttk.Label(janela, text="Aguardando clique.")
mensagem.grid(row=0, column=0, padx=12, pady=12)
ttk.Button(janela, text="Experimentar", command=responder).grid(row=1,
                                                         column=0, pady=12)
janela.mainloop()
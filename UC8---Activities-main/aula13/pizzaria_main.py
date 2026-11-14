# A13 — Pizzaria: transfere o mesmo contrato de comprovante para CSV
import tkinter as tk
from modelos import Pizza, Bebida
from main import criar_janela


def executar():
    catalogo = [
        Pizza("P01", "Pizza Calabresa Média", "Média", 4000),
        Pizza("P02", "Pizza Margherita Grande", "Grande", 5500),
        Bebida("B01", "Guaraná 2 L", 1200),
        Bebida("B02", "Água Mineral 500 ml", 500),
    ]
    criar_janela(catalogo=catalogo, nome_aplicacao="Pizzaria").mainloop()


if __name__ == "__main__":
    executar()

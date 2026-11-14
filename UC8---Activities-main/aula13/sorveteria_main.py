# A13 — Sorveteria: demonstra o mesmo contrato de exportação CSV
import tkinter as tk
from modelos import Produto
from main import criar_janela


def executar():
    catalogo = [
        Produto("S01", "Picolé; edição verão", 650),
        Produto("S02", "Sorvete de chocolate", 1200),
        Produto("S03", "Açaí com morango", 1650),
        Produto("S04", "Picolé de limão", 450),
    ]
    criar_janela(catalogo=catalogo, nome_aplicacao="Sorveteria").mainloop()


if __name__ == "__main__":
    executar()

"""Comparação opcional de foco/teclado entre ttk e CustomTkinter.
O núcleo A17 não depende deste pacote.
"""
import tkinter as tk
from tkinter import ttk, messagebox


def criar_comparacao():
    try:
        import customtkinter as ctk
    except ImportError:
        raiz = tk.Tk(); raiz.title("A17 — comparação opcional")
        ttk.Label(raiz, text="CustomTkinter não está instalado.\nO núcleo Tkinter/SQLite continua funcionando.", padding=18).pack()
        ttk.Button(raiz, text="Fechar", command=raiz.destroy).pack(pady=10)
        return raiz

    ctk.set_appearance_mode("system")
    app = ctk.CTk(); app.title("A17 — Comparação ttk x CustomTkinter")
    app.geometry("620x440")
    ctk.CTkLabel(app, text="Comparação visual e de teclado", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(18, 6))
    ctk.CTkLabel(app, text="Use Tab e Shift+Tab para observar a ordem do foco.").pack(pady=4)
    ctk.CTkLabel(app, text="Campo de teste (CustomTkinter):").pack(anchor="w", padx=24, pady=(14, 3))
    entrada = ctk.CTkEntry(app, placeholder_text="Digite um texto de teste")
    entrada.pack(fill="x", padx=24)
    resultado = ctk.CTkLabel(app, text="Aguardando interação")
    resultado.pack(pady=12)
    def testar():
        resultado.configure(text=f"Recebido: {entrada.get() or '(vazio)'}")
    ctk.CTkButton(app, text="Testar ação pelo teclado ou mouse", command=testar).pack(pady=6)
    ctk.CTkLabel(app, text="Compare contraste, foco visível, Tab/Shift+Tab e acionamento por Enter/Espaço.\nEsta janela é independente do fluxo de vendas e não grava dados.", justify="left").pack(padx=24, pady=18)
    entrada.focus_set()
    return app


if __name__ == "__main__":
    criar_comparacao().mainloop()

"""A05 — sistema escolar com registros agrupados por turma."""
import tkinter as tk
from tkinter import ttk


def calcular(campos, registro):
    # TODO: normalizar nome/turma e recusar texto vazio.
    nome = campos.get("nome", "").strip()
    turma = campos.get("turma", "").strip()
    if not nome or not turma:
        return "Nome e turma não podem ser vazios."
    # TODO: conferir a presença de exatamente cinco notas.
    notas_texto = campos.get("notas", [])
    if len(notas_texto) != 5:
        return "São necessárias exatamente cinco notas."
    # TODO: converter cada texto, validar de 0 a 10 e criar uma nova lista.
    notas = []
    for valor in notas_texto:
        try:
            nota = float(valor.replace(",", "."))
        except (ValueError, TypeError):
            return f"Nota inválida: '{valor}'."
        if not (0 <= nota <= 10):
            return f"Nota fora do intervalo (0–10): {nota}."
        notas.append(nota)
    # TODO: calcular a média com sum e len.
    media = sum(notas) / len(notas)
    # TODO: confirmar nome, turma, notas e média somente após validar tudo.
    registro.append({"nome": nome, "turma": turma, "notas": notas, "media": media})
    return f"Confirmado: {nome} | {turma} | média {media:.1f}"


def exibir(registro):
    # TODO: tratar ausência de registros.
    if not registro:
        return "Nenhum registro confirmado."
    # TODO: agrupar alunos por turma e calcular média da turma.
    grupos = {}
    for reg in registro:
        grupos.setdefault(reg["turma"], []).append(reg)
    linhas = []
    for turma, alunos in sorted(grupos.items()):
        linhas.append(f"Turma: {turma}")
        for reg in alunos:
            notas = " | ".join(str(n) for n in reg["notas"])
            linhas.append(f"  {reg['nome']}  Notas: {notas}  Média: {reg['media']:.1f}")
        media_turma = sum(a["media"] for a in alunos) / len(alunos)
        linhas.append(f"  Média da turma: {media_turma:.1f}")
    return "\n".join(linhas)


def limpar(campos):
    # TODO: esvaziar nome, turma e os cinco textos de notas.
    # O registro confirmado não é recebido por esta função.
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]


def criar_janela():
    janela = tk.Tk()
    janela.title("Sistema escolar com grupos — A05")
    janela.columnconfigure(1, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = []

    ttk.Label(janela, text="Dados fictícios. Cinco notas de 0 a 10; agrupados por turma.", wraplength=440).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    ttk.Label(janela, text="Nome fictício:").grid(row=1, column=0, padx=12, pady=4, sticky="w")
    entrada_nome = ttk.Entry(janela)
    entrada_nome.grid(row=1, column=1, padx=12, pady=4, sticky="ew")
    ttk.Label(janela, text="Turma fictícia:").grid(row=2, column=0, padx=12, pady=4, sticky="w")
    entrada_turma = ttk.Entry(janela)
    entrada_turma.grid(row=2, column=1, padx=12, pady=4, sticky="ew")
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(janela, text=f"Nota {numero} (0 a 10):").grid(row=numero+2, column=0, padx=12, pady=4, sticky="w")
        entrada = ttk.Entry(janela)
        entrada.grid(row=numero+2, column=1, padx=12, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
        # TODO: ler identificação e reunir os cinco textos de Entry numa lista.
        campos["nome"] = entrada_nome.get()
        campos["turma"] = entrada_turma.get()
        campos["notas"] = [e.get() for e in entradas_notas]
        # TODO: chamar calcular e atualizar aviso; preservar painel de grupos.
        aviso.configure(text=calcular(campos, registro))

    def ao_exibir():
        # TODO: consultar somente registro; não ler os Entry em edição.
        resultado.configure(text=exibir(registro))

    def ao_limpar():
        # TODO: limpar campos e os sete Entry; devolver foco ao nome.
        limpar(campos)
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)
        for e in entradas_notas:
            e.delete(0, tk.END)
        entrada_nome.focus_set()
        # TODO: preservar registro e painel do último válido.
        aviso.configure(text="Campos limpos. Registros preservados.")

    ttk.Button(janela, text="Calcular média", command=ao_calcular).grid(row=8, column=0, padx=12, pady=6)
    ttk.Button(janela, text="Exibir grupos", command=ao_exibir).grid(row=8, column=1, padx=12, pady=6)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=9, column=0, columnspan=2, pady=4)
    aviso = ttk.Label(janela, text="Preencha nome, turma e as cinco notas fictícias.", wraplength=440)
    aviso.grid(row=10, column=0, columnspan=2, padx=12, pady=6, sticky="w")
    resultado = ttk.Label(janela, text="Nenhum registro confirmado nesta sessão.", wraplength=440)
    resultado.grid(row=11, column=0, columnspan=2, padx=12, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    campos = {"nome": "Lia", "turma": "T1", "notas": ["6", "7", "8", "9", "10"]}
    registro = []
    print(exibir(registro))
    print(calcular(campos, registro))
    campos2 = {"nome": "Rui", "turma": "T1", "notas": ["5", "6", "7", "8", "9"]}
    print(calcular(campos2, registro))
    campos3 = {"nome": "Ana", "turma": "T2", "notas": ["8", "9", "10", "7", "6"]}
    print(calcular(campos3, registro))
    print(exibir(registro))
    # Acrescente as sequências da matriz, prevendo antes de executar.

"""A05 — complete: Escolar com consulta — A05."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path


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
    registro.append({"nome": nome, "turma": turma, "notas": notas, "media": 
                                                                        media})
    return f"Confirmado: {nome} | {turma} | média {media:.1f}"


def exibir(registro):
    # TODO: tratar ausência; consultar todos os registros confirmados.
    if not registro:
        return "Nenhum registro confirmado."
    # TODO: agrupar por turma e calcular média da turma.
    grupos = {}
    for reg in registro:
        grupos.setdefault(reg["turma"], []).append(reg)
    linhas = []
    for turma, alunos in sorted(grupos.items()):
        linhas.append(f"Turma: {turma}")
        for reg in alunos:
            notas = " | ".join(str(nota) for nota in reg["notas"])
            linhas.append(f"  {reg['nome']}  Notas: {notas}  Média: {
                                                            reg['media']:.1f}")
        media_turma = sum(a["media"] for a in alunos) / len(alunos)
        linhas.append(f"  Média da turma: {media_turma:.1f}")
    return "\n".join(linhas)


def limpar(campos):
    # TODO: esvaziar nome, turma e os cinco textos de notas.
    # O registro confirmado não é recebido por esta função.
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]


def inserir_marca(container, caminho=None):
    # TODO: procurar marca-a05.png ao lado do script com pathlib.
    caminho = caminho or Path(__file__).parent / "crab.png"
    # TODO: usar PhotoImage e conservar uma referência enquanto o rótulo existir.
    try:
        img = tk.PhotoImage(file=str(caminho))
        rotulo = ttk.Label(container, image=img)
        rotulo.image = img #type: ignore
        return rotulo
    # TODO: manter texto se o PNG não existir ou não puder ser lido.
    except Exception:
        return ttk.Label(container, text="Sistema escolar fictício — A05")


def abrir_consulta(principal, registro):
    # TODO: tratar ausência de registro sem criar uma janela vazia.
    if not registro:
        return None
    # TODO: obter o texto do confirmado no instante da abertura.
    texto = exibir(registro)
    # TODO: criar Toplevel e organizar sua consulta somente de leitura.
    consulta = tk.Toplevel(principal)
    consulta.title("Consulta — último registro confirmado")
    consulta.resizable(False, False)
    ttk.Label(consulta, text=texto, wraplength=380, justify="left").pack(padx=20, pady=16)
    ttk.Button(consulta, text="Fechar", command=consulta.destroy).pack(pady=(0, 12))
    # TODO: botão, X e Escape devem fechar somente a consulta.
    consulta.bind("<Escape>", lambda e: consulta.destroy())
    consulta.protocol("WM_DELETE_WINDOW", consulta.destroy)
    consulta.transient(principal)
    consulta.grab_set()
    return consulta


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar com consulta — A05")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = []
    inserir_marca(base).grid(row=0, column=0, columnspan=2, pady=6, sticky="w")
    # TODO: criar LabelFrame para identificação e notas e Frame para ações.
    identificacao = ttk.LabelFrame(base, text="Identificação", padding=6)
    identificacao.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)
    identificacao.columnconfigure(1, weight=1)
    grupo_notas = ttk.LabelFrame(base, text="Notas", padding=6)
    grupo_notas.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)
    grupo_notas.columnconfigure(1, weight=1)
    acoes = ttk.Frame(base)
    acoes.grid(row=3, column=0, columnspan=2, sticky="ew", pady=4)
    acoes.columnconfigure(0, weight=1)
    acoes.columnconfigure(1, weight=1)
    # TODO: posicionar os grupos na base e configurar expansão das colunas.
    base.columnconfigure(1, weight=1)

    ttk.Label(identificacao, text="Nome fictício:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(row=0, column=1, padx=6, pady=4, sticky="ew")
    ttk.Label(identificacao, text="Turma fictícia:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(row=1, column=1, padx=6, pady=4, sticky="ew")
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(grupo_notas, text=f"Nota {numero} (0 a 10):").grid(row=numero-1, column=0, padx=6, pady=4, sticky="w")
        entrada = ttk.Entry(grupo_notas)
        entrada.grid(row=numero-1, column=1, padx=6, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
        # TODO: reutilizar a leitura, validação e confirmação da sua A04.
        campos["nome"] = entrada_nome.get()
        campos["turma"] = entrada_turma.get()
        campos["notas"] = [e.get() for e in entradas_notas]
        aviso.configure(text=calcular(campos, registro))

    def ao_exibir():
        # TODO: consultar o último confirmado; na prática 2, abrir a Toplevel.
        if not registro:
            aviso.configure(text="Nenhum registro confirmado para consultar.")
            return
        abrir_consulta(janela, registro)

    def ao_limpar():
        # TODO: limpar as sete entradas sem apagar o último confirmado.
        limpar(campos)
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)
        for e in entradas_notas:
            e.delete(0, tk.END)
        entrada_nome.focus_set()
        aviso.configure(text="Campos limpos. Registro anterior preservado.")

    ttk.Button(acoes, text="Calcular média", command=ao_calcular).grid(row=0, column=0, padx=4, pady=6)
    ttk.Button(acoes, text="Consultar", command=ao_exibir).grid(row=0, column=1, padx=4, pady=6)
    ttk.Button(acoes, text="Limpar campos", command=ao_limpar).grid(row=1, column=0, columnspan=2, padx=4, pady=6)
    aviso = ttk.Label(base, text="Use dados fictícios e confira as cinco notas.", wraplength=430)
    aviso.grid(row=4, column=0, columnspan=2, pady=6, sticky="w")
    resultado = ttk.Label(base, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=430)
    resultado.grid(row=5, column=0, columnspan=2, pady=6, sticky="w")
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()

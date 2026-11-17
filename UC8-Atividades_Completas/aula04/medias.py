"""A04 — complete as funções e teste as cinco notas no terminal."""
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
    for t in notas_texto:
        try:
            n = float(t)
        except (ValueError, TypeError):
            return f"Nota inválida: '{t}'."
        if not (0 <= n <= 10):
            return f"Nota fora do intervalo (0–10): {n}."
        notas.append(n)
    # TODO: calcular a média com sum e len.
    media = sum(notas) / len(notas)
    # TODO: confirmar nome, turma, notas e média somente após validar tudo.
    registro.append({"nome": nome, "turma": turma, "notas": notas, "media": media})
    return f"Confirmado: {nome} | {turma} | notas {notas} | média {media:.1f}"


def exibir(registro):
    # TODO: tratar ausência; consultar apenas o último registro confirmado.
    if not registro:
        return "Nenhum registro confirmado."
    # TODO: mostrar identificação e cinco notas usadas, com média em uma casa.
    linhas = []
    for reg in registro:
        notas = " | ".join(str(n) for n in reg["notas"])
        linhas.append(f"Aluno: {reg['nome']}  Turma: {reg['turma']}  Notas: {notas}  Média: {reg['media']:.1f}")
    return "\n".join(linhas)


def limpar(campos):
    # TODO: esvaziar nome, turma e os cinco textos de notas.
    # O registro confirmado não é recebido por esta função.
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]


if __name__ == "__main__":
    campos = {"nome": "Lia", "turma": "T1", "notas": ["6", "7", "8", "9", "10"]}
    registro = []
    print(exibir(registro))
    print(calcular(campos, registro))
    print(exibir(registro))
    # Acrescente as sequências da matriz, prevendo antes de executar.

"""A06 — classe Aluno com validação reutilizada da A05."""


class Aluno:
    def __init__(self):
        # TODO: inicializar nome, turma, notas e média como None.
        self.nome = None
        self.turma = None
        self.notas = None
        self.media = None

    def confirmar(self, nome, turma, notas_texto):
        # TODO: normalizar nome/turma e recusar texto vazio.
        nome = str(nome).strip()
        turma = str(turma).strip()
        if not nome or not turma:
            return "Nome e turma não podem ser vazios."
        # TODO: conferir a presença de exatamente cinco notas.
        if len(notas_texto) != 5:
            return "São necessárias exatamente cinco notas."
        # TODO: converter cada texto, validar de 0 a 10 e criar uma nova lista.
        notas = []
        for valor in notas_texto:
            try:
                nota = float(str(valor).replace(",", "."))
            except (ValueError, TypeError):
                return f"Nota inválida: '{valor}'."
            if not (0 <= nota <= 10):
                return f"Nota fora do intervalo (0–10): {nota}."
            notas.append(nota)
        # TODO: calcular a média com sum e len.
        media = sum(notas) / len(notas)
        # TODO: confirmar somente após validar tudo; tentativa inválida 
        # preserva atributos anteriores.
        self.nome = nome
        self.turma = turma
        self.notas = notas
        self.media = media
        return f"Confirmado: {nome} | {turma} | média {media:.1f}"

    def exibir(self):
        # TODO: tratar ausência de confirmação.
        if self.nome is None:
            return "Nenhum registro confirmado."
        notas = " | ".join(str(nota) for nota in self.notas) #type: ignore
        return f"Aluno: {self.nome}  Turma: {self.turma}  Notas: {
                                                notas}  Média: {self.media:.1f}"

"""A20 — validação de vínculos por ID usando dados fictícios.

Contrato:
- alunos e planos aceitam dicionários {id: nome/dados} ou listas de dicts com 'id';
- matrículas são uma lista de dicts com id, aluno_id e plano_id;
- IDs precisam ser inteiros positivos (bool não é aceito) e não podem se repetir;
- validar_vinculos retorna True ou levanta ValueError sem modificar os dados;
- pode_excluir_aluno retorna False quando há matrícula vinculada.
"""

def _id_valido(valor):
    return type(valor) is int and valor > 0


def _normalizar_registros(colecao, nome):
    if isinstance(colecao, dict):
        registros = []
        for codigo, valor in colecao.items():
            registros.append({"id": codigo, "valor": valor})
        return registros
    if isinstance(colecao, (list, tuple)):
        if not all(isinstance(item, dict) for item in colecao):
            raise ValueError(f"{nome}: cada registro deve ser um dicionário.")
        return list(colecao)
    raise ValueError(f"{nome}: use dict, list ou tuple.")


def _mapear_ids(colecao, nome):
    resultado = {}
    for registro in _normalizar_registros(colecao, nome):
        codigo = registro.get("id")
        if not _id_valido(codigo):
            raise ValueError(f"{nome}: ID inválido {codigo!r}; use inteiro positivo.")
        if codigo in resultado:
            raise ValueError(f"{nome}: ID duplicado {codigo}.")
        resultado[codigo] = registro
    return resultado


def validar_vinculos(alunos, planos, matriculas):
    """Confere IDs e referências. Não altera alunos, planos ou matrículas."""
    mapa_alunos = _mapear_ids(alunos, "alunos")
    mapa_planos = _mapear_ids(planos, "planos")
    mapa_matriculas = _mapear_ids(matriculas, "matrículas")

    for codigo, matricula in mapa_matriculas.items():
        aluno_id = matricula.get("aluno_id")
        plano_id = matricula.get("plano_id")
        if not _id_valido(aluno_id) or aluno_id not in mapa_alunos:
            raise ValueError(
                f"Matrícula {codigo}: aluno_id {aluno_id!r} não existe ou é inválido."
            )
        if not _id_valido(plano_id) or plano_id not in mapa_planos:
            raise ValueError(
                f"Matrícula {codigo}: plano_id {plano_id!r} não existe ou é inválido."
            )
    return True


def pode_excluir_aluno(codigo, matriculas):
    """Indica se o aluno não está referenciado; não executa a exclusão."""
    if not _id_valido(codigo):
        raise ValueError("Código do aluno deve ser inteiro positivo.")
    mapa_matriculas = _mapear_ids(matriculas, "matrículas")
    return not any(m.get("aluno_id") == codigo for m in mapa_matriculas.values())


if __name__ == "__main__":
    alunos = {41: "Lia"}
    planos = {7: "Mensal"}
    matriculas = [{"id": 101, "aluno_id": 41, "plano_id": 7}]
    print("Vínculos iniciais:", validar_vinculos(alunos, planos, matriculas))
    alunos[41] = "Lia Silva"
    print("Após alterar nome:", validar_vinculos(alunos, planos, matriculas))
    print("Pode excluir aluno 41?", pode_excluir_aluno(41, matriculas))
    matricula_invalida = [{"id": 102, "aluno_id": 99, "plano_id": 7}]
    try:
        validar_vinculos(alunos, planos, matricula_invalida)
    except ValueError as erro:
        print("Referência recusada:", erro)

from aluno import Aluno


def verificar_independencia():
    lia = Aluno()
    rui = Aluno()
    # TODO: comparar os objetos, suas listas, médias e alterações independentes.
    assert lia is not rui
    lia.confirmar("Lia", "T1", ["6", "7", "8", "9", "10"])
    rui.confirmar("Rui", "T2", ["5", "5", "5", "5", "5"])
    assert lia.media == 8.0
    assert rui.media == 5.0
    assert lia.notas is not rui.notas
    # alterar Lia não muda Rui
    lia.confirmar("Lia", "T1", ["10", "10", "10", "10", "10"])
    assert lia.media == 10.0
    assert rui.media == 5.0
    assert rui.nome == "Rui"
    # TODO: usar assert nos resultados esperados; só então retornar True.
    return True


def verificar_validacao():
    # TODO: válido seguido de erro; conferir preservação de todos os atributos.
    a = Aluno()
    a.confirmar("Lia", "T1", ["6", "7", "8", "9", "10"])
    a.confirmar("Rui", "T2", ["5", "5", "5", "5", "abc"])
    assert a.nome == "Lia"
    assert a.turma == "T1"
    assert a.media == 8.0
    assert a.notas == [6.0, 7.0, 8.0, 9.0, 10.0]
    # TODO: testar limites 0/10, vírgula e lista de textos independente.
    b = Aluno()
    assert "Confirmado" in b.confirmar("X", "T1", ["0", "0", "0", "0", "0"])
    assert b.notas[0] == 0.0 #type: ignore
    assert "Confirmado" in b.confirmar("X", "T1", ["10", "10", "10", "10", "10"])
    assert b.notas[0] == 10.0 #type: ignore
    assert "fora do intervalo" in b.confirmar("X", "T1", ["-0,1", "5", "5", "5", "5"])
    assert "fora do intervalo" in b.confirmar("X", "T1", ["10,1", "5", "5", "5", "5"])
    c = Aluno()
    c.confirmar("X", "T1", ["7,5", "8", "6,5", "9", "7"])
    assert c.notas == [7.5, 8.0, 6.5, 9.0, 7.0]
    notas_originais = ["7,5", "8", "6,5", "9", "7"]
    assert c.notas is not notas_originais
    # TODO: retornar True somente depois das verificações implementadas.
    return True


if __name__ == "__main__":
    independencia = verificar_independencia()
    validacao = verificar_validacao()
    if independencia and validacao:
        print("Verificações do modelo concluídas.")
    else:
        print("Verificações incompletas; implemente e execute os casos.")

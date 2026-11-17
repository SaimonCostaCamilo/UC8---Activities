"""A20 — verificações automatizadas independentes, somente com dados fictícios."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from vinculos import validar_vinculos, pode_excluir_aluno
from relacoes_sqlite import demonstrar


def verificar():
    alunos = {41: "Lia"}
    planos = {7: "Mensal"}
    matriculas = [{"id": 101, "aluno_id": 41, "plano_id": 7}]

    # T01 — vínculo válido e identidade estável após alteração do nome.
    assert validar_vinculos(alunos, planos, matriculas) is True
    alunos[41] = "Lia Silva"
    assert validar_vinculos(alunos, planos, matriculas) is True
    print("T01 — IDs válidos e nome alterado sem romper vínculo: OK")

    # T02 — aluno/plano ausente recusado, sem alterar coleções.
    snapshot = (dict(alunos), dict(planos), [dict(m) for m in matriculas])
    for caso in (
        [{"id": 102, "aluno_id": 99, "plano_id": 7}],
        [{"id": 103, "aluno_id": 41, "plano_id": 88}],
    ):
        try:
            validar_vinculos(alunos, planos, caso)
        except ValueError:
            pass
        else:
            raise AssertionError("Referência ausente deveria ser recusada.")
    assert (alunos, planos, matriculas) == snapshot
    print("T02 — aluno/plano ausente recusado sem alterar dados: OK")

    # T03 — IDs duplicados, booleanos e negativos recusados.
    casos_invalidos = [
        ([{"id": 1, "nome": "A"}, {"id": 1, "nome": "B"}], {7: "P"},
         [{"id": 1, "aluno_id": 1, "plano_id": 7}]),
        ({True: "A"}, {7: "P"}, [{"id": 1, "aluno_id": 1, "plano_id": 7}]),
        ({-1: "A"}, {7: "P"}, [{"id": 1, "aluno_id": -1, "plano_id": 7}]),
        ({1: "A"}, {7: "P"}, [
            {"id": 1, "aluno_id": 1, "plano_id": 7},
            {"id": 1, "aluno_id": 1, "plano_id": 7},
        ]),
    ]
    for args in casos_invalidos:
        try:
            validar_vinculos(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("ID inválido/duplicado deveria ser recusado.")
    print("T03 — IDs booleanos/negativos e duplicados recusados: OK")

    # T04 — contrato impede exclusão lógica de aluno vinculado.
    assert pode_excluir_aluno(41, matriculas) is False
    assert pode_excluir_aluno(92, matriculas) is True
    print("T04 — exclusão vinculada identificada pelo contrato: OK")

    # T05/T06 — SQLite com FK + RESTRICT e preservação após erro.
    resultado = demonstrar()
    assert resultado["foreign_keys_ativo"] is True
    assert resultado["vinculo_apos_nome"] is True
    assert resultado["recusou_referencia_orfa"] is True
    assert resultado["recusou_exclusao_restrict"] is True
    assert resultado["aluno_preservado"] is True
    assert resultado["matricula_preservada"] is True
    assert resultado["integridade"] == "ok"
    print("T05 — SQLite recusou referência órfã e exclusão vinculada: OK")
    print("T06 — rollback preservou aluno e matrícula; integridade ok: OK")

    # T08 — teste de reprodução dos módulos a partir da própria pasta A20.
    raiz = Path(__file__).resolve().parent
    for script in ("vinculos.py", "relacoes_sqlite.py"):
        proc = subprocess.run(
            [sys.executable, "-B", str(raiz / script)],
            cwd=raiz, capture_output=True, text=True
        )
        assert proc.returncode == 0, proc.stderr
    print("T08 — módulos executados por subprocesso a partir da pasta A20: OK")

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")

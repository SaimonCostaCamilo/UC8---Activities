"""A20 — testes da lógica, do repositório integrado e das restrições SQLite."""
from pathlib import Path
import tempfile
from vinculos import validar_vinculos, pode_excluir_aluno
from relacoes_sqlite import demonstrar
from repositorio_relacional import RepositorioRelacional

def verificar():
    alunos={41:'Lia'}; planos={7:'Mensal'}; matriculas=[{'id':101,'aluno_id':41,'plano_id':7}]
    assert validar_vinculos(alunos,planos,matriculas) is True
    alunos[41]='Lia Silva'; assert validar_vinculos(alunos,planos,matriculas) is True
    print('T01 — IDs válidos e nome alterado sem romper vínculo: OK')
    antes=(dict(alunos),dict(planos),[dict(m) for m in matriculas])
    for caso in ([{'id':102,'aluno_id':99,'plano_id':7}],[{'id':103,'aluno_id':41,'plano_id':88}]):
        try: validar_vinculos(alunos,planos,caso)
        except ValueError: pass
        else: raise AssertionError('Referência inexistente deveria ser recusada.')
    assert (alunos,planos,matriculas)==antes
    print('T02 — aluno/plano inexistente recusado sem alterar dados: OK')
    invalidos=[([{'id':1},{'id':1}],{7:'P'},[]),({True:'A'},{7:'P'},[]),({-1:'A'},{7:'P'},[]),({1:'A'},{7:'P'},[{'id':1,'aluno_id':1,'plano_id':7},{'id':1,'aluno_id':1,'plano_id':7}])]
    for args in invalidos:
        try: validar_vinculos(*args)
        except ValueError: pass
        else: raise AssertionError('ID inválido/duplicado aceito.')
    print('T03 — IDs booleanos, negativos e duplicados recusados: OK')
    assert pode_excluir_aluno(41,matriculas) is False and pode_excluir_aluno(92,matriculas) is True
    print('T04 — contrato bloqueia exclusão lógica vinculada: OK')
    resumo=demonstrar()
    assert all([resumo['foreign_keys_ativo'],resumo['vinculo_apos_nome'],resumo['recusou_referencia_orfa'],resumo['recusou_exclusao_restrict'],resumo['aluno_preservado'],resumo['matricula_preservada'],resumo['integridade']=='ok'])
    print('T05/T06 — FK, RESTRICT e rollback preservam os registros: OK')
    with tempfile.TemporaryDirectory(prefix='a20_repo_') as tmp:
        repo=RepositorioRelacional(Path(tmp)/'academia.db')
        aid=repo.adicionar_aluno('Lia Fictícia'); pid=repo.adicionar_plano('Mensal',9900)
        mid=repo.adicionar_matricula(aid,pid)
        assert repo.listar_matriculas()==[(mid,aid,'Lia Fictícia',pid,'Mensal')]
        try: repo.adicionar_matricula(999,pid)
        except ValueError: pass
        else: raise AssertionError('Repositório aceitou aluno inexistente.')
        try: repo.excluir_aluno(aid)
        except ValueError: pass
        else: raise AssertionError('Repositório excluiu aluno vinculado.')
        assert len(repo.listar_alunos())==1 and len(repo.listar_matriculas())==1
        try: repo.excluir_plano(pid)
        except ValueError: pass
        else: raise AssertionError('Repositório excluiu plano vinculado.')
        assert repo.listar_planos()[0][0]==pid
        with repo.conectar() as con: assert con.execute('PRAGMA foreign_keys').fetchone()[0]==1
    print('T07 — aplicação integrada: cadastro, matrícula e exclusões protegidas: OK')
    return True

if __name__=='__main__':
    assert verificar()
    print('Todos os testes A20 passaram.')

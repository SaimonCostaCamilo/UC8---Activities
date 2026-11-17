"""A20 — comparação entre validação em memória e chave estrangeira SQLite."""
from contextlib import closing
import sqlite3
import tempfile
from pathlib import Path


def _conectar(caminho):
    con = sqlite3.connect(caminho)
    # A configuração é por conexão e precisa ocorrer antes das operações.
    con.execute("PRAGMA foreign_keys = ON")
    return con


def demonstrar():
    """Executa cenários em banco temporário fictício e devolve resumo verificável."""
    with tempfile.TemporaryDirectory(prefix="a20_sqlite_") as pasta:
        banco = Path(pasta) / "vinculos-ficticios.db"
        with closing(_conectar(banco)) as con:
            assert con.execute("PRAGMA foreign_keys").fetchone()[0] == 1
            con.executescript("""
                CREATE TABLE alunos (
                    id INTEGER PRIMARY KEY CHECK (id > 0),
                    nome TEXT NOT NULL
                );
                CREATE TABLE planos (
                    id INTEGER PRIMARY KEY CHECK (id > 0),
                    nome TEXT NOT NULL
                );
                CREATE TABLE matriculas (
                    id INTEGER PRIMARY KEY CHECK (id > 0),
                    aluno_id INTEGER NOT NULL,
                    plano_id INTEGER NOT NULL,
                    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE RESTRICT,
                    FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE RESTRICT
                );
            """)
            con.execute("INSERT INTO alunos VALUES (41, 'Lia')")
            con.execute("INSERT INTO planos VALUES (7, 'Mensal')")
            con.execute("INSERT INTO matriculas VALUES (101, 41, 7)")
            con.commit()

            # Mudar o nome não altera o ID nem rompe o vínculo.
            con.execute("UPDATE alunos SET nome = 'Lia Silva' WHERE id = 41")
            nome_atualizado = con.execute(
                "SELECT nome FROM alunos WHERE id = 41"
            ).fetchone()[0]
            vinculo_apos_nome = con.execute("""
                SELECT COUNT(*) FROM matriculas m
                JOIN alunos a ON a.id = m.aluno_id
                JOIN planos p ON p.id = m.plano_id
                WHERE m.id = 101
            """).fetchone()[0] == 1

            # Referência órfã é recusada pelo SQLite.
            recusou_orfao = False
            try:
                con.execute("INSERT INTO matriculas VALUES (102, 99, 7)")
                con.commit()
            except sqlite3.IntegrityError:
                con.rollback()
                recusou_orfao = True

            # RESTRICT impede apagar aluno ainda usado por matrícula.
            recusou_exclusao = False
            try:
                con.execute("DELETE FROM alunos WHERE id = 41")
                con.commit()
            except sqlite3.IntegrityError:
                con.rollback()
                recusou_exclusao = True

            aluno_preservado = con.execute(
                "SELECT COUNT(*) FROM alunos WHERE id = 41"
            ).fetchone()[0] == 1
            matricula_preservada = con.execute(
                "SELECT COUNT(*) FROM matriculas WHERE id = 101"
            ).fetchone()[0] == 1
            integridade = con.execute("PRAGMA integrity_check").fetchone()[0]

        resultado = {
            "foreign_keys_ativo": True,
            "nome_atualizado": nome_atualizado,
            "vinculo_apos_nome": vinculo_apos_nome,
            "recusou_referencia_orfa": recusou_orfao,
            "recusou_exclusao_restrict": recusou_exclusao,
            "aluno_preservado": aluno_preservado,
            "matricula_preservada": matricula_preservada,
            "integridade": integridade,
        }
        print("SQLite A20:")
        for chave, valor in resultado.items():
            print(f"{chave} -> {valor}")
        return resultado


if __name__ == "__main__":
    demonstrar()

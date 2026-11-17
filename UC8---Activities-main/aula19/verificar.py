"""A19 — verificações reproduzíveis com bancos SQLite exclusivamente fictícios."""
from pathlib import Path
import sqlite3
import tempfile

from backup_sqlite import criar_backup


def criar_base_ficticia(caminho):
    with sqlite3.connect(caminho) as con:
        con.execute("""CREATE TABLE vendas (
            id INTEGER PRIMARY KEY, cliente TEXT NOT NULL, total_centavos INTEGER NOT NULL
        )""")
        con.executemany(
            "INSERT INTO vendas(id, cliente, total_centavos) VALUES (?, ?, ?)",
            [(501, "Lia Fictícia", 2350), (502, "Rui Fictício", 4100)],
        )


def verificar():
    with tempfile.TemporaryDirectory(prefix="a19_ensaio_") as pasta:
        pasta = Path(pasta)
        origem = pasta / "origem-ficticia.db"
        copia = pasta / "copia-nova.db"
        criar_base_ficticia(origem)

        # T05 — destino novo; a cópia é aberta por outra conexão e consultada.
        esperado = [(501, "Lia Fictícia", 2350), (502, "Rui Fictício", 4100)]
        resultado = criar_backup(origem, copia)
        assert resultado == copia.resolve()
        with sqlite3.connect(copia) as con_copia:
            assert con_copia.execute("PRAGMA integrity_check").fetchone() == ("ok",)
            observado = con_copia.execute(
                "SELECT id, cliente, total_centavos FROM vendas ORDER BY id"
            ).fetchall()
        assert observado == esperado
        print("T05 — destino novo, backup API, integridade e registros conhecidos: OK")

        # A origem continua intacta.
        with sqlite3.connect(origem) as con_origem:
            origem_observada = con_origem.execute(
                "SELECT id, cliente, total_centavos FROM vendas ORDER BY id"
            ).fetchall()
        assert origem_observada == esperado
        print("T05 — origem preservada após a cópia: OK")

        # T05 — não sobrescreve uma cópia já existente.
        conteudo_anterior = copia.read_bytes()
        try:
            criar_backup(origem, copia)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Era esperado recusar destino existente.")
        assert copia.read_bytes() == conteudo_anterior
        print("T05 — destino existente recusado e bytes anteriores preservados: OK")

        # T06 — origem ausente é recusada e não cria destino.
        ausente = pasta / "nao-existe.db"
        destino_ausente = pasta / "nao-deve-ser-criado.db"
        try:
            criar_backup(ausente, destino_ausente)
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Era esperado recusar origem ausente.")
        assert not destino_ausente.exists()
        print("T06 — origem ausente recusada sem criar banco vazio: OK")

        # T07 — caminhos iguais são recusados.
        try:
            criar_backup(origem, origem)
        except ValueError:
            pass
        else:
            raise AssertionError("Era esperado recusar origem igual ao destino.")
        assert origem_observada == esperado
        print("T07 — origem igual ao destino recusada; dados originais intactos: OK")

    return True


if __name__ == "__main__":
    if verificar():
        print("Todos os testes A19 passaram.")

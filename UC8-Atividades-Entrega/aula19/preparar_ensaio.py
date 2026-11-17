"""Cria uma base de demonstração fictícia; recusa sobrescrever o arquivo."""
from pathlib import Path
import sqlite3

CAMINHO = Path(__file__).resolve().parent / "dados-ensaio" / "sorveteria-ficticia.db"


def main():
    CAMINHO.parent.mkdir(parents=True, exist_ok=True)
    if CAMINHO.exists():
        raise FileExistsError(
            f"{CAMINHO} já existe. Preserve-o; escolha outro caminho ou mova-o manualmente."
        )
    with sqlite3.connect(CAMINHO) as con:
        con.execute("""CREATE TABLE vendas (
            id INTEGER PRIMARY KEY, cliente TEXT NOT NULL, total_centavos INTEGER NOT NULL
        )""")
        con.executemany(
            "INSERT INTO vendas VALUES (?, ?, ?)",
            [(801, "Ana de Ensaio", 1890), (802, "Caio de Ensaio", 2750)],
        )
    print(f"Base fictícia criada: {CAMINHO}")


if __name__ == "__main__":
    main()

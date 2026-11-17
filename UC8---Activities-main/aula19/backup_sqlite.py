"""A19 — backup SQLite seguro: origem existente e destino obrigatoriamente novo."""
from pathlib import Path
import argparse
import sqlite3


def criar_backup(origem, destino):
    """Copia a base usando Connection.backup; nunca sobrescreve destino existente."""
    origem = Path(origem).expanduser().resolve()
    destino = Path(destino).expanduser().resolve()

    if origem == destino:
        raise ValueError("Origem e destino precisam ser caminhos diferentes.")
    if not origem.is_file():
        raise FileNotFoundError(f"Banco de origem não encontrado: {origem}")
    if destino.exists():
        raise FileExistsError(f"O destino já existe e será preservado: {destino}")

    destino.parent.mkdir(parents=True, exist_ok=True)
    entrada = None
    saida = None
    destino_reservado = False
    try:
        # Criação exclusiva: se outro processo criar o destino neste intervalo,
        # open("xb") falha em vez de permitir sobrescrita.
        with destino.open("xb"):
            destino_reservado = True
        entrada = sqlite3.connect(f"file:{origem.as_posix()}?mode=ro", uri=True)
        saida = sqlite3.connect(str(destino))
        entrada.backup(saida)
        resultado = saida.execute("PRAGMA integrity_check").fetchone()
        if not resultado or resultado[0] != "ok":
            raise sqlite3.DatabaseError(f"Falha na integridade da cópia: {resultado}")
        saida.close()
        saida = None
    except Exception:
        if saida is not None:
            saida.close()
            saida = None
        # Remove somente o destino que esta execução acabou de criar.
        if destino_reservado and destino.exists():
            destino.unlink()
        raise
    finally:
        if entrada is not None:
            entrada.close()
    return destino


def main():
    parser = argparse.ArgumentParser(
        description="Cria uma cópia SQLite em um destino novo, sem alterar a origem."
    )
    parser.add_argument("origem", help="caminho do banco SQLite existente")
    parser.add_argument("destino", help="caminho novo para a cópia")
    args = parser.parse_args()
    try:
        caminho = criar_backup(args.origem, args.destino)
    except (OSError, ValueError, sqlite3.Error) as erro:
        parser.exit(2, f"Erro: {erro}\n")
    print(f"Backup criado e integridade conferida: {caminho}")


if __name__ == "__main__":
    main()

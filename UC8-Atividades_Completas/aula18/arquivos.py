# A18 — Apoio: leitura, validação e gravação segura de catálogo JSON
from pathlib import Path
import json
import os
import tempfile


CHAVES_CATALOGO = {"id", "nome", "preco_centavos"}


def validar_catalogo(dados):
    """Valida e devolve uma lista de registros simples compatíveis com o contrato."""
    if not isinstance(dados, list):
        raise ValueError("O catálogo precisa ser uma lista JSON.")

    ids = set()
    catalogo_validado = []
    for indice, registro in enumerate(dados, start=1):
        if not isinstance(registro, dict):
            raise ValueError(f"O item {indice} precisa ser um objeto JSON.")
        if set(registro.keys()) != CHAVES_CATALOGO:
            raise ValueError(
                f"O item {indice} deve conter somente as chaves: id, nome e preco_centavos."
            )

        identificador = registro["id"]
        nome = registro["nome"]
        preco = registro["preco_centavos"]

        # bool é subclasse de int em Python; por isso é rejeitado explicitamente.
        if isinstance(identificador, bool) or not isinstance(identificador, int) or identificador <= 0:
            raise ValueError(f"O ID do item {indice} deve ser um inteiro positivo.")
        if identificador in ids:
            raise ValueError(f"ID repetido no catálogo: {identificador}.")
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError(f"O nome do item {indice} precisa conter texto.")
        if isinstance(preco, bool) or not isinstance(preco, int) or preco <= 0:
            raise ValueError(f"O preço do item {indice} deve ser um inteiro positivo em centavos.")

        ids.add(identificador)
        catalogo_validado.append({
            "id": identificador,
            "nome": nome.strip(),
            "preco_centavos": preco,
        })

    return catalogo_validado


def ler_catalogo(caminho):
    """Lê um catálogo UTF-8; arquivo ausente retorna [] sem criar arquivo."""
    destino = Path(caminho)
    try:
        conteudo = destino.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    except (OSError, UnicodeError) as erro:
        raise OSError(f"Não foi possível ler o catálogo: {erro}") from erro

    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as erro:
        raise ValueError(f"JSON inválido na linha {erro.lineno}, coluna {erro.colno}.") from erro

    return validar_catalogo(dados)


def salvar_catalogo(caminho, dados):
    """Valida e grava atomicamente em UTF-8 usando temporário no mesmo diretório."""
    catalogo = validar_catalogo(dados)  # validar antes de tocar no destino
    destino = Path(caminho)
    temporario = None

    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=destino.parent,
            prefix=f".{destino.name}.", suffix=".tmp", delete=False
        ) as arquivo_temp:
            temporario = Path(arquivo_temp.name)
            json.dump(catalogo, arquivo_temp, ensure_ascii=False, indent=4)
            arquivo_temp.write("\n")
            arquivo_temp.flush()
            os.fsync(arquivo_temp.fileno())

        os.replace(temporario, destino)
        temporario = None
        return destino
    except (OSError, TypeError, ValueError) as erro:
        raise OSError(f"Não foi possível salvar o catálogo: {erro}") from erro
    finally:
        if temporario is not None:
            try:
                temporario.unlink(missing_ok=True)
            except OSError:
                pass

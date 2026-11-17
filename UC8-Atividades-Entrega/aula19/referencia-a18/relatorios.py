# A18 — Exportação segura de comprovantes em CSV
import csv
import os
import tempfile
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


CABECALHOS = [
    "id",
    "nome",
    "quantidade",
    "preco_unitario_centavos",
    "subtotal_centavos",
    "forma_pagamento",
    "total_pedido_reais",
]


def _inteiro_positivo(valor, campo):
    """Valida inteiros positivos sem aceitar bool."""
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValueError(f"O campo {campo} precisa ser um inteiro positivo.")
    return valor


def validar_comprovante(comprovante):
    """
    Confere o retrato produzido por Pedido.finalizar.
    Não recebe widgets nem consulta a montagem atual.
    """
    if not isinstance(comprovante, dict):
        raise ValueError("Não existe comprovante confirmado para exportar.")

    itens = comprovante.get("itens")
    if not isinstance(itens, list) or not itens:
        raise ValueError("O comprovante precisa conter ao menos um item.")

    forma = comprovante.get("forma_pagamento")
    if not isinstance(forma, str) or not forma.strip():
        raise ValueError("O comprovante não possui forma de pagamento.")

    total_itens = _inteiro_positivo(comprovante.get("total_centavos"), "total_centavos")
    total_exportado = comprovante.get("total_pagamento_centavos", total_itens)
    _inteiro_positivo(total_exportado, "total_pagamento_centavos")

    soma = 0
    itens_validos = []
    for indice, item in enumerate(itens, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"O item {indice} do comprovante é inválido.")

        codigo = item.get("codigo", item.get("id"))
        nome = item.get("nome")
        if codigo is None or not str(codigo).strip():
            raise ValueError(f"O item {indice} não possui ID.")
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError(f"O nome do item {indice} está vazio.")

        quantidade = _inteiro_positivo(item.get("quantidade"), "quantidade")
        preco = _inteiro_positivo(item.get("preco_unitario"), "preco_unitario")
        subtotal = _inteiro_positivo(item.get("subtotal"), "subtotal")
        if subtotal != preco * quantidade:
            raise ValueError(f"O subtotal do item {indice} não corresponde ao preço e à quantidade.")

        soma += subtotal
        itens_validos.append({
            "id": str(codigo),
            "nome": nome.strip(),
            "quantidade": quantidade,
            "preco_unitario_centavos": preco,
            "subtotal_centavos": subtotal,
        })

    if soma != total_itens:
        raise ValueError("O total do comprovante não corresponde à soma dos itens.")

    return {
        "itens": itens_validos,
        "forma_pagamento": forma.strip(),
        "total_pedido_centavos": total_exportado,
    }


def _reais_com_virgula(centavos):
    """Formata centavos inteiros em reais com duas casas e vírgula decimal."""
    valor = (Decimal(centavos) / Decimal(100)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return f"{valor:.2f}".replace(".", ",")


def linhas_relatorio(comprovante):
    """Converte o comprovante confirmado em linhas prontas para CSV."""
    retrato = validar_comprovante(comprovante)
    linhas = []
    for item in retrato["itens"]:
        linhas.append([
            item["id"],
            item["nome"],
            item["quantidade"],
            item["preco_unitario_centavos"],
            item["subtotal_centavos"],
            retrato["forma_pagamento"],
            _reais_com_virgula(retrato["total_pedido_centavos"]),
        ])
    return linhas


def exportar_csv(comprovante, caminho=None):
    """
    Exporta um comprovante confirmado em UTF-8 com BOM e delimitador ';'.
    Usa temporário no mesmo diretório e os.replace para preservar o destino
    anterior se a gravação falhar.
    """
    # Compatibilidade: a A17 também apresenta a assinatura caminho, comprovante.
    if isinstance(comprovante, (str, Path)) and isinstance(caminho, dict):
        comprovante, caminho = caminho, comprovante
    if caminho is None or not str(caminho).strip():
        raise ValueError("Exportação cancelada ou caminho não informado.")

    linhas = linhas_relatorio(comprovante)
    destino = Path(caminho)
    temporario = None

    try:
        # Não cria diretórios automaticamente: um destino inexistente deve falhar.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            dir=destino.parent,
            prefix=f".{destino.name}.",
            suffix=".tmp",
            delete=False,
        ) as arquivo_temp:
            temporario = Path(arquivo_temp.name)
            escritor = csv.writer(arquivo_temp, delimiter=";", lineterminator="\n")
            escritor.writerow(CABECALHOS)
            escritor.writerows(linhas)
            arquivo_temp.flush()
            os.fsync(arquivo_temp.fileno())

        os.replace(temporario, destino)
        temporario = None
        return destino
    except (OSError, csv.Error, UnicodeError) as erro:
        raise OSError(f"Não foi possível exportar o relatório CSV: {erro}") from erro
    finally:
        if temporario is not None:
            try:
                temporario.unlink(missing_ok=True)
            except OSError:
                pass


def ler_relatorio(caminho):
    """Lê o CSV de volta com DictReader, removendo o BOM UTF-8 se existir."""
    try:
        with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=";")
            if leitor.fieldnames != CABECALHOS:
                raise ValueError("Cabeçalho CSV diferente do contrato A13.")
            linhas = list(leitor)
    except (OSError, UnicodeError, csv.Error) as erro:
        raise OSError(f"Não foi possível ler o relatório CSV: {erro}") from erro

    if not linhas:
        raise ValueError("O relatório CSV não contém linhas de venda.")
    return linhas

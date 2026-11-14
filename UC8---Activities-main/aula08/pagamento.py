# A08: assinaturas de apoio; traga sua implementação anterior.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}

def valor_monetario(texto, permitir_zero=True):
    """TODO A08: implemente valor_monetario conforme o contrato e reutilize seu código anterior."""
    if texto is None:
        raise ValueError("O valor monetário não pode ser nulo.")

    if isinstance(texto, (Decimal, int, float)):
        texto_str = str(texto)
    else:
        texto_str = str(texto).strip()

    if not texto_str:
        raise ValueError("O texto monetário não pode estar vazio.")

    limpo = texto_str.replace("R$", "").strip()
    limpo = limpo.replace(".", "").replace(",", ".") if "," in limpo and "." in limpo else limpo.replace(",", ".")

    try:
        valor = Decimal(limpo)
    except (InvalidOperation, ValueError):
        raise ValueError("O valor monetário deve ser um número válido.")

    if valor < 0:
        raise ValueError("O valor monetário não pode ser negativo.")

    if not permitir_zero and valor == 0:
        raise ValueError("O valor monetário deve ser maior que zero.")

    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def calcular_pagamento(subtotal_texto, forma):
    """TODO A08: implemente calcular_pagamento conforme o contrato e reutilize seu código anterior."""
    subtotal = valor_monetario(subtotal_texto, permitir_zero=True)

    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento inválida ou ausente: '{forma}'.")

    fator = Decimal(FATORES[forma])
    total = (subtotal * fator).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    desconto = (subtotal - total).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

    return {
        "subtotal": subtotal,
        "forma": forma,
        "fator": fator,
        "total": total,
        "desconto": desconto
    }

def preco_para_centavos(texto):
    """TODO A08: implemente preco_para_centavos conforme o contrato e reutilize seu código anterior."""
    valor_dec = valor_monetario(texto, permitir_zero=True)
    return int((valor_dec * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
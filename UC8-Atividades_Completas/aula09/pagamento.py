# A09: assinaturas de apoio; traga sua implementação anterior.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {'Dinheiro': '0.87', 'PIX': '0.87','Débito': '0.92', 'Crédito 1x': '1.00'}

def valor_monetario(texto, permitir_zero=True):
    """TODO A09: implemente valor_monetario conforme o contrato e reutilize seu código anterior."""
    if texto is None:
        raise ValueError("O valor monetário não pode ser nulo.")

    texto_str = str(texto).strip()
    if not texto_str:
        raise ValueError("O valor monetário não pode estar vazio.")

    limpo = texto_str.replace("R$", "").replace("r$", "").strip()

    if "." in limpo and "," in limpo:
        normalizado = limpo.replace(".", "").replace(",", ".")
    else:
        normalizado = limpo.replace(",", ".")

    try:
        dec = Decimal(normalizado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Formato monetário inválido: '{texto}'")

    if not permitir_zero and dec <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    if dec < 0:
        raise ValueError("O valor monetário não pode ser negativo.")

    return dec

def calcular_pagamento(subtotal_texto, forma):
    """TODO A09: implemente calcular_pagamento conforme o contrato e reutilize seu código anterior."""
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento desconhecida ou inválida: '{forma}'")

    subtotal_dec = valor_monetario(subtotal_texto, permitir_zero=True)
    fator = Decimal(FATORES[forma])

    total_calculado = (subtotal_dec * fator).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    desconto_calculado = (subtotal_dec - total_calculado).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        'forma': forma,
        'subtotal': subtotal_dec,
        'desconto': desconto_calculado,
        'total': total_calculado
    }

def preco_para_centavos(texto):
    """TODO A09: implemente preco_para_centavos conforme o contrato e reutilize seu código anterior."""
    dec = valor_monetario(texto, permitir_zero=True)
    return int((dec * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

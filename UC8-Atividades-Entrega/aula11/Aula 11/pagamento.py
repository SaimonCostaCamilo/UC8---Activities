# A11: Módulo de pagamento, interpretação monetária e cálculo de descontos
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}

def valor_monetario(texto, permitir_zero=True):
    """
    Interpreta um texto de valor monetário, convertendo para Decimal com duas casas.
    Retorna o valor ou lança ValueError se for inválido.
    """
    if texto is None:
        raise ValueError("O texto do valor monetário não pode ser None.")
    
    texto_limpo = str(texto).strip()
    if not texto_limpo:
        raise ValueError("O texto do valor monetário não pode ser vazio.")
    
    # Remove símbolos de moeda e substitui vírgula por ponto se necessário
    texto_limpo = re.sub(r'[^\d.,]', '', texto_limpo)
    
    if ',' in texto_limpo and '.' in texto_limpo:
        # Se ambos existem, assume que o último é o separador decimal
        if texto_limpo.rfind(',') > texto_limpo.rfind('.'):
            texto_limpo = texto_limpo.replace('.', '').replace(',', '.')
        else:
            texto_limpo = texto_limpo.replace(',', '')
    elif ',' in texto_limpo:
        texto_limpo = texto_limpo.replace(',', '.')

    try:
        valor = Decimal(texto_limpo)
    except InvalidOperation as e:
        raise ValueError(f"Valor monetário inválido: {texto}") from e

    if valor < 0:
        raise ValueError("O valor monetário não pode ser negativo.")
    
    if not permitir_zero and valor == 0:
        raise ValueError("O valor monetário deve ser maior que zero.")

    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def preco_para_centavos(texto):
    """Converte um texto de preço monetário para um inteiro representando centavos."""
    valor = valor_monetario(texto, permitir_zero=True)
    return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def calcular_pagamento(subtotal_texto, forma):
    """
    Calcula o valor final após aplicar o fator correspondente à forma de pagamento.
    Retorna um dicionário contendo o subtotal, o fator aplicado e o total calculado.
    """
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento desconhecida: {forma}")

    subtotal = valor_monetario(subtotal_texto, permitir_zero=False)
    fator = Decimal(FATORES[forma])
    
    total = (subtotal * fator).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return {
        "subtotal": subtotal,
        "fator": fator,
        "total": total,
        "forma": forma
    }
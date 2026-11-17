# A10: Implementação de interpretação monetária e cálculo de pagamentos com Decimal.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {
    'Dinheiro': '0.87', 
    'PIX': '0.87', 
    'Débito': '0.92', 
    'Crédito 1x': '1.00'
}

def valor_monetario(texto, permitir_zero=True):
    """
    Converte um texto em um objeto Decimal válido para valores monetários,
    verificando formato e limites (positivo ou zero, dependendo de permitir_zero).
    """
    if texto is None:
        raise ValueError("O texto do valor não pode ser nulo.")
    
    # Se já for Decimal ou número, normaliza para string limpa
    if isinstance(texto, (int, float)):
        texto_limpo = str(texto)
    elif isinstance(texto, Decimal):
        texto_limpo = str(texto)
    elif isinstance(texto, str):
        texto_limpo = texto.strip()
    else:
        raise ValueError("Tipo de dado inválido para valor monetário.")

    # Remove símbolos de moeda comuns, se houver
    texto_limpo = re.sub(r'^[R\$]?\s*', '', texto_limpo)
    
    # Substitui vírgula por ponto para o parse decimal padrão, se necessário
    if ',' in texto_limpo and '.' in texto_limpo:
        # Formato brasileiro provável: 1.234,56
        texto_limpo = texto_limpo.replace('.', '').replace(',', '.')
    elif ',' in texto_limpo:
        # Apenas vírgula: 47,00
        texto_limpo = texto_limpo.replace(',', '.')

    try:
        valor = Decimal(texto_limpo)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Formato de valor monetário inválido: '{texto}'")

    if valor < 0:
        raise ValueError("O valor monetário não pode ser negativo.")

    if not permitir_zero and valor == 0:
        raise ValueError("O valor monetário não pode ser zero.")

    # Quantiza para 2 casas decimais usando ROUND_HALF_UP
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def preco_para_centavos(texto):
    """
    Converte um texto de preço monetário (ex: 'R$ 47,00' ou '47.00') para um inteiro em centavos.
    """
    valor = valor_monetario(texto, permitir_zero=True)
    # Multiplica por 100 e converte para inteiro
    return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def calcular_pagamento(subtotal_texto, forma):
    """
    Calcula o valor do pagamento aplicando o fator de desconto/acréscimo 
    correspondente à forma de pagamento escolhida.
    """
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento inválida: '{forma}'. Escolha entre: {', '.join(FATORES.keys())}")

    subtotal = valor_monetario(subtotal_texto, permitir_zero=False)
    fator = Decimal(FATORES[forma])

    total_calculado = (subtotal * fator).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return total_calculado
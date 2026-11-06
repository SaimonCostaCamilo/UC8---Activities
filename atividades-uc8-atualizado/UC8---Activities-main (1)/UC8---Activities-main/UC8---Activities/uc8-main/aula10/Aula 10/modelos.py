# A10: Implementação do modelo de pedido, pizza e bebida com contratos reutilizados.
import re

def quantidade(texto):
    """Converte e valida o texto da quantidade para um número inteiro positivo."""
    if isinstance(texto, int):
        if texto <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        return texto
    
    if not isinstance(texto, str):
        raise ValueError("Quantidade inválida.")
    
    texto_limpo = texto.strip()
    if not re.fullmatch(r'\d+', texto_limpo):
        raise ValueError("Quantidade deve conter apenas dígitos.")
    
    qtd = int(texto_limpo)
    if qtd <= 0:
        raise ValueError("Quantidade deve ser maior que zero.")
    return qtd


def formatar(centavos):
    """Formata um valor em centavos para o padrão monetário brasileiro (R$)."""
    if not isinstance(centavos, (int, float)):
        raise ValueError("Valor em centavos inválido.")
    reais = centavos / 100
    return f"R$ {reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = str(codigo).strip()
        self.nome = str(nome).strip()
        if not self.codigo or not self.nome:
            raise ValueError("Código e nome do produto não podem ser vazios.")
        
        try:
            self.preco_centavos = int(preco_centavos)
        except (ValueError, TypeError):
            raise ValueError("Preço em centavos deve ser um número inteiro.")
        
        if self.preco_centavos < 0:
            raise ValueError("O preço não pode ser negativo.")


class Pizza:
    TAMANHOS_VALIDOS = {"Média", "Grande"}

    def __init__(self, codigo, nome, tamanho, preco_centavos):
        self.codigo = str(codigo).strip()
        self.nome = str(nome).strip()
        
        if tamanho not in self.TAMANHOS_VALIDOS:
            raise ValueError(f"Tamanho inválido. Escolha entre: {', '.join(self.TAMANHOS_VALIDOS)}")
        self.tamanho = tamanho
        
        try:
            self.preco_centavos = int(preco_centavos)
        except (ValueError, TypeError):
            raise ValueError("Preço em centavos deve ser um número inteiro.")
        
        if self.preco_centavos < 0:
            raise ValueError("O preço não pode ser negativo.")


class Bebida:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = str(codigo).strip()
        self.nome = str(nome).strip()
        
        try:
            self.preco_centavos = int(preco_centavos)
        except (ValueError, TypeError):
            raise ValueError("Preço em centavos deve ser um número inteiro.")
        
        if self.preco_centavos < 0:
            raise ValueError("O preço não pode ser negativo.")


class Item:
    def __init__(self, produto, texto_quantidade):
        self.produto = produto  # Composição: armazena a instância de Produto, Pizza ou Bebida
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade


class Pedido:
    def __init__(self):
        self._itens = {}  # Dicionário mapeando codigo -> Item
        self.aberto = True

    def exigir_aberto(self):
        if not self.aberto:
            raise RuntimeError("O pedido está fechado e não pode ser modificado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        qtd = quantidade(texto_quantidade)
        
        if produto.codigo in self._itens:
            # Se já existe, atualiza a quantidade somando
            item_existente = self._itens[produto.codigo]
            nova_qtd = item_existente.quantidade + qtd
            item_existente.quantidade = nova_qtd
        else:
            self._itens[produto.codigo] = Item(produto, qtd)

    def total_centavos(self):
        return sum(item.subtotal() for item in self._itens.values())

    def linhas(self):
        resultado = []
        for item in self._itens.values():
            nome_exibicao = item.produto.nome
            if hasattr(item.produto, 'tamanho'):
                nome_exibicao += f" ({item.produto.tamanho})"
            resultado.append({
                "codigo": item.produto.codigo,
                "nome": nome_exibicao,
                "preco_unitario": item.produto.preco_centavos,
                "quantidade": item.quantidade,
                "subtotal": item.subtotal()
            })
        return resultado

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()
        codigo_str = str(codigo).strip()
        if codigo_str not in self._itens:
            raise KeyError("Item não encontrado no pedido.")
        
        qtd = quantidade(texto_quantidade)
        self._itens[codigo_str].quantidade = qtd

    def remover(self, codigo):
        self.exigir_aberto()
        codigo_str = str(codigo).strip()
        if codigo_str not in self._itens:
            raise KeyError("Item não encontrado no pedido.")
        del self._itens[codigo_str]
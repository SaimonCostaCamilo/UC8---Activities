# A09: assinaturas de apoio; traga sua implementação anterior.

def quantidade(texto):
    """TODO A09: implemente quantidade conforme o contrato e reutilize seu código anterior."""
    if texto is None:
        raise ValueError("A quantidade não pode ser nula.")
    texto_str = str(texto).strip()
    if not texto_str:
        raise ValueError("A quantidade não pode estar vazia.")
    try:
        qtd = int(texto_str)
    except (ValueError, TypeError):
        raise ValueError("A quantidade deve ser um número inteiro válido.")
    if qtd <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")
    return qtd

def formatar(centavos):
    """TODO A09: implemente formatar conforme o contrato e reutilize seu código anterior."""
    if not isinstance(centavos, int):
        try:
            centavos = int(centavos)
        except (ValueError, TypeError):
            raise ValueError("O valor em centavos deve ser um inteiro.")
    reais = centavos / 100
    return f"R$ {reais:,.2f}"

class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        """TODO A09: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        if not codigo or not str(codigo).strip():
            raise ValueError("O código do produto não pode ser vazio.")
        if not nome or not str(nome).strip():
            raise ValueError("O nome do produto não pode ser vazio.")
        try:
            preco = int(preco_centavos)
        except (ValueError, TypeError):
            raise ValueError("O preço em centavos deve ser um inteiro.")
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")

        self.codigo = str(codigo).strip()
        self.nome = str(nome).strip()
        self.preco_centavos = preco

class Item:

    def __init__(self, produto, texto_quantidade):
        """TODO A09: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        if not isinstance(produto, Produto):
            raise TypeError("O item requer uma instância válida de Produto.")
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        """TODO A09: implemente subtotal conforme o contrato e reutilize seu código anterior."""
        return self.produto.preco_centavos * self.quantidade
    
class Pedido:

    def __init__(self):
        """TODO A09: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        self._itens = {}
        self._aberto = True

    def exigir_aberto(self):
        """TODO A09: implemente exigir_aberto conforme o contrato e reutilize seu código anterior."""
        if not self._aberto:
            raise RuntimeError("O pedido está fechado e não pode ser modificado.")

    def adicionar(self, produto, texto_quantidade):
        """TODO A09: implemente adicionar conforme o contrato e reutilize seu código anterior."""
        self.exigir_aberto()
        qtd = quantidade(texto_quantidade)
        codigo = produto.codigo
        if codigo in self._itens:
            self._itens[codigo].quantidade += qtd
        else:
            self._itens[codigo] = Item(produto, qtd)

    def total_centavos(self):
        """TODO A09: implemente total_centavos conforme o contrato e reutilize seu código anterior."""
        return sum(item.subtotal() for item in self._itens.values())

    def linhas(self):
        """TODO A09: implemente linhas conforme o contrato e reutilize seu código anterior."""
        resultado = []
        for codigo, item in self._itens.items():
            resultado.append((
                codigo,
                item.produto.nome,
                formatar(item.produto.preco_centavos),
                item.quantidade,
                formatar(item.subtotal())
            ))
        return resultado

    def atualizar(self, codigo, texto_quantidade):
        """TODO A09: implemente atualizar conforme o contrato e reutilize seu código anterior."""
        self.exigir_aberto()
        codigo_str = str(codigo).strip()
        if codigo_str not in self._itens:
            raise KeyError(f"Produto com código '{codigo_str}' não encontrado no pedido.")
        nova_qtd = quantidade(texto_quantidade)
        self._itens[codigo_str].quantidade = nova_qtd

    def remover(self, codigo):
        """TODO A09: implemente remover conforme o contrato e reutilize seu código anterior."""
        self.exigir_aberto()
        codigo_str = str(codigo).strip()
        if codigo_str not in self._itens:
            raise KeyError(f"Produto com código '{codigo_str}' não encontrado no pedido.")
        del self._itens[codigo_str]

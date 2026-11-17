# A08: assinaturas de apoio; traga sua implementação anterior.
from math import isfinite

def quantidade(texto):
    """TODO A08: implemente quantidade conforme o contrato e reutilize seu código anterior."""
    try:
        texto_limpo = str(texto).strip().replace(",", ".")
        val = float(texto_limpo)
    except (ValueError, TypeError):
        raise ValueError("A quantidade deve ser um valor numérico válido.")

    if not isfinite(val) or val < 0 or not val.is_integer():
        raise ValueError("A quantidade deve ser um número inteiro maior ou igual a zero.")

    return int(val)

def formatar(centavos):
    """TODO A08: implemente formatar conforme o contrato e reutilize seu código anterior."""
    try:
        val = int(centavos)
    except (ValueError, TypeError):
        raise ValueError("O valor em centavos deve ser um número inteiro.")

    reais = val / 100.0
    return f"R$ {reais:,.2f}"

class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        """TODO A08: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        self._codigo = str(codigo).strip()
        self._nome = str(nome).strip()

        try:
            self._preco_centavos = int(preco_centavos)
        except (ValueError, TypeError):
            raise ValueError("O preço em centavos deve ser um número inteiro.")

        if self._preco_centavos < 0:
            raise ValueError("O preço em centavos não pode ser negativo.")

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    @property
    def preco_centavos(self):
        return self._preco_centavos

class Item:

    def __init__(self, produto, texto_quantidade):
        """TODO A08: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        if not isinstance(produto, Produto):
            raise TypeError("O item deve estar associado a uma instância válida de Produto.")

        self._produto = produto
        self._quantidade = quantidade(texto_quantidade)

    @property
    def produto(self):
        return self._produto

    @property
    def quantidade(self):
        return self._quantidade

    @property
    def preco_unitario(self):
        return self._produto.preco_centavos

    def subtotal(self):
        """TODO A08: implemente subtotal conforme o contrato e reutilize seu código anterior."""
        return self._produto.preco_centavos * self._quantidade

class Pedido:

    def __init__(self):
        """TODO A08: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        self._itens = {}
        self._aberto = True

    def exigir_aberto(self):
        """TODO A08: implemente exigir_aberto conforme o contrato e reutilize seu código anterior."""
        if not self._aberto:
            raise RuntimeError("O pedido já foi fechado e não pode ser alterado.")

    def adicionar(self, produto, texto_quantidade):
        """TODO A08: implemente adicionar conforme o contrato e reutilize seu código anterior."""
        self.exigir_aberto()

        if not isinstance(produto, Produto):
            raise TypeError("O argumento deve ser uma instância válida de Produto.")

        qtd_incremento = quantidade(texto_quantidade)
        if qtd_incremento == 0:
            return

        codigo = produto.codigo
        if codigo in self._itens:
            quantidade_atual = self._itens[codigo].quantidade
            nova_quantidade = quantidade_atual + qtd_incremento
            self._itens[codigo] = Item(produto, nova_quantidade)
        else:
            self._itens[codigo] = Item(produto, qtd_incremento)

    def total_centavos(self):
        """TODO A08: implemente total_centavos conforme o contrato e reutilize seu código anterior."""
        return sum(item.subtotal() for item in self._itens.values())

    def linhas(self):
        """TODO A08: implemente linhas conforme o contrato e reutilize seu código anterior."""
        resultado = []
        for item in self._itens.values():
            resultado.append({
                "codigo": item.produto.codigo,
                "nome": item.produto.nome,
                "preco_unitario": item.preco_unitario,
                "quantidade": item.quantidade,
                "subtotal": item.subtotal()
            })
        return resultado

# A07: assinaturas de apoio; traga sua implementação anterior.
def quantidade(texto):
    """TODO A07: implemente quantidade conforme o contrato e reutilize seu código anterior."""
    valor = int(str(texto).strip())
    if valor <= 0:
        raise ValueError("Quantidade deve ser maior que zero.")
    return valor

def formatar(centavos):
    """TODO A07: implemente formatar conforme o contrato e reutilize seu código anterior."""
    return f"R$ {centavos // 100},{centavos % 100:02d}"

class Produto:

    def __init__(self, codigo, nome, preco_centavos):
        """TODO A07: implemente __init__ conforme o contrato e reutilize seu código anterior."""
        codigo = str(codigo).strip()
        nome = str(nome).strip()
        if not codigo or not nome:
            raise ValueError("Codigo e nome nao podem ser vazios.")
        if not isinstance(preco_centavos, int) or preco_centavos <= 0:
            raise ValueError("Preco deve ser inteiro positivo em centavos.")
        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = preco_centavos

class Item:

    def __init__(self, produto, texto_quantidade):
        """TODO A07: implemente __init__ conforme o contrato e reutilize 
        seu código anterior."""
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        """TODO A07: implemente subtotal conforme o contrato e reutilize 
        seu código anterior."""
        return self.produto.preco_centavos * self.quantidade

class Pedido:

    def __init__(self):
        """TODO A07: implemente __init__ conforme o contrato e reutilize 
        seu código anterior."""
        self.itens = []
        self.aberto = True

    def exigir_aberto(self):
        """TODO A07: implemente exigir_aberto conforme o contrato e reutilize 
        seu código anterior."""
        if not self.aberto:
            raise RuntimeError("Pedido ja esta fechado.")

    def adicionar(self, produto, texto_quantidade):
        """TODO A07: implemente adicionar conforme o contrato e reutilize 
        seu código anterior."""
        self.exigir_aberto()
        for item in self.itens:
            if item.produto.codigo == produto.codigo:
                raise ValueError(f"Produto '{produto.codigo}' esta no pedido.")
        self.itens.append(Item(produto, texto_quantidade))

    def total_centavos(self):
        """TODO A07: implemente total_centavos conforme o contrato e reutilize 
        seu código anterior."""
        return sum(item.subtotal() for item in self.itens)

    def linhas(self):
        """TODO A07: implemente linhas conforme o contrato e reutilize 
        seu código anterior."""
        resultado = []
        for item in self.itens:
            resultado.append(
                f"{item.produto.codigo} {item.produto.nome} "
                f"x{item.quantidade} = {formatar(item.subtotal())}"
            )
        resultado.append(f"Total: {formatar(self.total_centavos())}")
        return resultado

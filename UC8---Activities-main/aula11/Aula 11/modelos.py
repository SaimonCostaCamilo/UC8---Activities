# A11: Modelo completo da Pizzaria — Estados, Cancelamento e Versão de Prévia
from decimal import Decimal, ROUND_HALF_UP
import copy

def quantidade(texto):
    """Converte e valida a quantidade informada em texto."""
    if not texto or not str(texto).strip():
        raise ValueError("A quantidade não pode ser vazia.")
    try:
        val = int(texto)
        if val <= 0:
            raise ValueError("A quantidade deve ser um número inteiro maior que zero.")
        return val
    except (ValueError, TypeError) as e:
        raise ValueError(f"Quantidade inválida: {texto}") from e

def formatar(centavos):
    """Formata um valor em centavos para o padrão monetário brasileiro (R$)."""
    if centavos is None:
        return "R$ 0,00"
    dec = Decimal(centavos) / Decimal(100)
    return f"R$ {dec.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"

class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = str(codigo)
        self.nome = str(nome)
        self.preco_centavos = int(preco_centavos)

class Pizza(Produto):
    def __init__(self, codigo, nome, tamanho, preco_centavos):
        super().__init__(codigo, nome, preco_centavos)
        self.tamanho = str(tamanho)

class Bebida(Produto):
    def __init__(self, codigo, nome, preco_centavos):
        super().__init__(codigo, nome, preco_centavos)

class Item:
    def __init__(self, produto, texto_quantidade):
        self.produto = produto
        self.qtd = quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.qtd

class Pedido:
    def __init__(self):
        self.estado = "montagem"  # Estados possíveis: "montagem" ou "finalizado"
        self.versao = 1           # Incrementado a cada modificação na montagem
        self._itens = {}          # Dicionário mapeando codigo -> Item
        self.comprovante = None   # Retrato independente gerado na confirmação

    def exigir_aberto(self):
        """Garante que o pedido está em estado de montagem e aceita edições."""
        if self.estado != "montagem":
            raise RuntimeError("Operação bloqueada: o pedido já foi finalizado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        qtd = quantidade(texto_quantidade)
        if produto.codigo in self._itens:
            self._itens[produto.codigo].qtd += qtd
        else:
            self._itens[produto.codigo] = Item(produto, str(qtd))
        self.versao += 1

    def total_centavos(self):
        return sum(item.subtotal() for item in self._itens.values())

    def linhas(self):
        """Retorna uma lista de dicionários estruturados com os itens atuais."""
        resultado = []
        for item in self._itens.values():
            resultado.append({
                "codigo": item.produto.codigo,
                "nome": item.produto.nome,
                "preco_unitario": item.produto.preco_centavos,
                "quantidade": item.qtd,
                "subtotal": item.subtotal()
            })
        return resultado

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()
        cod = str(codigo)
        if cod not in self._itens:
            raise KeyError("Produto não encontrado no carrinho.")
        qtd = quantidade(texto_quantidade)
        self._itens[cod].qtd = qtd
        self.versao += 1

    def remover(self, codigo):
        self.exigir_aberto()
        cod = str(codigo)
        if cod in self._itens:
            del self._itens[cod]
            self.versao += 1

    def finalizar(self, forma, confirmado, versao_previa=None):
        """
        Finaliza o pedido se houver itens, confirmação explícita e se a versão
        da prévia conferir com a versão atual da montagem.
        """
        if self.estado == "finalizado":
            raise RuntimeError("Este pedido já foi finalizado anteriormente.")

        if not self._itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")

        if not forma or not str(forma).strip():
            raise ValueError("A forma de pagamento é obrigatória.")

        if not confirmado:
            raise ValueError("A finalização requer confirmação explícita.")

        # Rejeitar prévia antiga caso a montagem tenha sido alterada entretanto
        if versao_previa is not None and versao_previa != self.versao:
            raise ValueError("A prévia está desatualizada. Reabra a prévia para conferir as mudanças.")

        # Transição para o estado finalizado e criação do retrato independente
        self.estado = "finalizado"
        self.comprovante = {
            "itens": copy.deepcopy(self.linhas()),
            "total_centavos": self.total_centavos(),
            "forma_pagamento": str(forma),
            "versao_concluida": self.versao
        }
        return self.comprovante

    def novo(self):
        """Reseta o pedido para iniciar um novo ciclo de montagem."""
        self.estado = "montagem"
        self._itens.clear()
        self.versao += 1
        self.comprovante = None

    def finalizar(self, forma, confirmado, versao_previa=None):
        if self.estado == "finalizado":
            raise RuntimeError("Este pedido já foi finalizado anteriormente.")

        if not self._itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")

        if not forma or not str(forma).strip():
            raise ValueError("A forma de pagamento é obrigatória.")

        if not confirmado:
            raise ValueError("A finalização requer confirmação explícita.")

        if versao_previa is not None and versao_previa != self.versao:
            raise ValueError("A prévia está desatualizada. Reabra a prévia para conferir as mudanças.")

        self.estado = "finalizado"
        
        # Cria um dicionário base para o comprovante
        comprovante_dict = {
            "itens": copy.deepcopy(self.linhas()),
            "total_centavos": self.total_centavos(),
            "forma_pagamento": str(forma),
            "versao_concluida": self.versao
        }
        
        # Guarda o retrato internamente de forma isolada
        self.comprovante = copy.deepcopy(comprovante_dict)
        
        # Retorna uma cópia para o chamador, garantindo independência total
        return copy.deepcopy(comprovante_dict)
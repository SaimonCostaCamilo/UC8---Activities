"""Implementação em memória do mesmo contrato da persistência SQLite."""
from copy import deepcopy
from repositorio import validar_nome, validar_preco, validar_id


class RepositorioMemoria:
    def __init__(self):
        self._produtos = []
        self._clientes = []
        self._proximo_produto = 1
        self._proximo_cliente = 1

    def adicionar_produto(self, nome, preco):
        nome = validar_nome(nome)
        centavos = validar_preco(preco)
        item = {"id": self._proximo_produto, "nome": nome, "preco_centavos": centavos}
        self._proximo_produto += 1
        self._produtos.append(item)
        return deepcopy(item)

    def listar_produtos(self):
        return deepcopy(self._produtos)

    def editar_produto(self, codigo, nome, preco):
        codigo, nome, centavos = validar_id(codigo), validar_nome(nome), validar_preco(preco)
        for item in self._produtos:
            if item["id"] == codigo:
                item.update(nome=nome, preco_centavos=centavos)
                return True
        return False

    def excluir_produto(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if confirmado is not True:
            return False
        antes = len(self._produtos)
        self._produtos = [p for p in self._produtos if p["id"] != codigo]
        return len(self._produtos) == antes - 1

    def adicionar_cliente(self, nome):
        nome = validar_nome(nome)
        item = {"id": self._proximo_cliente, "nome": nome}
        self._proximo_cliente += 1
        self._clientes.append(item)
        return deepcopy(item)

    def listar_clientes(self):
        return deepcopy(self._clientes)

    def editar_cliente(self, codigo, nome):
        codigo, nome = validar_id(codigo), validar_nome(nome)
        for item in self._clientes:
            if item["id"] == codigo:
                item["nome"] = nome
                return True
        return False

    def excluir_cliente(self, codigo, confirmado=False):
        codigo = validar_id(codigo)
        if confirmado is not True:
            return False
        antes = len(self._clientes)
        self._clientes = [c for c in self._clientes if c["id"] != codigo]
        return len(self._clientes) == antes - 1

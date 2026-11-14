"""Coordenação entre interface, cadastros, pedido em memória e venda persistida."""
from copy import deepcopy
from repositorio import validar_id, validar_nome

class CadastroController:
    def __init__(self, repositorio):
        if repositorio is None: raise ValueError("Informe um repositório.")
        self.repositorio = repositorio

    def listar(self, tipo):
        if tipo == "produto": return self.repositorio.listar_produtos()
        if tipo == "cliente": return self.repositorio.listar_clientes()
        if tipo == "venda": return self.repositorio.listar_vendas()
        raise ValueError("Tipo de cadastro inválido.")

    def salvar(self, tipo, nome, preco_texto="", codigo=None):
        nome = validar_nome(nome)
        if tipo == "produto":
            if codigo is None: return self.repositorio.adicionar_produto(nome, preco_texto)
            codigo = validar_id(codigo)
            if not self.repositorio.editar_produto(codigo, nome, preco_texto): raise ValueError(f"Produto ID {codigo} não encontrado.")
            return next(x for x in self.listar("produto") if x["id"] == codigo)
        if tipo == "cliente":
            if codigo is None: return self.repositorio.adicionar_cliente(nome)
            codigo = validar_id(codigo)
            if not self.repositorio.editar_cliente(codigo, nome): raise ValueError(f"Cliente ID {codigo} não encontrado.")
            return next(x for x in self.listar("cliente") if x["id"] == codigo)
        raise ValueError("Tipo de cadastro inválido.")

    def excluir(self, tipo, codigo, confirmado):
        codigo = validar_id(codigo)
        if tipo == "produto": ok = self.repositorio.excluir_produto(codigo, confirmado)
        elif tipo == "cliente": ok = self.repositorio.excluir_cliente(codigo, confirmado)
        else: raise ValueError("Tipo de cadastro inválido.")
        return bool(confirmado is True and ok)

    def registrar_venda(self, cliente_id, pedido, forma, confirmado, versao_previa=None):
        """Persiste primeiro; só depois transforma a montagem em comprovante finalizado."""
        if confirmado is not True: raise ValueError("A venda exige confirmação explícita.")
        pedido.exigir_aberto()
        if not pedido.linhas(): raise ValueError("Adicione ao menos um produto.")
        if not forma or not str(forma).strip(): raise ValueError("Selecione a forma de pagamento.")
        if versao_previa is not None and versao_previa != pedido.versao:
            raise ValueError("A prévia mudou. Confira o pedido novamente.")
        # Nenhuma alteração de estado é feita antes da gravação atômica.
        venda = self.repositorio.registrar_venda(cliente_id, pedido.linhas(), forma)
        comprovante = pedido.finalizar(forma, True, versao_previa)
        comprovante.update({
            "venda_id": venda["id"], "cliente_id": venda["cliente_id"],
            "cliente_nome": venda["cliente_nome"],
            "total_pagamento_centavos": venda["total_pagamento_centavos"],
            "subtotal_centavos": venda["subtotal_centavos"],
        })
        pedido.comprovante = deepcopy(comprovante)
        return deepcopy(comprovante)

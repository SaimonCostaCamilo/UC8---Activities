"""Coordenação das operações de cadastro, independente da interface gráfica."""
from repositorio import validar_id, validar_nome


class CadastroController:
    """Encaminha operações de produtos e clientes ao contrato do repositório."""

    def __init__(self, repositorio):
        if repositorio is None:
            raise ValueError("Informe um repositório.")
        self.repositorio = repositorio

    def listar(self, tipo):
        if tipo == "produto":
            return self.repositorio.listar_produtos()
        if tipo == "cliente":
            return self.repositorio.listar_clientes()
        raise ValueError("Tipo de cadastro inválido.")

    def salvar(self, tipo, nome, preco_texto="", codigo=None):
        nome = validar_nome(nome)
        if tipo == "produto":
            if codigo is None:
                return self.repositorio.adicionar_produto(nome, preco_texto)
            codigo = validar_id(codigo)
            if not self.repositorio.editar_produto(codigo, nome, preco_texto):
                raise ValueError(f"Produto ID {codigo} não encontrado; nada foi alterado.")
            return next(item for item in self.listar("produto") if item["id"] == codigo)
        if tipo == "cliente":
            if codigo is None:
                return self.repositorio.adicionar_cliente(nome)
            codigo = validar_id(codigo)
            if not self.repositorio.editar_cliente(codigo, nome):
                raise ValueError(f"Cliente ID {codigo} não encontrado; nada foi alterado.")
            return next(item for item in self.listar("cliente") if item["id"] == codigo)
        raise ValueError("Tipo de cadastro inválido.")

    def excluir(self, tipo, codigo, confirmado):
        codigo = validar_id(codigo)
        if tipo == "produto":
            removido = self.repositorio.excluir_produto(codigo, confirmado=confirmado)
        elif tipo == "cliente":
            removido = self.repositorio.excluir_cliente(codigo, confirmado=confirmado)
        else:
            raise ValueError("Tipo de cadastro inválido.")
        if confirmado is not True or not removido:
            return False
        return True

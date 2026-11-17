# A13 — Simulação local de identificação e perfil


class SessaoDemo:
    """
    Simulação didática de sessão.
    Não autentica pessoas e não substitui controle de acesso de produção.
    """

    PERFIS_VALIDOS = ("Caixa", "Administração")

    def __init__(self):
        self.nome = None
        self.perfil = None

    def entrar(self, nome, perfil):
        """Inicia uma sessão fictícia após validar nome e perfil selecionado."""
        nome_limpo = str(nome or "").strip()
        perfil_limpo = str(perfil or "").strip()

        if not nome_limpo:
            raise ValueError("Informe um nome fictício para a demonstração.")
        if perfil_limpo not in self.PERFIS_VALIDOS:
            raise ValueError("Escolha Caixa ou Administração.")

        self.nome = nome_limpo
        self.perfil = perfil_limpo
        return {"nome": self.nome, "perfil": self.perfil}

    def pode_configurar(self):
        """Somente o perfil Administração recebe a permissão demonstrativa."""
        return self.nome is not None and self.perfil == "Administração"

    def sair(self):
        """Encerra a sessão de demonstração sem apagar vendas ou relatórios."""
        self.nome = None
        self.perfil = None
        return True

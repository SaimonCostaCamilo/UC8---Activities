# A13 — Verificações de integração Tkinter (execute em ambiente com display)
"""Smoke tests da interface. Não substituem a demonstração visual pelo aluno."""
import copy
import tempfile
import tkinter as tk
from pathlib import Path
from unittest.mock import patch

from main import AplicacaoVendas
from modelos import Produto, Pizza, Bebida
from pagamento import calcular_pagamento
from relatorios import ler_relatorio


def _criar_comprovante(app, forma="PIX"):
    total_itens = app.pedido.total_centavos()
    subtotal_texto = f"{total_itens // 100},{total_itens % 100:02d}"
    calculo = calcular_pagamento(subtotal_texto, forma)
    comprovante = app.pedido.finalizar(forma, True, app.pedido.versao)
    comprovante["total_pagamento_centavos"] = int(calculo["total"] * 100)
    app.comprovante_exportacao = copy.deepcopy(comprovante)


def verificar_interface():
    raiz = tk.Tk()
    temporario = tempfile.TemporaryDirectory()
    pasta = Path(temporario.name)
    try:
        # Mercado/Sorveteria: estado inicial, ausência de comprovante e perfis.
        app = AplicacaoVendas(
            raiz,
            catalogo=[Produto("S01", 'Picolé; edição "verão"', 650),
                      Produto("S02", "Açaí com morango", 450)],
            nome_aplicacao="Sorveteria",
        )
        raiz.update_idletasks()
        raiz.update()
        assert app.pedido.linhas() == []

        # Checklist automatizado de teclado: Tab avança e Shift+Tab retorna
        # entre campos focáveis da interface.
        app.entry_nome.focus_force()
        raiz.update()
        foco_inicial = raiz.focus_get()
        app.entry_nome.event_generate("<Tab>")
        raiz.update()
        foco_seguinte = raiz.focus_get()
        assert foco_seguinte is not None and foco_seguinte is not foco_inicial
        foco_seguinte.event_generate("<Shift-Tab>")
        raiz.update()
        assert raiz.focus_get() is foco_inicial

        # Erro recuperável: quantidade inválida não altera o pedido;
        # após corrigir o campo, a mesma ação deve funcionar.
        app.combo_produtos.current(0)
        app.entry_qtd.delete(0, "end")
        app.entry_qtd.insert(0, "abc")
        with patch("main.messagebox.showerror") as erro_qtd:
            app.acao_adicionar()
            erro_qtd.assert_called_once()
        assert app.pedido.linhas() == []
        app.entry_qtd.delete(0, "end")
        app.entry_qtd.insert(0, "1")
        app.acao_adicionar()
        assert len(app.pedido.linhas()) == 1
        app.pedido.remover(app.pedido.linhas()[0]["codigo"])
        app.atualizar_interface()
        assert app.pedido.linhas() == []

        # Acionamento por teclado: barra de espaço em botão focado executa o callback.
        def localizar_botao(widget, texto):
            for filho in widget.winfo_children():
                try:
                    if filho.winfo_class() == "TButton" and filho.cget("text") == texto:
                        return filho
                except tk.TclError:
                    pass
                encontrado = localizar_botao(filho, texto)
                if encontrado is not None:
                    return encontrado
            return None

        botao_adicionar = localizar_botao(raiz, "Adicionar")
        assert botao_adicionar is not None
        botao_adicionar.focus_force()
        raiz.update()
        botao_adicionar.event_generate("<space>")
        raiz.update()
        assert len(app.pedido.linhas()) == 1
        app.pedido.remover(app.pedido.linhas()[0]["codigo"])
        app.atualizar_interface()

        # Redimensionamento: janela aceita tamanho maior e mantém os widgets.
        raiz.geometry("1100x760")
        raiz.update()
        assert raiz.winfo_width() >= 1100 and raiz.winfo_height() >= 760
        assert app.combo_produtos.winfo_exists() and app.tree.winfo_exists()

        with patch("main.messagebox.showwarning") as aviso:
            app.acao_exportar()
            aviso.assert_called_once()

        app.entry_nome.insert(0, "Caixa fictício")
        app.combo_perfil.set("Caixa")
        app.acao_entrar()
        assert not app.sessao.pode_configurar()
        assert app.menu_configuracoes.entrycget(
            "Configurações (Administração)", "state"
        ) == "disabled"

        app.entry_nome.delete(0, "end")
        app.entry_nome.insert(0, "Admin fictício")
        app.combo_perfil.set("Administração")
        app.acao_entrar()
        assert app.sessao.pode_configurar()
        assert app.menu_configuracoes.entrycget(
            "Configurações (Administração)", "state"
        ) == "normal"

        # Seleção por IID/código e remoção do último item.
        app.combo_produtos.current(0)
        app.entry_qtd.delete(0, "end")
        app.entry_qtd.insert(0, "1")
        app.acao_adicionar()
        assert len(app.pedido.linhas()) == 1
        app.tree.selection_set("S01")
        app.acao_remover()
        assert app.pedido.linhas() == []

        # Venda fictícia, cancelamento do seletor e exportação efetiva.
        app.acao_adicionar()
        _criar_comprovante(app)
        comprovante_antes = copy.deepcopy(app.comprovante_exportacao)
        with patch("main.filedialog.asksaveasfilename", return_value=""):
            app.acao_exportar()
        assert app.comprovante_exportacao == comprovante_antes
        assert app.pedido.estado == "finalizado"

        destino = pasta / "sorveteria.csv"
        with patch("main.filedialog.asksaveasfilename", return_value=str(destino)), \
             patch("main.messagebox.showinfo") as sucesso:
            app.acao_exportar()
            sucesso.assert_called_once()
        linhas = ler_relatorio(destino)
        assert linhas[0]["nome"] == 'Picolé; edição "verão"'
        assert linhas[0]["preco_unitario_centavos"] == "650"
        assert linhas[0]["forma_pagamento"] == "PIX"

        # Sair encerra somente a sessão; comprovante e arquivo continuam.
        bytes_antes = destino.read_bytes()
        app.acao_sair()
        assert app.sessao.nome is None and app.sessao.perfil is None
        assert destino.read_bytes() == bytes_antes

        # A mesma interface inicia com os catálogos de Pizzaria e Sorveteria.
        configuracoes = [
            ("Pizzaria", [Pizza("P01", "Pizza Calabresa Média", "Média", 4000),
                          Bebida("B01", "Guaraná 2 L", 1200)]),
            ("Sorveteria", [Produto("S01", "Picolé; edição verão", 650),
                            Produto("S02", "Açaí com morango", 1650)]),
        ]
        for nome, catalogo in configuracoes:
            janela = tk.Toplevel(raiz)
            janela.withdraw()
            instancia = AplicacaoVendas(janela, catalogo=catalogo, nome_aplicacao=nome)
            janela.update_idletasks()
            assert instancia.nome_aplicacao == nome
            assert instancia.pedido.linhas() == []
            # Finaliza e exporta ao menos uma venda de cada catálogo.
            instancia.combo_produtos.current(0)
            instancia.entry_qtd.delete(0, "end")
            instancia.entry_qtd.insert(0, "1")
            instancia.acao_adicionar()
            _criar_comprovante(instancia)
            arquivo = pasta / ("pizzaria.csv" if nome == "Pizzaria" else "sorveteria-segunda.csv")
            with patch("main.filedialog.asksaveasfilename", return_value=str(arquivo)), \
                 patch("main.messagebox.showinfo"):
                instancia.acao_exportar()
            assert arquivo.exists() and len(ler_relatorio(arquivo)) == 1
            janela.destroy()

        app.janela.destroy()
        print("Interface: inicialização, Tab/Shift+Tab, acionamento por barra de espaço, erro e correção, redimensionamento, perfis, seleção/remoção, ausência de comprovante, cancelamento, exportação CSV e preservação após sair: OK")
        return True
    finally:
        try:
            raiz.destroy()
        except tk.TclError:
            pass
        temporario.cleanup()


if __name__ == "__main__":
    if not verificar_interface():
        raise SystemExit(1)

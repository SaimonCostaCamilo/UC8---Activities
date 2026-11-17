# A13 — Verificações sem GUI: CSV, comprovante, perfis, pedido, JSON e pagamento
import copy
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from modelos import Pedido, Produto, Pizza, Bebida
from pagamento import valor_monetario, calcular_pagamento, preco_para_centavos
from arquivos import validar_catalogo, ler_catalogo, salvar_catalogo
from relatorios import exportar_csv, ler_relatorio, CABECALHOS
from perfis import SessaoDemo


def _esperar_erro(tipo, funcao, *args, **kwargs):
    try:
        funcao(*args, **kwargs)
    except tipo:
        return
    raise AssertionError(f"Era esperado {tipo.__name__} em {funcao.__name__}.")


def verificar():
    print("Iniciando verificações automatizadas A13...")

    # T00 — Demonstra que uma previsão falsa realmente interrompe um assert;
    # em seguida, a previsão correta é restaurada e conferida.
    falha_controlada = False
    try:
        assert 2 == 3, "Falha intencional para conferir o comportamento de assert."
    except AssertionError:
        falha_controlada = True
    assert falha_controlada is True
    assert 2 == 2
    print("T00 — assert falso detectado e previsão correta restaurada: OK")

    # T01 — Sem comprovante não existe exportação nem venda fictícia.
    with tempfile.TemporaryDirectory() as pasta_temp:
        pasta = Path(pasta_temp)
        destino = pasta / "venda.csv"
        _esperar_erro(ValueError, exportar_csv, None, destino)
        assert not destino.exists()
    print("T01 — sem comprovante não exporta nem cria arquivo: OK")

    # Preparação de venda fictícia com acentos, ponto e vírgula e aspas.
    pedido = Pedido()
    produto_especial = Produto("S01", 'Picolé; edição "verão"', 650)
    produto_simples = Produto("S02", "Açaí com morango", 450)
    pedido.adicionar(produto_especial, "2")
    pedido.adicionar(produto_simples, "1")
    versao_confirmada = pedido.versao
    comprovante = pedido.finalizar(
        forma="PIX", confirmado=True, versao_previa=versao_confirmada
    )
    calculo = calcular_pagamento("17,50", "PIX")
    comprovante["total_pagamento_centavos"] = int(calculo["total"] * 100)
    retrato = copy.deepcopy(comprovante)

    with tempfile.TemporaryDirectory() as pasta_temp:
        pasta = Path(pasta_temp)
        destino = pasta / "venda.csv"

        # T02/T03 — CSV de volta, cabeçalho, caracteres especiais, quantidades e centavos.
        exportar_csv(retrato, destino)
        assert destino.read_bytes().startswith(b"\xef\xbb\xbf"), "CSV deve conter BOM UTF-8."
        linhas = ler_relatorio(destino)
        assert CABECALHOS == [
            "id", "nome", "quantidade", "preco_unitario_centavos",
            "subtotal_centavos", "forma_pagamento", "total_pedido_reais"
        ]
        assert len(linhas) == 2
        assert linhas[0]["nome"] == 'Picolé; edição "verão"'
        assert linhas[1]["nome"] == "Açaí com morango"
        assert linhas[0]["quantidade"] == "2"
        assert linhas[0]["preco_unitario_centavos"] == "650"
        assert linhas[0]["subtotal_centavos"] == "1300"
        assert linhas[1]["subtotal_centavos"] == "450"
        assert linhas[0]["forma_pagamento"] == "PIX"
        assert linhas[0]["total_pedido_reais"] == "15,23"
        assert linhas[1]["total_pedido_reais"] == "15,23"
        assert retrato["total_centavos"] == 1750
        print("T02/T03 — CSV com acentos, aspas, delimitador, quantidades e valores: OK")

        # T04 — Exportador usa o retrato confirmado, não dados atuais da montagem.
        produto_especial.nome = "Nome alterado depois da confirmação"
        pedido.novo()
        pedido.adicionar(Produto("S99", "Produto de outra montagem", 999), "1")
        exportar_csv(retrato, destino)
        linhas_releitura = ler_relatorio(destino)
        assert linhas_releitura[0]["nome"] == 'Picolé; edição "verão"'
        assert linhas_releitura[0]["subtotal_centavos"] == "1300"
        assert linhas_releitura[0]["total_pedido_reais"] == "15,23"
        print("T04 — comprovante permanece estável após alteração e nova montagem: OK")

        # T05 — Cancelar o seletor equivale a não chamar a gravação; caminho vazio não toca no arquivo.
        bytes_antes = destino.read_bytes()
        montagem_antes_cancelar = pedido.linhas()
        _esperar_erro(ValueError, exportar_csv, retrato, "")
        assert destino.read_bytes() == bytes_antes
        assert pedido.linhas() == montagem_antes_cancelar
        assert retrato["itens"][0]["nome"] == 'Picolé; edição "verão"'
        print("T05 — cancelamento/caminho vazio preserva arquivo e comprovante: OK")

        # T06 — Erro de gravação preserva destino anterior e remove temporário.
        with patch("relatorios.os.replace", side_effect=OSError("falha simulada")):
            _esperar_erro(OSError, exportar_csv, retrato, destino)
        assert destino.read_bytes() == bytes_antes
        assert not list(pasta.glob(".venda.csv.*.tmp"))
        pasta_inexistente = pasta / "nao_existe" / "venda.csv"
        _esperar_erro(OSError, exportar_csv, retrato, pasta_inexistente)
        assert destino.read_bytes() == bytes_antes
        print("T06 — falha de escrita preserva destino e limpa temporário: OK")

        # Exportação inválida após exportação válida não apaga nem substitui o CSV correto.
        invalido = copy.deepcopy(retrato)
        invalido["itens"][0]["subtotal"] = 1
        _esperar_erro(ValueError, exportar_csv, invalido, destino)
        assert destino.read_bytes() == bytes_antes
        print("T06b — tentativa inválida depois da válida preserva o relatório: OK")

    # T07 — Perfis demonstrativos e autorização consultada na operação.
    sessao = SessaoDemo()
    sessao.entrar("Caixa de teste", "Caixa")
    assert sessao.pode_configurar() is False
    _esperar_erro(ValueError, sessao.entrar, "   ", "Caixa")
    _esperar_erro(ValueError, sessao.entrar, "Nome", "Gerência")
    sessao.entrar("Admin de teste", "Administração")
    assert sessao.pode_configurar() is True
    sessao.sair()
    assert sessao.nome is None and sessao.perfil is None
    assert sessao.pode_configurar() is False
    print("T07 — Caixa/Administração, validação e encerramento de sessão: OK")

    # T08 — Sair da sessão não remove arquivo já exportado.
    with tempfile.TemporaryDirectory() as pasta_temp:
        destino_sessao = Path(pasta_temp) / "relatorio.csv"
        exportar_csv(retrato, destino_sessao)
        bytes_sessao = destino_sessao.read_bytes()
        sessao_arquivo = SessaoDemo()
        sessao_arquivo.entrar("Operador fictício", "Administração")
        sessao_arquivo.sair()
        assert sessao_arquivo.pode_configurar() is False
        assert destino_sessao.exists() and destino_sessao.read_bytes() == bytes_sessao
    print("T08 — sair encerra sessão sem apagar venda/relatório: OK")

    # T09 — Regressão A09: identidade pelo código não depende da ordem visual;
    # remover o último item deixa a coleção vazia sem depender de seleção antiga.
    pedido_a09 = Pedido()
    p1 = Produto("P01", "Produto A", 500)
    p2 = Produto("P02", "Produto B", 450)
    pedido_a09.adicionar(p1, "2")
    pedido_a09.adicionar(p2, "1")
    ids_visuais = [linha["codigo"] for linha in pedido_a09.linhas()]
    ids_visuais.reverse()  # simula apenas uma ordem de exibição diferente
    assert pedido_a09._itens["P01"].produto.nome == "Produto A"
    pedido_a09.remover("P02")
    pedido_a09.remover("P01")
    assert pedido_a09.linhas() == []
    assert pedido_a09.total_centavos() == 0
    print("T09 — remoção do último item e identidade por código: OK")

    # T10 — Confirmação explícita, estado finalizado e versão da prévia.
    pedido_estado = Pedido()
    pedido_estado.adicionar(Pizza("P10", "Pizza fictícia", "Média", 4000), "1")
    versao = pedido_estado.versao
    linhas_antes_cancelar = pedido_estado.linhas()
    _esperar_erro(ValueError, pedido_estado.finalizar, "PIX", False, versao)
    assert pedido_estado.estado == "montagem"
    assert pedido_estado.linhas() == linhas_antes_cancelar
    pedido_estado.adicionar(Bebida("B10", "Água", 500), "1")
    _esperar_erro(ValueError, pedido_estado.finalizar, "PIX", True, versao)
    versao_atual = pedido_estado.versao
    pedido_estado.finalizar("PIX", True, versao_atual)
    _esperar_erro(RuntimeError, pedido_estado.adicionar, Bebida("B11", "Suco", 700), "1")
    pedido_estado.novo()
    assert pedido_estado.estado == "montagem" and pedido_estado.linhas() == []
    print("T10 — cancelamento preserva montagem, prévia antiga é rejeitada e pedido finalizado bloqueia edição: OK")

    # T11 — Regressão A12: JSON válido, ausente, inválido e preservação de bytes.
    catalogo = [
        {"id": 1, "nome": "Picolé de limão", "preco_centavos": 450},
        {"id": 2, "nome": "Sorvete de chocolate", "preco_centavos": 1200},
    ]
    with tempfile.TemporaryDirectory() as pasta_temp:
        pasta = Path(pasta_temp)
        ausente = pasta / "ausente.json"
        assert ler_catalogo(ausente) == []
        assert not ausente.exists()
        json_path = pasta / "catalogo.json"
        salvar_catalogo(json_path, catalogo)
        assert ler_catalogo(json_path) == catalogo
        quebrado = pasta / "quebrado.json"
        bytes_quebrados = b'{"nome": '
        quebrado.write_bytes(bytes_quebrados)
        _esperar_erro(ValueError, ler_catalogo, quebrado)
        assert quebrado.read_bytes() == bytes_quebrados
        encoding_ruim = pasta / "encoding-invalido.json"
        bytes_encoding = b'[{"nome":"\xff"}]'
        encoding_ruim.write_bytes(bytes_encoding)
        _esperar_erro(OSError, ler_catalogo, encoding_ruim)
        assert encoding_ruim.read_bytes() == bytes_encoding
        bytes_validos = json_path.read_bytes()
        with patch("arquivos.os.replace", side_effect=OSError("falha simulada")):
            _esperar_erro(OSError, salvar_catalogo, json_path, [
                {"id": 3, "nome": "Novo", "preco_centavos": 300}
            ])
        assert json_path.read_bytes() == bytes_validos
        assert not list(pasta.glob(".catalogo.json.*.tmp"))
        invalidos = [
            [{"id": 1, "nome": "A", "preco_centavos": 100},
             {"id": 1, "nome": "B", "preco_centavos": 200}],
            [{"id": 0, "nome": "A", "preco_centavos": 100}],
            [{"id": 1, "nome": " ", "preco_centavos": 100}],
            [{"id": 1, "nome": "A", "preco_centavos": 0}],
        ]
        for dados in invalidos:
            _esperar_erro(ValueError, validar_catalogo, dados)
    print("T11 — regressão JSON A12: leitura, ausência e validação: OK")

    # T12 — Regressão pagamento decimal A12.
    assert str(valor_monetario("R$ 12,345")) == "12.35"
    assert preco_para_centavos("R$ 4,50") == 450
    assert calcular_pagamento("10,00", "PIX")["total"] == valor_monetario("8,70")
    _esperar_erro(ValueError, valor_monetario, "-5,00")
    _esperar_erro(ValueError, calcular_pagamento, "10,00", "Cripto")
    print("T12 — regressão pagamento Decimal: OK")

    print("Todos os casos automatizados A13 foram concluídos.")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")

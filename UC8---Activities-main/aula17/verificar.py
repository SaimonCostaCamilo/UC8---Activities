"""Testes automatizados A14–A17. Não abre GUI e usa bancos/arquivos temporários."""
import copy
import importlib
import json
import sqlite3
import tempfile
from pathlib import Path

from modelos import Pedido, Produto, formatar
from pagamento import valor_monetario, calcular_pagamento, preco_para_centavos
from arquivos import validar_catalogo, ler_catalogo, salvar_catalogo
from relatorios import exportar_csv, ler_relatorio
from perfis import SessaoDemo
from repositorio import RepositorioSqlite, validar_nome, validar_id, validar_preco
from memoria import RepositorioMemoria
from controller import CadastroController


def esperar_erro(tipo, funcao, *args, **kwargs):
    try:
        funcao(*args, **kwargs)
    except tipo:
        return
    except Exception as erro:
        raise AssertionError(
            f"{funcao.__name__}: esperado {tipo.__name__}, recebido {type(erro).__name__}: {erro}"
        ) from erro
    raise AssertionError(f"{funcao.__name__}: era esperado {tipo.__name__}.")


def verificar():
    print("Iniciando verificações A14–A17 — SQLite, transações e regressão dos módulos anteriores...")

    # T00 — Importar/construir o repositório não cria banco; apenas conectar/iniciar cria.
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "nao_criar_ao_importar.db"
        importlib.reload(importlib.import_module("repositorio"))
        repo = RepositorioSqlite(caminho)
        assert not caminho.exists()
        print("T00 — importação e construção não criam banco: OK")

        # T01 — Inicialização idempotente, sem apagar linhas existentes.
        assert repo.iniciar() is True
        primeiro = repo.adicionar_produto("Arroz", "7,50")
        esperado_primeiro = {"id": 1, "nome": "Arroz", "preco_centavos": 750}
        assert primeiro == esperado_primeiro
        repo.iniciar()
        esperado_lista = [esperado_primeiro]
        observado_lista = repo.listar_produtos()
        assert observado_lista == esperado_lista
        print("T01/T02 — tabelas sem apagar dados e R$ 7,50 armazenado como 750 centavos: OK")

        # T03 — Apóstrofo é dado literal enviado em parâmetro, nunca concatenado no SQL.
        nome_especial = "D'água"
        esperado_especial = {"id": 2, "nome": nome_especial, "preco_centavos": 1250}
        observado_especial = repo.adicionar_produto(nome_especial, "12,50")
        assert observado_especial == esperado_especial
        assert repo.listar_produtos()[1] == esperado_especial
        print("T03 — nome com apóstrofo gravado/consultado por placeholder: OK")

        # T04 — Erro depois de cadastro válido não altera os registros existentes.
        antes = repo.listar_produtos()
        esperar_erro(ValueError, repo.adicionar_produto, "   ", "3,00")
        esperar_erro(ValueError, repo.adicionar_produto, "Produto inválido", "abc")
        esperar_erro(ValueError, repo.adicionar_produto, "Preço zero", "0,00")
        assert repo.listar_produtos() == antes
        print("T04 — nome vazio, preço inválido e zero recusados sem inserir: OK")

        # T05 — IDs inteiros positivos e únicos, independentes da posição visual.
        terceiro = repo.adicionar_produto("Café", "5,99")
        assert terceiro["id"] == 3
        ids = [r["id"] for r in repo.listar_produtos()]
        assert ids == [1, 2, 3] and len(ids) == len(set(ids))
        esperar_erro(ValueError, validar_id, 0)
        esperar_erro(ValueError, validar_id, "abc")
        assert validar_id("3") == 3
        print("T05 — IDs positivos, únicos e validados: OK")

        # T06 — Fechar/reabrir o mesmo caminho mantém registros.
        repo_reaberto = RepositorioSqlite(caminho)
        esperado_reabertura = repo.listar_produtos()
        observado_reabertura = repo_reaberto.listar_produtos()
        assert observado_reabertura == esperado_reabertura
        assert Path(repo_reaberto.caminho) == caminho.resolve()
        # Operações de leitura já encerraram suas conexões; outra conexão consegue escrever.
        with sqlite3.connect(str(caminho), timeout=1) as conexao_teste:
            conexao_teste.execute("BEGIN IMMEDIATE")
            conexao_teste.rollback()
        print("T06 — reabertura do mesmo arquivo preserva produtos: OK")

        # T07 — Banco inacessível não retorna sucesso nem modifica banco válido.
        antes_falha = repo.listar_produtos()
        repo_ruim = RepositorioSqlite(Path(pasta) / "pasta_que_nao_existe" / "db.sqlite")
        # A conexão cria diretórios por projeto; simula falha usando um diretório como arquivo DB.
        caminho_diretorio = Path(pasta) / "eh_diretorio"
        caminho_diretorio.mkdir()
        repo_diretorio = RepositorioSqlite(caminho_diretorio)
        esperar_erro(sqlite3.OperationalError, repo_diretorio.iniciar)
        assert repo.listar_produtos() == antes_falha
        print("T07 — falha de conexão é propagada e banco válido permanece intacto: OK")

    # T08 — Validadores de apoio e representação monetária.
    assert validar_nome("  Leite  ") == "Leite"
    esperar_erro(ValueError, validar_nome, "  ")
    assert validar_preco("7,50") == 750
    assert preco_para_centavos("R$ 2,35") == 235
    esperar_erro(ValueError, validar_preco, "texto")
    assert formatar(750) == "R$ 7.50"
    assert valor_monetario("7,50") == valor_monetario("7.50")
    assert calcular_pagamento("10,00", "PIX")["total"] == valor_monetario("8,70")
    print("T08 — validação de nome, preço, centavos, formatação e pagamento: OK")

    # T09 — Regressão: pedido continua em memória e total vem do modelo, não da tela.
    pedido = Pedido()
    arroz = Produto("1", "Arroz", 750)
    agua = Produto("2", "D'água", 1250)
    pedido.adicionar(arroz, "2")
    pedido.adicionar(agua, "1")
    assert pedido.total_centavos() == 2750
    assert pedido.linhas()[0]["subtotal"] == 1500
    pedido.atualizar("1", "3")
    assert pedido.total_centavos() == 3500
    pedido.remover("2")
    assert pedido.total_centavos() == 2250
    print("T09 — pedido permanece em memória e calcula total pelos subtotais do modelo: OK")

    # T10 — Sessão fictícia não apaga dados do pedido.
    sessao = SessaoDemo()
    sessao.entrar("Operador de teste", "Caixa")
    assert sessao.pode_configurar() is False
    sessao.entrar("Admin de teste", "Administração")
    assert sessao.pode_configurar() is True
    sessao.sair()
    assert sessao.nome is None and sessao.perfil is None
    assert pedido.total_centavos() == 2250
    print("T10 — sair limpa somente a sessão fictícia, não o pedido: OK")

    # T11 — JSON ausente versus inválido e gravação segura continuam funcionais.
    with tempfile.TemporaryDirectory() as pasta:
        caminho_json = Path(pasta) / "catalogo.json"
        assert ler_catalogo(caminho_json) == [] and not caminho_json.exists()
        catalogo = [{"id": 1, "nome": "D'água", "preco_centavos": 1250}]
        salvar_catalogo(caminho_json, catalogo)
        assert ler_catalogo(caminho_json) == catalogo
        caminho_json.write_text("{ json inválido", encoding="utf-8")
        esperar_erro(ValueError, ler_catalogo, caminho_json)
        assert caminho_json.read_text(encoding="utf-8") == "{ json inválido"
        esperar_erro(ValueError, validar_catalogo, [{"id": 1, "nome": "", "preco_centavos": 10}])
    print("T11 — JSON: ausente distinto de inválido; origem inválida preservada: OK")

    # T12 — CSV é gerado a partir do comprovante confirmado, não de widgets.
    pedido_csv = Pedido()
    pedido_csv.adicionar(Produto("P1", 'Pão d' + "'" + 'água', 350), "2")
    comprovante = pedido_csv.finalizar("Crédito 1x", True, pedido_csv.versao)
    with tempfile.TemporaryDirectory() as pasta:
        caminho_csv = Path(pasta) / "comprovante.csv"
        exportar_csv(comprovante, caminho_csv)
        linhas = ler_relatorio(caminho_csv)
        assert len(linhas) == 1
        assert linhas[0]["nome"] == "Pão d'água"
        assert linhas[0]["subtotal_centavos"] == "700"
        assert caminho_csv.read_bytes().startswith(b"\xef\xbb\xbf")
    print("T12 — exportação CSV baseada no comprovante confirmado: OK")

    # T13 — Clientes também usam parâmetros e persistem no arquivo.
    with tempfile.TemporaryDirectory() as pasta:
        repo_clientes = RepositorioSqlite(Path(pasta) / "clientes.db")
        repo_clientes.iniciar()
        esperado_cliente = {"id": 1, "nome": "O'Connor"}
        observado_cliente = repo_clientes.adicionar_cliente("O'Connor")
        assert observado_cliente == esperado_cliente
        assert repo_clientes.listar_clientes() == [esperado_cliente]
    print("T13 — CRUD inicial de clientes com SQL parametrizado: OK")

    # A15 — edição por ID atualiza uma linha, mesmo após reordenação.
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "a15.db"
        repo15 = RepositorioSqlite(caminho)
        repo15.iniciar()
        p1 = repo15.adicionar_produto("Caneca", "10,00")
        p2 = repo15.adicionar_produto("Prato", "15,00")
        id_alvo = p1["id"]  # identidade guardada, não posição visual
        assert repo15.editar_produto(id_alvo, "Caneca premium", "12,50") is True
        assert repo15.editar_produto(9999, "Fantasma", "1,00") is False
        # Ordenação visual simulada: lista invertida; a edição continua usando o ID.
        visual = list(reversed(repo15.listar_produtos()))
        assert visual[1]["id"] == id_alvo
        assert repo15.editar_produto(id_alvo, "Caneca azul", "13,00") is True
        atuais = repo15.listar_produtos()
        assert len(atuais) == 2
        assert next(p for p in atuais if p["id"] == id_alvo) == {
            "id": id_alvo, "nome": "Caneca azul", "preco_centavos": 1300
        }
        # Entrada inválida falha antes do UPDATE e preserva o valor anterior.
        esperar_erro(ValueError, repo15.editar_produto, id_alvo, "", "0")
        assert next(p for p in repo15.listar_produtos() if p["id"] == id_alvo)["nome"] == "Caneca azul"
        assert repo15.excluir_produto(p2["id"], confirmado=False) is False
        assert len(repo15.listar_produtos()) == 2
        assert repo15.excluir_produto(p2["id"], confirmado=True) is True
        assert repo15.listar_produtos() == [{
            "id": id_alvo, "nome": "Caneca azul", "preco_centavos": 1300
        }]
        assert repo15.excluir_produto(id_alvo, confirmado=True) is True
        assert repo15.listar_produtos() == []
        # Banco reaberto: edição/exclusão confirmada permanece gravada.
        repo_reaberto = RepositorioSqlite(caminho)
        repo_reaberto.iniciar()
        assert repo_reaberto.listar_produtos() == []
        # Expectativa deliberadamente falsa: deve falhar; não modifica o banco.
        try:
            assert repo_reaberto.listar_produtos() == [{"id": 1}]
        except AssertionError:
            pass
        else:
            raise AssertionError("A expectativa deliberadamente errada deveria falhar.")
        assert repo_reaberto.listar_produtos() == []
    print("A15 T14 — editar mesmo ID, reordenar, inválido, ID ausente e reabertura: OK")
    print("A15 T15 — cancelamento preserva dados; confirmar remove só o alvo; lista vazia: OK")

    # A15 — inclusão e listagem de clientes persistem após reabrir.
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "clientes-a15.db"
        rc = RepositorioSqlite(caminho)
        rc.iniciar()
        cliente = rc.adicionar_cliente("Cliente Fictício")
        rc2 = RepositorioSqlite(caminho)
        rc2.iniciar()
        assert rc2.listar_clientes() == [cliente]
    print("A15 T16 — clientes fictícios incluídos, listados e persistidos: OK")

    # A16 — mesmo contrato em memória e SQLite, coordenado pelo controller.
    with tempfile.TemporaryDirectory() as pasta:
        repositorios = [
            RepositorioMemoria(),
            RepositorioSqlite(Path(pasta) / "contrato-a16.db"),
        ]
        for repo in repositorios:
            if hasattr(repo, "iniciar"):
                repo.iniciar()
            ctl = CadastroController(repo)
            p1 = ctl.salvar("produto", "Caneta", "2,50")
            c1 = ctl.salvar("cliente", "Lia")
            assert p1 == {"id": 1, "nome": "Caneta", "preco_centavos": 250}
            assert c1 == {"id": 1, "nome": "Lia"}
            assert ctl.listar("produto") == [p1]
            assert ctl.listar("cliente") == [c1]
            produto_editado = ctl.salvar("produto", "Caneta azul", "3,00", codigo=p1["id"])
            assert produto_editado == {"id": 1, "nome": "Caneta azul", "preco_centavos": 300}
            try:
                ctl.salvar("produto", "ID ausente", "1,00", codigo=999)
            except ValueError:
                pass
            else:
                raise AssertionError("Edição de produto inexistente deveria falhar.")
            assert ctl.listar("produto") == [produto_editado]
            atualizado = ctl.salvar("cliente", "Lia Silva", codigo=c1["id"])
            assert atualizado == {"id": 1, "nome": "Lia Silva"}
            assert ctl.excluir("cliente", c1["id"], False) is False
            assert ctl.listar("cliente") == [atualizado]
            assert ctl.excluir("cliente", c1["id"], True) is True
            assert ctl.listar("cliente") == []
            assert ctl.excluir("produto", p1["id"], True) is True
            assert ctl.listar("produto") == []
            try:
                ctl.listar("desconhecido")
            except ValueError:
                pass
            else:
                raise AssertionError("Tipo de cadastro inválido deveria falhar.")
            try:
                ctl.salvar("cliente", "   ")
            except ValueError:
                pass
            else:
                raise AssertionError("Nome vazio deveria ser recusado.")
            # A lista devolvida não pode alterar o estado interno em memória.
            if isinstance(repo, RepositorioMemoria):
                ctl.salvar("cliente", "Protegida")
                copia = ctl.listar("cliente")
                copia[0]["nome"] = "Alteração externa"
                assert ctl.listar("cliente")[0]["nome"] == "Protegida"
            else:
                ctl.salvar("cliente", "Persistente")
                reaberto = RepositorioSqlite(Path(pasta) / "contrato-a16.db")
                reaberto.iniciar()
                assert reaberto.listar_clientes() == [{"id": 2, "nome": "Persistente"}]
    print("A16 T17 — contrato comum, CRUD por ID, cancelamento, erro e cópia defensiva: OK")

    # A17 T05 — cenário obrigatório: 2 unidades a R$ 6,50 no PIX = R$ 11,31.
    with tempfile.TemporaryDirectory() as pasta:
        repo_pix = RepositorioSqlite(Path(pasta) / "pix-a17.db"); repo_pix.iniciar()
        cli_pix = repo_pix.adicionar_cliente("Cliente PIX")
        sorvete = repo_pix.adicionar_produto("Casquinha", "6,50")
        pedido_pix = Pedido(); pedido_pix.adicionar(Produto(str(sorvete["id"]), sorvete["nome"], sorvete["preco_centavos"]), "2")
        recibo_pix = CadastroController(repo_pix).registrar_venda(cli_pix["id"], pedido_pix, "PIX", True, pedido_pix.versao)
        assert recibo_pix["total_centavos"] == 1300
        assert recibo_pix["total_pagamento_centavos"] == 1131
        assert repo_pix.listar_vendas()[0]["itens"][0]["quantidade"] == 2
    print("A17 T05 — 2 x R$ 6,50 no PIX: R$ 13,00 → R$ 11,31: OK")

    # A17 T01/T02 — catálogos e clientes continuam persistidos e são consultados por ID.
    with tempfile.TemporaryDirectory() as pasta:
        db = Path(pasta) / "sorveteria.db"
        repo17 = RepositorioSqlite(db); repo17.iniciar()
        cliente = repo17.adicionar_cliente("Cliente de teste")
        produto = repo17.adicionar_produto("Sorvete de creme", "6,50")
        repo17_reaberto = RepositorioSqlite(db); repo17_reaberto.iniciar()
        assert repo17_reaberto.listar_clientes() == [cliente]
        assert repo17_reaberto.listar_produtos() == [produto]
        print("A17 T01/T02 — clientes e catálogo persistem e reabrem por ID: OK")

    # A17 T03 — preço/nome alterado no catálogo exige revisão e não grava venda parcial.
        ctl = CadastroController(repo17_reaberto)
        pedido = Pedido(); pedido.adicionar(Produto(str(produto["id"]), produto["nome"], produto["preco_centavos"]), "2")
        assert pedido.total_centavos() == 1300
        repo17_reaberto.editar_produto(produto["id"], "Sorvete de creme premium", "7,00")
        esperar_erro(ValueError, ctl.registrar_venda, cliente["id"], pedido, "PIX", True, pedido.versao)
        assert pedido.estado == "montagem" and len(pedido.linhas()) == 1
        assert repo17_reaberto.listar_vendas() == []
        pedido.substituir_produto(Produto(str(produto["id"]), "Sorvete de creme premium", 700))
        assert pedido.total_centavos() == 1400
        print("A17 T03 — catálogo alterado bloqueia venda; montagem preservada e revisável: OK")

        # A17 T04/T05/T07 — cliente obrigatório, valor PIX exato e bloqueio de repetição.
        esperar_erro(ValueError, ctl.registrar_venda, 9999, pedido, "PIX", True, pedido.versao)
        comprovante = ctl.registrar_venda(cliente["id"], pedido, "PIX", True, pedido.versao)
        assert comprovante["total_centavos"] == 1400
        assert comprovante["total_pagamento_centavos"] == 1218
        assert pedido.estado == "finalizado"
        esperar_erro(RuntimeError, ctl.registrar_venda, cliente["id"], pedido, "PIX", True, pedido.versao)
        assert len(repo17_reaberto.listar_vendas()) == 1
        print("A17 T04/T05/T07 — cliente validado, pagamento decimal e finalização única: OK")

        # A17 T06 — erro real na segunda inserção de item desfaz cabeçalho e primeiro item.
        p2 = repo17_reaberto.adicionar_produto("Chocolate", "4,00")
        p3 = repo17_reaberto.adicionar_produto("Morango", "3,00")
        pedido_falha = Pedido()
        pedido_falha.adicionar(Produto(str(p2["id"]), p2["nome"], p2["preco_centavos"]), "1")
        pedido_falha.adicionar(Produto(str(p3["id"]), p3["nome"], p3["preco_centavos"]), "1")
        with sqlite3.connect(str(db)) as con:
            con.execute(f"""CREATE TRIGGER falhar_segundo_item BEFORE INSERT ON itens_venda
                           WHEN NEW.produto_id = {int(p3['id'])} BEGIN SELECT RAISE(ABORT, 'falha de ensaio no segundo item'); END""")
        vendas_antes = len(repo17_reaberto.listar_vendas())
        itens_antes = sum(len(v["itens"]) for v in repo17_reaberto.listar_vendas())
        esperar_erro(sqlite3.IntegrityError, ctl.registrar_venda, cliente["id"], pedido_falha, "Crédito 1x", True, pedido_falha.versao)
        vendas_depois = repo17_reaberto.listar_vendas()
        assert len(vendas_depois) == vendas_antes
        assert sum(len(v["itens"]) for v in vendas_depois) == itens_antes
        assert pedido_falha.estado == "montagem" and len(pedido_falha.linhas()) == 2
        with sqlite3.connect(str(db)) as con: con.execute("DROP TRIGGER falhar_segundo_item")
        print("A17 T06 — falha no segundo item faz rollback da venda e de todos os itens: OK")

        # A17 T08 — vínculos impedem excluir cadastro usado por venda.
        esperar_erro(sqlite3.IntegrityError, repo17_reaberto.excluir_cliente, cliente["id"], True)
        esperar_erro(sqlite3.IntegrityError, repo17_reaberto.excluir_produto, produto["id"], True)
        assert repo17_reaberto.listar_clientes() == [cliente]
        print("A17 T08 — exclusão de cliente/produto vinculado é bloqueada: OK")

        # A17 T09 — CSV usa apenas o comprovante já confirmado e mantém os totais.
        with tempfile.TemporaryDirectory() as pasta_csv:
            csv_path = Path(pasta_csv) / "venda.csv"
            exportar_csv(comprovante, csv_path)
            linhas_csv = ler_relatorio(csv_path)
            assert len(linhas_csv) == 1
            assert linhas_csv[0]["subtotal_centavos"] == "1400"
            assert linhas_csv[0]["total_pedido_reais"] == "12,18"
            # Assinatura alternativa apresentada no roteiro da A17 também funciona.
            csv_path2 = Path(pasta_csv) / "venda2.csv"
            exportar_csv(csv_path2, comprovante)
            assert len(ler_relatorio(csv_path2)) == 1
        print("A17 T09 — CSV exportado do comprovante, com subtotal e total pago: OK")

        # A17 T01/T07 — histórico completo permanece após fechar e reabrir.
        historico = RepositorioSqlite(db); historico.iniciar()
        vendas = historico.listar_vendas()
        assert len(vendas) == 1 and vendas[0]["cliente_id"] == cliente["id"]
        assert len(vendas[0]["itens"]) == 1
        assert vendas[0]["itens"][0]["preco_unitario"] == 700
        print("A17 T01/T07 — venda e itens conferidos após reabrir o banco: OK")

    print("Todos os casos automatizados A14 + A15 + A16 + A17 foram aprovados.")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")

# A12 — Testes sem GUI: mercado, pagamento decimal e catálogo JSON
import json
import tempfile
from unittest.mock import patch
from pathlib import Path

from arquivos import validar_catalogo, ler_catalogo, salvar_catalogo
from pagamento import valor_monetario, calcular_pagamento, preco_para_centavos
from modelos import Pedido, Pizza, Bebida


def verificar():
    # Pagamento decimal (contrato reutilizado da A11)
    assert str(valor_monetario("R$ 12,345")) == "12.35"
    assert str(valor_monetario("1.234,56")) == "1234.56"
    assert preco_para_centavos("R$ 4,50") == 450
    assert calcular_pagamento("10,00", "PIX")["total"] == valor_monetario("8,70")
    try:
        valor_monetario("-5,00")
        assert False, "Valor negativo deveria ser rejeitado."
    except ValueError:
        pass
    try:
        valor_monetario("", permitir_zero=False)
        assert False, "Texto vazio deveria ser rejeitado."
    except ValueError:
        pass
    try:
        calcular_pagamento("10,00", "Cripto")
        assert False, "Forma desconhecida deveria ser rejeitada."
    except ValueError:
        pass

    catalogo = [
        {"id": 1, "nome": "Picolé de limão", "preco_centavos": 450},
        {"id": 2, "nome": "Sorvete de chocolate", "preco_centavos": 1200},
    ]

    with tempfile.TemporaryDirectory() as pasta_temp:
        pasta = Path(pasta_temp)
        ausente = pasta / "nao_criado.json"
        assert ler_catalogo(ausente) == []
        assert not ausente.exists(), "Leitura de ausente não pode criar arquivo."

        valido = pasta / "catalogo.json"
        salvar_catalogo(valido, catalogo)
        assert ler_catalogo(valido) == catalogo
        assert "Picolé de limão" in valido.read_text(encoding="utf-8")

        # JSON malformado: a leitura falha e os bytes permanecem idênticos.
        quebrado = pasta / "quebrado.json"
        bytes_antes = b'{"id": 1, "nome": '
        quebrado.write_bytes(bytes_antes)
        try:
            ler_catalogo(quebrado)
            assert False, "JSON quebrado deveria falhar."
        except ValueError:
            pass
        assert quebrado.read_bytes() == bytes_antes

        # UTF-8 inválido também não pode ser substituído.
        encoding_ruim = pasta / "encoding.json"
        bytes_encoding = b'[{"nome":"\xff"}]'
        encoding_ruim.write_bytes(bytes_encoding)
        try:
            ler_catalogo(encoding_ruim)
            assert False, "Encoding inválido deveria falhar."
        except OSError:
            pass
        assert encoding_ruim.read_bytes() == bytes_encoding

        # JSON válido sintaticamente, mas inválido no contrato.
        invalidos = [
            {"caso": [{"id": 1, "nome": "A", "preco_centavos": 100}, {"id": 1, "nome": "B", "preco_centavos": 200}]},
            {"caso": [{"id": 0, "nome": "A", "preco_centavos": 100}]},
            {"caso": [{"id": 1, "nome": "A", "preco_centavos": 0}]},
            {"caso": [{"id": 1, "nome": " ", "preco_centavos": 100}]},
            {"caso": {"id": 1, "nome": "A", "preco_centavos": 100}},
        ]
        for caso in invalidos:
            try:
                validar_catalogo(caso["caso"])
                assert False, "Estrutura inválida deveria ser rejeitada."
            except ValueError:
                pass

        # Uma tentativa inválida de salvar não toca no arquivo existente.
        bytes_validos_antes = valido.read_bytes()
        try:
            salvar_catalogo(valido, [{"id": 1, "nome": "Duplicado", "preco_centavos": 100}, {"id": 1, "nome": "Duplicado 2", "preco_centavos": 200}])
            assert False, "Catálogo inválido não deveria ser salvo."
        except ValueError:
            pass
        assert valido.read_bytes() == bytes_validos_antes

        # Simula falha real na substituição atômica: o destino antigo permanece intacto.
        with patch("arquivos.os.replace", side_effect=OSError("falha simulada de substituição")):
            try:
                salvar_catalogo(valido, [{"id": 9, "nome": "Novo catálogo", "preco_centavos": 999}])
                assert False, "A falha de substituição deveria ser comunicada."
            except OSError:
                pass
        assert valido.read_bytes() == bytes_validos_antes
        assert not list(pasta.glob(".catalogo.json.*.tmp")), "Temporário deve ser removido após falha."

        # Falha de caminho/destino não deve ser confundida com sucesso.
        destino_diretorio = pasta / "sou_diretorio"
        destino_diretorio.mkdir()
        try:
            salvar_catalogo(destino_diretorio, catalogo)
            assert False, "Não se deve substituir um diretório por arquivo."
        except OSError:
            pass
        assert destino_diretorio.is_dir()

    # Regressão A11: o pedido é independente do catálogo JSON e sobrevive à navegação.
    pedido = Pedido()
    pizza = Pizza("P01", "Chocolate", "Médio", 1200)
    bebida = Bebida("B01", "Água", 500)
    pedido.adicionar(pizza, "2")
    estado_antes = (pedido.estado, pedido.versao, pedido.total_centavos(), pedido.linhas())
    # Simula trabalho no módulo JSON: nenhuma chamada de arquivo recebe o pedido.
    validar_catalogo(catalogo)
    assert (pedido.estado, pedido.versao, pedido.total_centavos(), pedido.linhas()) == estado_antes
    pedido.adicionar(bebida, "1")
    assert pedido.total_centavos() == 2900

    print("T01–T11: pagamentos, ausente, UTF-8, JSON inválido, contrato, falha de escrita e pedido: OK")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")

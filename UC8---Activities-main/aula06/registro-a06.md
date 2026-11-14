# Registro A06 — Modelagem de aluno e validação de dados

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Separar regras de domínio em `aluno.py` e verificá-las sem depender da interface. Cada instância criada com `Aluno()` possui seu próprio estado; atribuir uma variável a outra (`rui = lia`) cria uma referência ao mesmo objeto, não uma cópia. `self` identifica a instância que recebeu a chamada do método.

## Arquitetura
`aluno.py` contém a classe e suas regras; `verificar_modelo.py` executa verificações; a interface, quando presente, fica em `main.py` e importa o modelo.

## Testes executados
`python -B verificar_modelo.py` — concluído com código de saída 0: “Verificações do modelo concluídas.”

**Situação:** testes automatizados do modelo aprovados; inspeção visual da interface não está incluída nessa execução.

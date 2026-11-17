# Relatório da Aula 14 — Produtos persistidos com SQLite

**Aluno:** Saimon Costa Camilo  
**Turma:** TDS  
**Data do relatório:** 12/11/2026

## 1. Objetivo da atividade

Introduzir persistência relacional para produtos e clientes, mantendo o pedido em memória e reutilizando os módulos de domínio, pagamento, JSON e CSV.

## 2. Arquivos e organização do projeto

- `main.py`: interface Tkinter.
- `repositorio.py`: acesso SQLite e validações.
- `modelos.py`: produto, item e pedido.
- `pagamento.py`, `arquivos.py`, `relatorios.py` e `perfis.py`: funcionalidades reaproveitadas.
- `verificar.py`: testes automatizados.

## 3. Conceitos e decisões técnicas

- Criar tabelas com `CREATE TABLE IF NOT EXISTS` sem apagar dados existentes.
- Usar SQL parametrizado e armazenar preços em centavos inteiros.
- Confirmar gravações com `commit()` e fechar conexões.
- Manter pedido em memória enquanto produtos/clientes persistem.

## 4. Execução e evidências

O registro A14 documenta execução de `python verificar.py` e aprovação dos casos T00–T13: inicialização idempotente, preço em centavos, apóstrofo em nome, validações, IDs, reabertura do banco, falha de conexão, JSON, CSV, pedido em memória e clientes. O checklist visual Tkinter está explicitamente pendente.

## 5. Dificuldades, correções e pontos de atenção

Abrir `main.py` em ambiente gráfico e completar o checklist manual de cadastro, mensagens, persistência após reabertura, navegação por teclado e redimensionamento.

## 6. Conclusão

A atividade contribui para a evolução gradual do projeto da UC8. Este relatório foi elaborado a partir dos arquivos, README e registros existentes nesta pasta. Os testes são considerados concluídos somente quando há evidência explícita de execução; itens sem resultado observado permanecem identificados como pendentes, evitando registrar como realizado algo que não está comprovado.

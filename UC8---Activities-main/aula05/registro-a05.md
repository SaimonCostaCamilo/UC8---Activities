# Registro A05 — Interfaces escolares com organização por grupos e janelas

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Organizar a interface Tkinter em frames/grupos, separar a janela principal das consultas e manter o retrato do último registro confirmado independente das edições em andamento.

## Retomada e respostas
- O registro confirmado reúne identificação, turma, cinco notas e média.
- Uma quinta nota inválida não altera o nome nem os demais dados do último registro confirmado; a tentativa inteira é rejeitada.
- `command` recebe a referência do callback; a função é executada quando o usuário aciona o botão.
- A janela raiz contém o frame principal; cada `grid()` organiza os widgets filhos do respectivo frame, sem misturar os grids de pais diferentes.
- Editar altera os campos; confirmar valida e atualiza o registro; limpar remove apenas o conteúdo de edição, sem apagar indevidamente o registro confirmado.

## Matriz de validação prevista
A matriz contempla grupos e hierarquia dos widgets, média 8,0 para notas 6–10, consulta sem registro, abertura de consultas C1/C2, edição sem confirmação, tentativa inválida, confirmação de novo registro, limpeza e fechamento de janelas por botão, Escape e X. Os casos de limite, faixa, vírgula/ponto e identificação também estão previstos.

**Situação:** respostas e previsões preenchidas. Os casos dependentes da janela precisam de execução manual em desktop; não há verificador automatizado nesta aula.

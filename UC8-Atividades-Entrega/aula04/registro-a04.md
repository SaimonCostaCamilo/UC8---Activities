# Registro A04 — Sistema escolar e cálculo de médias

**Nome:** Saimon Camilo  
**Turma:** TDS  
**Data:** 13/11/2026

## Objetivo e conceitos
Validar identificação e cinco notas, calcular a média e manter separado o registro confirmado dos campos em edição.

## Retomada e respostas
- Uma última entrada inválida não pode substituir o registro válido anterior; a confirmação só ocorre após validar todos os campos.
- `get()` retorna texto. A entrada decimal com vírgula deve ser normalizada para ponto antes da conversão numérica.
- Digitar outro nome não confirma uma nova consulta: é necessário executar a ação de calcular/confirmar, pois campos editados ainda não constituem registro válido.
- Devem ficar juntos nome, turma, cinco notas e média da mesma tentativa.
- A quantidade deve ser validada antes da divisão para evitar média incorreta ou divisão por zero.
- Para notas 6, 7, 8, 9 e 10, a média prevista é 8,0.

## Matriz de validação prevista
Foram definidos os casos de lista vazia, notas nos limites 0 e 10, decimais com vírgula/ponto, edição sem confirmar, tentativa inválida seguida de correção, identificação vazia, notas vazias/textuais e valores fora da faixa.

**Situação:** respostas conceituais e matriz de casos preenchidas. Não há script automatizado nesta aula; execução visual dos casos deve ser conferida no desktop.

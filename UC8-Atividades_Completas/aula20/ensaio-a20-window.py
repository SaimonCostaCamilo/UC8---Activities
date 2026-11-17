"""Roteiro de apoio; inspeção visual e de teclado deve ser feita pelo aluno."""
ROTEIRO = [
    'Executar python -B main.py a partir da pasta aula20.',
    'Cadastrar aluno e plano fictícios e anotar os IDs gerados.',
    'Criar matrícula com os IDs existentes e confirmar a listagem.',
    'Tentar matrícula com aluno/plano inexistente e conferir mensagem de erro.',
    'Confirmar que aluno/plano com matrícula vinculada não pode ser excluído.',
    'Percorrer controles com Tab e Shift+Tab; conferir foco e acionamento por Enter.',
    'Redimensionar a janela e conferir se tabelas e campos continuam acessíveis.',
]
if __name__ == '__main__':
    print('ROTEIRO DE INSPEÇÃO MANUAL — marque somente após observar:')
    for i, item in enumerate(ROTEIRO, 1): print(f'{i}. [ ] {item}')

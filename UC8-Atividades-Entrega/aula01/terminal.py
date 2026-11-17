"""A01 — prática 1. Use somente nome e idade fictícios."""

def conferir(nome, idade_texto):
    novo_nome = nome.strip()
    try:
        idade = int(idade_texto)
        if idade <= 0:
            return "idade deve ser maior que zero"
    except ValueError as e:
        return f"idade deve ser um número inteiro maior que zero: {e}"
    
    return f"Nome: {novo_nome} de idade {idade}"


if __name__ == "__main__":
    nome = input("Nome fictício: ")
    idade_texto = input("Idade fictícia: ")
    print(conferir(nome, idade_texto))

"""Ensaio didático correspondente à sequência da atividade A20."""
alunos = {1: "Lia"}
planos = {7: "Mensal"}
matricula = {"aluno_id": 1, "plano_id": 7}

def vinculo_valido(dados):
    return dados["aluno_id"] in alunos and dados["plano_id"] in planos

print(vinculo_valido(matricula))
alunos[1] = "Lia Souza"
print(vinculo_valido(matricula))
matricula["aluno_id"] = 99
print(vinculo_valido(matricula))

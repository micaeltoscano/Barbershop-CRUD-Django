from crud import Crud


class Funcionario(Crud):

    tabela = 'funcionario'
    colunas_permitidas = ['nome', 'email', 'cpf', 'endereco', 'numero_celular', 'salario', 'especialidade', 'status']
    coluna_id = 'idfuncionario'

    def cadastrar_funcionario(self, nome, email, cpf, endereco, numero_celular, salario, especialidade):

        super().cadastro(
            nome = nome,
            email = email, 
            cpf = cpf, 
            endereco = endereco,
            numero_celular = numero_celular,
            salario = salario,
            especialidade = especialidade,
        )

        query = "SELECT IDFUNCIONARIO FROM FUNCIONARIO WHERE CPF = %s ORDER BY IDFUNCIONARIO DESC LIMIT 1"
        result = self.processar(query, (cpf,))
        return result
    
    def ler_todos_funcionarios(self):
        return super().ler_todos()
    
    def pesquisar_nome(self, nome):
        return super().pesquisar_nome(nome) 
    
    def ler_todos_funcionarios_ativos(self):
        return super().ler_todos_ativos()
    
    def ler_um_funcionario(self, id):
        return super().listar_um(id)
    
    def atualizar_funcionario(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_funcionario(self, id):
        return super().deletar(id)
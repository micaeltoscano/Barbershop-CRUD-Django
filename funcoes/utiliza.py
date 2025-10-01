from crud import Crud

class Utiliza(Crud):

    tabela = "utiliza"
    colunas_permitidas = ['id_servico', 'id_produto', 'quantidade']
    coluna_id = 'idutiliza'

    
    def cadastro_utiliza(self, id_servico, id_produto, quantidade):
        super().cadastro(
            id_servico = id_servico,
            id_produto = id_produto,
            quantidade = quantidade
        )

    def ler_todos_utiliza(self):
        return super().ler_todos()

    def pesquisar_nome_utiliza(self, nome):
        return super().pesquisar_nome(nome)

    def ler_um_utiliza(self, id):
        return super().listar_um(id)

    def atualizar_utiliza(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)

    def deletar_utiliza(self, id):
        return super().deletar(id)

from crud import Crud

class Categoria(Crud):

    tabela = 'categoria'
    colunas_permitidas = ['nome_categoria']
    coluna_id = 'idcategoria'

    def cadastro_categoria(self, nome_categoria):
        super().cadastro(
            nome_categoria = nome_categoria
        )

    def ler_todas_categorias(self):
        return super().ler_todos()
    
    def pesquisar_nome_categoria(self, nome):
        return super().pesquisar_nome(nome)
    
    def ler_um_categoria(self, id):
        return super().listar_um(id)
    
    def atualizar_categoria(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_categoria(self, id):
        return super().deletar(id)
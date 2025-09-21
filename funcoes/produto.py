from crud import Crud

class Produto(Crud):

    tabela = 'produto'
    colunas_permitidas = ['nome','valor', 'tipo', 'status', 'cidade']
    coluna_id = 'idproduto'
    
    def cadastro_produto(self, nome, valor, tipo, cidade):
        
        super().cadastro(
            nome = nome, 
            valor = valor, 
            tipo = tipo,
            cidade = cidade
                         )
    
    def ler_todos_produtos(self):
        return super().ler_todos()
    
    def pesquisar_nome_produto(self, nome):
        return super().pesquisar_nome(nome)
    
    def ler_todos_produtos_ativos(self):
        return super().ler_todos_ativos()
    
    def ler_um_produto(self, id):
        return super().listar_um(id)
    
    def atualizar_produto(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_produto(self, id):
        return super().deletar(id)
    


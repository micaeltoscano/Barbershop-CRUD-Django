from crud import Crud
from django.db import transaction

class Estoque(Crud):
    
    tabela = 'estoque'
    colunas_permitidas = ['id_produto','quantidade_atual', 'quantidade_minima', 'ultima_atualizacao']
    coluna_id = 'idestoque'

    def cadastro_estoque(self, nome_produto, quantidade_atual, quantidade_minima):
        try:

            consulta = self.processar("""SELECT idproduto FROM produto WHERE nome = %s""", (nome_produto,), fetch=True)
            
            print(f"{consulta}: id do produto")
            if not consulta:
                raise ValueError(f"Produto '{nome_produto}' não encontrado")
            
            id_produto = consulta[0]['idproduto']
            
            super().cadastro(
                id_produto=id_produto, 
                quantidade_atual=quantidade_atual, 
                quantidade_minima=quantidade_minima,
                )
            
            print("chegou aqui!")
            return True
            
        except Exception as e:
            print(f"Erro ao cadastrar estoque: {e}")
            return False
    
    def ler_todo_estoque(self):
        return self.processar("""
                                SELECT e.*, p.nome 
                                FROM estoque e 
                                LEFT JOIN produto p ON e.id_produto = p.idproduto
                                ORDER BY e.idestoque ASC  -- Ordena pelo ID do estoque (menor para maior)
                            """, fetch=True)
                            
    def pesquisar_nome_estoque(self, nome):
        return super().pesquisar_nome(nome)
    
    def ler_um_estoque(self, id):
        return self.processar(""" 
                              SELECT e.*, p.nome 
                              FROM estoque e
                              LEFT JOIN produto p ON e.id_produto = p.idproduto
                              WHERE e.idestoque = %s
                              """, (id,), fetch=True)
    
    def atualizar_estoque(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_estoque(self, id):
        return super().deletar(id)
    
    def atualizar_quantidade(self, origem, id_origem): 
        
        #DICIONARIO COM AS OPERAÇÕES POSSÍVEIS PARA ATUALIZAÇÃO DO ESTOQUE
        config = {
            'servico': {
                'tabela_origem': 'utiliza', 
                'coluna_origem': 'id_servico',
                'operacao': -1  
                },
            'venda': {                                  #A VENDA É A COMPRA DE PRODUTOS PELO CLIENTE
                'tabela_origem': 'itens_compra',
                'coluna_origem': 'id_compra',
                'operacao': -1   
                },
            'compra': {                                 #A COMPRA É A COMPRA DE PRODUTOS PELA BARBEARIA
                'tabela_origem': 'itens_compra',
                'coluna_origem': 'id_compra',
                'operacao': 1    
                }
            }

        if origem not in config:
            raise ValueError("Origem inválida. Use 'servico', 'venda' ou 'compra'")
        
        tabela_origem = config[origem]['tabela_origem'] #RETORNA A TABELA DE ONDE VAI BUSCAR OS DADOS
        coluna_origem = config[origem]['coluna_origem'] #RETORNA A COLUNA DE ONDE VAI BUSCAR OS DADOS
        operacao = config[origem]['operacao']           #RETORNA A OPERAÇÃO A SER REALIZADA 

        with transaction.atomic():
            #FAZ UMA CONSULTA NAS TABELAS DE ORIGEM PARA PEGAR A QUANTIDADE E O ID DO PRODUTO
            pesquisa = self.processar(f"""SELECT QUANTIDADE, ID_PRODUTO 
                                        FROM {tabela_origem}
                                        WHERE {coluna_origem} = %s""", (id_origem,), fetch=True)
            
                    
            if not pesquisa:
                raise ValueError("Serviço não encontrado ou não utiliza produtos.")

            #ATUALIZA O ESTOQUE DE CADA PRODUTO UTILIZADO NO SERVIÇO
            for item in pesquisa:
                quantidade = item['quantidade']
                id_produto = item['id_produto']
            
                estoque_info = self.processar(f"""SELECT {self.coluna_id} FROM {self.tabela} 
                                            WHERE id_produto = %s""", 
                                        (id_produto,), fetch=True)
                
                if not estoque_info:
                    raise ValueError(f"Produto ID {id_produto} não encontrado no estoque.")
                
                id_estoque = estoque_info[0][self.coluna_id]  
            
                quantidade_atual_info = self.processar(f"""SELECT quantidade_atual FROM {self.tabela} 
                                                        WHERE {self.coluna_id} = %s""",
                                                    (id_estoque,), fetch=True)
                
                if not quantidade_atual_info:
                    raise ValueError(f"Estoque ID {id_estoque} não encontrado.")
                
                estoque_atual = quantidade_atual_info[0]['quantidade_atual'] + (quantidade * operacao)

                estoque_atual = quantidade_atual_info[0]['quantidade_atual']

                novo_estoque = estoque_atual + (quantidade * operacao)

                if novo_estoque < 0:

                    raise ValueError(
                        f"Operação inválida: Produto ID {id_produto} ficaria com estoque negativo "
                        f"({estoque_atual} disponível, tentativa de retirar {quantidade})."
                    )
                
                self.atualizar_estoque('quantidade_atual', novo_estoque, id_estoque)

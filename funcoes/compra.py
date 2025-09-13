from crud import Crud
from itens_compra import Itens_compra
from estoque import Estoque
from pagamentos import Pagamento

class Compra(Crud):
    tabela = 'compra'
    colunas_permitidas = ['data_compra', 'valor_total']
    coluna_id = 'idcompra'
    
    def ler_todas_compras(self):
        return super().ler_todos()
    
    def atualizar_compra(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_compra(self, id):
        return super().deletar(id)
    

    def registrar_compra(self, metodo_pagamento):
        
        estoque = Estoque()
        pagamento = Pagamento()
        itens = Itens_compra()
        
        #FAZ UM CADASTRO INICIAL PARA CRIAR UM ID
        super().cadastro(valor_total=0)

        #USA FUNCAO MAX PARA BUSCAR O ÚLTIMO ID INSERIDO
        id_compra = self.processar("SELECT MAX(idcompra) FROM compra", fetch=True)[0]['max']

        #CHAMA A FUNCAO DE RECEBER OS ITENS DA COMPRA
        itens.receber_produtos(id_compra)

        #CALCULA O TOTAL DA COMPRA
        total_compra = self.processar(
                                    "SELECT SUM(valor_total_item) FROM itens_compra WHERE id_compra = %s",
                                    (id_compra,), fetch=True)[0]['sum']

        #ATUALIZA A TABELA DE COMPRA COM O VALOR TOTAL REALIZADO NA COMPRA
        self.atualizar_compra('valor_total', total_compra, id_compra)

        #REGISTRA O PAGAMENTO NA TABELA DE PAGAMENTOS
        pagamento.registrar_pagamento_produto(id_compra, metodo_pagamento)

        #ATUALIZA O ESTOQUE
        estoque.atualizar_quantidade('venda', id_compra)

        print(f"Compra {id_compra} registrada com sucesso! Total: {total_compra}")

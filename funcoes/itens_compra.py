from crud import Crud

class Itens_compra(Crud):

    tabela = 'itens_compra'
    colunas_permitidas = ['id_compra', 'id_produto', 'quantidade', 'valor_unitario', 'valor_total_item']
    coluna_id = 'iditenscompra'

    def receber_produtos(self, idcompra):
        condicao = True

        while condicao:
            try:
                #RECEBE OS ID'S DOS PRODUTOS QUE ESTAO SENDO COMPRADOS
                idproduto = int(input("Digite o ID do produto que está recebendo (ou 0 para sair): "))
                if idproduto == 0:
                    break
                
                #RECEBE A QUANTIDADE DO PRODUTO
                quantidade = int(input("Digite a quantidade recebida: "))
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero.")
                    continue
                
                #CONSULTA PARA BUSCAR O VALOR DAQUELE PRODUTO
                consulta = self.processar(
                                            """ SELECT VALOR
                                                FROM PRODUTO 
                                                WHERE IDPRODUTO = %s """,
                                            (idproduto,), fetch=True)
                
                #PEGA O VALOR E DEPOIS CALCULA O VALOR TOTAL DA COMPRA
                valor_unitario = consulta[0]['valor']
                valor_total_item = valor_unitario * quantidade
                
                #CADASTRA NA TABELA DE ITENS COMPRADOS
                super().cadastro(
                                id_compra = idcompra,
                                id_produto = idproduto,
                                quantidade = quantidade,
                                valor_unitario = valor_unitario,
                                valor_total_item = valor_total_item)
                
            except ValueError:
                print("Por favor, digite um número válido.")

    def ler_todos_itens_compra(self):
        return super().ler_todos()
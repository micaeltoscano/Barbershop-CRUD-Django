from crud import Crud
from itens_compra import Itens_compra
from estoque import Estoque
from pagamentos import Pagamento
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction

class Compra(Crud):
    tabela = 'compra'
    colunas_permitidas = ['id_cliente', 'id_funcionario', 'valor_total', 'data_compra', 'valor_total']
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


    def registrar_compra_django(self, id_cliente, id_funcionario, metodo_pagamento, produtos_selecionados, quantidades, request):
        estoque = Estoque()
        pagamento = Pagamento()
        itens = Itens_compra()
        
        try:
            with transaction.atomic():
                
                cliente_info = self.processar(
                    "SELECT c.cidade, c.is_flamengo, c.is_onepiece FROM cliente c "
                    "WHERE c.idcliente = %s",
                    (id_cliente,), fetch=True
                )
                        
                # VARIÁVEL PARA ARMAZENAR O DESCONTO QUE SERÁ APLICADO
                desconto = Decimal('0.0')

                if cliente_info:
                    cliente = cliente_info[0]
                    if cliente['cidade'] == 'Souza' or cliente['is_flamengo'] or cliente['is_onepiece']:
                        desconto = Decimal('0.1')  # aplica 10% de desconto
                        messages.info(request, "Cliente elegível para 10% de desconto!")
            
                #LEMBRETE: COLOCAR STATUS DA COMPRA

                # INICIALIZA UMA COMPRA
                super().cadastro(
                    valor_total=0, 
                    id_cliente=int(id_cliente), 
                    id_funcionario=int(id_funcionario)
                )

                # OBTÉM O ÚLTIMO ID INSERIDO
                id_compra_result = self.processar("SELECT MAX(idcompra) FROM compra", fetch=True)
                id_compra = id_compra_result[0]['max'] if id_compra_result else None

                # INSERE ITENS DA COMPRA
                itens.receber_produtos_django(id_compra, produtos_selecionados, quantidades)

                print(id_compra)
                estoque.atualizar_quantidade('venda', id_compra)

                # CALCULA O TOTAL DA COMPRA
                total_compra = self.processar(
                    "SELECT SUM(valor_total_item) FROM itens_compra WHERE id_compra = %s",
                    (id_compra,), fetch=True
                )[0]['sum']
                
                # ATUALIZA A COMPRA COM O VALOR TOTAL
                valor_final = total_compra * (1 - desconto)

                self.atualizar_compra('valor_total', valor_final, id_compra)

                
                # REGISTRA O PAGAMENTO
                pagamento.registrar_pagamento_produto(id_compra, metodo_pagamento)


                messages.info(
                    request,
                    f"Compra registrada com sucesso! Total: {valor_final:.2f}. "
                    f"Total sem desconto: {total_compra:.2f}"
                )
        
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao registrar a compra: {str(e)}")
            raise  # relança para que a view também saiba do erro

        


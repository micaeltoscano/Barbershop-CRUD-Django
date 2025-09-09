from crud import Crud

class Pagamento(Crud):

    tabela = 'pagamento'
    colunas_permitidas = ['id_agenda', 'id_venda', 'valor', 'forma_pagamento', 'data_pagamento', 'status']
    coluna_id = 'idpagamento'
    
    def ler_todos_pagamentos(self):
        return super().ler_todos()

    def ler_um_pagamento(self, id):
        return super().listar_um(id)
    
    def atualizar_pagamento(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_pagamento(self, id):
        return super().deletar(id)
    
    def registrar_pagamento_servico(self, idagenda, metodo_pagamento):
        try:
            #FAZ UMA CONSULTA PARA BUSCAR O VALOR DO SERVICO
            buscar_valor = self.processar(
                                        """ SELECT S.VALOR
                                            FROM AGENDA A
                                            INNER JOIN SERVICO S ON A.ID_SERVICO = S.IDSERVICO
                                            WHERE A.IDAGENDA = %s """,
                                            (idagenda,), fetch=True)
            if not buscar_valor:  
                raise ValueError(f"Nenhum valor encontrado para a agenda {idagenda}")
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar valor do serviço: {e}")
        
        #CADASTRA NA TABELA DE PAGAMENTOS
        super().cadastro(
            id_agenda=idagenda,
            id_compra = None,
            valor=buscar_valor[0]['valor'],
            forma_pagamento=metodo_pagamento,
            status='APROVADO',
        )

        print("Pagamento registrado com sucesso.")

    #UNIFICAR AS DUAS FUNCOES EM UMA SÓ (NAO FIZ AGORA -- PREGUICA)
    def registrar_pagamento_produto(self, id_compra, metodo_pagamento):
        try:
    
            buscar_valor = self.processar(
                """SELECT SUM(P.VALOR * IC.QUANTIDADE)
                FROM ITENS_COMPRA IC
                INNER JOIN PRODUTO P ON IC.ID_PRODUTO = P.IDPRODUTO
                WHERE IC.ID_COMPRA = %s""",
                (id_compra,), fetch=True
            )
            
        except Exception as e:
            raise ValueError(f"Erro ao buscar valor do produto: {e}")
            
        valor_total = buscar_valor[0]['sum']
            
        super().cadastro(
            id_agenda=None,
            id_compra = id_compra,
            valor=valor_total,
            forma_pagamento=metodo_pagamento,
            status='APROVADO',
            )

        print("Pagamento de produtos registrado com sucesso.")        

    

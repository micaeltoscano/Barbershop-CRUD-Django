from crud import Crud
from pagamentos import Pagamento
from estoque import Estoque
from disponibilidade import Disponibilidade
from servico import Servico

class Agenda(Crud):
    
    tabela = 'agenda'
    colunas_permitidas = ['id_cliente', 'id_funcionario', 'id_servico', 'dia', 'horario', 'status'] 
    coluna_id = 'idagenda'

    def verificar_agendamento(self, id_funcionario, horario, dia):

        #VERIFICA SE JÁ HÁ UM AGENDAMENTO PARA O FUNCIONARIO NAQUELE DIA E HORARIO
        try:
            jaagendado = self.processar(
                                        """ SELECT 1 
                                            FROM agenda 
                                            WHERE dia = %s AND horario = %s AND id_funcionario = %s""",
                                        (dia, horario, id_funcionario),
                                        fetch=True
                                    )
            if jaagendado:
                raise ValueError(f"O funcionário de ID {id_funcionario} já tem um agendamento no dia {dia} no horário {horario}")
            else:
                return True
            
        except Exception as e:
            raise ValueError(f"Erro ao verificar se havia agendamento para o funcionário no dia: {e}")

    def cadastrar_agenda(self, dia, horario, id_funcionario, id_servico, id_cliente, status='agendado'):

        disponibilidade = Disponibilidade()
        servico = Servico()

        if not disponibilidade.disponibilidade_funcionario(id_funcionario, horario, dia):
            raise ValueError("Funcionário não está disponível nesse horário.")

        if not self.verificar_agendamento(id_funcionario, horario, dia):
            raise ValueError("Já existe um agendamento para esse horário.")

        if not servico.verificar_servico(id_funcionario, horario, dia, id_servico):
            raise ValueError("Serviço não pode ser agendado nesse horário.")

        #CADASTRO NA TABELA DE AGENDA
        super().cadastro(
        dia=dia,
        horario=horario,
        id_funcionario=id_funcionario,
        id_servico=id_servico,
        id_cliente=id_cliente,
        status=status
    )

    #FUNCOES DE LEITURA:
    def ler_toda_agenda(self):
        return super().ler_todos()
    
    def ler_um_agenda(self, id):
        return super().listar_um(id)

    #FUNCAO PARA ATUALIZAÇÃO  - Precisa corrigir a disponibilidade do funcionario quando altera a agenda
    def atualizar_agenda(self, coluna, novo_valor, id):
        if coluna in ['id_funcionario', 'id_servico', 'dia', 'horario']:
            #PROCURAR AGENDAMENTO ASSOCIADO Á ALTERAÇÃO
            agendamento = self.ler_um_agenda(id)
            #debug: print(agendamento[0]['horario'])
            if not agendamento:
                return 
            
            #ATUALIZAÇÃO DO NOME DA COLUNA E CONSULTA DOS ATRIBUTOS NECESSARIOS PARA REALIZAR A VERIFICACAO:
            agendamento[0][coluna] = novo_valor
            id_funcionario = agendamento[0]['id_funcionario']
            horario = agendamento[0]['horario']
            dia = agendamento[0]['dia']
            id_servico = agendamento[0]['id_servico']

            #VERIFICACAO:
            disponibilidade = Disponibilidade()
            servico = Servico()

            if not disponibilidade.disponibilidade_funcionario(id_funcionario, horario, dia):
                raise ValueError("Funcionário não está disponível nesse horário.")

            if not self.verificar_agendamento(id_funcionario, horario, dia):
                raise ValueError("Já existe um agendamento para esse horário.")

            if not servico.verificar_servico(id_funcionario, horario, dia, id_servico):
                raise ValueError("Serviço não pode ser agendado nesse horário.")

        #ATUALIZA A COLUNA 
        return super().atualizar(coluna, novo_valor, id)

    #FUNCAO DE DELETAR
    def deletar(self, id):
        return super().deletar(id)

    #FUNCAO PARA CONFIRMAR O ENCERRAMENTO DO SERVICO
    def confirmar_servico(self, id_agenda, metodo_pagamento):
        try:     
            #ATUALIZA O STATUS DA AGENDA PARA CONCLUIDO
            self.atualizar_agenda("status", "concluido", id_agenda)
            print("to aqui")
            #REGISTRA UM PAGAMENTO NA TABELA DE PAGAMENTOS
            pagamento = Pagamento()
            pagamento.registrar_pagamento_servico(id_agenda, metodo_pagamento)

            #CONSULTA PARA BUSCAR O ID DO SERVIÇO ASSOCIADO AO AGENDAMENTO
            consulta = self.processar(
                                        """ SELECT ID_SERVICO
                                            FROM AGENDA
                                            WHERE IDAGENDA = %s """,
                                            (id_agenda,), fetch=True)
            if not consulta:
                raise ValueError(f"Serviço não encontrado para o agendamento ID {id_agenda}.")
            
           
            #COM O ID, ATUALIZA O ESTOQUE COM A QUANTIDADE DE PRODUTOS QUE FORAM USADOS DURANTE O SERVICO
            id_servico = consulta[0]['id_servico']
            estoque = Estoque()
            estoque.atualizar_quantidade(origem='servico', id_origem=id_servico) 
            
            print(f"Serviço {id_agenda} confirmado com sucesso!")

        except Exception as e:
            raise ValueError(f"Erro ao confirmar serviço e registrar pagamento: {e}")

            



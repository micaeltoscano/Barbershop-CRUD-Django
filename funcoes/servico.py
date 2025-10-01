from crud import Crud

class Servico(Crud):

    tabela = "servico"
    colunas_permitidas = ['nome', 'valor', 'id_categoria','duracao', 'status']
    coluna_id = 'idservico'

    def cadastro_servico(self, nome, valor, id_categoria, duracao):

        super().cadastro(
            nome = nome, 
            valor = valor, 
            id_categoria = id_categoria, 
            duracao = duracao
        )
        
        consulta = self.processar("""SELECT idservico FROM servico WHERE nome = %s ORDER BY idservico DESC LIMIT 1""", (nome,), fetch=True)
        return consulta[0]['idservico'] if consulta else None

    def ler_todos_servicos(self):
        return super().ler_todos()
    
    def ler_todos_servicos_ativos(self):
        return super().ler_todos_ativos()
    
    def pesquisar_nome(self, nome):
        return super().pesquisar_nome(nome)
    
    def ler_um_servico(self, id):
        return super().listar_um(id)
    
    def atualizar_servico(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_servico(self, id):
        return super().deletar(id)
    
    def verificar_servico(self, id_funcionario, horario, dia, id_servico):
        
        try:
            #CONSULTA PARA VER A DURACAO DO SERVICO
            resultado = self.processar(
                                        """ SELECT DURACAO
                                            FROM SERVICO
                                            WHERE IDSERVICO = %s """,
                                        (id_servico,), fetch=True
                                    )

            if not resultado:
                raise ValueError(f"Serviço de ID {id_servico} não encontrado.")

            duracao_servico = resultado[0]['duracao']
        
        except Exception as e:
            raise ValueError(f"erro ao consultar duração do servico")
        
        try:

            #CONSULTA PARA VERIFICAR SE A DURACAO DO SERVICO INTERFERE NA DURAÇÃO DE OUTROS SERVICOS
            indisponibilidade_horario = self.processar(
                                                        """ SELECT 1
                                                            FROM agenda a
                                                            JOIN servico s ON a.id_servico = s.idservico
                                                            WHERE a.id_funcionario = %s
                                                            AND a.dia = %s
                                                            AND NOT (
                                                                %s + interval '%s minute' <= a.horario
                                                                OR %s >= a.horario + s.duracao * interval '1 minute'
                                                            )
                                                            AND A.STATUS = 'ATIVO' """,
                                                        (id_funcionario, dia, horario, duracao_servico, horario),
                                                        fetch=True
                                                    )

            if indisponibilidade_horario:
                raise ValueError("Horário indisponível, por haver conflito com outro agendamento.")
            
            return True
        
        except Exception as e:
            raise ValueError(f"erro ao verificar se havia interferencia de horarios: {e}")
    
    
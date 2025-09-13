from crud import Crud

class Disponibilidade(Crud):

    tabela = "disponibilidade"
    colunas_permitidas = ['id_funcionario', 'dia_semana', 'hora_inicio', 'hora_fim']
    coluna_id = 'iddisponibilidade'

    def cadastro_disponibilidade(self,  id_funcionario, dia_semana, hora_inicio, hora_fim):

        try:
            jacadastrado = self.processar(
                                        """SELECT 1 
                                        FROM disponibilidade 
                                        WHERE  id_funcionario = %s AND dia_semana = %s AND hora_inicio = %s AND hora_fim = %s""",
                                        ( id_funcionario, dia_semana, hora_inicio, hora_fim), fetch=True)
            if jacadastrado:
                print("Disponibilidade já cadastrada para esse funcionário nesse horário.")
                return
        
            super().cadastro(
                id_funcionario=id_funcionario,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            )
        except Exception as e:
            raise ValueError(f"Ocorreu um erro durante o cadastro na tabela {self.tabela}: {e}")

    def ler_todas_disponibilidades(self):
        return super().ler_todos()
    
    def pesquisar_nome(self, nome):
        return super().pesquisar_nome(nome)
    
    def ler_um_disponibilidade(self, coluna_id):
        return super().listar_um(coluna_id)
    
    def atualizar_disponibilidade(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)
    
    def deletar_disponibilidade(self, id):
        return super().deletar(id)
    
    def disponibilidade_funcionario(self, id_funcionario, horario, dia):

        #VERIFICAR A DISPONIBILIDADE DO FUNCIONARIO NO DIA
        try:
            disponibilidade_dia = self.processar(
                                                """ SELECT 1 
                                                    FROM disponibilidade 
                                                    WHERE id_funcionario = %s AND %s BETWEEN hora_inicio AND hora_fim""",
                                                (id_funcionario, horario),
                                                fetch=True
                                            )
            if disponibilidade_dia:
                return True
            
            else:
                raise ValueError(f"O funcionário de ID {id_funcionario} não está disponível no dia {dia} no horário {horario}")
            
        except Exception as e:
            raise ValueError(f"Erro ao consultar a disponibilidade do funcionario: {e}")
       
    

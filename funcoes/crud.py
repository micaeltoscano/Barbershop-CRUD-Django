from banco import Banco
from psycopg2 import IntegrityError

class Crud(Banco):
    tabela = None
    colunas_permitidas = []
    coluna_id = 'id'

    def cadastro(self, **kwargs):
        try:
            #TRATAMENTO DE STRING PARA PASSAGEM DOS PARAMETROS DENTRO DA FUNCAO:

            #O KWARGS RETORNA UM DICIONARIO {'COLUNA1': 'PARAMETRO1', ... }, ENTÃO USAMOS KEY() PARA PEGAR O NOME DAS COLUNAS E UM ','.JOIN PARA TIRAR OS VALORES DA LISTA
            colunas = ','.join(kwargs.keys()) 

            #PRECISAMOS DOS PLACEHOLDERS %s PARA RECEBER A PASSAGEM DE VALORES, ENTAO MULTIPLICAMOS A %s * QUANTIDADE DE ARGUMENTOS PARA QUE FOSSEM GERADOS PLACEHOLDERS EQUIVALENTES 
            placeholder = ', '.join(['%s'] * len(kwargs))

            #RECEBER OS VALORES DA FUNCAO EM FORMATO DE TUPLA
            valores = tuple(kwargs.values())

            #FUNCAO PARA FAZER CADASTRO:
            self.processar(f"""
                            INSERT INTO {self.tabela} ({colunas}) VALUES ({placeholder})""",
                            valores)
            
            print(f"registro em {self.tabela} cadastrado com sucesso ")    

        except IntegrityError as e:
            # Apenas mostra a mensagem amigável
            if 'funcionario_email_key' in str(e):
                print("Esse e-mail já está cadastrado!")
            else:
                print(f"Erro de integridade: {e}")
            raise  # relança se precisar de tratamento externo
       
    def ler_todos(self):
        try:
            leitura = self.processar(f"SELECT * FROM {self.tabela} ORDER BY {self.coluna_id}", fetch = True)
            return leitura
        
        except Exception as e:
            print(f"Ocorreu um erro durante o leitura da tabela {self.tabela}: {e}")
            return []
    
    def ler_todos_ativos(self):
        try:
            consulta = self.processar(f"""SELECT * FROM {self.tabela} WHERE STATUS = 'ATIVO' ORDER BY {self.coluna_id}""", fetch = True)
            return consulta
        
        except Exception as e:
            print(f"Ocorreu um erro durante o leitura da tabela {self.tabela}: {e}")
            return []
        
    def pesquisar_nome(self, nome):
        try:
            pesquisa = self.processar(f"SELECT * FROM {self.tabela} WHERE nome = %s", (nome,), fetch = True)
            return pesquisa
        
        except Exception as e:
            print(f"Ocorreu um erro durante a pesquisa na tabela {self.tabela}: {e}")
            return []
    
    def listar_um(self, id):
        try:
            listar = self.processar(f"SELECT * FROM {self.tabela} WHERE {self.coluna_id} = %s", (id,), fetch = True)
            if not listar:
                print("Não foram encontrados registros")
    
            return listar
        
        except Exception as e:
            print(f"Ocorreu um erro durante a listagem na tabela {self.tabela}: {e}")
            return []
        
    def atualizar(self, coluna, novo_valor, id):
        if coluna not in self.colunas_permitidas:
            print(f"Não é possível alterar a coluna: {coluna}")

            return False  # Retorna False indicando falha

        try:
            linhas_afetadas = self.processar(
                f"UPDATE {self.tabela} SET {coluna} = %s WHERE {self.coluna_id} = %s",
                (novo_valor, id)
            )
            
            if linhas_afetadas == 0:
                print("Registro não encontrado, nenhuma atualização realizada.")
                return False
            else:
                print("Registro atualizado com sucesso!")
                return True  

        except IntegrityError as e:
            
            if 'funcionario_email_key' in str(e):
                print("Esse e-mail já está cadastrado!")
            else:
                print(f"Erro de integridade: {e}")
            raise 

    def deletar(self, id):
        
        try:
            deletar = self.processar(f"DELETE FROM {self.tabela} WHERE {self.coluna_id} = %s", 
                                    (id,))
            if deletar == 0:
                print("Registro não encontrado, nenhum registro foi removido.")
            else:
                print("Registro foi removido com sucesso!")

        except Exception as e:
            print(f"Erro ao deletar registro da tabela {self.tabela}: {e}")

            


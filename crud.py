from banco import Banco
import tabulate

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

        except Exception as e:
            raise ValueError(f"Ocorreu um erro durante o cadastro na tabela {self.tabela}: {e}")
       
    def ler_todos(self):
        try:
            leitura = self.processar(f"SELECT * FROM {self.tabela} ORDER BY {self.coluna_id}", fetch = True)
            if leitura:
                return leitura
            else:
                print("Nenhum registro encontrado.")
            return leitura
        except Exception as e:
            print(f"Ocorreu um erro durante o leitura da tabela {self.tabela}: {e}")
            return []
        
    def pesquisar_nome(self, nome):
        try:
            pesquisa = self.processar(f"SELECT * FROM {self.tabela} WHERE nome = %s", (nome,), fetch = True)
            if pesquisa:
                return pesquisa
            else:
                print("Nenhum registro encontrado.")
            return pesquisa
        except Exception as e:
            print(f"Ocorreu um erro durante a pesquisa na tabela {self.tabela}: {e}")
            return []
    
    def listar_um(self, id):
        try:
            listar = self.processar(f"SELECT * FROM {self.tabela} WHERE {self.coluna_id} = %s", (id,), fetch = True)
            if listar:
                return listar
            else:
                print("Nenhum registro encontrado.")
            return listar
        except Exception as e:
            print(f"Ocorreu um erro durante a listagem na tabela {self.tabela}: {e}")
            return []
        
    def atualizar(self, coluna, novo_valor, id):
        if coluna not in self.colunas_permitidas:
            print(f"Não é possível alterar a coluna: {coluna}")
            return False  # Retorna False indicando falha

        try:
            # Certifique-se que self.processar RETORNA o número de linhas afetadas
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

        except Exception as e:
            print(f"Erro ao atualizar {self.tabela}: {e}")
            return False  # Retorna False indicando falha

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
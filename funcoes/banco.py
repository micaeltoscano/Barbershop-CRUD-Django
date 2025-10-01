import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import IntegrityError, ProgrammingError

load_dotenv()

class Banco:

    #construtor para os parâmetros de conexão com o bd
    def __init__(self):
        #Inicializa os parâmetros de conexão pegando do .env
        self.config = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }
    
    
    #CONECTAR O BANCO DE DADOS COM O PYTHON
    def conectar(self):
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn 
    
    def processar(self, query, parametros=None, fetch = False):
        conn = self.conectar() #AQUI ELE TENTA CONECTAR COM O SERVIDOR
        if not conn:
            return
        try:
            with conn.cursor() as cur: #ESSE CURSOR É O QUE PERMITE USAR COMANDOS SQL NO PYTHON, USEI O WITH PQ PRECISA FECHAR ESSE CURSOR DEPOIS, DAI O WITH JÁ FECHA AUTOMATICO


                cur.execute(query, parametros) #ELE EXECUTA A QUERY (CONSULTA DO BD)
                if fetch: #SE COLOCAR FETCH=TRUE ELE DEVOLVE O RESULTADO DE UMA CONSULTA SQL 
                    colunas = [desc[0] for desc in cur.description] #PEGA O PRIMEIRO ITEM DE CADA TUPLA, QUE NESSE CASO É O NOME DA COLUNA
                    # Converte para lista de dicionários
                    resultados = []
                    for linha in cur.fetchall():
                        resultados.append(dict(zip(colunas, linha)))
                    return resultados 
                else:
                    conn.commit() #CONFIRMA AS ALTERAÇÕES FEITAS 
                    return cur.rowcount #UM CONTADOR PARA SABER QUANTAS LINHAS FORAM RETORNADAS (USA NAS CONSULTAS PARA SABER SE JÁ ESTA CADASTRADO, AGENDADO, ETC)
            
        except IntegrityError as e:
            conn.rollback()
            print(f"Erro de integridade: {e}")
            raise  # relança para o chamador decidir o que fazer

        except ProgrammingError as e:
            conn.rollback()
            print(f"Erro de programação SQL: {e}")
            raise

        except Exception as e:
            conn.rollback()
            print(f"Erro ao executar query: {e}")
            raise

        finally:
            conn.close()

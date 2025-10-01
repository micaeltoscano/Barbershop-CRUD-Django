import psycopg2
import os
from dotenv import load_dotenv

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
                if fetch:
                    return cur.fetchall() #SE COLOCAR FETCH=TRUE ELE DEVOLVE O RESULTADO DE UMA CONSULTA SQL 
                conn.commit() #CONFIRMA AS ALTERAÇÕES FEITAS 
                return cur.rowcount #UM CONTADOR PARA SABER QUANTAS LINHAS FORAM RETORNADAS (USA NAS CONSULTAS PARA SABER SE JÁ ESTA CADASTRADO, AGENDADO, ETC)
            
        except Exception as e:
            print("Erro ao executar query:", e)
            conn.rollback() #EVITA QUE ALTERAÇÕES SEJAM FEITAS EM CASO DE ERRO
            return None
        
        finally:
            conn.close()

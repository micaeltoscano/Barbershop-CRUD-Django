from crud import Crud

class Clientes(Crud):

    tabela = 'cliente'
    colunas_permitidas = ['nome', 'email', 'cpf', 'endereco', 'numero_celular', 'cidade', 'is_flamengo', 'is_onepiece']  
    coluna_id = 'idcliente'

    def cadastrar_cliente(self, nome, email, cpf, endereco, numero_celular, cidade, is_flamengo, is_onepiece):
        
        super().cadastro(
            nome = nome,
            email = email,
            cpf = cpf,
            endereco = endereco, 
            numero_celular = numero_celular,
            cidade = cidade,
            is_flamengo = is_flamengo,
            is_onepiece = is_onepiece,
        )
    
    def ler_todos_clientes(self):
        return super().ler_todos()
    
    def pesquisar_nome(self, nome):
        return super().pesquisar_nome(nome) 
    
    def ler_um_cliente(self, id):
        return super().listar_um(id)
    
    def atualizar_cliente(self, coluna, novo_valor, id):
        return super().atualizar(coluna, novo_valor, id)

    def deletar_cliente(self, id):
        return super().deletar(id)
    
    def buscar_por_cpf(self, cpf: str):
        try:
            print('BUSCANDO CLIENTE PELO CPF:', cpf)  # DEBUG
            # Agora buscamos todas as colunas para devolver o registro completo
            consulta = self.processar("SELECT * FROM cliente WHERE cpf = %s", (cpf,), fetch=True)
            cliente = consulta[0] if consulta else None
            print('CLIENTE ENCONTRADO:', cliente)  # DEBUG
            return cliente
        except Exception as e:
            raise ValueError(f"Erro ao buscar cliente por CPF: {e}")
        
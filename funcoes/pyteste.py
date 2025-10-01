from funcionarios import Funcionario
from clientes import Clientes
from agendas import Agenda
from disponibilidade import Disponibilidade
from categoria import Categoria
from servico import Servico
from compra import Compra
from utiliza import Utiliza
from produto import Produto
from estoque import Estoque
from pagamentos import Pagamento
from compra import Compra
from itens_compra import Itens_compra
from datetime import datetime
from psycopg2 import IntegrityError
from django.contrib import messages
from django.http import JsonResponse


agenda = Agenda()
funcionario = Funcionario()
cliente = Clientes()
disponibilidade = Disponibilidade()
categoria = Categoria()
servico = Servico()
compra = Compra()
utiliza = Utiliza()
produto = Produto()
estoque = Estoque()
pagamento = Pagamento()
compra = Compra()
itenscompra = Itens_compra()

# print((pagamento.ler_todos_pagamentos()[0]['valor']))

# for n in range(len(pagamento.ler_todos_pagamentos())):
#      print(pagamento.ler_todos_pagamentos()[n]['valor'])

# a = [(pagamento.ler_todos_pagamentos()[n]['valor']) for n in range(len(pagamento.ler_todos_pagamentos()))]

# pg = pagamento.ler_todos_pagamentos()
# # print(sum(p['valor'] for p in pg))

# #print(pg[0]['data_pagamento'].month)

# mes_atual = datetime.now().month


# quantidade = [sum(1 for p in pg if p['data_pagamento'].month == mes_atual)]

# print(quantidade)

#print(servico.pesquisar_nome('raspagem de caneco'))


#funcionario.cadastrar_funcionario('micael', 'a@gmail.com', '1, 'novo_add', '99999999999', 15000, 'caneco')

#uncionario.deletar_funcionario(1)
#funcionario.atualizar_funcionario('status', 'INATIVO', 2)
#print(compra.ler_todas_compras())

# id_funcionario = funcionario.processar("SELECT idfuncionario FROM FUNCIONARIO WHERE CPF = %s", ('12312322212',), fetch=True)

# id_funcionario = id_funcionario[0]['idfuncionario']

# try:
#     funcionario_id = funcionario.cadastrar_funcionario(
#         'antonio', 'micael#@gmail.com', '33333333333',
#         'Rua A, 123', '11999999999', 3000, 'Cabeleireiro'
#     )
# except IntegrityError as e:
#     print(f"Erro ao cadastrar funcionário: {str(e)}")

# status = funcionario.processar("SELECT STATUS FROM FUNCIONARIO WHERE IDFUNCIONARIO = %s", (5,), fetch=True)[0]['status']
# print(type(status))

# print(disponibilidade.ler_todas_disponibilidades())
# print(funcionario.ler_todos_funcionarios())

#funcionario.cadastrar_funcionario(nome = 'jorge', email = "jorggge@gmail.com", cpf = '22242222322', endereco = 'casa', numero_celular = '947445573', salario = 1900, especialidade = 'caneco')

print(pagamento.ler_todos_pagamentos())
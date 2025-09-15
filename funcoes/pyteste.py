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


#funcionario.cadastrar_funcionario('micael', 'a@gmail.com', '11538620421', 'novo_add', '99999999999', 15000, 'caneco')

print(utiliza.ler_todos_utiliza())


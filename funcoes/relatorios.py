from pagamentos import Pagamento
from datetime import datetime
from produto import Produto
from estoque import Estoque
from clientes import Clientes

def relatorios():

    pagamento = Pagamento()
    produto = Produto()
    estoque = Estoque()
    cliente = Clientes()

    mes_atual = datetime.now().month

    p = pagamento.ler_todos_pagamentos()

    valor_total_vendas = sum(n['valor'] for n in p)
    ticket_medio = ((valor_total_vendas)/len(p))
    venda_mes = [sum(1 for p in p if p['data_pagamento'].month == mes_atual)]
    
    total_produtos = len(produto.ler_todos_produtos())
    produtos_baixo_estoque = len([e for e in estoque.ler_todo_estoque() if e['quantidade_atual'] < 5])
    
    total_clientes = len(cliente.ler_todos_clientes())
    novos_clientes_mes = len([c for c in cliente.ler_todos_clientes() if c['data_cadastro'].month == mes_atual])
    frequencia_media = (len(p)/total_clientes) if total_clientes > 0 else 0


    relatorio = {
        'total_vendas': len(p),
        'valor_total_vendas': valor_total_vendas,
        'ticket_medio': ticket_medio,
        'vendas_mes': venda_mes[0],

        'total_produtos': total_produtos,
        'produtos_baixo_estoque': produtos_baixo_estoque,

        'total_clientes': total_clientes,
        'novos_clientes_mes': novos_clientes_mes,
        'frequencia_media': frequencia_media, 
        
    }

    return relatorio

relatorios = relatorios()
print(relatorios)
# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_funcionario, name='cliente_funcionario'),
    path('cliente/', views.pagina_compra_cliente, name='home_cliente'),
    path('cliente/compras/', views.compras_cliente, name='compras_cliente'),
    path('cliente/pagar/', views.cliente_pagar, name='cliente_pagar'),
    path('funcionario/', views.pagina_funcionario, name='home'),

    path('clientes/', views.cliente_list_view, name='cliente_list'),
    path('clientes/novo/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/editar/', views.atualizar_cliente, name='atualizar_cliente'),
    path('clientes/deletar/', views.deletar_cliente, name='deletar_cliente'),

    path('funcionarios/', views.funcionario_list_view, name='listar_funcionarios'),
    path('funcionario/novo/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('funcionario/editar/', views.atualizar_funcionario, name='atualizar_funcionario'),
    path('funcionario/deletar/', views.deletar_funcionario, name='deletar_funcionario'),

    
    path('agenda/', views.agenda_list_view, name='lista_agenda'),
    path('agenda/novo/', views.cadastrar_agenda, name='cadastrar_agenda'),
    path('agenda/editar/', views.atualizar_agenda, name='atualizar_agenda'),
    path('agenda/deletar/', views.deletar_agenda, name='deletar_agenda'),

    path('servicos/', views.servico_list_view, name='lista_servico'),
    path('servicos/novo/', views.cadastrar_servico, name='cadastrar_servico'),
    path('servicos/editar/', views.atualizar_servico, name='atualizar_servico'),
    path('servicos/deletar/', views.deletar_servico, name='deletar_servico'),

    
    path('estoque/', views.estoque_list_view, name='lista_estoque'),
    path('estoque/novo/', views.cadastrar_estoque, name='cadastrar_estoque'),
    path('estoque/editar/', views.atualizar_estoque, name='atualizar_estoque'),
    path('estoque/deletar/', views.deletar_estoque, name='deletar_estoque'),

    path('categorias/novo/', views.cadastrar_categoria, name='cadastrar_categoria'),

    path('produtos/', views.produto_list_view, name='listar_produtos'),
    path('produto/novo/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produto/editar/', views.editar_produto, name='editar_produto'),
    path('produto/deletar/', views.deletar_produto, name='deletar_produto'),

    path('pagamentos/', views.pagamento_list_view, name='lista_pagamento'),
    path('pagamentos/servico/', views.registrar_pagamento, name='registrar_pagamento'),
    #path('pagamentos/produto/', views.registrar_pagamento_produto, name='registrar_pagamento_produto'),

    path('relatorios/', views.relatorios, name='relatorios'),
    path('compras-servicos/', views.compras_servicos, name='compras_servicos'),

    

   
]
# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('clientes/', views.cliente_list_view, name='cliente_list'),
    path('api/clientes/', views.listar_clientes, name='api_clientes'),
    path('clientes/novo/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/editar/', views.atualizar_cliente, name='atualizar_cliente'),
    path('clientes/deletar/', views.deletar_cliente, name='deletar_cliente'),

    path('funcionarios/', views.funcionario_list_view, name='listar_funcionarios'),
    path('api/funcionarios/', views.listar_funcionarios, name='api_funcionarios'),
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

    path('produto/novo/', views.cadastrar_produto, name='cadastrar_produto'),
    path('produto/deletar/', views.deletar_produto, name='deletar_produto'),

    path('pagamentos/', views.pagamento_list_view, name='lista_pagamento'),
    path('pagamentos/servico/', views.registrar_pagamento_servico, name='registrar_pagamento_servico'),
    #path('pagamentos/produto/', views.registrar_pagamento_produto, name='registrar_pagamento_produto'),

    path('relatorios/', views.relatorios, name='relatorios'),

    

   
]
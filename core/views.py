from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from funcoes.disponibilidade import Disponibilidade
from funcoes.clientes import Clientes
from funcoes.funcionarios import Funcionario
from funcoes.servico import Servico
from funcoes.agendas import Agenda
from funcoes.estoque import Estoque
from django.shortcuts import render, redirect
from funcoes.categoria import Categoria
from funcoes.produto import Produto
from funcoes.utiliza import Utiliza
from funcoes.pagamentos import Pagamento
from datetime import datetime
from django.db import transaction

def list_view(request, classe, path):
    
    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    obj = classe() 

    registros = obj.ler_todos()

    if id_busca:
        registros = obj.listar_um(id_busca)

    if nome_busca:
        registros = obj.pesquisar_nome(nome_busca)

    context = {
        'tabela': registros
    }
    return render(request, path , context)
    
#-----------------------CLIENTES-----------------------------------
def cliente_list_view(request):

    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    c = Clientes()
    clientes = c.ler_todos_clientes()

    if id_busca:
        clientes = c.listar_um(id_busca)

    if nome_busca:
        clientes = c.pesquisar_nome(nome_busca)
    
    context = {
        'clientes': clientes
    }
    return render(request, 'core/cliente_list.html', context)

def listar_clientes(request):
    c = Clientes()
    dados = c.ler_todos_clientes()
    return JsonResponse(dados, safe=False)

def cadastrar_cliente(request):
    if request.method == 'POST':

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        endereco = request.POST.get('endereco')
        numero_celular = request.POST.get('numero_celular')
        
        if not nome:
            messages.error(request, 'Nome é obrigatório')
            return render(request, 'core/cadastro_cliente.html')
        
        try:
            c = Clientes()

            c.cadastrar_cliente(nome, email, cpf, endereco, numero_celular)
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'core/cadastro_cliente.html')

def atualizar_cliente(request):
    if request.method == 'POST':

        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        id = request.POST.get('idcliente')
        
        try:
            c = Clientes()
            c.atualizar_cliente(coluna, novo_valor, id)
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
    
    return render(request, 'core/atualizar_cliente.html')

def deletar_cliente(request):
    if request.method == 'POST':

        id = request.POST.get('id')
        
        try:
            c = Clientes()
            c.deletar_cliente(id)
            messages.success(request, 'Cliente deletado com sucesso!')
            return redirect('cliente_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar: {str(e)}')
    
    return render(request, 'core/deletar_cliente.html')

#-----------------------FUNCIONARIOS-----------------------------------

def cadastrar_funcionario(request):

    horarios = []
    for hora in range(8, 19):  
        horarios.append(f"{hora:02d}:00")
        horarios.append(f"{hora:02d}:30")

    if request.method == 'POST':
       
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        endereco = request.POST.get('endereco')
        numero_celular = request.POST.get('numero_celular')
        salario = request.POST.get('salario')
        especialidade = request.POST.get('especialidade')
        
        dias_semana = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fim = request.POST.getlist('hora_fim[]')
        
        if not nome:
            messages.error(request, 'Nome é obrigatório')
            return render(request, 'core/cadastro_funcionario.html')
            
        try:
            with transaction.atomic():
                f = Funcionario()

                id_funcionario = f.processar("SELECT 1 FROM FUNCIONARIO WHERE CPF = %s", (cpf,), fetch=True)
                print("aqui 1")
                if id_funcionario:
                    print("aqui 2")
                    id_funcionario = id_funcionario[0]['idfuncionario']
                    f.atualizar_funcionario('status', 'ATIVO', id_funcionario) 
                    f.atualizar_funcionario('email', email, id_funcionario) 
                    f.atualizar_funcionario('endereco', endereco, id_funcionario) 
                    f.atualizar_funcionario('numero_celular', numero_celular, id_funcionario)
                    f.atualizar_funcionario('salario', salario, id_funcionario)
                    f.atualizar_funcionario('especialidade', especialidade, id_funcionario)

                    d = Disponibilidade()
                    for i in range(len(dias_semana)):
                        if dias_semana[i] and horas_inicio[i] and horas_fim[i]:
                            d.cadastro_disponibilidade(
                                funcionario_id,  
                                dias_semana[i],
                                horas_inicio[i],
                                horas_fim[i]
                            )
                    messages.success(request, f'Funcionario "{nome}" REATIVADO NO SISTEMA com sucesso!')
                    return redirect('cadastrar_produto')  
                
                else:
                    funcionario_id = f.cadastrar_funcionario(nome, email, cpf, endereco, numero_celular, salario, especialidade)
                    
                    d = Disponibilidade()
                    for i in range(len(dias_semana)):
                        if dias_semana[i] and horas_inicio[i] and horas_fim[i]:
                            d.cadastro_disponibilidade(
                                funcionario_id,  
                                dias_semana[i],
                                horas_inicio[i],
                                horas_fim[i]
                            )

                    messages.success(request, 'Funcionário cadastrado com sucesso!')
                    return redirect('listar_funcionarios')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'core/cadastro_funcionario.html', {'horarios': horarios})

def funcionario_list_view(request):

    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    f = Funcionario()
    funcionarios = f.ler_todos_funcionarios()
    
    if id_busca:
        funcionarios = f.listar_um(id_busca)

    if nome_busca:
        funcionarios = f.pesquisar_nome(nome_busca)
   
    context = {
        'funcionarios': funcionarios
    }
    return render(request, 'core/funcionario_list.html', context)

def listar_funcionarios(request):
    f = Funcionario()
    dados = f.ler_todos_funcionarios()
    return JsonResponse(dados, safe=False)

def atualizar_funcionario(request):
    if request.method == 'POST':

        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        id = request.POST.get('idfuncionario')
        
        try:
            c = Funcionario()
            c.atualizar_funcionario(coluna, novo_valor, id)
            messages.success(request, 'Funcionario atualizado com sucesso!')
            return redirect('listar_funcionarios')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {str(e)}')
    
    return render(request, 'core/funcionario_atualizar.html')

def deletar_funcionario(request):
    if request.method == 'POST':

        id = request.POST.get('id')
        
        try:
            c = Funcionario()
            c.atualizar_funcionario('status', 'INATIVO', id)
            messages.success(request, 'Funcionario desativado da empresa com sucesso!')
            return redirect('listar_funcionarios')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar: {str(e)}')
    
    return render(request, 'core/funcionario_deletar.html')

#-----------------------AGENDA-----------------------------------

def cadastrar_agenda(request):
    horarios = []
    for hora in range(8, 19):  
        horarios.append(f"{hora:02d}:00")
        horarios.append(f"{hora:02d}:30")

    if request.method == 'POST':

        dia = request.POST.get('dia')
        horario = request.POST.get('horario')
        id_funcionario = request.POST.get('id_funcionario')
        id_servico = request.POST.get('id_servico')
        id_cliente = request.POST.get('id_cliente')
        status = request.POST.get('status', 'agendado')  
        
        if not dia or not horario or not id_funcionario or not id_servico or not id_cliente:
            messages.error(request, 'Data, horário, ID do funcionário, ID do serviço e ID do cliente são obrigatórios!')
            return render(request, 'core/cadastrar_agenda.html')
        
        try:
            a = Agenda()
            a.cadastrar_agenda(
                dia=dia,
                horario=horario,
                id_funcionario=id_funcionario,
                id_servico=id_servico,
                id_cliente=id_cliente,
                status=status
            )
            messages.success(request, 'Agendamento cadastrado com sucesso!')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Erro ao agendar: {str(e)}')
            return render(request, 'core/agenda_cadastrar.html')
    
    return render(request, 'core/agenda_cadastrar.html', {'horarios': horarios})

def agenda_list_view(request):

    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    a = Agenda()
    agendas = a.ler_toda_agenda()
    
    if id_busca:
        agendas = a.listar_um(id_busca)
   
    context = {
        'agendas': agendas
    }
    return render(request, 'core/agenda_list.html', context)

def atualizar_agenda(request):
    if request.method == 'POST':
        idagenda = request.POST.get('idagenda')
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        
        if not idagenda or not coluna or not novo_valor:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/agenda_atualizar.html')
        
        try:
            a = Agenda()
            a.atualizar_agenda(coluna, novo_valor, idagenda)
            messages.success(request, f'Agendamento {idagenda} atualizado com sucesso!')
            return redirect('lista_agenda')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar agendamento: {str(e)}')
    
    return render(request, 'core/agenda_atualizar.html')

def deletar_agenda(request):
    if request.method == 'POST':
        idagenda = int(request.POST.get('idagenda'))
        
        if not idagenda:
            messages.error(request, 'ID do agendamento é obrigatório!')
            return render(request, 'core/agenda_deletar.html')
        
        try:
            a = Agenda()
            if a.deletar_agenda(idagenda):
                messages.success(request, f'Agendamento {idagenda} deletado com sucesso!')
            return redirect('lista_agenda')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar agendamento: {str(e)}')
    
    return render(request, 'core/agenda_deletar.html')

#-----------------------SERVICO-----------------------------------

def servico_list_view(request):

    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    s = Servico()
    servicos = s.ler_todos_servicos()

    if id_busca:
        servicos = s.listar_um(id_busca)

    if nome_busca:
        servicos = s.pesquisar_nome(nome_busca)
    
    context = {
        'servicos': servicos
    }
    return render(request, 'core/servico_list.html', context)

def cadastrar_servico(request):
    # Buscar categorias e produtos
    c = Categoria()
    categorias = c.ler_todas_categorias()
    
    p = Produto()
    produtos = p.ler_todos_produtos_ativos()
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        valor = request.POST.get('valor')
        duracao = request.POST.get('duracao')
        categoria_id = request.POST.get('categoria')
        
        produto_ids = request.POST.getlist('produto_id[]')
        produto_quantidades = request.POST.getlist('produto_quantidade[]')
        
        if nome and valor and duracao and categoria_id:
            try:
                s = Servico()
                servico_id = s.cadastro_servico(
                    nome=nome,
                    valor=valor,
                    duracao=duracao,
                    id_categoria=categoria_id
                )
                print(servico_id)
                if servico_id and produto_ids and produto_ids[0]:  
                    print("cheguei aqui!!!")
                    u = Utiliza()
                    for i in range(len(produto_ids)):
                        if produto_ids[i] and produto_quantidades[i]:  
                            u.cadastro_utiliza(
                                id_servico=servico_id,
                                id_produto=produto_ids[i],
                                quantidade=produto_quantidades[i]
                            )
                
                messages.success(request, 'Serviço cadastrado com sucesso!')
                return redirect('lista_servico')
                
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar serviço: {str(e)}')
    
    return render(request, 'core/servico_cadastrar.html', {
        'categorias': categorias,
        'produtos': produtos
    })

def atualizar_servico(request):
    if request.method == 'POST':
        idservico = request.POST.get('idservico')
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        
        if not idservico or not coluna or not novo_valor:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/servico_atualizar.html')
        
        try:
            s = Servico()
            s.atualizar_servico(coluna, novo_valor, idservico)
            messages.success(request, f'Serviço {idservico} atualizado com sucesso!')
            return redirect('lista_servico')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar serviço: {str(e)}')
    
    return render(request, 'core/servico_atualizar.html')

def deletar_servico(request):
    if request.method == 'POST':
        idservico = request.POST.get('idservico')
        
        if not idservico:
            messages.error(request, 'ID do serviço é obrigatório!')
            return render(request, 'core/servico_deletar.html')
        
        try:
            s = Servico()
            s.deletar_servico(idservico)
            messages.success(request, f'Serviço {idservico} deletado com sucesso!')
            return redirect('lista_servico')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar serviço: {str(e)}')
    
    return render(request, 'core/servico_deletar.html')

#-----------------------ESTOQUE-----------------------------------
def estoque_list_view(request):

    id_estoque_busca = request.GET.get('id_estoque_busca')
    id_produto_busca = request.GET.get('id_produto_busca')
    nome_produto_busca = request.GET.get('nome_produto_busca')

    e = Estoque()
    p = Produto()
    estoques = e.ler_todo_estoque()
    
    if id_estoque_busca:
        estoques = e.listar_um(id_estoque_busca)

    if id_produto_busca:
        estoques = p.listar_um(id_produto_busca)

    if nome_produto_busca:
        estoques = p.pesquisar_nome(nome_produto_busca)

    context = {
        'estoques': estoques
    }
    return render(request, 'core/estoque_list.html', context)

def cadastrar_estoque(request):
    try:
        #FAZ UMA CONSULTA PARA LER TODOS OS PRODUTOS CADASTRADOS NO SISTEMA QUE ESTÃO ATIVOS
        p = Produto()
        produtos = p.ler_todos_produtos_ativos()

    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        produtos = []
        messages.error(request, 'Erro ao carregar lista de produtos')

    if request.method == 'POST':
        nome_produto = request.POST.get('produto')  
        quantidade_atual = request.POST.get('quantidade_atual')
        quantidade_minima = request.POST.get('quantidade_minima')
        
        # DEBUG: Verifique o que está chegando
        print(f"Nome produto: '{nome_produto}'")
        print(f"Quantidade: {quantidade_atual}")
        print(f"Mínima: {quantidade_minima}")
        
        if not nome_produto or not quantidade_atual or not quantidade_minima:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/estoque_cadastrar.html', {'produtos': produtos})
        
        try:
            # ↓↓↓ MOVER a inicialização para DENTRO do bloco POST ↓↓↓
            e = Estoque()
            sucesso = e.cadastro_estoque(nome_produto, quantidade_atual, quantidade_minima)
            
            if sucesso:
                messages.success(request, 'Item adicionado ao estoque com sucesso!')
                return redirect('lista_estoque')
            else:
                messages.error(request, 'Erro ao adicionar item ao estoque!')
                
        except Exception as e:
            print(f"Erro completo no cadastro: {e}")  
            messages.error(request, f'Erro ao adicionar item: {str(e)}')
    
    return render(request, 'core/estoque_cadastrar.html', {'produtos': produtos})

def atualizar_estoque(request):
    if request.method == 'POST':
        idestoque = request.POST.get('idestoque')
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        
        if not idestoque or not coluna or not novo_valor:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/estoque_atualizar.html')
        
        try:
            e = Estoque()
            e.atualizar_estoque(coluna, novo_valor, idestoque)
            messages.success(request, f'Estoque {idestoque} atualizado com sucesso!')
            return redirect('lista_estoque')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar estoque: {str(e)}')
    
    return render(request, 'core/estoque_atualizar.html')

def deletar_estoque(request):
    
    if request.method == 'POST':
        idestoque = request.POST.get('idestoque')
        
        if not idestoque:
            messages.error(request, 'ID do estoque é obrigatório!')
            return render(request, 'core/estoque_deletar.html')
        
        try:
            e = Estoque()
            e.deletar_estoque(idestoque)
            messages.success(request, f'Item {idestoque} removido do estoque com sucesso!')
            return redirect('lista_estoque')
            
        except Exception as e:
            messages.error(request, f'Erro ao remover item: {str(e)}')
    
    return render(request, 'core/estoque_deletar.html')

#-----------------------CATEGORIA-----------------------------------

def cadastrar_categoria(request):
    if request.method == 'POST':
        nome_categoria = request.POST.get('nome_categoria')
        
        if nome_categoria:
            try:
                c = Categoria()
                c.cadastro_categoria(nome_categoria)
                messages.success(request, f'Categoria "{nome_categoria}" cadastrada com sucesso!')
                return redirect('cadastrar_servico')  # Ou redirecione para onde preferir
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar categoria: {str(e)}')
    
    return render(request, 'core/categoria_cadastrar.html')

#-----------------------PRODUTO-----------------------------------

def cadastrar_produto(request):

    #RECUPERA OS DADOS DE ENTRADA PARA O CADASTRO DO PRODUTO
    if request.method == 'POST':

        valor = request.POST.get('valor')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        
        if nome:
            try:
                p = Produto()
                #CASO O PRODUTO JÁ ESTEJA CADASTRADO NO BANCO, ELE VAI SER APENAS REATIVADO
                if p.pesquisar_nome_produto(nome):

                    idproduto = p.pesquisar_nome_produto('navalha de caneco')[0]['idproduto'] #ATRAVES DA CONSULTA DE PESQUISAR POR NOME, PEGA O ID
                    p.atualizar_produto('status', 'ATIVO', idproduto) #ATUALIZA O PRODUTO
                    p.atualizar_produto('valor', valor , idproduto)
                    p.atualizar_produto('tipo', tipo, idproduto)
                    messages.success(request, f'Produto "{nome}" REATIVADO NO SISTEMA com sucesso!')
                    return redirect('cadastrar_produto')  

                else:    
                    #CASO NÃO TENHA CADASTRO, ELE É CADASTRADO
                    p.cadastro_produto(nome, valor, tipo)
                    messages.success(request, f'Produto "{nome}" cadastrado com sucesso!')
                    return redirect('cadastrar_produto')  
            
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    return render(request, 'core/produto_cadastrar.html')
  
def deletar_produto(request):

    if request.method == 'POST':
        idproduto = request.POST.get('idproduto')
        
        if not idproduto:
            messages.error(request, 'ID do produto é obrigatório!')
            return render(request, 'core/produto_deletar.html')
        
        try:
            p = Produto()
            p.atualizar_produto('status', 'INATIVO', idproduto)
            messages.success(request, f'produto {idproduto} desativado do sistema com sucesso!')
            return redirect('lista_estoque')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar produto: {str(e)}')
    
    return render(request, 'core/produto_deletar.html')

#-----------------------PAGAMENTO-----------------------------------  

def registrar_pagamento_servico(request):
    a = Agenda()

    if request.method == 'POST':
        id_agenda = request.POST.get('id_agenda')  
        metodo_pagamento = request.POST.get('metodo_pagamento')
    
        if id_agenda and metodo_pagamento:  
            try:
                a.confirmar_servico(id_agenda, metodo_pagamento)  
                messages.success(request, 'Pagamento registrado com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao registrar confirmação do serviço: {str(e)}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
    
    return render(request, 'core/pagamento_registrar.html')

def pagamento_list_view(request):

    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    p = Pagamento()
    pagamento = p.ler_todos_pagamentos()
    
    if id_busca:
        pagamento = p.listar_um(id_busca)

    if nome_busca:
        pagamento = p.pesquisar_nome(nome_busca)

    context = {
        'pagamentos': pagamento
    }
    return render(request, 'core/pagamento_list.html', context)

#-----------------------HOME-----------------------------------
def home(request):
    return render(request, 'core/home.html')

def relatorios(request):

    pagamento = Pagamento()
    mes_atual = datetime.now().month

    p = pagamento.ler_todos_pagamentos()

    valor_total_vendas = sum(n['valor'] for n in p)
    ticket_medio = ((valor_total_vendas)/len(p))
    venda_mes = [sum(1 for p in p if p['data_pagamento'].month == mes_atual)]
    

    context = {
        'total_vendas': len(p),
        'valor_total_vendas': valor_total_vendas,
        'ticket_medio': ticket_medio,
        'vendas_mes': venda_mes[0],
        # 'total_produtos': total_produtos,
        # 'valor_total_estoque': valor_total_estoque,
        # 'produtos_baixo_estoque': produtos_baixo_estoque,
        # 'categorias_count': categorias_count,
        # 'total_clientes': total_clientes,
        # 'clientes_ativos': clientes_ativos,
        # 'novos_clientes_mes': novos_clientes_mes,
        # 'frequencia_media': 2.5, 
        # 'ultimas_vendas': ultimas_vendas,
        # 'produtos': produtos,
        # 'clientes': clientes,
    }
    
    return render(request, 'core/relatorio.html', context)


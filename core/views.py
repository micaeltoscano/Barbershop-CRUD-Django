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
from funcoes.compra import Compra
from funcoes.itens_compra import Itens_compra
from decimal import Decimal

def buscar_cliente_por_cpf(request):
    cliente = None
    compras = []
    total_gasto = 0

    if request.method == "POST":
        cpf = request.POST.get('cpf_cliente')
        c = Clientes()
        cliente = c.buscar_por_cpf(cpf)
        
        if cliente:
            #Buscando as compras do cliente com o CPF fornecido
            compras = Compra.objects.filter(cliente_id=cliente['idcliente'])
            total_gasto = sum([compra.valor_total for compra in compras])
        else:
            messages.error(request, "Cliente não encontrado.")
            return render(request, 'core/home_cliente.html')

    context = {
        'cliente': cliente,
        'compras': compras,
        'total_gasto': total_gasto,
        'cpf': cpf
    }
    return render(request, 'compras_cliente.html', context)

def cliente_funcionario(request):
    return render(request, 'core/cliente_funcionario.html')

def pagina_compra_cliente(request):
    return render(request, 'core/home_cliente.html')

def pagina_funcionario(request):
    return render(request, 'core/home.html')

def compras_cliente(request):
        cliente = None
        compras = []
        total_gasto = 0

        if request.method == "POST":
            cpf = request.POST.get('cpf_cliente')
            cliente_id = None
            c = Clientes()
            cliente_id = c.buscar_por_cpf(cpf)

            if cliente_id:
                #Buscando as compras do cliente com o CPF fornecido
                compras = Compra().processar("SELECT * FROM COMPRA WHERE id_cliente = %s", (cliente_id,), fetch=True)
                cliente = c.ler_um_cliente(cliente_id)[0]['nome']
                total_gasto = sum([compra['valor_total'] for compra in compras])

                for compra in compras:
                    compra_id = compra['idcompra']  # pega o id da compra

                    # Pega todos os itens daquela compra
                    itens = Itens_compra().processar(
                        "SELECT ic.iditenscompra, p.nome as produto, ic.quantidade, ic.valor_unitario, ic.valor_total_item "
                        "FROM itens_compra ic "
                        "JOIN produto p ON ic.id_produto = p.idproduto "
                        "WHERE ic.id_compra = %s",
                        (compra_id,), fetch=True
                    )

                    # Pega a forma de pagamento daquela compra
                    forma_pagamento = Pagamento().processar(
                        "SELECT forma_pagamento FROM pagamento WHERE id_compra = %s",
                        (compra_id,), fetch=True
                    )

                    # Adiciona os itens e a forma de pagamento dentro do dicionário da compra
                    compra['itens'] = itens
                    compra['forma_pagamento'] = forma_pagamento[0]['forma_pagamento'] if forma_pagamento else None
                print('FORMA DE PAGAMENTO:', forma_pagamento) #DEBUG
            else:
                messages.error(request, "Cliente não encontrado.")
                return render(request, 'core/home_cliente.html')
            
        context = {
            'cliente': cliente,
            'compras': compras,
            'total_gasto': total_gasto,
            'cpf': cpf,
            'itens' : itens,
            'forma_pagamento': forma_pagamento
        }

        return render(request, 'core/compras_cliente.html', context)


def cliente_pagar(request):
    if request.method == 'POST':

        #PEGA O TIPO DO PAGAMENTO A SER FEITO (SERVIÇO OU PRODUTO) E O METODO DE PAGAMENTO
        tipo = request.POST.get('tipo_pagamento')
        metodo_pagamento = request.POST.get('metodo_pagamento')
        
        try:
            if tipo == 'servico':

                #PEGA O ID DA AGENDA
                id_agenda = request.POST.get('id_agenda')
                
                if not id_agenda or not metodo_pagamento:
                    messages.error(request, "Preencha todos os campos obrigatórios.")
                    return redirect('cliente_pagar')
                
                #CONFIRMA O SERVICO PELA FUNCAO DA CLASSE AGENDA
                a = Agenda()
                a.confirmar_servico(int(id_agenda), metodo_pagamento)

                messages.success(request, f"Pagamento do serviço {id_agenda} registrado com sucesso!")
                return redirect('home_cliente')

            #SE FOR PAGAMENTO DE PRODUTOS
            elif tipo == 'produto':

                #PEGA O ID DO CLIENTE E O DO FUNCIONARIO QUE REALIZOU AQUELA VENDA
                pagamento = Pagamento()
                
                cpf = request.POST.get('cpf_cliente')
                id_cliente = pagamento.processar("SELECT IDCLIENTE FROM CLIENTE WHERE CPF = %s", (cpf,), fetch=True)[0]['idcliente']
                id_funcionario = request.POST.get('id_funcionario')
                
                #VERIFICA
                if not metodo_pagamento or not id_cliente or not id_funcionario:
                    messages.error(request, "Preencha todos os campos obrigatórios.")
                    return redirect('cliente_pagar')
                
                #CHAMA A CLASSE
                compra = Compra()

                #RECEBE OS PRODUTOS SELECIONADOS E AS QUANTIDADES REFERENTES
                produtos_selecionados = request.POST.getlist('produtos')
                quantidades = request.POST.getlist('quantidades')

                #REGISTRA A COMPRA
                compra.registrar_compra_django(id_cliente, id_funcionario, metodo_pagamento, produtos_selecionados, quantidades, request)
                messages.success(request, "Pagamento dos produtos registrado com sucesso!")
                return redirect('home_cliente')

            
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return redirect('cliente_pagar')
    
    #CARREGAR A LISTA DE PRODUTOS, DEPOIS CLIENTES E FUNCIONARIOS PARA PASSAR P O HTML:

    produtos = Produto()
    clientes = Clientes()
    funcionarios = Funcionario()

    produtos = produtos.ler_todos_produtos_ativos()
    
    clientes = clientes.ler_todos_clientes()
    
    funcionarios = funcionarios.ler_todos_funcionarios_ativos()
    
    return render(request, 'core/cliente_pagar.html', {
        'produtos': produtos,
        'clientes': clientes,
        'funcionarios': funcionarios
    })

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

#TODAS AS FUNCOES QUE TIVEREM LIST_VIEW SÃO USADAS PARA EXIBIR OS DADOS NA ABA DE LISTAR
def cliente_list_view(request):

    #O ID_BUSCA E NOME_BUSCA SAO VARIAVEIS PARA FAZER A CONSULTA BASEADA NO ID OU NOME
    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    #CHAMA A CLASSE CLIENTES E A FUNCAO LER_TODOS_CLIENTES PARA PEGAR TODOS OS CLIENTES CADASTRADOS NO BANCO DE DADOS
    c = Clientes()
    clientes = c.ler_todos_clientes()

    #SE TIVER O ID_BUSCA ELE PEGA O CLIENTE COM ESSE ID. O MESMO PARA NOME_BUSCA
    if id_busca:
        clientes = c.listar_um(id_busca)

    if nome_busca:
        clientes = c.pesquisar_nome(nome_busca)
    
    #CONTEXT SERVE PARA MANDAR OS DADOS PARA O HTML
    context = {
        'clientes': clientes
    }

    #RENDER É A FUNÇÃO QUE RENDERIZA O HTML E MANDA TODOS OS DADOS P ELE
    return render(request, 'core/cliente_list.html', context)

def cadastrar_cliente(request):

    #PEGA OS DADOS DO FORMULARIO. (TEM A FUNCAO POST E GET, POST É PARA PEGAR OS DADOS E GET É P EXIBICAO)
    if request.method == 'POST':

        #DICIONARIO COM TODOS OS CAMPOS OBRIGATORIOS 
        campos_obrigatorios = {
        'nome': 'Nome',
        'email': 'E-mail',
        'cpf': 'CPF',
        'endereco': 'Endereço',
        'numero_celular': 'Número de celular', 
        'cidade': 'cidade',
        'is_flamengo': 'is_flamengo',
        'is_onepiece': 'is_onepiece' }

        #PEGA OS DADOS NECESSARIOS P O CADASTRO
        dados = {campo: request.POST.get(campo) for campo in campos_obrigatorios}

        #É O MESMO QUE FAZER ISSO:
            # nome = request.POST.get('nome')
            # email = request.POST.get('email')
            # cpf = request.POST.get('cpf')
            # endereco = request.POST.get('endereco')
            # numero_celular = request.POST.get('numero_celular')

        #VERIFICACAO SE TODOS OS CAMPOS FORAM PREENCHIDOS 
        for campo, valor in dados.items():
            if not valor:
                messages.error(request, f'{campos_obrigatorios[campo]} é obrigatório')
                return render(request, 'core/cadastro_cliente.html')
        try:
            #CHAMA A CLASSE CLIENTES E A FUNCAO CADASTRAR CLIENTE
            c = Clientes()

            c.cadastrar_cliente(**dados) #AQUI EU DESEMPACOTEI OS DADOS 

            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'core/cadastro_cliente.html')

def atualizar_cliente(request):
    if request.method == 'POST':

        #PEGA A COLUNA A SER ALTERADA (JÁ É PASSADO NO HTML A LISTA DE COLUNAS QUE PODEM SER ALTERADAS), O NOVO VALOR E O ID DO CLIENTE
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        id = request.POST.get('idcliente')
        
        try:
            #CHAMA A CLASSE CLIENTE E A FUNCAO DE ATUALIZAR 
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

    #FOR PARA GERAR TODOS OS HORARIOS DE ATENDIMENTO DOS FUNCIONARIOS
    horarios = []
    for hora in range(8, 19):  
        horarios.append(f"{hora:02d}:00")
        horarios.append(f"{hora:02d}:30")

    campos_obrigatorios = {
        'nome': 'Nome',
        'email': 'E-mail',
        'cpf': 'CPF',
        'endereco': 'Endereço',
        'numero_celular': 'Número de celular',
        'salario': 'Salário',
        'especialidade': 'Especialidade'
    }

    #PEGAR OS DADOS DO FORMULARIO
    if request.method == 'POST':
       
        dados = {campo: request.POST.get(campo) for campo in campos_obrigatorios}

        # VERIFICAR SE TODOS OS CAMPOS FORAM PREENCHIDOS CORRETAMENTE
        for campo, valor in dados.items():
            if not valor:
                messages.error(request, f'{campos_obrigatorios[campo]} é obrigatório!')
                return render(request, 'core/cadastro_funcionario.html')

        #PEGA OS HORARIOS DE DISPO DO FUNCIONARIO
        dias_semana = request.POST.getlist('dia_semana[]')
        horas_inicio = request.POST.getlist('hora_inicio[]')
        horas_fim = request.POST.getlist('hora_fim[]')

        try:
            #ESSE ATOMIC SERVE PARA GARANTIR QUE TODAS AS OPERAÇÕES DENTRO DELE SEJAM CONCLUÍDAS COM SUCESSO, CASO CONTRÁRIO, NENHUMA DELAS SERÁ APLICADA NO BANCO DE DADOS
            with transaction.atomic():
                
                #CHAMA A CLASSE FUNCIONARIO
                f = Funcionario()

                #PEGAR O ID DO FUNCIONARIO PARA VERIFICAR SE ELE JA ESTA CADASTRADO NO SISTEMA
                id_funcionario = f.processar("SELECT IDFUNCIONARIO FROM FUNCIONARIO WHERE CPF = %s", (dados['cpf'],), fetch=True)

                print("stou aqui agora 2") #DEBUG

                #CASO JA ESTEJA CADASTRADO
                if id_funcionario:
                    
                    #PEGA O ID REFERENTE A ELE
                    id_funcionario = id_funcionario[0]['idfuncionario']

                    #CONSULTA PARA VERIFICAR QUAL O STATUS DELE NO SISTEMA
                    status = f.processar("SELECT STATUS FROM FUNCIONARIO WHERE IDFUNCIONARIO = %s", (id_funcionario,), fetch=True)[0]['status']
                    
                    #SE ESTIVER ATIVO, NAO DEIXA CADASTRAR NOVAMENTE 
                    if status == 'ATIVO':
                        messages.error(request, f'O CPF {dados['cpf']} já está cadastrado para um funcionário ativo!')

                    #CASO NAO ESTEJA ATIVO, MAS CADASTRADO, REATIVA O FUNCIONARIO   
                    else:

                        f.atualizar_funcionario('status', 'ATIVO', id_funcionario)

                        #ITERA NOS DADOS PASSADOS PELO FORMULARIO E ATUALIZA CADA UM DELES
                        for coluna, valor in dados.items():
                                f.atualizar_funcionario(coluna, valor, id_funcionario)

                        #CADASTRA A DISPONIBILIDADE DO FUNCIONARIO
                        d = Disponibilidade()
                        for i in range(len(dias_semana)):
                            if dias_semana[i] and horas_inicio[i] and horas_fim[i]:
                                d.cadastro_disponibilidade(
                                    id_funcionario,  
                                    dias_semana[i],
                                    horas_inicio[i],
                                    horas_fim[i])
                                
                        messages.success(request, f'Funcionario "{dados["nome"]}" REATIVADO NO SISTEMA com sucesso!')
                        return redirect('listar_funcionarios')  
                
                #CASO NAO ESTEJA CADASTRADO NO SISTEMA
                else:

                    funcionario_id = f.cadastrar_funcionario(**dados) #DESEMPACOTA OS DADOS PARA CADASTRAR O FUNCIONARIO

                    #CADASTRA A DISPONIBILIDADE DO FUNCIONARIO
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

    #VARIAVEIS P BUSCA POR NOME OU ID
    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    #CHAMA A CLASSE E LE TODOS OS ATIVOS (CASO SEJA NECESSÁRIO, PODE SER ALTERADO P MOSTRAR OS ATIVOS E INATIVOS)
    f = Funcionario()
    funcionarios = f.ler_todos_funcionarios_ativos()
    
    #BUSCA:
    if id_busca:
        funcionarios = f.listar_um(id_busca)

    if nome_busca:
        funcionarios = f.pesquisar_nome(nome_busca)
   
   #RETORNA OS DADOS PRO HTML
    context = {
        'funcionarios': funcionarios
    }
    return render(request, 'core/funcionario_list.html', context)

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
        
        #VERIFICA SE O ID FOI PREENCHIDO
        if not id:
            messages.error(request, 'ID é obrigatório')
            return render(request, 'core/funcionario_deletar.html')
        
        try:
            #USO DO ATOMIC P GARANTIR QUE TUDO SEJA CONCLUIDO COM SUCESOS 
            with transaction.atomic():
                
                #CHAMA AS CLASSES UTILIZADAS
                f = Funcionario()
                d = Disponibilidade()

                #TRANSFORMA O STATUS DO FUNCIONARIO EM INATIVO
                f.atualizar_funcionario('status', 'INATIVO', id)

                #CONSULTA PARA PEGAR O ID DO FUNCIONARIO
                iddisponibilidade = d.processar("SELECT IDDISPONIBILIDADE FROM DISPONIBILIDADE WHERE ID_FUNCIONARIO = %s", (id,), fetch=True)[0]['iddisponibilidade']

                #DELETA A DISPONIBILIDADE DELE (CASO SEJA REATIVADO, SERAO PASSADOS NOVOS HORARIOS P ELE, ENTAO NAO É NECESSARIO PERMANECER COM OS HORARIOS ANTIGOS)
                d.deletar_disponibilidade(iddisponibilidade)
                    
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
        status = request.POST.get('status', 'ATIVO')  
        
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

    a = Agenda()
    agendas = a.ler_todas_agendas_ativas()
    
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

            status_agendamento = a.processar("SELECT STATUS FROM AGENDA WHERE IDAGENDA = %s", (idagenda,), fetch=True)[0]['status']

            if status_agendamento == 'CANCELADO':
                messages.error(request, f'O agendamento {idagenda} já está cancelado.')

            elif status_agendamento == 'CONCLUIDO':
                messages.error(request, f'O agendamento {idagenda} já foi concluído e não pode ser cancelado.')

            elif status_agendamento == 'ATIVO':    
                a.atualizar_agenda('status', 'CANCELADO', idagenda)

            messages.success(request, f'Agendamento {idagenda} deletado com sucesso!')
            return redirect('lista_agenda')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar agendamento: {str(e)}')
    
    return render(request, 'core/agenda_deletar.html')

#-----------------------SERVICO-----------------------------------

def servico_list_view(request):

    #BUSCA POR ID OU PELO NOME
    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    #CHAMA A CLASSE E PEGA TODOS OS SERVICOS Q ESTAO ATIVOS
    s = Servico()
    servicos = s.ler_todos_servicos_ativos()

    #BUSCA
    if id_busca:
        servicos = s.listar_um(id_busca)

    if nome_busca:
        servicos = s.pesquisar_nome(nome_busca)
    
    #RETORNA PRO HTML
    context = {
        'servicos': servicos
    }
    return render(request, 'core/servico_list.html', context)

def cadastrar_servico(request):

    campos_obrigatorios = {
        'nome': 'valor',
        'valor': 'valor',
        'duracao': 'duracao',
        'categoria_id': 'categoria'
    }

    #BUSCAR TODAS AS CATEGORIAS E PRODUTOS DO SISTEMA
    c = Categoria()
    categorias = c.ler_todas_categorias()
    
    p = Produto()
    produtos = p.ler_todos_produtos_ativos()
    
    if request.method == 'POST':

        dados = {campo: request.POST.get(campo) for campo in campos_obrigatorios}

        # VERIFICAR SE TODOS OS CAMPOS FORAM PREENCHIDOS CORRETAMENTE
        for campo, valor in dados.items():
            if not valor:
                messages.error(request, f'{campos_obrigatorios[campo]} é obrigatório!')
                return render(request, 'core/servico_cadastrar.html', {'categorias': categorias,'produtos': produtos})

        #TRATAR OS CAMPOS QUE PRECISAM SER NUMERICOS
        try:
            dados['valor'] = float(dados['valor'])
            dados['duracao'] = int(dados['duracao'])
            dados['id_categoria'] = int(dados.pop('categoria_id'))

        except ValueError:
            messages.error(request, 'Valor, duração e categoria devem ser numéricos.')
            return render(request, 'core/servico_cadastrar.html', {'categorias': categorias,'produtos': produtos})

        #PEGA OS PRODUTOS E QUANTIDADES SELECIONADOS
        produto_ids = request.POST.getlist('produto_id[]')
        produto_quantidades = request.POST.getlist('produto_quantidade[]')

        try:

            with transaction.atomic():
                
                #CHAMA A CLASSE SERVICO E CADASTRA O SERVICO COM OS DADOS PASSADOS
                s = Servico()

                resultado = s.processar("SELECT IDSERVICO FROM SERVICO WHERE NOME = %s", (dados['nome'],), fetch=True)
                if resultado:
                    id_servico = resultado[0]['idservico']
                    status = resultado[0]['status']
                else:
                    id_servico = None
                    status = None
                
                if id_servico:

                    #SE ESTIVER ATIVO, NAO DEIXA CADASTRAR NOVAMENTE 
                    if status == 'ATIVO':
                        messages.error(request, f'Já existe um serviço com o mesmo nome no sistema!')
                        

                    #CASO NAO ESTEJA ATIVO, MAS CADASTRADO, REATIVA O SERVICO 
                    else:
                        s.atualizar_servico('status', 'ATIVO', id_servico)

                        #ITERA NOS DADOS PASSADOS PELO FORMULARIO E ATUALIZA CADA UM DELES
                        for coluna, valor in dados.items():
                            s.atualizar_servico(coluna, valor, id_servico)
                        
                        u = Utiliza()

                        for i in range(len(produto_ids)):

                            if produto_ids[i] and produto_quantidades[i]: 
                                    
                                    u.cadastro_utiliza(
                                        id_servico=id_servico,
                                        id_produto=produto_ids[i],
                                        quantidade=produto_quantidades[i]
                                    )
                        messages.success(request, f'Serviço "{dados["nome"]}" REATIVADO NO SISTEMA com sucesso!')
                        return redirect('lista_servico')

                #SE NAO ESTIVER CADASTRADO NO SISTEMA
                else:
                    id_servico = s.cadastro_servico(**dados)

                    #SE HOUVER PRODUTOS/QUANTIDADES QUE ELE USA:
                    if id_servico and produto_ids and produto_ids[0]: 
                        
                        #CHAMA A CLASSE DE UTILIZA E CADASTRA TODOS AQUELES PRODUTOS/QUANT
                        u = Utiliza()

                        for i in range(len(produto_ids)):

                            if produto_ids[i] and produto_quantidades[i]: 
                                    
                                    u.cadastro_utiliza(
                                        id_servico= id_servico,
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

        #PEGA OS DADOS 
        idservico = request.POST.get('idservico')
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        
        #VERIFICA OS CAMPOS
        if not idservico or not coluna or not novo_valor:

            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/servico_atualizar.html')
        
        try:
            #CHAMA A CLASSE E ATUALIZA O SERVICO
            s = Servico()
            s.atualizar_servico(coluna, novo_valor, idservico)

            messages.success(request, f'Serviço {idservico} atualizado com sucesso!')
            return redirect('lista_servico')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar serviço: {str(e)}')
    
    return render(request, 'core/servico_atualizar.html')

def deletar_servico(request):

    if request.method == 'POST':

        #PEGA O ID DO SERVICO
        idservico = request.POST.get('idservico')
        
        #VERIFICA
        if not idservico:
            messages.error(request, 'ID do serviço é obrigatório!')
            return render(request, 'core/servico_deletar.html')
        
        try:

            #CHAMA A CLASSE E ATUALIZA O STATUS PARA INATIVO
            s = Servico()
            s.atualizar_servico('status', 'INATIVO', idservico)

            messages.success(request, f'Serviço {idservico} desativado com sucesso!')
            return redirect('lista_servico')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar serviço: {str(e)}')
    
    return render(request, 'core/servico_deletar.html')

#-----------------------ESTOQUE-----------------------------------
def estoque_list_view(request):

    #PEGA OS DADOS VIA GET 
    id_estoque_busca = request.GET.get('id_estoque_busca')
    id_produto_busca = request.GET.get('id_produto_busca')
    nome_produto_busca = request.GET.get('nome_produto_busca')

    estoque_minimo = request.GET.get('estoque_minimo')

   

    #CHAMA AS CLASSES E LER O ESTOQUE TODO
    e = Estoque()
    p = Produto()
    estoques = e.ler_todo_estoque()
    
    #TIPOS DE PESQUISA QUE PODEM SER FEITAS

    if id_estoque_busca:
        estoques = e.ler_um_estoque(id_estoque_busca)

    if id_produto_busca:
        estoques = p.listar_um(id_produto_busca)

    if nome_produto_busca:
        estoques = p.pesquisar_nome(nome_produto_busca)

    if estoque_minimo == "5":
        
        estoques = [estoque for estoque in e.ler_todo_estoque() if estoque['quantidade_atual'] >= 5]

    elif estoque_minimo == 'baixo':
            
        estoques = [estoque for estoque in e.ler_todo_estoque() if estoque['quantidade_atual'] <= estoque['quantidade_minima']]

    elif estoque_minimo == 'normal':
            
        estoques = [estoque for estoque in e.ler_todo_estoque() if estoque['quantidade_atual'] > estoque['quantidade_minima']]

    #RETORNA PRO HTML
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

        #PEGA OS DADOS DO FORMULARIO
        nome_produto = request.POST.get('produto')  
        quantidade_atual = request.POST.get('quantidade_atual')
        quantidade_minima = request.POST.get('quantidade_minima')
        
        #VERIFICA SE FORAM PREENCHIDOS
        if not nome_produto or not quantidade_atual or not quantidade_minima:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/estoque_cadastrar.html', {'produtos': produtos})
        
        try:
            
            #CHAMA A CLASSE ESTOQUE E CADASTRA
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

        #PEGA OS DADOS DO FORMULARIO
        idestoque = request.POST.get('idestoque')
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        
        #VERIFICA
        if not idestoque or not coluna or not novo_valor:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/estoque_atualizar.html')
        
        try:
            #CHAMA A CLASSE E ATUALIZA
            e = Estoque()

            e.atualizar_estoque(coluna, novo_valor, idestoque)

            messages.success(request, f'Estoque {idestoque} atualizado com sucesso!')
            return redirect('lista_estoque')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar estoque: {str(e)}')
    
    return render(request, 'core/estoque_atualizar.html')

def deletar_estoque(request):
    
    if request.method == 'POST':

        #PEGA O ID DO ESTOQUE
        idestoque = request.POST.get('idestoque')
        
        #VERIFICA
        if not idestoque:
            messages.error(request, 'ID do estoque é obrigatório!')
            return render(request, 'core/estoque_deletar.html')
        
        try:
            #CHAMA A CLASSE E DELETA O ESTOQUE
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
        #PEGA O NOME DA CATEGORIA
        nome_categoria = request.POST.get('nome_categoria')
        
        if nome_categoria:
            try:
                #CHAMA A CLASSE E CADASTRA A CATEGORIA

                c = Categoria()
                c.cadastro_categoria(nome_categoria)

                messages.success(request, f'Categoria "{nome_categoria}" cadastrada com sucesso!')
                return redirect('cadastrar_servico')  
            
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar categoria: {str(e)}')
    
    return render(request, 'core/categoria_cadastrar.html')

#-----------------------PRODUTO-----------------------------------

def produto_list_view(request):

    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    tipo = request.GET.get('tipo')
    cidade = request.GET.get('cidade')

    p = Produto()
    produtos = p.ler_todos_produtos_ativos()

    categorias = sorted(set([produto['tipo'] for produto in produtos if produto['tipo']]))
    cidades = sorted(set([produto['cidade'] for produto in produtos if produto['cidade']]))
    
    categorias = [produto['tipo'] for produto in produtos]

    if id_busca:
        produtos = p.listar_um(id_busca)

    if nome_busca:
        produtos = p.pesquisar_nome_produto(nome_busca)
        

    if preco_min and preco_max:
        try:
            preco_min = float(preco_min)
            preco_max = float(preco_max)

            produtos = [produto for produto in produtos if preco_min <= float(produto['valor']) <= preco_max]

        except ValueError:
            messages.error(request, 'Preços devem ser valores numéricos.')

    if tipo:

        produtos = [produto for produto in produtos if produto['tipo'].lower() == tipo.lower()]
       
    
    if cidade:
        produtos = [produto for produto in produtos if produto['cidade'].lower() == cidade.lower()]
   
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'cidades': cidades    
    }
    return render(request, 'core/produto_list.html', context)

def cadastrar_produto(request):

    #RECUPERA OS DADOS DE ENTRADA PARA O CADASTRO DO PRODUTO
    if request.method == 'POST':

        valor = request.POST.get('valor')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        cidade = request.POST.get('cidade')
        
        if nome:
            try:
                p = Produto()

                #CASO O PRODUTO JÁ ESTEJA CADASTRADO NO BANCO, ELE VAI SER APENAS REATIVADO
                if p.pesquisar_nome_produto(nome):

                    idproduto = p.pesquisar_nome_produto(nome)[0]['idproduto'] #ATRAVES DA CONSULTA DE PESQUISAR POR NOME, PEGA O ID
                    p.atualizar_produto('status', 'ATIVO', idproduto) #ATUALIZA O PRODUTO
                    p.atualizar_produto('valor', valor , idproduto)
                    p.atualizar_produto('tipo', tipo, idproduto)
                    p.atualizar_produto('cidade', cidade, idproduto)

                    messages.success(request, f'Produto "{nome}" REATIVADO NO SISTEMA com sucesso!')
                    return redirect('cadastrar_produto')  

                else:  

                    #CASO NÃO TENHA CADASTRO, ELE É CADASTRADO
                    p.cadastro_produto(nome, valor, tipo, cidade)
                    messages.success(request, f'Produto "{nome}" cadastrado com sucesso!')
                    return redirect('cadastrar_produto')  
            
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    return render(request, 'core/produto_cadastrar.html')

def editar_produto(request):

    if request.method == 'POST':

        idproduto = request.POST.get('idproduto')
        coluna = request.POST.get('coluna')
        novo_valor = request.POST.get('novo_valor')
        
        if not idproduto or not coluna or not novo_valor:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return render(request, 'core/produto_atualizar.html')
        
        try:
            p = Produto()
            p.atualizar_produto(coluna, novo_valor, idproduto)

            messages.success(request, f'Produto {idproduto} atualizado com sucesso!')
            return redirect('lista_estoque')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar produto: {str(e)}')
    
    return render(request, 'core/produto_atualizar.html')

def deletar_produto(request):

    if request.method == 'POST':

        #PEGA O ID DO PRODUTO
        idproduto = request.POST.get('idproduto')
        
        #VERIFICA
        if not idproduto:
            messages.error(request, 'ID do produto é obrigatório!')
            return render(request, 'core/produto_deletar.html')
        
        try:
            #CHAMA A CLASSE PRODUTO E ATUALIZA ELE P INATIVO
            p = Produto()
            p.atualizar_produto('status', 'INATIVO', idproduto)

            messages.success(request, f'produto {idproduto} desativado do sistema com sucesso!')
            return redirect('lista_estoque')
            
        except Exception as e:
            messages.error(request, f'Erro ao deletar produto: {str(e)}')
    
    return render(request, 'core/produto_deletar.html')

#-----------------------PAGAMENTO-----------------------------------  

def registrar_pagamento(request):
    if request.method == 'POST':

        #PEGA O TIPO DO PAGAMENTO A SER FEITO (SERVIÇO OU PRODUTO) E O METODO DE PAGAMENTO
        tipo = request.POST.get('tipo_pagamento')
        metodo_pagamento = request.POST.get('metodo_pagamento')
        
        try:
            if tipo == 'servico':

                #PEGA O ID DA AGENDA
                id_agenda = request.POST.get('id_agenda')
                
                if not id_agenda or not metodo_pagamento:
                    messages.error(request, "Preencha todos os campos obrigatórios.")
                    return redirect('registrar_pagamento')
                
                #CONFIRMA O SERVICO PELA FUNCAO DA CLASSE AGENDA
                a = Agenda()
                a.confirmar_servico(int(id_agenda), metodo_pagamento)

                messages.success(request, f"Pagamento do serviço {id_agenda} registrado com sucesso!")

            #SE FOR PAGAMENTO DE PRODUTOS
            elif tipo == 'produto':

                #PEGA O ID DO CLIENTE E O DO FUNCIONARIO QUE REALIZOU AQUELA VENDA
                pagamento = Pagamento()
                
                cpf = request.POST.get('cpf_cliente')
                id_cliente = pagamento.processar("SELECT IDCLIENTE FROM CLIENTE WHERE CPF = %s", (cpf,), fetch=True)[0]['idcliente']
                id_funcionario = request.POST.get('id_funcionario')
                
                #VERIFICA
                if not metodo_pagamento or not id_cliente or not id_funcionario:
                    messages.error(request, "Preencha todos os campos obrigatórios.")
                    return redirect('registrar_pagamento')
                
                #CHAMA A CLASSE
                compra = Compra()

                #RECEBE OS PRODUTOS SELECIONADOS E AS QUANTIDADES REFERENTES
                produtos_selecionados = request.POST.getlist('produtos')
                quantidades = request.POST.getlist('quantidades')

                #REGISTRA A COMPRA
                compra.registrar_compra_django(id_cliente, id_funcionario, metodo_pagamento, produtos_selecionados, quantidades, request)
                messages.success(request, "Pagamento dos produtos registrado com sucesso!")

            
        except Exception as e:
            messages.error(request, f"Ocorreu um erro: {str(e)}")
            return redirect('registrar_pagamento')
    
    #CARREGAR A LISTA DE PRODUTOS, DEPOIS CLIENTES E FUNCIONARIOS PARA PASSAR P O HTML:

    produtos = Produto()
    clientes = Clientes()
    funcionarios = Funcionario()

    produtos = produtos.ler_todos_produtos_ativos()
    
    clientes = clientes.ler_todos_clientes()
    
    funcionarios = funcionarios.ler_todos_funcionarios_ativos()
    
    return render(request, 'core/pagamento_registrar.html', {
        'produtos': produtos,
        'clientes': clientes,
        'funcionarios': funcionarios
    })

def pagamento_list_view(request):

    #PEGA VIA GET OS DADOS
    id_busca = request.GET.get('id_busca')
    nome_busca = request.GET.get('nome_busca')

    #CHAMA A CLASSE E LE TODOS OS PAGAMENTOS
    p = Pagamento()
    pagamento = p.ler_todos_pagamentos()
    
    #FUNCOES PARA PESQUISA
    if id_busca:
        pagamento = p.listar_um(id_busca)

    if nome_busca:
        pagamento = p.pesquisar_nome(nome_busca)

    #RETORNA P O HTML
    context = {
        'pagamentos': pagamento
    }
    return render(request, 'core/pagamento_list.html', context)

#-----------------------HOME-----------------------------------
def home(request):
    return render(request, 'core/home.html')

def relatorios(request):
    # Instâncias das classes
    pagamento = Pagamento()
    estoque = Estoque()
    produto = Produto()
    cliente = Clientes()
    servico = Servico()
    agenda = Agenda()
    funcionario = Funcionario()
    compra = Compra()
    
    # Dados básicos
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    
    # Dados financeiros
    pagamentos = pagamento.ler_todos_pagamentos()
    valor_total_vendas = sum(n['valor'] for n in pagamentos)
    total_vendas = len(pagamentos)
    ticket_medio = valor_total_vendas / total_vendas if total_vendas > 0 else 0
    
    # Vendas do mês atual
    vendas_mes = len([p for p in pagamentos 
                     if p['data_pagamento'].month == mes_atual 
                     and p['data_pagamento'].year == ano_atual])
    valor_vendas_mes = sum(p['valor'] for p in pagamentos 
                          if p['data_pagamento'].month == mes_atual 
                          and p['data_pagamento'].year == ano_atual)
    
    # Dados de estoque
    estoques = estoque.ler_todo_estoque()
    total_produtos = len(estoques)
    produtos_baixo_estoque = len([e for e in estoques 
                                 if e['quantidade_atual'] <= e['quantidade_minima']])
    
    # Dados de clientes
    clientes = cliente.ler_todos_clientes()
    total_clientes = len(clientes)
    
    # Dados de serviços
    servicos = servico.ler_todos_servicos_ativos()
    categorias_count = {}
    for s in servicos:
        # Buscar nome da categoria
        categoria_nome = "Sem categoria"
        if 'id_categoria' in s:
            categoria = Categoria().listar_um(s['id_categoria'])
            if categoria:
                categoria_nome = categoria[0].get('nome_categoria', 'Sem categoria')
        categorias_count[categoria_nome] = categorias_count.get(categoria_nome, 0) + 1
    
    # VENDAS MENSIAIS POR FUNCIONÁRIO (SUPER IMPORTANTE!)
    vendas_por_funcionario = {}
    funcionarios = funcionario.ler_todos_funcionarios_ativos()
    
    for func in funcionarios:
        # Vendas de serviços (via agenda)
        agendas_funcionario = agenda.processar(
            "SELECT a.*, p.valor FROM agenda a "
            "JOIN pagamento p ON a.idagenda = p.id_agenda "
            "WHERE a.id_funcionario = %s "
            "AND EXTRACT(MONTH FROM p.data_pagamento) = %s "
            "AND EXTRACT(YEAR FROM p.data_pagamento) = %s",
            (func['idfuncionario'], mes_atual, ano_atual),
            fetch=True
        )
        
        # Vendas de produtos (via compra)
        compras_funcionario = compra.processar(
            "SELECT c.* FROM compra c "
            "JOIN pagamento p ON c.idcompra = p.id_compra "
            "WHERE c.id_funcionario = %s "
            "AND EXTRACT(MONTH FROM p.data_pagamento) = %s "
            "AND EXTRACT(YEAR FROM p.data_pagamento) = %s",
            (func['idfuncionario'], mes_atual, ano_atual),
            fetch=True
        )
        
        total_vendas_func = len(agendas_funcionario) + len(compras_funcionario)
        valor_vendas_func = sum(a['valor'] for a in agendas_funcionario) + sum(c['valor_total'] for c in compras_funcionario)
        
        vendas_por_funcionario[func['nome']] = {
            'total_vendas': total_vendas_func,
            'valor_vendas': valor_vendas_func,
            'servicos_realizados': len(agendas_funcionario),
            'produtos_vendidos': len(compras_funcionario)
        }
    
    # Formas de pagamento mais utilizadas
    formas_pagamento = {}
    for p in pagamentos:
        forma = p.get('forma_pagamento', 'Desconhecida')
        formas_pagamento[forma] = formas_pagamento.get(forma, 0) + 1
    
    # Agendamentos do mês
    agendas_mes = agenda.processar(
        "SELECT COUNT(*) as total FROM agenda "
        "WHERE EXTRACT(MONTH FROM dia) = %s "
        "AND EXTRACT(YEAR FROM dia) = %s",
        (mes_atual, ano_atual),
        fetch=True
    )
    agendamentos_mes = agendas_mes[0]['total'] if agendas_mes else 0
    
    # Taxa de conclusão de agendamentos
    agendamentos_concluidos = agenda.processar(
        "SELECT COUNT(*) as total FROM agenda "
        "WHERE status = 'CONCLUIDO' "
        "AND EXTRACT(MONTH FROM dia) = %s "
        "AND EXTRACT(YEAR FROM dia) = %s",
        (mes_atual, ano_atual),
        fetch=True
    )
    taxa_conclusao = (agendamentos_concluidos[0]['total'] / agendamentos_mes * 100) if agendamentos_mes > 0 else 0
    
    # Produtos mais vendidos
    produtos_mais_vendidos = compra.processar(
        "SELECT p.nome, SUM(ic.quantidade) as total_vendido "
        "FROM itens_compra ic "
        "JOIN produto p ON ic.id_produto = p.idproduto "
        "JOIN compra c ON ic.id_compra = c.idcompra "
        "JOIN pagamento pg ON c.idcompra = pg.id_compra "
        "WHERE EXTRACT(MONTH FROM pg.data_pagamento) = %s "
        "AND EXTRACT(YEAR FROM pg.data_pagamento) = %s "
        "GROUP BY p.nome ORDER BY total_vendido DESC LIMIT 5",
        (mes_atual, ano_atual),
        fetch=True
    )
    
    # Serviços mais solicitados
    servicos_mais_solicitados = agenda.processar(
        "SELECT s.nome, COUNT(*) as total_realizado "
        "FROM agenda a "
        "JOIN servico s ON a.id_servico = s.idservico "
        "JOIN pagamento p ON a.idagenda = p.id_agenda "
        "WHERE EXTRACT(MONTH FROM p.data_pagamento) = %s "
        "AND EXTRACT(YEAR FROM p.data_pagamento) = %s "
        "GROUP BY s.nome ORDER BY total_realizado DESC LIMIT 5",
        (mes_atual, ano_atual),
        fetch=True
    )

    context = {
        'total_vendas': total_vendas,
        'valor_total_vendas': valor_total_vendas,
        'ticket_medio': ticket_medio,
        'vendas_mes': vendas_mes,
        'valor_vendas_mes': valor_vendas_mes,
        'total_produtos': total_produtos,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'total_clientes': total_clientes,
        'categorias_count': categorias_count,
        'vendas_por_funcionario': vendas_por_funcionario,
        'formas_pagamento': formas_pagamento,
        'agendamentos_mes': agendamentos_mes,
        'taxa_conclusao': taxa_conclusao,
        'produtos_mais_vendidos': produtos_mais_vendidos or [],
        'servicos_mais_solicitados': servicos_mais_solicitados or [],
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
    }
    
    return render(request, 'core/relatorio.html', context)

# ---------------------- COMPRAS & SERVIÇOS ----------------------
def compras_servicos(request):
    """Página para registrar compras e visualizar serviços."""
    try:
        produtos = Produto().ler_todos_produtos_ativos()
    except Exception:
        produtos = []

    try:
        clientes = Clientes().ler_todos_clientes()
    except Exception:
        clientes = []

    try:
        funcionarios = Funcionario().ler_todos_funcionarios_ativos()
    except Exception:
        funcionarios = []

    try:
        servicos = Servico().ler_todos_servicos_ativos()
    except Exception:
        servicos = []

    return render(request, 'core/compras_servicos.html', {
        'produtos': produtos,
        'clientes': clientes,
        'funcionarios': funcionarios,
        'servicos': servicos,
    })
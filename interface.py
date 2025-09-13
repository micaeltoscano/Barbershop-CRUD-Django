import crud
import clientes
import funcionarios
import servico
import categoria
import agendas
import tabulate
import disponibilidade
import produto
import estoque
import itens_compra
import compra
import pagamentos
import relatorios


class Interface:
    def __init__(self):
        pass

    def display_menu(self):
        input_opcao = 0

        while input_opcao != 10:
            print(
            "==============================\n"
            "   Bem-vindo ao sistema!  \n"
            "==============================\n"
            "1 - Clientes\n"
            "2 - Funcionários\n"
            "3 - Serviços\n"
            "4 - Agendas\n"
            "5 - Produtos\n"
            "6 - Estoque\n"
            "7 - Compra\n"
            "8 - Pagamentos\n"
            "9 - Relatórios\n"
            "10 - Sair\n"
            "==============================")

            #Corrige a entrada do usuário:
            try:
                input_opcao = int(input("Escolha uma opção (1-9): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 9.")
                continue
            
            match input_opcao:
                case 1:
                    self.display_opcao_clientes()
                
                case 2:
                    self.display_opcao_funcionarios()
                
                case 3:
                    self.display_opcao_servicos()
                
                case 4:
                    self.display_opcao_agendas()
                
                case 5:
                    self.display_opcao_produtos()
                
                case 6:
                    self.display_opcao_estoque()
                
                case 7:
                    self.display_opcao_compras()
                
                case 8:
                    self.display_opcao_pagamentos()
                
                case 9:
                    relatorio = relatorios.relatorios()
                    print(tabulate.tabulate(relatorio.items(), headers=["Métrica", "Valor"], tablefmt="fancy_grid"))

                case 10:
                    print("Saindo do sistema. Até mais!")
                    break
                
                case _:
                    print("Opção inválida. Tente novamente.")

#Clientes ----------------------------------------------------------------------------------------------------

    def display_opcao_clientes(self):
        input_opcao = 0
        cliente = clientes.Clientes()

        while input_opcao != 7:
            print("==============================")
            print("--- Menu Clientes ---")
            print("1 - Listar clientes")
            print("2 - Adicionar cliente")
            print("3 - Pesquisar_nome")
            print("4 - Ver um cliente (id)")
            print("5 - Atualizar cliente")
            print("6 - Deletar cliente")
            print("7 - Voltar")
            print("==============================")

            try:
                input_opcao = int(input("Escolha uma opção (1-7): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 7.")
                continue

            match input_opcao:
                case 1:
                    print("Listando clientes...")
                    print(tabulate.tabulate(cliente.ler_todos_clientes(), headers="keys", tablefmt="fancy_grid"))
                    
                case 2:
                    print("Adicionando cliente...")

                    #Caso o usuário deseje adicionar um novo cliente, pra previnir as entradas inválidas
                    try:
                        nome = input("Nome: ")
                        email = input("Email: ")
                        cpf = input("CPF: ")
                        endereco = input("Endereço: ")
                        numero_celular = input("Número de celular: ")
                        clientes.Clientes().cadastrar_cliente(nome, email, cpf, endereco, numero_celular)

                    except Exception as e:
                        print(f"Erro ao adicionar cliente: \n{e}")
                    
                case 3:
                    nome = input("Nome para pesquisa: ")
                    resultados = print(tabulate.tabulate(cliente.pesquisar_nome(nome), headers="keys", tablefmt="fancy_grid"))
                    
                case 4:
                    id_cliente = input("ID do cliente: ")
                    resultado = cliente.ler_um_cliente(id_cliente)
                    if len(resultado) == 0: #Já tem tratamento de erro na função ler_um_cliente
                        continue
                    else:
                        print(tabulate.tabulate(resultado, headers="keys", tablefmt="fancy_grid"))

                case 5:
                    try:
                        coluna = input("Coluna a ser atualizada (nome, email, cpf, endereco, numero_celular): ")
                        novo_valor = input("Novo valor: ")
                        id_cliente = input("ID do cliente a ser atualizado: ")
                        cliente.atualizar_cliente(coluna, novo_valor, id_cliente)

                    except Exception as e:
                        print(f"Erro ao atualizar cliente: {e}")

                case 6:
                    id_cliente = input("ID do cliente a ser deletado: ")
                    cliente.deletar_cliente(id_cliente)

                case 7:
                    input("Pressione Enter para voltar ao menu principal...")
                    continue
                    
                case _:
                    print("Opção inválida. Tente novamente.")

#Funcionarios ------------------------------------------------------------------------------------------------

    def display_opcao_funcionarios(self):
        input_opcao = 0
        funcionario = funcionarios.Funcionario()
        disponibilidades = disponibilidade.Disponibilidade()

        while input_opcao != 8:
            print("==============================\n"
            "--- Menu Funcionários ---\n"
            "1 - Listar Funcionários\n"
            "2 - Adicionar Funcionário\n"
            "3 - Pesquisar Funcionário\n"
            "4 - Ver um Funcionário (id)\n"
            "5 - Atualizar Funcionário\n"
            "6 - Deletar Funcionário\n"
            "7 - Cadastrar Disponibilidade\n"
            "8 - Voltar\n"
            "==============================")

            try:
                input_opcao = int(input("Escolha uma opção (1-8): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 8.")
                continue
            
            match input_opcao:
                case 1:
                    print("Listando Funcionários...")
                    print(tabulate.tabulate(funcionario.ler_todos_funcionarios(), headers="keys", tablefmt="fancy_grid"))

                case 2:
                    print("Adicionando Funcionário...")

                    # Caso o usuário deseje adicionar um novo funcionário, pra previnir as entradas inválidas
                    try:
                        nome = input("Nome: ")
                        email = input("Email: ")
                        cpf = input("CPF: ")
                        endereco = input("Endereço: ")
                        numero_celular = input("Número de celular: ")
                        salario = input("Salário: ")
                        especialidade = input("Especialidade: ")
                        funcionario.cadastrar_funcionario(nome, email, cpf, endereco, numero_celular, salario, especialidade)

                    except Exception as e:
                        print(f"Erro ao adicionar funcionário: {e}")

                case 3:
                    nome = input("Nome para pesquisa: ")
                    resultados = funcionario.pesquisar_nome(nome)
                    if len(resultados) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultados, headers="keys", tablefmt="fancy_grid"))

                case 4:
                    id_funcionario = input("ID do funcionário: ")
                    resultado = funcionario.ler_um_funcionario(id_funcionario)
                    if len(resultado) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultado, headers="keys", tablefmt="fancy_grid"))

                case 5:
                    try:
                        coluna = input("Coluna a ser atualizada (nome, email, cpf, endereco, numero_celular, salario, especialidade): ")
                        novo_valor = input("Novo valor: ")
                        id_funcionario = input("ID do funcionário a ser atualizado: ")
                        funcionario.atualizar_funcionario(coluna, novo_valor, id_funcionario)

                    except Exception as e:
                        print(f"Erro ao atualizar funcionário: {e}")

                case 6:
                    id_funcionario = input("ID do funcionário a ser deletado: ")
                    funcionario.deletar_funcionario(id_funcionario)

                case 7:
                    print("Cadastrando disponibilidade para funcionário...\n"
                    "0 - segunda-feira\n"
                    "1 - terça-feira\n"
                    "2 - quarta-feira\n"
                    "3 - quinta-feira\n"
                    "4 - sexta-feira\n"
                    "5 - sábado\n"
                    "6 - domingo")
                    dia_semana = input("Qual o dia da semana ele estará disponível ?")
                    hora_inicio = input("Hora de início (formato 24h, ex: 14:00): ")
                    hora_fim = input("Hora de término (formato 24h, ex: 18:00): ")
                    id_funcionario = input("ID do funcionário: ")
                    try:
                        disponibilidades.cadastro_disponibilidade(id_funcionario, dia_semana, hora_inicio, hora_fim)
                    except Exception as e:
                        print(f"Erro ao cadastrar disponibilidade: {e}")

                case 8:
                    input("Pressione Enter para voltar ao menu principal...")
                    continue

                case _:
                    print("Opção inválida. Tente novamente.")

#Serviços ----------------------------------------------------------------------------------------------------

    def display_opcao_servicos(self):
        input_opcao = 0
        servicos = servico.Servico()
        categorias = categoria.Categoria()

        while input_opcao != 10:
            print("==============================\n"
                    "--- Menu Serviços ---\n"
                    "1 - Listar serviços\n"
                    "2 - Adicionar serviço\n"
                    "3 - Pesquisar nome do serviço\n"
                    "4 - Ver um serviço\n"
                    "5 - Atualizar serviço\n"
                    "6 - Deletar serviço\n"
                    "7 - Deletar categoria\n"
                    "8 - Atualizar categoria\n"
                    "9 - Listar categorias\n"
                    "10 - Voltar\n"
                    "==============================")

            try:
                input_opcao = int(input("Escolha uma opção (1-10): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 10.")
                continue

            match input_opcao:
                case 1:
                    print("Listando Serviços...")
                    print(tabulate.tabulate(servicos.ler_todos_servicos(), headers="keys", tablefmt="fancy_grid"))

                case 2:
                    try:
                        nome_servico  = input("Digite o nome do serviço:")
                        valor = input("Digite o valor do serviço:")
                        print("Categorias já cadastradas:")
                        print(tabulate.tabulate(categorias.ler_todas_categorias(), headers="keys", tablefmt="fancy_grid"))
                        resposta = int(input("A categoria já foi cadastrada? (1 ou 0): "))

                        #Verifica se a categoria já existe
                        if resposta == 1 :
                            id_categoria = input("Digite o id da categoria do serviço:")

                        else:
                            categoria_nome = input("Digite o nome da categoria:")
                            categorias.cadastro_categoria(categoria_nome)
                            print(tabulate.tabulate(categorias.ler_todas_categorias(), headers="keys", tablefmt="fancy_grid"))
                            id_categoria = input("Digite o id da categoria do serviço:")

                        duracao = input("Digite a duração do serviço em minutos:")

                        servicos.cadastro_servico(nome_servico, valor, id_categoria, duracao)
                    
                    except Exception as e:
                        print(f"Erro ao adicionar serviço: {e}")

                case 3:
                    nome = input("Digite o nome do serviço: ")
                    resultados = servicos.pesquisar_nome(nome)
                    
                    if len(resultados) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultados, headers="keys", tablefmt="fancy_grid"))
                    

                case 4:
                    id_servico = input("ID do serviço: ")
                    resultado = servicos.ler_um_servico(id_servico)
                    if len(resultado) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultado, headers="keys", tablefmt="fancy_grid"))

                case 5:
                    try:
                        coluna = input("Coluna a ser atualizada (nome, valor, id_categoria, duracao): ")
                        novo_valor = input("Novo valor: ")
                        id_servico = input("ID do serviço a ser atualizado: ")
                        servicos.atualizar_servico(coluna, novo_valor, id_servico)

                    except Exception as e:
                        print(f"Erro ao atualizar serviço: {e}")

                case 6:
                    id_servico = input("ID do serviço a ser deletado: ")
                    servicos.deletar_servico(id_servico)

                case 7:
                    print(tabulate.tabulate(categorias.ler_todas_categorias(), headers="keys", tablefmt="fancy_grid"))
                    id_categoria = input("ID da categoria a ser deletada: ")
                    categorias.deletar_categoria(id_categoria)

                case 8:
                    print("Atualizando categoria...")
                    id_categoria = input("ID da categoria a ser atualizada: ")
                    coluna = "nome"
                    novo_valor = input("Digite o novo nome de categoria: ")
                    categorias.atualizar_categoria(coluna, novo_valor, id_categoria)

                case 9:
                    print("Listando categorias...")
                    print(tabulate.tabulate(categorias.ler_todas_categorias(), headers="keys", tablefmt="fancy_grid"))

                case 10:
                    input("Pressione Enter para voltar ao menu principal...")
                    continue

                case _:
                    print("Opção inválida. Tente novamente.")

#Agendas ----------------------------------------------------------------------------------------------------

    def display_opcao_agendas(self):
        input_opcao = 0
        agenda = agendas.Agenda()
        disponibilidades = disponibilidade.Disponibilidade()
        servicos = servico.Servico()
        cliente = clientes.Clientes()
        
        while input_opcao != 6:
            print("==============================\n"
                  "1 - Listar agendas\n"
                  "2 - Cadastrar agenda\n"  
                  "3 - Ver uma agenda\n" 
                  "4 - Atualizar agenda\n" 
                  "5 - Deletar agenda\n"
                  "6 - Voltar\n"
                  "==============================")

            try:
                input_opcao = int(input("Escolha uma opção (1-6): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 6.")
                continue

            match input_opcao:
                case 1:
                    print("Listando Agendas...")
                    print(tabulate.tabulate(agenda.ler_toda_agenda(), headers="keys", tablefmt="fancy_grid"))

                case 2:
                    try:
                        print("Disponibilidades já cadastradas:")
                        print(tabulate.tabulate(disponibilidades.ler_todas_disponibilidades(), headers="keys", tablefmt="fancy_grid"))
                        dia = input("Digite o dia da agenda (dd/mm/aaaa):")
                        horario = input("Digite o horario da agenda:")
                        id_funcionario = input("Digite o id do funcionário:")

                        print("Serviços já cadastrados:")
                        print(tabulate.tabulate(servicos.ler_todos_servicos(), headers="keys", tablefmt="fancy_grid"))
                        id_servico = input("Digite o id de servico:")

                        print("Clientes já cadastrados:")
                        print(tabulate.tabulate(cliente.ler_todos_clientes(), headers="keys", tablefmt="fancy_grid"))
                        id_cliente = input("Digite o id do cliente:")

                        agenda.cadastrar_agenda(dia, horario, id_funcionario, id_servico, id_cliente, status='agendado')

                    except Exception as e:
                        print(f"Erro ao adicionar agenda: {e}")

                case 3:
                    id_agenda = input("Digite o id da agenda: ")
                    resultados = agenda.ler_um_agenda(id_agenda)
                    if len(resultados) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultados, headers="keys", tablefmt="fancy_grid"))

                case 4:
                    print(tabulate.tabulate(agenda.ler_toda_agenda(), headers="keys", tablefmt="fancy_grid"))
                    id_agenda = input("ID da agenda: ")
                    coluna = input("Coluna a ser atualizada (dia, horario, id_funcionario, id_servico, id_cliente, status): ")
                    novo_valor = input("Novo valor: ")          
                    agenda.atualizar_agenda(coluna, novo_valor, id_agenda)

                case 5:
                    id_agenda = input("ID da agenda a ser deletada: ")
                    agenda.deletar_agenda(id_agenda)
                    
                case 6:
                    input("Pressione Enter para voltar ao menu principal...")
                    continue

                case _:
                    print("Opção inválida. Tente novamente.")

#Produtos ----------------------------------------------------------------------------------------------------

    def display_opcao_produtos(self):
            input_opcao = 0
            produtos = produto.Produto()

            while input_opcao != 7:
                print("==============================\n"
                    "--- Menu Produtos ---\n"
                    "1 - Listar produtos\n"
                    "2 - Adicionar produto\n"
                    "3 - Pesquisar nome do produto\n"
                    "4 - Ver um produto\n"
                    "5 - Atualizar produto\n"
                    "6 - Deletar produto\n"
                    "7 - Voltar\n"
                    "==============================")

                try:
                    input_opcao = int(input("Escolha uma opção (1-7): "))
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número entre 1 e 7.")
                    continue

                match input_opcao:
                    case 1:
                        print("Listando Produtos...")
                        print(tabulate.tabulate(produtos.ler_todos_produtos(), headers="keys", tablefmt="fancy_grid"))

                    case 2:
                        try:
                            nome  = input("Digite o nome do produto:")
                            valor = input("Digite o valor do produto:")
                            tipo = input("Digite o tipo do produto:")
                            produtos.cadastro_produto(nome, valor, tipo)
                        
                        except Exception as e:
                            print(f"Erro ao adicionar produto: {e}")

                    case 3:
                        nome = input("Digite o nome do produto: ")
                        resultados = produtos.pesquisar_nome_produto(nome)
                        
                        if len(resultados) == 0:
                            continue
                        else:
                            print(tabulate.tabulate(resultados, headers="keys", tablefmt="fancy_grid"))

                    case 4:
                        id_produto = input("ID do produto: ")
                        resultado = produtos.ler_um_produto(id_produto)
                        if len(resultado) == 0:
                            continue
                        else:
                            print(tabulate.tabulate(resultado, headers="keys", tablefmt="fancy_grid"))

                    case 5:
                        try:
                            coluna = input("Coluna a ser atualizada (nome, valor, tipo, status): ")
                            novo_valor = input("Novo valor: ")
                            id_produto = input("ID do produto a ser atualizado: ")
                            produtos.atualizar_produto(coluna, novo_valor, id_produto)

                        except Exception as e:
                            print(f"Erro ao atualizar produto: {e}")

                    case 6:
                        id_produto = input("ID do produto a ser deletado: ")
                        produtos.deletar_produto(id_produto)

                    case 7:
                        input("Pressione Enter para voltar ao menu principal...")
                        continue

                    case _:
                        print("Opção inválida. Tente novamente.")

#Estoque ----------------------------------------------------------------------------------------------------

    def display_opcao_estoque(self):
        input_opcao = 0
        estoques = estoque.Estoque()

        while input_opcao != 6:
            print("==============================\n"
                  "--- Menu Estoque ---\n"
                  "1 - Listar estoque\n"
                  "2 - Adicionar ao estoque\n"
                  "3 - Ver um item do estoque\n"
                  "4 - Atualizar estoque\n"
                  "5 - Deletar do estoque\n"
                  "6 - Voltar\n"
                  "==============================")

            try:
                input_opcao = int(input("Escolha uma opção (1-6): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 6.")
                continue

            match input_opcao:
                case 1:
                    print("Listando Estoque...")
                    print(tabulate.tabulate(estoques.ler_todo_estoque(), headers="keys", tablefmt="fancy_grid"))
                
                case 2:
                    try:
                        nome = input("Digite o nome do produto: ")
                        quantidade = int(input("Digite a quantidade: "))
                        quantidade_min = int(input("Digite a quantidade mínima: "))
                        estoques.cadastro_estoque(nome, quantidade, quantidade_min)

                    except Exception as e:
                        print(f"Erro ao adicionar ao estoque: {e}")

                case 3:
                    id_estoque = input("ID do item do estoque: ")
                    resultado = estoques.ler_um_estoque(id_estoque)
                    if len(resultado) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultado, headers="keys", tablefmt="fancy_grid"))
                    
                case 4:
                    try:
                        coluna = input("Coluna a ser atualizada (quantidade_atual, quantidade_minima): ")
                        novo_valor = input("Novo valor: ")
                        id_estoque = input("ID do item do estoque a ser atualizado: ")
                        estoques.atualizar_estoque(coluna, novo_valor, id_estoque)

                    except Exception as e:
                        print(f"Erro ao atualizar estoque: {e}")
                
                case 5:
                    id_estoque = input("ID do item do estoque a ser deletado: ")
                    estoques.deletar_estoque(id_estoque)
                
                case 6:
                    input("Pressione Enter para voltar ao menu principal...")
                    break

                case _:
                    print("Opção inválida. Tente novamente.")
                    continue
            
#Compras ----------------------------------------------------------------------------------------------------

    def display_opcao_compras(self):
        compras = compra.Compra()
        input_opcao = 0

        while input_opcao != 3:
            print("==============================\n"
                "--- Menu Compras ---\n"
                "1 - Listar compras\n"
                "2 - Registrar compra\n"
                "3 - Voltar\n"
                "==============================")
            
            try:
                input_opcao = int(input("Escolha uma opção (1-5): "))
            
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 5.")
                continue

            match input_opcao:
                case 1:
                    print("Listando Compras...")
                    print(tabulate.tabulate(compras.ler_todas_compras(), headers="keys", tablefmt="fancy_grid"))

                case 2:
                    try:
                        metodo_pagamento = input("Digite o método de pagamento (ex: 'DINHEIRO','CARTAO_DEBITO','CARTAO_CREDITO','PIX','TRANSFERENCIA'): ")
                        compras.registrar_compra(metodo_pagamento)

                    except Exception as e:
                        print(f"Erro ao registrar compra: {e}")

                case 3:
                    input("Pressione Enter para voltar ao menu principal...")
                    break

                case _:
                    print("Opção inválida. Tente novamente.")
                    continue

# Pagamento ----------------------------------------------------------------------------------------------------

    def display_opcao_pagamentos(self):
        input_opcao = 0
        pagamento = pagamentos.Pagamento()
        compras = compra.Compra()
        agenda = agendas.Agenda()

        while input_opcao != 6:
            print("==============================\n"
                  "--- Menu Pagamentos ---\n"
                  "1 - Listar pagamentos\n"
                  "2 - Registrar pagamento produto\n"
                  "3 - Registrar pagamento serviço\n"
                  "4 - Ver um pagamento\n"
                  "5 - Voltar\n"
                  "==============================")

            try:
                input_opcao = int(input("Escolha uma opção (1-5): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 5.")
                continue

            match input_opcao:
                case 1:
                    print("Listando Pagamentos...")
                    print(tabulate.tabulate(pagamento.ler_todos_pagamentos(), headers="keys", tablefmt="fancy_grid"))

                case 2:
                    try:
                        print(tabulate.tabulate(compras.ler_todas_compras(), headers="keys", tablefmt="fancy_grid"))
                        id_compra = input("Digite o ID da compra associada ao pagamento: ")
                        metodo_pagamento = input("Digite o método de pagamento (ex: 'DINHEIRO','CARTAO_DEBITO','CARTAO_CREDITO','PIX','TRANSFERENCIA': ")
                        pagamento.registrar_pagamento_produto(id_compra, metodo_pagamento)

                    except Exception as e:
                        print(f"Erro ao adicionar pagamento: {e}")

                case 3:
                    try:
                        print(tabulate.tabulate(agenda.ler_toda_agenda(), headers="keys", tablefmt="fancy_grid"))
                        id_agenda = input("Digite o ID da agenda associada ao pagamento: ")
                        metodo_pagamento = input("Digite o método de pagamento (ex: 'DINHEIRO','CARTAO_DEBITO','CARTAO_CREDITO','PIX','TRANSFERENCIA': ")
                        pagamento.registrar_pagamento_servico(id_agenda, metodo_pagamento)

                    except Exception as e:
                        print(f"Erro ao adicionar pagamento: {e}")

                case 4:
                    id_pagamento = input("ID do pagamento a ser visualizado: ")
                    resultado = pagamento.ler_um_pagamento(id_pagamento)
                    if len(resultado) == 0:
                        continue
                    else:
                        print(tabulate.tabulate(resultado, headers="keys", tablefmt="fancy_grid"))

                case 5:
                    input("Pressione Enter para voltar ao menu principal...")
                    break

                case _:
                    print("Opção inválida. Tente novamente.")
                    continue

interface = Interface()
interface.display_menu()

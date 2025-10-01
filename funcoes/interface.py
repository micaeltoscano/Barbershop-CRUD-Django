import crud
import clientes
import funcionarios


#agenda = Agenda()
#funcionario = Funcionario()
cliente = clientes.Clientes()
#disponibilidade = Disponibilidade()
#categoria = Categoria()
#servico = Servico()
#compra = Compra()

class Interface:
    def __init__(self):
        pass

    def display_menu(self):
        input_opcao = 0

        while input_opcao != 5:
            print("==============================")
            print("   Bem-vindo ao sistema!")
            print("==============================")
            print("1 - Clientes")
            print("2 - Funcionários")
            print("3 - Serviços")
            print("4 - Agendas")
            print("5 - Sair")
            print("==============================")

            #Corrige a entrada do usuário:
            try:
                input_opcao = int(input("Escolha uma opção (1-5): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número entre 1 e 5.")
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
                    print("Saindo do sistema. Até logo!")
                case _:
                    print("Opção inválida. Tente novamente.")
















    def display_opcao_clientes(self):
        input_opcao = 0

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
                    print(cliente.ler_todos_clientes())
                    
                case 2:
                    print("Adicionando cliente...")

                    #Caso o usuário deseje adicionar um novo cliente, pra previnir as entradas inválidas
                    try:
                        nome = input("Nome: ")
                        idade = input("Idade: ")
                        email = input("Email: ")
                        cpf = input("CPF: ")
                        endereco = input("Endereço: ")
                        numero_celular = input("Número de celular: ")
                        clientes.Clientes().cadastrar_cliente(nome, idade, email, cpf, endereco, numero_celular)

                    except Exception as e:
                        print(f"Erro ao adicionar cliente: {e}")
                    
                case 3:
                    nome = input("Nome para pesquisa: ")
                    resultados = cliente.pesquisar_nome(nome)
                    print(resultados)
                            
                case 4:
                    id_cliente = input("ID do cliente: ")
                    resultado = cliente.ler_um_cliente(id_cliente)
                    if len(resultado) == 0:
                        print("Cliente não encontrado.")
                    else:
                        print(resultado)

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

    def display_opcao_funcionarios(self):
        print("--- Menu Funcionários ---")
        print("1 - Listar funcionários")
        print("2 - Adicionar funcionário")
        print("3 - Voltar")

    def display_opcao_servicos(self):
        print("--- Menu Serviços ---")
        print("1 - Listar serviços")
        print("2 - Adicionar serviço")
        print("3 - Voltar")

    def display_opcao_agendas(self):
        print("--- Menu Agendas ---")
        print("1 - Listar agendas")
        print("2 - Adicionar agenda")
        print("3 - Voltar")

interface = Interface()
interface.display_menu()

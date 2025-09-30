
-----------------------------------------------------
-- CLIENTES
-----------------------------------------------------
INSERT INTO CLIENTE (NOME, EMAIL, CPF, ENDERECO, CIDADE, NUMERO_CELULAR, IS_FLAMENGO, IS_ONEPIECE) VALUES
('João Silva', 'joao@email.com', '12345678901', 'Rua A, 123', 'João Pessoa', '83999990001', TRUE, FALSE),
('Maria Souza', 'maria@email.com', '23456789012', 'Rua B, 456', 'Campina Grande', '83999990002', FALSE, TRUE),
('Carlos Oliveira', 'carlos@email.com', '34567890123', 'Rua C, 789', 'João Pessoa', '83999990003', TRUE, TRUE);

-----------------------------------------------------
-- FUNCIONARIOS
-----------------------------------------------------
INSERT INTO FUNCIONARIO (NOME, EMAIL, CPF, ENDERECO, NUMERO_CELULAR, SALARIO, ESPECIALIDADE) VALUES
('Ana Lima', 'ana@email.com', '45678901234', 'Rua D, 101', '83999990004', 2500.00, 'Cabeleireiro'),
('Pedro Santos', 'pedro@email.com', '56789012345', 'Rua E, 202', '83999990005', 3000.00, 'Manicure'),
('Lucas Rocha', 'lucas@email.com', '67890123456', 'Rua F, 303', '83999990006', 2800.00, 'Barbeiro');

-----------------------------------------------------
-- CATEGORIAS
-----------------------------------------------------
INSERT INTO CATEGORIA (NOME_CATEGORIA) VALUES
('Cabelo'), ('Unha'), ('Barba');

-----------------------------------------------------
-- SERVICOS
-----------------------------------------------------
INSERT INTO SERVICO (NOME, VALOR, ID_CATEGORIA, DURACAO) VALUES
('Corte de Cabelo', 50.00, 1, 30),
('Pintura de Unha', 40.00, 2, 45),
('Barba Completa', 35.00, 3, 25);

-----------------------------------------------------
-- PRODUTOS
-----------------------------------------------------
INSERT INTO PRODUTO (NOME, VALOR, TIPO, CIDADE) VALUES
('Shampoo Premium', 20.00, 'Higiene', 'João Pessoa'),
('Esmalte Vermelho', 10.00, 'Cosmético', 'Campina Grande'),
('Espuma de Barbear', 15.00, 'Higiene', 'João Pessoa');

-----------------------------------------------------
-- ESTOQUE
-----------------------------------------------------
INSERT INTO ESTOQUE (ID_PRODUTO, QUANTIDADE_ATUAL, QUANTIDADE_MINIMA) VALUES
(1, 50, 10),
(2, 100, 20),
(3, 30, 5);

-----------------------------------------------------
-- DISPONIBILIDADE DE FUNCIONARIOS
-----------------------------------------------------
INSERT INTO DISPONIBILIDADE (ID_FUNCIONARIO, DIA_SEMANA, HORA_INICIO, HORA_FIM) VALUES
(1, 'SEGUNDA', '08:00', '17:00'),
(2, 'TERCA', '09:00', '18:00'),
(3, 'QUARTA', '10:00', '19:00');

-----------------------------------------------------
-- AGENDA
-----------------------------------------------------
INSERT INTO AGENDA (ID_CLIENTE, ID_FUNCIONARIO, ID_SERVICO, DIA, HORARIO) VALUES
(1, 1, 1, '2025-09-15', '10:00'),
(2, 2, 2, '2025-09-16', '11:00'),
(3, 3, 3, '2025-09-17', '15:00');

-----------------------------------------------------
-- COMPRA
-----------------------------------------------------
INSERT INTO COMPRA (ID_CLIENTE, ID_FUNCIONARIO, DATA_COMPRA, VALOR_TOTAL) VALUES
(1, 1, '2025-09-10 14:30', 70.00),
(2, 2, '2025-09-12 16:00', 30.00);

-----------------------------------------------------
-- ITENS_COMPRA
-----------------------------------------------------
INSERT INTO ITENS_COMPRA (ID_COMPRA, ID_PRODUTO, QUANTIDADE, VALOR_UNITARIO, VALOR_TOTAL_ITEM) VALUES
(1, 1, 2, 20.00, 40.00),
(1, 3, 2, 15.00, 30.00),
(2, 2, 3, 10.00, 30.00);

-----------------------------------------------------
-- PAGAMENTO
-----------------------------------------------------
INSERT INTO PAGAMENTO (ID_AGENDA, ID_COMPRA, VALOR, FORMA_PAGAMENTO, STATUS) VALUES
(1, NULL, 50.00, 'PIX', 'APROVADO'),
(NULL, 1, 70.00, 'CARTAO_CREDITO', 'APROVADO'),
(NULL, 2, 30.00, 'DINHEIRO', 'APROVADO');

-----------------------------------------------------
-- UTILIZA
-----------------------------------------------------
INSERT INTO UTILIZA (ID_SERVICO, ID_PRODUTO, QUANTIDADE) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1);
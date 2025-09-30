CREATE OR REPLACE FUNCTION filtrar_compras(p_ano INT, p_mes INT)
RETURNS TABLE (
    idcompra INT,
    id_cliente INT,
    id_funcionario NUMERIC, 
    valor_total NUMERIC,
    data_compra TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.idcompra,
           c.id_cliente,
           c.id_funcionario::NUMERIC, 
           c.valor_total::NUMERIC,
           c.data_compra
    FROM compra c
    WHERE EXTRACT(YEAR FROM c.data_compra) = p_ano
      AND EXTRACT(MONTH FROM c.data_compra) = p_mes;
END;
$$ LANGUAGE plpgsql;

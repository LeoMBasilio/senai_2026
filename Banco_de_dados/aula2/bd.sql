CREATE TABLE Cliente (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Nome TEXT NOT NULL,
Email TEXT
);
CREATE TABLE Produto (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Nome TEXT NOT NULL,
Preco DECIMAL(10,2)
);
CREATE TABLE Pedido (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
ClienteID INTEGER,
ProdutoID INTEGER,
Quantidade INTEGER,
Data DATE,
FOREIGN KEY (ClienteID) REFERENCES Cliente(ID),
FOREIGN KEY (ProdutoID) REFERENCES Produto(ID)
);

CREATE TABLE Forncedor(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnpj TEXT(14)
);

DROP TABLE Fornecedor;

ALTER TABLE Cliente ADD telefone INTEGER(11)

INSERT INTO Cliente(ID, nome, email) VALUES (1, "joana", "joana@email.com");
INSERT INTO Produtos(preco, nome) VALUES (8.50, "cafe");
INSERT INTO Pedidos(ClienteID, ProdutoID, quantidade, data) VALUES (1, 10, 8, "25/03/2026");

UPDATE Cliente SET email = "joana.silva@email.com" WHERE ID = 1;

DELETE FROM pedido WHERE id = 1;

SELECT * FROM Cliente LIMIT 10; /* select ALL FROM Clientes*/

SELECT nome FROM Produtos where preco > 10 ORDER BY nome;

SELECT Cliente.nome, pedido.data
From Clientes
INNER JOIN pedidos ON cliente.Id == Pedido.clienteID;

SELECT Prduto.nome, SUM(pedido.quantidade)
FROM produtos
INNER JOIN pedidos on Produto.Id == pedido.produtoid
GROUP by nome

SELECT Prduto.nome, pedido.quantidade
FROM pedidos
WHERE pedido.quantidade == 0
INNER JOIN Produtos on Produto.Id == pedido.produtoid
GROUP by nome

CREATE TABLE Stock (
        Cproducto INT PRIMARY KEY,  
            Cantidad INT                
        );
CREATE TABLE Pedido (
            Cpedido INT PRIMARY KEY,    
            Ccliente INT,               
            Fecha_pedido DATE          
        );
CREATE TABLE Detalle_Pedido (
            Cpedido INT,                
            Cproducto INT,              
            Cantidad INT,               
            PRIMARY KEY (Cpedido, Cproducto), 
            FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),  
            FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto)
        );
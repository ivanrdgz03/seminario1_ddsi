import oracledb
import os
import sys

# Función para obtener las credenciales de un archivo externo "config.ini"
# El formato de este archivo es el siguiente:
#<user>
#<password>
#<dsn>
def get_credentials():
    try:
        with open('config.ini', 'r') as file:
            user = file.readline().strip()
            password = file.readline().strip()
            dsn = file.readline().strip()
    except FileNotFoundError as errorFNFE:  #Error al abrir el archivo
        print("Error reading the file: ", errorFNFE)
    finally:
        file.close()
    return [user, password, dsn]

#Esta función limpia la pantalla de la consola, para cuando se haga el menú
def clear():
    if(os.name == 'nt'):    #Si el sistema es windows se usa el comando cls si es otro se usa clear
        os.system('cls')
    else:
        os.system('clear')
        
def opcion1(cursor):
    try:
        # Borrar las tablas si existen
        print("Eliminando tablas...")
        cursor.execute("DROP TABLE Detalle_Pedido CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Pedido CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Stock CASCADE CONSTRAINTS")
        
        # Crear de nuevo las tablas
        print("Creando tablas...")
        cursor.execute("""
            CREATE TABLE Stock (
                Cproducto INT PRIMARY KEY,  
                Cantidad INT                
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Pedido (
                Cpedido INT PRIMARY KEY,    
                Ccliente INT,               
                Fecha_pedido DATE          
            )
        """)
        
        cursor.execute("""
            CREATE TABLE Detalle_Pedido (
                Cpedido INT,                
                Cproducto INT,              
                Cantidad INT,               
                PRIMARY KEY (Cpedido, Cproducto), 
                FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),  
                FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto)
            )
        """)
        
        # Insertar los datos predefinidos en la tabla Stock
        print("Insertando datos predefinidos en Stock...")
        productos = [
            (1, 100), (2, 50), (3, 200), (4, 75), (5, 150),
            (6, 120), (7, 300), (8, 90), (9, 60), (10, 180)
        ]
        
        for producto in productos:
            cursor.execute("""
                INSERT INTO Stock (Cproducto, Cantidad) 
                VALUES (:1, :2)
            """, producto)
        
        # Confirmar los cambios
        cursor.connection.commit()
        print("Tablas creadas y datos insertados correctamente.")
    
    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()
  
def opcion2(cursor):
    try:
        Cpedido= int(input("Codigo del pedido: "))
        Ccliente = int(input("Codigo del cliente: "))
        fecha = input("Introduce una fecha (formato dd/mm/aaaa): ")
        fecha2 = datetime.strptime(fecha, "%d/%m/%Y")
        Fecha_pedido = fecha2.strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Pedido (Cpedido, Ccliente, Fecha_pedido) VALUES (?,?,?)",(Cpedido,Ccliente,Fecha_pedido))
        #print("cpedido ", Cpedido, "ccliente ", Ccliente , "fecha ", Fecha_pedido)
        
        print("Pendiente de implementar.", file=sys.stderr)


    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()
    
def opcion3(cursor):
    print("Pendiente de implementar.", file=sys.stderr)
    
def opcion4(cursor):
    return

def imprimir_menu():
    espaciado = 46
    clear()
    print("=" * espaciado)
    print("               MENÚ INTERACTIVO")
    print("=" * espaciado)
    print("[1] Borrado y creación de tuplas predefinidas.")
    print("[2] Dar de alta nuevo pedido.")
    print("[3] Mostrar contenido de las tablas.")
    print("[4] Salir.")
    print("=" * espaciado)
    
def menu(cursor):
    funciones = [opcion1,opcion2,opcion3,opcion4]
    imprimir_menu()
    opcion = int(input("Introduzca un número del 1 al 4: "))
    while opcion not in range(1,5):
        print("Debe introducir un número entre el 1 y el 4", file=sys.stderr)
        opcion = int(input())
    funciones[opcion-1](cursor)

def main():
    try: 
        user, password, dsn = get_credentials()
        conexion = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = conexion.cursor()
        # Solicitudes y resto de codigo aquí
        menu(cursor)
    except oracledb.DatabaseError as errorBD:   #Error al establecer la conexión de la base de datos
        error = errorBD.args[0]
        print("Error connecting to the database: ", error.message)
        print("Error code: ", error.code)
    except KeyboardInterrupt:   #Si hacemos control + c
        print("\nSaliendo con Ctrl+C...")
    except Exception as otroError:  #Otro tipo de error
        print("Another error: ", otroError)
    finally:    #Al final, pase lo que pase se cierran el cursor y la conexión
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()
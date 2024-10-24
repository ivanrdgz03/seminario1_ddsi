import oracledb
import os
import sys
from datetime import datetime
# Función para obtener las credenciales de un archivo externo "config.ini"
# El formato de este archivo es el siguiente:
#<user>
#<password>
#<dsn>
def get_credentials():
    try:
        #obtener ruta del fichero
        directorio = os.path.dirname(__file__)
        archivo = os.path.join(directorio, 'config.ini')
        with open(archivo, 'r') as file:
            user = file.readline().strip()
            password = file.readline().strip()
            dsn = file.readline().strip()
    except FileNotFoundError as errorArchivo:  #Error al abrir el archivo
        print("Error reading the file: ", errorArchivo)
    finally:
        file.close()
    return [user, password, dsn]
#Función para obtener las instrucciones de creación de la tabla del archivo "create_table.sql", 
# estas instrucciones deben tener cada una al final ";" obligatoriamente.
def get_create_table_query(cursor):
    try:
        directorio = os.path.dirname(__file__)
        archivo = os.path.join(directorio, 'create_table.sql')
        with open(archivo, 'r') as file:
            sql_script = file.read()
            
        sql_commands = sql_script.split(';')
        
        for command in sql_commands:
            cursor.execute(command)
            
    except FileNotFoundError as errorArchivo:
        print("Error reading the file: ", errorArchivo)
    finally:
        file.close()
        
#Esta función limpia la pantalla de la consola, para cuando se haga el menú
def clear():
    if(os.name == 'nt'):    #Si el sistema es windows se usa el comando cls si es otro se usa clear
        os.system('cls')
    else:
        os.system('clear')
        
def opcion1(cursor):
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

def opcion2(cursor):

    Cpedido= int(input("Codigo del pedido: "))
    Ccliente = int(input("Codigo del cliente: "))
    fecha = input("Introduce una fecha (formato dd/mm/aaaa): ")
    fecha2 = datetime.strptime(fecha, "%d/%m/%Y")
    Fecha_pedido = fecha2.strftime("%d-%m-%Y")
    cursor.execute("""
        INSERT INTO Pedido (Cpedido, Ccliente, Fecha_pedido) 
        VALUES (:Cpedido, :Ccliente, TO_DATE(:Fecha_pedido, 'DD-MM-YYYY'))
        """, {
        "Cpedido": Cpedido,
        "Ccliente": Ccliente,
        "Fecha_pedido": Fecha_pedido
        })
    Cantidad=0
    Cproducto=0
    menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)
    
    cursor.connection.commit()
    
def opcion3(cursor):
    print("Pendiente de implementar.", file=sys.stderr)
    
def opcion4(cursor):
    return


def Añadir_detalle(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    Cproducto = int(input("Codigo del producto: "))
    Cantidad = int(input("Cantidad del producto: "))
    cursor.execute("SELECT Cantidad FROM Stock WHERE Cproducto = :Cproducto", {"Cproducto": Cproducto})
    resultado = cursor.fetchone()
    Cantidad_disponible = resultado[0]
    print(Cantidad_disponible)
    while True:
        Cantidad = int(input("Cantidad del producto: "))
        if Cantidad > Cantidad_disponible:
            print("Cantidad inválida. Inténtalo de nuevo.")
        else:
            break  # Número válido y dentro del rango
        
    cursor.execute("""
        UPDATE Stock
        SET Cantidad = Cantidad - :cantidad_a_restar
        WHERE Cproducto = :Cproducto
    """, {
        "cantidad_a_restar": Cantidad,
        "Cproducto": Cproducto
    })
    
    cursor.execute("""
            INSERT INTO Detalle_Pedido (Cpedido, Cproducto, Cantidad) 
            VALUES (:Cpedido, :Cproducto, :Cantidad )
            """, {
            "Cpedido": Cpedido,
            "Cproducto": Cproducto,
            "Cantidad": Cantidad
            })
    menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)

def Eliminar_detalles(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):

    cursor.execute("""
        DELETE FROM Detalle_Pedido
        WHERE Cpedido = :Cpedido
    """, {
        "Cpedido": Cpedido
    })
     
    
    cursor.execute("""
        UPDATE Stock
        SET Cantidad = Cantidad + :cantidad_a_sumar
        WHERE Cproducto = :Cproducto
    """, {
        "cantidad_a_sumar": Cantidad,
        "Cproducto": Cproducto
    })
    
    Cantidad = 0
    
    menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)

def Cancelar_pedido(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    cursor.execute("""
        DELETE FROM Detalle_Pedido
        WHERE Cpedido = :Cpedido
    """, {
        "Cpedido": Cpedido
    })
    cursor.execute("""
        DELETE FROM Pedido
        WHERE Cpedido = :Cpedido
    """, {
        "Cpedido": Cpedido
    })
    cursor.execute("""
        UPDATE Stock
        SET Cantidad = Cantidad + :cantidad_a_sumar
        WHERE Cproducto = :Cproducto
    """, {
        "cantidad_a_sumar": Cantidad,
        "Cproducto": Cproducto
    })
    
    menu(cursor)

def Finalizar_pedido(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    cursor.connection.commit()

    menu(cursor)

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
    
def imprimir_menu_opcion2():
    espaciado = 46
    clear()
    print("=" * espaciado)
    print("               MENÚ INTERACTIVO")
    print("=" * espaciado)
    print("[1] Añadir detalle de producto.")
    print("[2] Eliminar todos los detalles del producto.")
    print("[3] Cancelar pedido.")
    print("[4] Finalizar pedido.")
    print("=" * espaciado)


def menu(cursor):
    funciones = [opcion1,opcion2,opcion3,opcion4]
    imprimir_menu()
    opcion = int(input("Introduzca un número del 1 al 4: "))
    while opcion not in range(1,5):
        print("Debe introducir un número entre el 1 y el 4", file=sys.stderr)
        opcion = int(input())
    funciones[opcion-1](cursor)

def menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    funciones = [Añadir_detalle,Eliminar_detalles,Cancelar_pedido,Finalizar_pedido]
    imprimir_menu_opcion2()
    opcion = int(input("Introduzca un número del 1 al 4: "))
    while opcion not in range(1,5):
        print("Debe introducir un número entre el 1 y el 4", file=sys.stderr)
        opcion = int(input())
    
    funciones[opcion-1](cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)

    


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
        cursor.connection.rollback()
    except KeyboardInterrupt:   #Si hacemos control + c
        print("\nSaliendo con Ctrl+C...")
        cursor.connection.rollback()
    except Exception as otroError:  #Otro tipo de error
        print("Another error: ", otroError)
        cursor.connection.rollback()
    finally:    #Al final, pase lo que pase se cierran el cursor y la conexión
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()
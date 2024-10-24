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
    print("Pendiente de implementar.", file=sys.stderr)
    
def opcion2(cursor):
    try:
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

        
        menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido)
        
        cursor.connection.commit()

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


def Añadir_detalle(cursor,Cpedido,Ccliente,Fecha_pedido):
    try:
        Cproducto = int(input("Codigo del producto: "))
        Cantidad = int(input("Cantidad del producto: "))
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
        
        
    
        menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido)

    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()


def Eliminar_detalles(cursor,Cpedido,Ccliente,Fecha_pedido):
    try:
        cursor.execute("""
            DELETE FROM Detalle_Pedido
            WHERE Cpedido = :Cpedido
        """, {
            "Cpedido": Cpedido
        })
         
        #Hay que actualizar la cantidad aquí

        
    
        menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido)
    

    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()


def Cancelar_pedido(cursor,Cpedido,Ccliente,Fecha_pedido):
    try:
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

       

        menu(cursor)

    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()

    


def Finalizar_pedido(cursor,Cpedido,Ccliente,Fecha_pedido):
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
4

def menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido):
    funciones = [Añadir_detalle,Eliminar_detalles,Cancelar_pedido,Finalizar_pedido]
    imprimir_menu_opcion2()
    opcion = int(input("Introduzca un número del 1 al 4: "))
    while opcion not in range(1,5):
        print("Debe introducir un número entre el 1 y el 4", file=sys.stderr)
        opcion = int(input())
    
    funciones[opcion-1](cursor,Cpedido,Ccliente,Fecha_pedido)

    


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
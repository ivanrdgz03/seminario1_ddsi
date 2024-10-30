import oracledb
import os
import sys
from datetime import datetime
from tkinter import *
import tkinter as tk

# Función para obtener las credenciales de un archivo externo "config.ini"
# El formato de este archivo es el siguiente:
#<user>
#<password>
#<dsn>
def get_credentials():
    try:
        #obtener ruta del fichero
        directorio = os.path.dirname(os.path.abspath(__file__))
        archivo = os.path.join(directorio, 'config.ini')
        with open(archivo, 'r') as file:
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

    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()

   
    
def opcion3(cursor):
    output_label.config(text="Pendiente de implementar.")

    
def opcion4(cursor):
    return


def Añadir_detalle(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
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
        
        
    
        menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)

    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()


def Eliminar_detalles(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    try:
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
    

    except oracledb.DatabaseError as errorBD:
        error = errorBD.args[0]
        print("Error in database operation: ", error.message)
        print("Error code: ", error.code)
        cursor.connection.rollback()  # Revertir cambios en caso de error
    except Exception as otroError:
        print("Another error: ", otroError)
        cursor.connection.rollback()


def Cancelar_pedido(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
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

        cursor.execute("""
            UPDATE Stock
            SET Cantidad = Cantidad + :cantidad_a_sumar
            WHERE Cproducto = :Cproducto
        """, {
            "cantidad_a_sumar": Cantidad,
            "Cproducto": Cproducto
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



#Limpia ventana
def clear_window(window):
    # Elimina todos los widgets en la ventana dada
    for widget in window.winfo_children():
        widget.destroy()


def menu_principal(cursor):
    #Menu principal
    clear_window(root)

    # Option 1: Create tables button
    create_table_btn = tk.Button(root, text="Borrar y Crear Tablas", font=("Arial", 20), command=lambda: opcion1(cursor))
    create_table_btn.pack(pady=10)

    # Option 2: Add new order
    global order_id_entry, client_id_entry, order_date_entry
    order_id_entry = tk.Entry(root, width=50, font=("Arial", 20))
    client_id_entry = tk.Entry(root, width=50, font=("Arial", 20))
    order_date_entry = tk.Entry(root, width=50, font=("Arial", 20))
    
    tk.Label(root, text="ID del Pedido:",font=("Arial", 20)).pack()
    order_id_entry.pack(pady=10)
    
    tk.Label(root, text="ID del Cliente:", font=("Arial", 20)).pack()
    client_id_entry.pack(pady=10)
    
    tk.Label(root, text="Fecha del Pedido (dd/mm/yyyy):", font=("Arial", 20)).pack()
    order_date_entry.pack(pady=10)
    
    add_order_btn = tk.Button(root, text="Añadir Nuevo Pedido", font=("Arial", 20), command=lambda: opcion2(cursor))
    add_order_btn.pack(pady=20)
    
    # Option 3: Show table contents
    show_tables_btn = tk.Button(root, text="Mostrar Stock", font=("Arial", 20) ,command=lambda: opcion3(cursor))
    show_tables_btn.pack(pady=20)
    
    # Output Label to show results/errors
    global output_label
    output_label = tk.Label(root, text="", wraplength=400, font=("Arial", 20))
    output_label.pack(pady=20)



def menu_secundario(cursor,Cpedido,Ccliente,Fecha_pedido, Cproducto, Cantidad):
    #Menu secundario
    clear_window(root)

    # Etiqueta de título del menú secundario
    tk.Label(root, text="Gestionar Pedido", font=("Arial", 20)).pack(pady=10)
    
    # Campo para ID del producto
    tk.Label(root, text="Código del Producto:", font=("Arial", 15)).pack(pady=5)
    product_id_entry = tk.Entry(root, width=50, font=("Arial", 15))
    product_id_entry.pack(pady=5)

    # Campo para cantidad del producto
    tk.Label(root, text="Cantidad:", font=("Arial", 15)).pack(pady=5)
    quantity_entry = tk.Entry(root, width=50, font=("Arial", 15))
    quantity_entry.pack(pady=5)

     # Botón para añadir detalle de producto
    add_detail_btn = tk.Button(root, text="Añadir Detalle de Producto", font=("Arial", 15), 
                               command=lambda: Añadir_detalle(cursor, Cpedido, Ccliente, Fecha_pedido,Cproducto, Cantidad ))
    add_detail_btn.pack(pady=10)

    # Botón para eliminar detalles del producto
    delete_details_btn = tk.Button(root, text="Eliminar Detalles del Producto", font=("Arial", 15), 
                                   command=lambda: Eliminar_detalles(cursor, Cpedido, Ccliente, Fecha_pedido,Cproducto, Cantidad ))
    delete_details_btn.pack(pady=10)

    # Botón para cancelar el pedido
    cancel_order_btn = tk.Button(root, text="Cancelar Pedido", font=("Arial", 15), 
                                 command=lambda: Cancelar_pedido(cursor, Cpedido, Ccliente, Fecha_pedido,Cproducto, Cantidad ))
    cancel_order_btn.pack(pady=10)

    # Botón para finalizar el pedido
    finalize_order_btn = tk.Button(root, text="Finalizar Pedido", font=("Arial", 15), 
                                   command=lambda: Finalizar_pedido(cursor))
    finalize_order_btn.pack(pady=10)

    global output_label_secundario
    output_label_secundario = tk.Label(root, text="", wraplength=400, font=("Arial", 20))
    output_label_secundario.pack(pady=20)




# Main GUI setup
def create_gui(cursor):
    # Create the main window
    global root
    root = tk.Tk()
    root.geometry('800x700')
    root.title("Database Management")

    menu_principal(cursor)
    
    # Start the GUI event loop
    root.mainloop()


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
        create_gui(cursor)
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

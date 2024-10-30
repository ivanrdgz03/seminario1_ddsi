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

gui = True

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
        if gui:
            output_label.configure(text="Error reading the file: " + errorArchivo.args[0])
        else:
            print("Error reading the file: ", errorArchivo.args[0])
    finally:
        file.close()
    return [user, password, dsn]
#Función para obtener las instrucciones de creación de la tabla del archivo "create_table.sql", 
# estas instrucciones deben tener cada una al final ";" obligatoriamente.
def get_create_table_query(cursor):
    try:
        directorio = os.path.dirname(__file__)
        archivo = os.path.join(directorio, 'create_tables.sql')
        with open(archivo, 'r') as file:
            sql_script = file.read()
            
        sql_commands = sql_script.split(';')
        
        for command in sql_commands:
            cursor.execute(command)
            
    except FileNotFoundError as errorArchivo:
        if gui:
            output_label.configure(text="Error reading the file: " + errorArchivo.args[0])
        else:
            print("Error reading the file: ", errorArchivo.args[0])
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
    if gui:
        output_label.configure(text="Eliminando tablas...")
    else:
        print("Eliminando tablas...")
    cursor.execute("DROP TABLE Detalle_Pedido CASCADE CONSTRAINTS")
    cursor.execute("DROP TABLE Pedido CASCADE CONSTRAINTS")
    cursor.execute("DROP TABLE Stock CASCADE CONSTRAINTS")
    
    # Crear de nuevo las tablas
    if gui:
        output_label.configure(text="Creando tablas...")
    else:
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
    if gui:
        output_label.configure(text="Insertando datos predefinidos en Stock...")
    else:
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
    if gui:
        output_label.configure(text="Tablas creadas y datos insertados correctamente.")
    else:
        print("Tablas creadas y datos insertados correctamente.")

def opcion2(cursor):
    if(gui):
        Cpedido = int(order_id_entry.get())
        Ccliente = int(client_id_entry.get())
        fecha = order_date_entry.get()
    else:
        Cpedido= int(input("Codigo del pedido: "))
        Ccliente = int(input("Codigo del cliente: "))
        fecha = input("Introduce una fecha (formato dd/mm/aaaa): ")
    if Cpedido <0:
        if gui:
            output_label.config(text="Codigo de pedido incorrecto")
        else:
            print("Codigo de pedido incorrecto")
        return
    if Ccliente <0:
        if gui:
            output_label.config(text="Codigo de cliente incorrecto")
        else:
            print("Codigo de cliente incorrecto")
        return
    try:
        fecha2 = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        if gui:
            output_label.config(text="Formato de fecha incorrecto")
        else:
            print("Formato de fecha incorrecto")
        return
    cursor.execute("SELECT * FROM Pedido WHERE Cpedido = :Cpedido", {"Cpedido": Cpedido})
    if cursor.fetchone() != None:
        if gui:
            output_label.config(text="Codigo de pedido ya existente")
        else:
            print("Codigo de pedido ya existente")
        return
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
    if gui:
        menu_secundario(cursor,Cpedido,Ccliente,Fecha_pedido, Cproducto, Cantidad)
    else:
        menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)
    

#Función para mostrar el contenido de todas las tablas: Stock, Pedido, y Detalle_Pedido.

def opcion3(cursor):
<<<<<<< Updated upstream
<<<<<<< HEAD
    output_label.config(text="Pendiente de implementar.")
=======
    tablas = ["Stock", "Pedido", "Detalle_Pedido"]
    for tabla in tablas:
        print(f"\nContenido de la tabla {tabla}:")
        cursor.execute(f"SELECT * FROM {tabla}")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                if(len(row) == 3 and isinstance(row[2], datetime)):
                    print(f"({row[0]}, {row[1]}, {row[2].strftime('%d/%m/%Y')})")
                else:
                    print(row)
        else:
            print("La tabla está vacía.")

>>>>>>> main
=======
    # Lista de tablas a mostrar
    tablas = ["Stock", "Pedido", "Detalle_Pedido"]
    if(gui):
        # Crea una nueva ventana para mostrar las tablas
        ventana_tablas = tk.Toplevel(root)
        ventana_tablas.geometry('1200x600')
        ventana_tablas.title("Contenido de las Tablas")

        # Recorre cada tabla y muestra su contenido
        for tabla_index, tabla in enumerate(tablas):
            tk.Label(ventana_tablas, text=f"Contenido de la tabla {tabla}:  ", font=("Arial", 14, "bold")).grid(row=0, column=tabla_index*3, columnspan=3, pady=10)

            # Ejecuta la consulta para obtener los datos de la tabla actual
            cursor.execute(f"SELECT * FROM {tabla}")
            rows = cursor.fetchall()
            
            # Si hay filas, las muestra en una cuadrícula, si no, muestra un mensaje de vacío
            if rows:
                # Añade los encabezados de columnas
                columns = [desc[0] for desc in cursor.description]
                for col_index, column_name in enumerate(columns):
                    tk.Label(ventana_tablas, text=column_name, font=("Arial", 12, "bold")).grid(row=1, column=tabla_index*3 + col_index, padx=5, pady=5)

                # Muestra los datos en la cuadrícula
                for row_index, row in enumerate(rows, start=2):
                    for col_index, cell in enumerate(row):
                        # Formatea las fechas en el formato deseado
                        if isinstance(cell, datetime):
                            cell_text = cell.strftime('%d/%m/%Y')
                        else:
                            cell_text = str(cell)
                        
                        tk.Label(ventana_tablas, text=cell_text, font=("Arial", 10)).grid(row=row_index, column=tabla_index*3 + col_index, padx=5, pady=5)
            else:
                # Muestra un mensaje indicando que la tabla está vacía
                tk.Label(ventana_tablas, text="La tabla está vacía.", font=("Arial", 10, "italic")).grid(row=1, column=tabla_index*3, columnspan=3, pady=10)
    else:
        for tabla in tablas:
            print(f"\nContenido de la tabla {tabla}:")
            cursor.execute(f"SELECT * FROM {tabla}")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    if(len(row) == 3 and isinstance(row[2], datetime)):
                        print(f"({row[0]}, {row[1]}, {row[2].strftime('%d/%m/%Y')})")
                    else:
                        print(row)
            else:
                print("La tabla está vacía.")
>>>>>>> Stashed changes

    
def opcion4(cursor):
    return


def Añadir_detalle(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    if gui:
        Cproducto = int(product_id_entry.get())
        Cantidad = int(quantity_entry.get())
    else:
        Cproducto = int(input("Codigo del producto: "))
        Cantidad = int(input("Cantidad del producto: "))
    cursor.execute("SELECT Cantidad FROM Stock WHERE Cproducto = :Cproducto", {"Cproducto": Cproducto})
    resultado = cursor.fetchone()
    if resultado != None:
        Cantidad_disponible = resultado[0]
    else:
        if gui:
            output_label_secundario.config(text="Codigo de producto incorrecto")
        else:
            print("Codigo de producto incorrecto")
        return
    if Cantidad > Cantidad_disponible or Cantidad <=0:
        if gui:
            output_label_secundario.config(text="Cantidad del producto incorrecta")
            return
        else:
            while Cantidad > Cantidad_disponible:
                Cantidad = int(input("Cantidad invalida, introduzcala de nuevo: "))
        
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
    if gui:
        output_label_secundario.config(text="Detalle añadido correctamente")
    else:
        print("Detalle añadido correctamente")
        menu_opcion2(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad)

def Eliminar_detalles(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    cursor.execute("""SELECT * FROM Detalle_Pedido WHERE Cpedido = :Cpedido""", {"Cpedido": Cpedido})
    if cursor.fetchone() == None:
        if gui:
            output_label_secundario.config(text="No hay detalles que eliminar")
        else:
            print("No hay detalles que eliminar")
        return
    cursor.execute("""SELECT Cproducto, Cantidad FROM Detalle_Pedido WHERE Cpedido = :Cpedido""", {"Cpedido": Cpedido})
    data = cursor.fetchall()
    Cantidad = data[0][1]
    Cproducto = data[0][0]
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
    
    if gui:
        output_label_secundario.config(text="Detalles eliminados correctamente")
    else:
        print("Detalles eliminados correctamente")
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
    if gui:
        menu_principal(cursor)
    else:
        menu(cursor)

def Finalizar_pedido(cursor,Cpedido,Ccliente,Fecha_pedido,Cproducto,Cantidad):
    cursor.connection.commit()
    if(not gui):
        menu(cursor)
    else:
        root.destroy()

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
    global product_id_entry, quantity_entry
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
                                   command=lambda: Finalizar_pedido(cursor, Cpedido, Ccliente, Fecha_pedido,Cproducto, Cantidad ))
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
    if(not gui):
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
    global gui
    try:
        if(len(sys.argv) == 2 and sys.argv[1] == "--no-gui"):
            gui = False
        user, password, dsn = get_credentials()
        conexion = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = conexion.cursor()
        # Solicitudes y resto de codigo aquí
        if(gui):
            create_gui(cursor)
        else:
            menu(cursor)  
    except oracledb.DatabaseError as errorBD:   #Error al establecer la conexión de la base de datos
        error = errorBD.args[0]
        if(gui):
            output_label.config(text="Error connecting to the database: " + error.message)
            output_label.config(text="Error code: " + error.code)
        else:
            print("Error connecting to the database: ", error.message)
            print("Error code: ", error.code)
        cursor.connection.rollback()
    except KeyboardInterrupt:   #Si hacemos control + c
        if(gui):
            output_label.config(text="Saliendo con Ctrl+C...")
        else:
            print("\nSaliendo con Ctrl+C...")
        cursor.connection.rollback()
    except Exception as otroError:  #Otro tipo de error
        if(gui):
            output_label.config(text="Another error: " + otroError.args[0])
        else:
            print("Another error: ", otroError.args[0])
        cursor.connection.rollback()
    finally:    #Al final, pase lo que pase se cierran el cursor y la conexión
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()

import oracledb;

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

def main():
    try: 
        user, password, dsn = get_credentials()
        con = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = con.cursor()
        # Solicitudes y resto de codigo aquí
    except oracledb.DatabaseError as errorBD:   #Error al establecer la conexión de la base de datos
        error = errorBD.args[0]
        print("Error connecting to the database: ", error.message)
        print("Error code: ", error.code)
    except Exception as otroError:  #Otro tipo de error
        print("Another error: ", otroError)
    finally:    #Al final, pase lo que pase se cierran el cursor y la conexión
        cursor.close()
        con.close()

if __name__ == "__main__":
    main()
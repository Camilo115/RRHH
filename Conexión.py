import mysql.connector

class Conexion:

    # Declaración de variables.
    mydb = ""
    host = ""
    user = ""
    password = ""
    database = ""

    # Función __init__ para inicializar Base de datos.
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        # Conexión a Base de datos.
        self.mydb = mysql.connector.connect(host=self.host, user=self.user,
                                     password=self.password, database=self.database)


    # Esta función nos permite conocer, si la conexión a Base de datos, resultó ser exitosa.
    def getEstado(self):
        if self.mydb:
            print("conexión exitosa")
        else:
            print("problemas de conexión")
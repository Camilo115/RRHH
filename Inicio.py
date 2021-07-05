from Conexión import Conexion
from itertools import cycle
import re

#Declaración de variables.
mycursor = ""

#Conexión a Base de datos
bbdd = Conexion("localhost", "root", "", "recursos_humanos")
bbdd.getEstado()

#Instaciando cursor para recorrer Base de datos.
mycursor = bbdd.mydb.cursor()

#Mostrar todos los elementos de Base de datos.
#mycursor.execute("SELECT * FROM empleado")
#myresult = mycursor.fetchall()
#for x in myresult:
#  print(x)

# Esta función verifica si el Rut ingresado al sistema es válido.
def validarRut(rut):
    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    try:
       s = sum(d * f for d, f in zip(revertido, factors))
       res = (-s) % 11
       if str(res) == dv:
           return True
       elif dv == "K" and res == 10:
           return True
       else:
           return False
    except:
       print("Problemas al verificar RUT")


# Esta función se encarga de verificar, que no existan caracteres especiales, en un texto en particular.
def check_splcharacter(test):
    # Make an RE character set and pass
    # this as an argument in compile function

    string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    # Pass the string in search function
    # of RE object (string_check).

    if (string_check.search(test) == None):
        return False
    else:
        return True

# Esta función verifica si el texto ingresado, contiene algún dígito.
def validarNA(texto):
    i = 0
    while(i<len(texto)):
     # print(texto[i],"",texto[i].isdigit())
      if (texto[i].isdigit()==True):
        return True
      i+=1

# Esta función se encarga de verificar, si un telefono no contiene letras.
def validarTel(num):
    i=0
    while(i<len(num)):
        if(num[i].isalpha==True):
            return True
        i+=1

# Esta función, agrupa las dos funciones encargadas de verificar texto.
def validarTexto(texto):
    return validarNA(texto)==True or check_splcharacter(texto)==True

# Como su nombre lo indica, esta función se encarga de validar, si el correo electrónico ingresado es válido.
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

#Ejecución de CRUD

op = int(input("Ingrese el número de la operación a realizar:\n 1-Crear \n 2-Leer"
                "\n 3-Actualizar \n 4-Borrar \n 5-Salir \n Ingrese su opción: "))
print("\n")

while op != 5:
    if op == 1:
        print("Crear registro")
        print("Ingrese información \n")

        #Ingreso de RUT
        rut = input("Ingrese RUT: ")
        while validarRut(rut)!=True:
            rut = input("Ingrese RUT nuevamente: ")

        #Ingreso de Nombre
        nombre = input("Ingrese nombre: ")
        while(validarTexto(nombre)):
            nombre = input("Ingrese nombre nuevamente: ")
        s_nombre = input("Ingrese segundo nombre: ")

        #Ingreso de Segundo Nombre
        while (validarTexto(s_nombre)):
            s_nombre = input("Ingrese nombre nuevamente: ")
        apellido_p = input("Ingrese apellido paterno: ")

        #Ingreso de Apellido Paterno
        while (validarTexto(apellido_p)):
            apellido_p = input("Ingrese apellido paterno nuevamente: ")
        apellido_m = input("Ingrese apellido materno: ")

        #Ingreso de Apellido Materno
        while (validarTexto(apellido_m)):
            apellido_m = input("Ingrese apellido materno nuevamente: ")

        #Ingreso de Número de telefono
        num_telef = input("Ingrese número de teléfono: ")
        while(len(num_telef)<5 or len(num_telef)>13 or validarTel(num_telef)):
            num_telef = input("Ingrese número de teléfono nuevamente: ")

        #Ingreso de Correo electrónico
        correo = input("Ingrese correo: ")
        while (es_correo_valido(correo) != True):
            correo = input("Ingrese correo nuevamente")

        #Ingreso de dirección
        direccion = input("Ingrese dirección: ")
        while (direccion == ""):
            direccion = input("Ingrese dirección nuevamente")

        #Realizando sentencia SQL, para ingresar datos a Base de datos MySQL
        try:
            sql ="INSERT INTO empleado (rut , nombre, s_nombre, apellido_p, apellido_m, num_telef, correo, direccion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (rut, nombre, s_nombre, apellido_p, apellido_m, num_telef, correo, direccion)
            mycursor.execute(sql, val)
            bbdd.mydb.commit()
            print("Sentencia SQL ejecutada con éxito\n")
        except Exception as e:
            print(e)
            bbdd.mydb.rollback()
            bbdd.mydb.close()
        bbdd.mydb.rollback()
        bbdd.mydb.close()

        #Muestra de valores ingresados por pantalla
        print("Nombre:",nombre,"\nSegundo Nombre:",s_nombre,"\nApellido paterno:",apellido_p,"\nApellido materno:",apellido_m,
              "\nNúmero de teléfono:",num_telef,"\nCorreo:",correo,"\nDirección:",direccion,"\n")

    elif op == 2:
        print("Leer registros")
        mycursor.execute("SELECT * FROM empleado")
        myresult = mycursor.fetchall()
        for x in myresult:
          print(x)
        print("\n")
    elif op == 3:
        print("Actualizar registro")
        id = int(input("Ingrese id de empleado"))
        print("Ingrese información: \n")

        # Ingreso de RUT
        rut = input("Ingrese RUT: ")
        if(bool(rut)==False):
            rut = ""
        else:
            while validarRut(rut) != True:
                rut = input("Ingrese RUT nuevamente: ")

        # Ingreso de Nombre
        nombre = input("Ingrese nombre: ")
        if(bool(nombre)==False):
            nombre = ""
        else:
            while (validarTexto(nombre)):
                nombre = input("Ingrese nombre nuevamente: ")

        # Ingreso de Segundo Nombre
        s_nombre = input("Ingrese segundo nombre: ")
        if(bool(s_nombre)==False):
            s_nombre = ""
        else:
            while (validarTexto(s_nombre)):
                s_nombre = input("Ingrese nombre nuevamente: ")

        # Ingreso de Apellido Paterno
        apellido_p = input("Ingrese apellido paterno: ")
        if (bool(apellido_p)==False):
            apellido_p = ""
        else:
            while (validarTexto(apellido_p)):
                apellido_p = input("Ingrese apellido paterno nuevamente: ")

        # Ingreso de Apellido Materno
        apellido_m = input("Ingrese apellido materno: ")
        if(bool(apellido_m)==False):
            apellido_m = ""
        else:
            while (validarTexto(apellido_m)):
                apellido_m = input("Ingrese apellido materno nuevamente: ")

        # Ingreso de Número de telefono
        num_telef = input("Ingrese número de teléfono: ")
        if(bool(num_telef)==False):
            num_telef = ""
        else:
            while (len(num_telef) < 5 or len(num_telef) > 13 or validarTel(num_telef)):
                num_telef = input("Ingrese número de teléfono nuevamente: ")

        # Ingreso de Correo electrónico
        correo = input("Ingrese correo: ")
        if(bool(correo)==False):
            correo = ""
        else:
            while (es_correo_valido(correo) != True):
                correo = input("Ingrese correo nuevamente: ")

        # Ingreso de dirección
        direccion = input("Ingrese dirección: ")
        if(bool(direccion)==False):
            direccion = ""

        # Verificación de la información
        select = "SELECT * FROM empleado WHERE id_empleado = %s"
        val_select = (id,)
        mycursor.execute(select, val_select)
        myresult = mycursor.fetchall()

        """ En caso de que no se ingrese nueva infomación, se reemplaza la variable, con el dato alojado en la Base de Datos,
        ingresado con anterioridad."""
        for x in myresult:
          if (bool(rut)==False):
                rut = x[1]
          if (bool(nombre) == False):
                nombre = x[2]
          if (bool(s_nombre) == False):
                s_nombre = x[3]
          if (bool(apellido_p) == False):
                apellido_p = x[4]
          if (bool(apellido_m) == False):
                apellido_m = x[5]
          if (bool(num_telef) == False):
                num_telef = x[6]
          if (bool(correo) == False):
                correo = x[7]
          if (bool(direccion) == False):
                direccion = x[8]

        # Realizando sentencia SQL, para ingresar datos a Base de datos MySQL
        try:
            sql = "UPDATE empleado SET rut = %s , nombre = %s, s_nombre = %s, apellido_p = %s, apellido_m = %s, num_telef = %s, correo = %s, direccion = %s WHERE id_empleado = %s"
            val = (rut, nombre, s_nombre, apellido_p, apellido_m, num_telef, correo, direccion, id,)
            mycursor.execute(sql, val)
            bbdd.mydb.commit()
            print("Sentencia SQL ejecutada con éxito\n")
        except Exception as e:
            print(e)
            bbdd.mydb.rollback()
            bbdd.mydb.close()
        bbdd.mydb.rollback()
        bbdd.mydb.close()

        # Muestra de valores ingresados por pantalla
        print("Nombre:", nombre, "\nSegundo Nombre:", s_nombre, "\nApellido paterno:", apellido_p,
              "\nApellido materno:", apellido_m,
              "\nNúmero de teléfono:", num_telef, "\nCorreo:", correo, "\nDirección:", direccion, "\n")
    elif op == 4:
        print("Borrar registro")
        id = int(input("Ingrese el id del empleado que sea eliminar: "))
        if bool(id)==False:
            print("No ha ingresado nada")
        else:
            try:
                sql = "DELETE FROM empleado WHERE id_empleado = %s"
                val = (id,)
                mycursor.execute(sql, val)
                bbdd.mydb.commit()
            except Exception as e:
                print(e)
                bbdd.mydb.rollback()
                bbdd.mydb.close()
    else:
        print("Por favor ingrese un opción correcta :")

    op = int(input("Ingrese el número de la operación a realizar:\n 1-Crear \n 2-Leer"
                   "\n 3-Actualizar \n 4-Borrar \n 5-Salir \n Ingrese su opción: "))



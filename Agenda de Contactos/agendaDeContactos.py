import json
import os

VER = 1
BUSCAR = 2
AGREGAR = 3
EDITAR = 4
ELIMINAR = 5
GUARDAR = 6
SALIR = 7

def cargarDatos():
    if os.path.exists("listaContactos.json"):
        with open("listaContactos.json", "r") as archivo:
            contactos = json.load(archivo)
            return contactos
    else: return []

def menuPrincipal():
    while True:
        print("\n1. Ver contactos")
        print("2. Buscar contacto")
        print("3. Agregar contacto")
        print("4. Editar contacto")
        print("5. Eliminar contacto")
        print("6. Guardar")
        print("7. Salir")
        try:
            opc = int(input("Elige una opción: "))
            if opc >= 1 and opc <= 7:
                return opc
            else: print("Opcion fuera de rango")
        except ValueError:
            print("Ingresa una opcion valida")

def obtenerNuevoID():
    if not contactos:
        return 1
    return contactos[-1]["id"] + 1

def reorganizarIDs(contactos):
    contador = 1
    for contacto in contactos:
        contacto["id"] = contador
        contador += 1
    return contactos

def validarTelefono(tel):
    while True:
        if tel.isdigit() and len(tel) == 10:
            return tel
        else:        
            print("Telefono no valido, ingresa un numero de 10 digitos")
            tel = input("Telefono: ")

def validarCorreo(correo):
    while True:
        if "@" in correo and "." in correo:
            return correo
        else:
            print("Correo no valido, ingresa un correo con formato valido")
            correo = input("Correo: ")
    
def agregarContacto():
    nombre = input("Nombre: ")
    telefono = validarTelefono(input("Telefono: "))
    email = validarCorreo(input("Correo: "))
    contacto = {
        "id": obtenerNuevoID(),
        "nombre": nombre,
        "telefono": telefono,
        "email": email,
    }
    contactos.append(contacto)

def verContactos():
    if not contactos:
        print("No hay contactos registrados")
        return
    for contacto in contactos:
        print(f'{contacto["id"]} - {contacto["nombre"]} - {contacto["telefono"]} - {contacto["email"]}')
    
def buscarContactos():
    if not contactos:
        print("No hay contactos registrados")
        return
    busqueda = input("Escribe el contacto a buscar: ")
    seEncontro = False
    for contacto in contactos:
        if busqueda.lower() in contacto["nombre"].lower():
            seEncontro = True
            print(f'{contacto["id"]} - {contacto["nombre"]} - {contacto["telefono"]} - {contacto["email"]}')
    if not seEncontro:
        print("No se encontraron coincidencias")

def pedirID():
    if not contactos:
        print("No hay contactos registrados")
        return
    while True:
        try:
            id = int(input("Ingresa el ID: "))
        except ValueError:
            print("Ingresa un ID valido")
        else:
            for contacto in contactos:
                if id == contacto["id"]:
                    return id
                else:
                    continue
            print("No se encontraron coincidencias")
    
def editarContacto():
    id = pedirID()
    if not id:
        return
    for contacto in contactos:
        if id == contacto["id"]:
            while True:
                print("1. Nombre")
                print("2. Telefono")
                print("3. Correo")
                try:
                    opc = int(input("Elige que quieres editar: "))
                except ValueError:
                    print("Ingresa un numero valido")
                else:
                    if opc == 1:
                        nombre = input("Ingresa el nuevo nombre: ")
                        contacto["nombre"] = nombre
                    elif opc == 2:
                        telefono = validarTelefono(input("Ingresa el nuevo telefono: "))
                        contacto["telefono"] = telefono
                    elif opc == 3:
                        correo = validarCorreo(input("Ingresa el nuevo correo: "))
                        contacto["email"] = correo
                    else:
                        print("Opcion fuera de rango")
                        continue
                    return
                
def eliminarContacto():
    id = pedirID()
    for contacto in contactos:
        if id == contacto["id"]:
            confirmar = input(f'Estas seguro de eliminar el contacto {contacto["nombre"]} si/ no: ')
            if "si" in confirmar.lower():
                contactos.remove(contacto)
                print("El contacto fue eliminado exitosamente")
            else:
                print("Cancelado por el usuario!")
            return

def guardarContactos():
    with open ("listaContactos.json", "w") as archivo:
        json.dump(contactos, archivo)

def ordenarContactos(contactos):
    contactosOrdenados = reorganizarIDs(sorted(contactos, key=lambda x: x['nombre']))
    return contactosOrdenados

contactos = cargarDatos()
opc = 0
while opc != SALIR:
    opc = menuPrincipal()
    print()
    if opc == VER:
        print("VER CONTACTOS\n")
        verContactos()
    elif opc == BUSCAR:
        print("BUSCAR CONTACTO\n")
        buscarContactos()
    elif opc == AGREGAR:
        print("AGREGAR CONTACTO\n")
        agregarContacto()
    elif opc == EDITAR:
        print("EDITAR CONTACTO\n")
        editarContacto()
    elif opc == ELIMINAR:
        print("ELIMINAR CONTACTO\n")
        eliminarContacto()
    elif opc == GUARDAR:
        guardarContactos()
        print("\nSe guardaron los datos correctamente!")
    elif opc == SALIR:
        guardarContactos()
    
    if opc >= AGREGAR and opc <= ELIMINAR:
        contactos = ordenarContactos(contactos)
        guardarContactos()
import json
import os

ARCHIVO_USUARIOS = "usuarios.json"

REGISTRARSE = 1
INICIAR_SESION = 2
SALIR = 3

CAMBIAR_NOMBRE_USUARIO = 1
CAMBIAR_CONTRASEÑA = 2

VER_USUARIOS = 1
CAMBIAR_ROL = 2
CAMBIAR_ESTADO = 3
ELIMINAR_USUARIO = 4
CERRAR_SESION = 5

def cargarUsuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as archivo:
            usuarios = json.load(archivo)
            return usuarios
    else:
        usuarios = [
            {
                "id": 1,
                "username": "admin",
                "password": "admin",
                "role": "admin",
                "estado": "activo"
            }
        ]
        guardarUsuarios(usuarios)
        return usuarios
    
def guardarUsuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

def menuPrincipal():
    print("MENU PRINCIPAL\n")
    while True:
        print("1. Registrarse")
        print("2. Iniciar Sesion")
        print("3. Salir")
        try:
            opc = int(input("Elige una opcion: "))
        except ValueError:
            print("Ingresa una opcion valida")
        else:
            if opc < 1 or opc > 3:
                print("Opcion fuera de rango")
            else: return opc

def obtenerNuevoID(lista):
    if not lista:
        return 1
    return lista[-1]["id"] + 1

def registrarUsuario(usuarios):
    print("REGISTRO DE USUARIO\n")
    print("Escribe 0 para cancelar")
    while True:
        estaRepetido = False
        print()
        username = input("Escribe un nombre de usuario nuevo: ")
        print()
        if username == "0":
            print("Se ha cancelado el registro!")
            return
        if username == "":
            print("No puedes crear un usuario vacio")
            continue
        for usuario in usuarios:
            if username.lower() == usuario["username"].lower():
                print("El usuario ya ha sido registrado anteriormente")
                estaRepetido = True
                break
        if not estaRepetido:   
            while True:
                password = input("Escribe una contraseña: ")
                if len(password) < 4:
                    print("\nLa contraseña tiene que tener al menos 4 caracteres!\n")
                    continue
                confpassword = input("Confirma tu contraseña: ")
                print()
                if confpassword != password:
                    print("Las contraseñas no coinciden\n")
                else:
                    usuario = {
                        "id": obtenerNuevoID(usuarios),
                        "username": username.strip(),
                        "password": password,
                        "role": "user",
                        "estado": "activo"
                    }
                    usuarios.append(usuario)
                    guardarUsuarios(usuarios)
                    print("Se registró el usuario con exito!")
                    return usuarios
                
def iniciarSesion(usuarios):
    print("INICIO DE SESION\n")
    print("Escribe 0 para cancelar")
    username = input("Ingresa tu nombre de usuario: ")
    if username == "0":
        return
    seEncontro = False
    for usuario in usuarios:
        if username.lower() == usuario["username"].lower():
            seEncontro = True
            intentos = 0
            if usuario["estado"] != "activo":
                print("El usuario no esta activo!")
                return None
            while intentos < 3:
                password = input("Ingresa tu contraseña (0 para cancelar): ")
                if password == "0":
                    return None
                if password == usuario["password"]:
                    print("Haz iniciado sesion con exito!")
                    return usuario
                else:
                    intentos+=1
                    print(f"La contraseña es incorrecta! (Intentos restantes: {3-intentos})")
                    continue
            print("Haz excedido el maximo de intentos")
            usuario["estado"] = "bloqueado"
            guardarUsuarios(usuarios)
            return None
    if not seEncontro:
        print(f'El usuario "{username}" no existe')
        return None
    
def menuUsuario():
    print("MENU USUARIO\n")
    while True:
        print("1. Cambiar nombre de usuario")
        print("2. Cambiar contraseña")
        print("3. Cerrar sesion")
        try:
            opc = int(input("Elige una opcion: "))
        except ValueError:
            print("Ingresa una opcion valida")
        else:
            if opc < 1 or opc > 3:
                print("Opcion fuera de rango")
            else: return opc

def cambiarUsername(usuarioActual, usuarios):
    password = input("Ingresa tu contraseña: ")
    if password == usuarioActual["password"]:
        while True:
            nuevoUsername = input("Ingresa tu nuevo nombre de usuario (ingresa 0 para cancelar): ")
            nuevoUsername = nuevoUsername.strip()

            if nuevoUsername == "0":
                return
            
            if nuevoUsername == "":
                print("El nombre de usuario no puede estar vacio")
                continue

            seRegistro = False
            for usuario in usuarios:
                if nuevoUsername.lower() == usuario["username"].lower():
                    seRegistro = True
                    print("El usuario ya ha sido registrado anteriormente!")
                    break

            if not seRegistro:
                usuarioActual["username"] = nuevoUsername
                guardarUsuarios(usuarios)
                print("Se cambio el nombre de usuario exitosamente!")
                return
    else:
        print("Contraseña incorrecta")

def cambiarPassword(usuarioActual, usuarios):
    password = input("Ingresa tu contraseña: ")
    if password == usuarioActual["password"]:
        while True:
            nuevaPassword = input("Ingresa tu nueva contraseña (ingresa 0 para salir): ")
            nuevaPassword = nuevaPassword.strip()

            if nuevaPassword == "0":
                return
            
            if nuevaPassword == "":
                print("La contraseña no puede estar vacía")
                continue

            if len(nuevaPassword) < 4:
                print("\nLa contraseña tiene que tener al menos 4 caracteres!\n")
                continue
            confNuevaPassword = input("Confirma tu contraseña: ")
            print()
            if confNuevaPassword != nuevaPassword:
                print("Las contraseñas no coinciden\n")
            else:
                usuarioActual["password"] = nuevaPassword
                guardarUsuarios(usuarios)
                print("Se cambio la contraseña exitosamente!")
                return
    else:
        print("Contraseña incorrecta")

def menuAdmin():
    print("MENU ADMINISTRADORES\n")
    while True:
        print("1. Ver usuarios")
        print("2. Cambiar rol")
        print("3. Cambiar estado")
        print("4. Eliminar usuario")
        print("5. Cerrar sesion")
        try:
            opc = int(input("Elige una opcion: "))
        except ValueError:
            print("Opcion no valida")
        else:
            if opc < 1 or opc > 5:
                print("Opcion fuera de rango")
            else:
                return opc
            
def verUsuarios(usuarios):
    print("MOSTRAR USUARIOS\n")
    if not usuarios:
        print("No hay usuarios por mostrar")
        return
    for usuario in usuarios:
        print(f'{usuario["id"]} - {usuario["username"]} - {usuario["role"]} - {usuario["estado"]}')

def cambiarRol(usuarios):
    print("CAMBIAR ROL\n")
    try:
        id = int(input("Ingresa el ID del usuario: "))
    except ValueError:
        print("ID invalido")
        return
    if id == 1:
        print("No se permite cambiar el rol al admin principal!")
        return
    for usuario in usuarios:
        if id == usuario["id"]:
            while True:
                print(f'Rol actual: {usuario["role"]}')
                print("1. user")
                print("2. admin")
                print("0. Cancelar")

                try:
                    opc = int(input("Seleccione el nuevo rol (ingrese 0 para cancelar): "))
                except ValueError:
                    print("Opcion no valida")
                    continue
                    
                if opc == 0:
                    return
                elif opc == 1:
                    usuario["role"] = "user"
                elif opc == 2:
                    usuario["role"] = "admin"
                else:
                    print("Opcion fuera de rango")
                    continue
                
                guardarUsuarios(usuarios)
                print("Rol cambiado correctamente!")
                return

    print("No se encontraron coincidencias")                    

def cambiarEstado(usuarios):
    print("CAMBIAR ESTADO\n")
    try:
        id = int(input("Ingresa el ID del usuario: "))
    except ValueError:
        print("ID invalido")
        return
    if id == 1:
        print("No se permite cambiar el estado al admin principal!")
        return
    for usuario in usuarios:
        if id == usuario["id"]:
            while True:
                print(f'Estado actual: {usuario["estado"]}')
                print("1. activo")
                print("2. bloqueado")
                print("0. Cancelar")

                try:
                    opc = int(input("Seleccione el nuevo estado (ingrese 0 para cancelar): "))
                except ValueError:
                    print("Opcion no valida")
                    continue
                    
                if opc == 0:
                    return
                elif opc == 1:
                    usuario["estado"] = "activo"
                elif opc == 2:
                    usuario["estado"] = "bloqueado"
                else:
                    print("Opcion fuera de rango")
                    continue
                
                guardarUsuarios(usuarios)
                print("Estado cambiado correctamente!")
                return

    print("No se encontraron coincidencias")

def eliminarUsuario(usuarios):
    print("ELIMINAR USUARIO\n")
    try:
        id = int(input("Ingresa el ID del usuario: "))
    except ValueError:
        print("ID invalido")
        return
    if id == 1:
        print("No se permite eliminar al admin principal!")
        return
    for usuario in usuarios:
        if id == usuario["id"]:
            confirmacion = input(f'Estas seguro que quieres eliminar al usuario "{usuario["username"]}" (si/no): ')
            if "si" in confirmacion.lower():
                usuarios.remove(usuario)
                guardarUsuarios(usuarios)
                print("Se ha eliminado al usuario exitosamente!")
            else:
                print("Se cancelo la operacion!")
            return

    print("No se encontraron coincidencias")

def main():
    usuarios = cargarUsuarios()
    usuarioActual = None
    sistemaActivo = True

    while sistemaActivo:
        opc = menuPrincipal()
        if opc == REGISTRARSE:
            registrarUsuario(usuarios)
            guardarUsuarios(usuarios)

        elif opc == INICIAR_SESION:
            usuario = iniciarSesion(usuarios)
            if usuario:
                usuarioActual = usuario
                while usuarioActual != None:

                    if usuarioActual["role"] == "user":
                        opc2 = menuUsuario()
                        if opc2 == CAMBIAR_NOMBRE_USUARIO:
                            cambiarUsername(usuarioActual, usuarios)
                        elif opc2 == CAMBIAR_CONTRASEÑA:
                            cambiarPassword(usuarioActual, usuarios)
                        elif opc2 == SALIR:
                            usuarioActual = None
                            break
                        
                    if usuarioActual["role"] == "admin":
                        opc2 = menuAdmin()
                        if opc2 == VER_USUARIOS:
                            verUsuarios(usuarios)
                        elif opc2 == CAMBIAR_ROL:
                            cambiarRol(usuarios)
                        elif opc2 == CAMBIAR_ESTADO:
                            cambiarEstado(usuarios)
                        elif opc2 == ELIMINAR_USUARIO:
                            eliminarUsuario(usuarios)
                        elif opc2 == CERRAR_SESION:
                            usuarioActual = None
                            break

        elif opc == SALIR:
            guardarUsuarios(usuarios)
            sistemaActivo = False

main()
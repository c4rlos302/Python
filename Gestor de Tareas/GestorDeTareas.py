import json
import os

tareas = []
VER = 1
AGREGAR = 2
EDITAR = 3
MARCAR_COMPLETADO = 4
ELIMINAR = 5
GUARDAR = 6
SALIR = 7

def estaVacio():
    if not len(tareas):
        print("No hay ninguna tarea")
        return True
    else: return False

def cargarDatos():
    if os.path.exists("tareas.json"):
        with open("tareas.json", "r") as archivo:
            tareas = json.load(archivo)
            return tareas
    else: return []

def menuPrincipal():
    while True:
        try:
            print("\n1. Ver tareas \n"
                "2. Agregar tarea \n"
                "3. Editar tarea \n"
                "4. Marcar tarea como completada \n"
                "5. Eliminar tarea \n"
                "6. Guardar Cambios \n"
                "7. Salir")
            opc = int(input("Elige una opcion: "))
            if opc < 1 or opc > 7:
                print("Opcion fuera de rango")
            else:
                return opc
        except ValueError:
            print("Opcion no valida")

def obtenerNuevoID():
    if not tareas:
        return 1
    return tareas[-1]["id"] + 1

def reorganizarIDs():
    contador = 1
    for tarea in tareas:
        tarea["id"] = contador
        contador += 1

def agregarTarea():
    titulo = input("Ingresa el titulo de la tarea: ")
    descripcion = input("Ingresa la descripcion de la tarea: ")
    tarea = {
        "id": obtenerNuevoID(),
        "titulo": titulo,
        "descripcion": descripcion,
        "completada": False
        }
    tareas.append(tarea)
    guardarArchivo()

def verTareas():
    if estaVacio():
        return
    for tarea in tareas:
        print(f'[{"X" if tarea["completada"] else " "}] {tarea["id"]} - {tarea["titulo"]}')

def pedirID():
    if not len(tareas):
        print("No hay ninguna tarea")
        return
    while True:
        try:
            id = int(input("Ingresa el id de la tarea: "))
        except ValueError:
            print("ID no valido")
        else:
            for tarea in tareas:
                if id == tarea["id"]:
                    return id
                else:
                    print("No se encontraron coincidencias")
                    continue


def editarTarea():
    id = pedirID()
    if not id:
        return
    for tarea in tareas:
        if id == tarea["id"]:
            print(f'1. Titulo: {tarea["titulo"]}')
            print(f'2. Descripcion: {tarea["descripcion"]}')
            try:
                opc = int(input("Elige que quieres modificar: "))
                if opc == 1:
                    titulo = input("Ingresa el nuevo titulo: ")
                    tarea["titulo"] = titulo
                    guardarArchivo()
                    print("Se cambio el titulo exitosamente")
                elif opc == 2:
                    descripcion = input("Ingresa la nueva descripcion: ")
                    tarea["descripcion"] = descripcion
                    guardarArchivo()
                    print("Se cambio la descripcion exitosamente")
                else:
                    print("Opcion fuera de rango")
            except ValueError:
                print("Opcion no valida")

def marcarCompletada():
    id = pedirID()
    if not id:
        return
    for tarea in tareas:
        if id == tarea["id"]:
            tarea["completada"] = True
            guardarArchivo()
            print("Se completo con exito!")

def eliminarTarea():
    id = pedirID()
    if not id:
        return
    for tarea in tareas:
        if id == tarea["id"]:
            tareas.remove(tarea)
            reorganizarIDs()
            guardarArchivo()
            print("Se elimino la tarea correctamente")

def guardarArchivo():
    with open("tareas.json", "w") as archivo:
        json.dump(tareas, archivo)

tareas = cargarDatos()
opc = 0
while opc != SALIR:
    opc = menuPrincipal()
    print()
    if(opc == VER):
        print("Tareas: \n")
        verTareas()
    elif(opc == AGREGAR):
        print("AGREGAR TAREA: \n")
        agregarTarea()
    elif(opc == EDITAR):
        print("EDITAR TAREA: \n")
        editarTarea()
    elif(opc == MARCAR_COMPLETADO):
        print("MARCAR COMO COMPLETADO: \n")
        marcarCompletada()
    elif(opc == ELIMINAR):
        print("ELIMINAR TAREA: \n")
        eliminarTarea()
    elif(opc == GUARDAR):
        guardarArchivo()
        print("Se guardaron los datos correctamente")
    elif(opc == SALIR):
        guardarArchivo()
import json
import os

ARCHIVO_PRODUCTOS = "inventario.json"

REGISTRAR = 1
VER = 2 
BUSCAR = 3
ACTUALIZAR = 4
ELIMINAR = 5
PRODUCTOS_AGOTADOS = 6
SALIR = 7

def cargarInventario():
    if os.path.exists(ARCHIVO_PRODUCTOS):
        with open(ARCHIVO_PRODUCTOS, "r") as archivo:
            productos = json.load(archivo)
            return productos
    else: return []

def guardarInventario(productos):
    with open(ARCHIVO_PRODUCTOS, "w") as archivo:
        json.dump(productos, archivo, indent=4)

def menu():
    print("MENU\n")
    while True:
        print("1. Registrar producto")
        print("2. Ver productos")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Productos agotados")
        print("7. Salir")
        try:
            opc = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Opcion invalida. Intente de nuevo")
            continue
        if opc in range(1, 7):
            return opc
        else: print("Opcion fuera de rango. Intente de nuevo")
        
def obtenerNuevoID(lista):
    if not lista:
        return 1
    return lista[-1]["id"] + 1

def validarNombre(nombre):
    while True:
        if nombre.strip() == "":
            nombre = input("Nombre invalido. Ingrese un nombre valido: ")
        else:
            return nombre.strip()

def validarPrecio(precio):
    while True:
        try:
            precio = float(precio)
            if precio < 0:
                raise ValueError
            return precio
        except ValueError:
            precio = input("Precio invalido. Ingrese un precio valido: ")

def validarStock(stock):
    while True:
        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError
            return stock
        except ValueError:
            stock = input("Stock invalido. Ingrese un stock valido: ")

def registrarProducto(productos):
    nombre = validarNombre(input("Ingrese el nombre del producto: "))
    precio = validarPrecio(input("Ingrese el precio del producto: "))
    stock = validarStock(input("Ingrese el stock del producto: "))
    categoria = input("Ingrese la categoria del producto: ")
    producto = {
        "id": obtenerNuevoID(productos),
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "categoria": categoria,
        "activo": True
    }
    productos.append(producto)
    guardarInventario(productos)
    print("Producto registrado exitosamente.")

def verProductos(productos):
    print("LISTA DE PRODUCTOS\n")
    if not productos:
        print("No hay productos registrados")
        return
    print(f"{'ID':<5} {'Nombre':<20} {'Precio':<10} {'Stock':<10} {'Categoria':<15} {'Activo':<10}")
    for producto in productos:
        print(f"{producto['id']:<5} {producto['nombre']:<20} {producto['precio']:<10} {producto['stock']:<10} {producto['categoria']:<15} {'Activo' if producto['activo'] else 'Inactivo':<10}")

def buscarProducto(productos):
    print("BUSCAR PRODUCTO\n")
    buscar = input("Ingrese el ID o nombre del producto a buscar: ").strip()
    encontrado = False
    print(f"{'ID':<5} {'Nombre':<40} {'Precio':<10} {'Stock':<10} {'Categoria':<15} {'Estado':<10}")
    print("-"*70)
    if buscar.isdigit():
        for producto in productos:
            if producto["id"] == int(buscar):
                encontrado = True
                estado = "Activo" if producto["activo"] else "Inactivo"
                print(f"{producto['id']:<5} {producto['nombre']:<40} {producto['precio']:<10} {producto['stock']:<10} {producto['categoria']:<15} {estado:<10}")
                return
    else:
        for producto in productos:
            if buscar.lower() in producto["nombre"].lower():
                encontrado = True
                estado = "Activo" if producto["activo"] else "Inactivo"
                print(f"{producto['id']:<5} {producto['nombre']:<40} {producto['precio']:<10} {producto['stock']:<10} {producto['categoria']:<15} {estado:<10}")

    if not encontrado:
        print("Producto no encontrado.")

def actualizarProducto(productos):
    print("ACTUALIZAR PRODUCTO\n")
    try:
        id = int(input("Ingrese el ID del producto a actualizar: "))
    except ValueError:
        print("ID no valido")
        return
    for producto in productos:
        if id == producto["id"]:
            while True:
                print("\nProducto encontrado:")
                print(f"1. Nombre: {producto['nombre']}")
                print(f"2. Precio: {producto['precio']}")
                print(f"3. Stock: {producto['stock']}")
                print(f"4. Categoria: {producto['categoria']}")
                print("0. Cancelar")
                try:
                    opc = int(input("Seleccione el campo a actualizar: "))
                except ValueError:
                    print("Opcion no valida")
                    continue
                
                if opc == 0:
                    return
                elif opc == 1:
                    producto["nombre"] = validarNombre(input("Ingrese el nuevo nombre: "))
                elif opc == 2:
                    producto["precio"] = validarPrecio(input("Ingrese el nuevo precio: "))
                elif opc == 3:
                    producto["stock"] = validarStock(input("Ingrese el nuevo stock: "))
                elif opc == 4:
                    producto["categoria"] = input("Ingrese la nueva categoria: ").strip()
                else:
                    print("Opcion no valida")
                    continue

                guardarInventario(productos)
                print("Producto actualizado exitosamente")
                return
    print("Producto no encontrado.")

def eliminarProducto(productos):
    print("ELIMINAR PRODUCTO\n")
    try:
        id = int(input("Ingrese el ID del producto a eliminar: "))
    except ValueError:
        print("ID no valido")
        return
    
    for producto in productos:
        if id == producto["id"]:
            if not producto["activo"]:
                print("El producto ya se encuentra eliminado.")
                return
            print("\nProducto encontrado:")
            print(f"Nombre: {producto['nombre']}")
            print(f"Precio: {producto['precio']}")
            print(f"Stock: {producto['stock']}")
            confirmar = input("¿Desea eliminar este producto? (si/no): ")
            if "si" in confirmar.lower():
                producto["activo"] = False
                guardarInventario(productos)
                print("Producto eliminado exitosamente")
            else:
                print("Operacion cancelada")
            return
    print("Producto no encontrado.")

def productosAgotados(productos):
    print("PRODUCTOS AGOTADOS\n")
    encontrados = False
    print(f"{'ID':<5} {'Nombre':<20} {'Stock':<10}")
    print("-"*40)
    for producto in productos:
        if producto["stock"] == 0 and producto["activo"]:
            print(f"{producto['id']:<5} {producto['nombre']:<20} {producto['stock']:<10}")
            encontrados = True
    if not encontrados:
        print("No hay productos agotados")


def main():
    productos = cargarInventario()
    while True:
        opc = menu()
        if opc == REGISTRAR:
            registrarProducto(productos)
        elif opc == VER:
            verProductos(productos)
        elif opc == BUSCAR:
            buscarProducto(productos)
        elif opc == ACTUALIZAR:
            actualizarProducto(productos)
        elif opc == ELIMINAR:
            eliminarProducto(productos)
        elif opc ==PRODUCTOS_AGOTADOS:
            productosAgotados(productos)
        elif opc == SALIR:
            break

main()
import random

# CONFIGURACIÓN

MIN_NUM = 1

FACIL = 1
MEDIO = 2
DIFICIL = 3
SALIR = 4

# FUNCIONES

def mensaje_inicio(min_num, max_num, max_intentos):
    print("\nADIVINA EL NÚMERO")
    print(f"Rango: {min_num} - {max_num}")
    print(f"Intentos máximos: {max_intentos}")

def menu_principal():
    while True:
        try:
            print("\nNivel de dificultad")
            print("1. Fácil (1-10)")
            print("2. Medio (1-50)")
            print("3. Difícil (1-100)")
            print("4. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion < 1 or opcion > 4:
                print("Opción fuera de rango")
            else:
                return opcion
        except ValueError:
            print("Ingresa un número válido")

def menu_final():
    while True:
        try:
            print("\n1. Jugar de nuevo")
            print("2. Volver al menú")
            print("3. Salir")
            opcion = int(input("Elige una opción: "))
            if opcion < 1 or opcion > 3:
                print("Opción fuera de rango")
            else:
                return opcion
        except ValueError:
            print("Ingresa un número válido")

def configurar_dificultad(opcion):
    if opcion == FACIL:
        return 10, 10
    elif opcion == MEDIO:
        return 50, 7
    elif opcion == DIFICIL:
        return 100, 5

def jugar(min_num, max_num, max_intentos):
    numero_secreto = random.randint(min_num, max_num)
    intentos = 0

    mensaje_inicio(min_num, max_num, max_intentos)

    while intentos < max_intentos:
        try:
            intento = int(input(f"\nIntento {intentos+1}/{max_intentos}: "))
            if intento < min_num or intento > max_num:
                print("Número fuera de rango")
                continue
        except ValueError:
            print("Ingresa un número válido")
            continue

        intentos += 1

        if intento == numero_secreto:
            print(f"\nGanaste en {intentos} intentos")
            return True
        elif intento < numero_secreto:
            print("El número secreto es mayor")
        else:
            print("El número secreto es menor")

    print(f"\nPerdiste. El número era: {numero_secreto}")
    return False

# PROGRAMA PRINCIPAL

while True:

    opcion = menu_principal()

    if opcion == SALIR:
        break

    max_num, max_intentos = configurar_dificultad(opcion)

    while True:
        jugar(MIN_NUM, max_num, max_intentos)
        decision = menu_final()

        if decision == 1:
            continue
        elif decision == 2:
            break
        else:
            exit()

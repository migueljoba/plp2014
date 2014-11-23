# -*- coding: utf-8 -*-
import platform
import os
from datetime import datetime, date

def limpiar_pantalla():
    sistema_operativo = platform.system()
    if sistema_operativo.lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

def leer_entero(mensaje, min_val=None, max_val=None, requerido=False):
    """
        leer_entero(string, int, int, boolean) -> int
            Pide que se ingrese número entre un rango dado. Los rangos son opcionales. Solo se retorna resultado cuando se ingresa
            un valor válido, si éste es requerido.
        @Parámetros
            mensaje   : mensaje que se muestra al usuario. Obligatorio.
            min_val   : el valor mínimo que usuario debe ingresar. default: None
            max_val   : el valor máximo que usuario debe ingresar. default: None
            requerido : Indica si el valor es obligatorio (True). default: False
    """

    while True:     # establecer un ciclo indefinido, hasta que el valor ingresado sea válido.

        val = input(mensaje)

        if not requerido and val.strip() == '':   # permite ingresar cadena vacía si el valor no es obligatorio.
            return val   

        else:   # valor es requerido. Validar entero.
            try: 
                val = int(val)
            except ValueError:      #  no se puede parsear a int. Valor inválido.
                print("Debe introducir un número entero.")

            else:
                # verificamos si se encuentra dentro del rango (min_val, max_val)
                if min_val is not None and val < min_val:
                    print("Valor fuera de rango. No puede ser menor a {}".format(min_val))
                
                elif max_val is not None and val > max_val:
                    print("Valor fuera de rango. No puede ser mayor a {}".format(max_val))

                else:   # se superó la validación. Retornar valor ingresado.
                    return val

def leer_cadena(mensaje, requerido=False):
    """
        leer_cadena(string, boolean) -> str
            Pide que se ingrese una cadena.
        @Parámetros
            mensaje   : mensaje que se muestra al usuario. Obligatorio.
            requerido : Indica si el valor es obligatorio (True). default: False
    """
    while True:  # establecer un ciclo indefinido, hasta que el valor ingresado sea válido.
        val = input(mensaje)

        if requerido and val.strip() == '':   
            print("No puede dejar vacío este campo. Ingrese de nuevo")
        else:
            return val

def presiona_continuar():
    mensaje = "Presione 'Enter' para continuar..."
    leer_cadena(mensaje, requerido=False)
    limpiar_pantalla()

def leer_dato_binario(mensaje, opciones):
    """ Función para validar el ingreso de datos donde sólamente son posibles dos respuestas.
        Case sensitive.
        @Parámetros
            opciones: lista de elementos str. con las posibles respuestas   
    """
    print(mensaje)
    while True:
        val = input()

        if val in opciones:
            return val
        else:
            print("Ingresó un valor incorrecto. Las opciones son " + str(opciones))


def si_no_pregunta(pregunta):
    pregunta += " (S/N):"
    valores_si = ['si', 'sí', 's', 'yes', 'y']
    valores_no = ['no', 'n']
    while True:
        val = input(pregunta)

        if val.lower() in valores_si:
            return True
        elif val.lower() in valores_no:
            return False
        else:
            print("Ingresó una respuesta no válida...")

def fecha_actual():
    """Función que retorna la fecha actual"""
    return datetime.now().date()

def hora_actual():
    """Función que retorna la hora actual"""
    return datetime.now().time()


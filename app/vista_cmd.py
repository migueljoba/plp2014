# -*- coding: utf-8 -*-
from controladores import PersonaControlador, VisitaControlador
import util

util.limpiar_pantalla()

def buscar_cedula():
	mensaje = "Ingrese número de cédula: "
	cedula = util.leer_cadena(mensaje, requerido=True)

	existe = PersonaControlador().existe(cedula)

	if existe:
		persona = PersonaControlador().recuperar(cedula)
		print(persona)
		util.presiona_continuar()
	else:
		print("No se encontró esa cédula")
		pregunta = "¿Desea registrar una nueva persona ahora?"
		accion = util.si_no_pregunta(pregunta)

		if accion is True:
			registrar_persona()
		else:
			print("Registrar más tarde")

def registrar_persona():
	print("Debe ingresar los siguientes datos: ")
	cedula = util.leer_cadena("Número de Cédula: ", requerido=True)
	nombre = util.leer_cadena("Nombre: ", requerido=True)
	apellido = util.leer_cadena("Apellido: ", requerido=True)
	sexo = util.leer_dato_binario("Sexo (M/F): ", ["M", "F"])
	edad = util.leer_entero("Edad: ", requerido=True)

	guardar = PersonaControlador().crear(cedula=cedula, nombre=nombre, 
				apellido=apellido, sexo=sexo,
				edad=edad)
	
	if guardar is True:
		print("Se registraron los datos correctamente.")
	else:
		print("Ocurrió un error y no se pudieron registrar los datos. Vuelva a intentarlo.")

	util.presiona_continuar()

def registrar_entrada():
	mensaje = "Ingrese número de cédula para marcar su entrada: "
	cedula = util.leer_cadena(mensaje, requerido=True)
	try:
		visita = VisitaControlador().crear(cedula)
		print(visita)
	except Exception as e:
		print(e)

	util.presiona_continuar()

def registrar_salida():
	mensaje = "Ingrese número de cédula para marcar su salida: "
	cedula = util.leer_cadena(mensaje, requerido=True)

	try:
		VisitaControlador().marcar_salida(cedula)
	except Exception as e:
		print(e)

def salir():
	util.limpiar_pantalla()
	exit()


def menu_principal():
	menu_principal = {}
	titulo = "titulo"
	funcion = "funcion"

	menu_principal[1] = {titulo: "Buscar persona por cédula", funcion: buscar_cedula}
	menu_principal[2] = {titulo: "Registrar entrada", funcion: registrar_entrada}
	menu_principal[3] = {titulo: "Registrar salida", funcion: registrar_salida}
	menu_principal[4] = {titulo: "Registrar persona", funcion: registrar_persona}
	menu_principal[5] = {titulo: "Salir", funcion: salir}
	menu_principal[6] = {titulo: "Salir", funcion: salir}

	while True:
		# util.limpiar_pantalla()
		print("-------------------MENU PRINCIPAL -------------------------")
		for key in menu_principal.keys():
			print("{}- {}".format(key, menu_principal[key][titulo]))
		print("-----------------------------------------------------------")
		max_val = len(menu_principal)
		opcion = util.leer_entero("Ingrese una opción: ", min_val=1, max_val=max_val, requerido=True)
		#ejecutamos la opcion asociada al menú
		menu_principal[opcion][funcion]()


menu_principal() 
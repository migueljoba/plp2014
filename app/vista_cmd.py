# -*- coding: utf-8 -*-
from controladores import PersonaControlador, VisitaMenorControlador, VisitaControlador, BicicletaControlador
import util

util.limpiar_pantalla()

edad_adulto = 18	# persona adulta >= 18 años

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

	persona = PersonaControlador()
	creado = persona.crear(cedula=cedula, nombre=nombre, 
					apellido=apellido, sexo=sexo,
					edad=edad)

	if creado is True:
		print("Se registraron los datos correctamente.")
	else:
		print("No se pudieron registrar los datos.")

	util.presiona_continuar()

def registrar_entrada():
	mensaje = "Ingrese número de cédula para marcar su entrada: "
	cedula = util.leer_cadena(mensaje, requerido=True)

	p = PersonaControlador()
	try:
		persona = p.recuperar(cedula)
	except NoExistePersona as ex:
		print(ex)
		util.presiona_continuar()
		menu_principal()

	edad_persona = persona.get_edad()

	if edad_persona < 18:	# visitante es menor?
		pregunta = "¿Esta persona viene acompañada de un adulto?"
		acompanha_adulto = util.si_no_pregunta(pregunta)

		if acompanha_adulto:
			cedula_adulto = util.leer_cadena("Ingrese cédula del adulto responsable: ", requerido=True)
		else:
			cedula_adulto = None
		
		visita = VisitaMenorControlador().marcar_entrada(cedula, cedula_adulto)
		print(visita)
	else:	# visitante es adulto
		try:
			visita = VisitaControlador().marcar_entrada(cedula)
			print(visita)
		except Exception as e:
			print(e)

	util.presiona_continuar()

def registrar_salida():
	mensaje = "Ingrese número de cédula para marcar su salida: "
	cedula = util.leer_cadena(mensaje, requerido=True)

	try:
		visita = VisitaControlador().marcar_salida(cedula)
		print(visita)
	except Exception as e:
		print(e)

def salir():
	util.limpiar_pantalla()
	exit()

def alquilar_bici():
	disponible = BicicletaControlador().cantidad_disponible()
	
	if disponible == 0:
		print("No hay bicicletas disponibles en este momento.")
	
	else:
		mensaje = "Existen {0} bicicletas disponible(s).\n".format(disponible)
		print(mensaje)

		cedula = util.leer_cadena("Ingrese el nro. de cédula del solicitante: ", requerido=True)
		if not BicicletaControlador().validar_solicitante(cedula):
			print("Esta cédula no corresponde a alguien presente en el parque.")
			return False

		nro_solicitado = util.leer_entero("¿Cuántas desea alquilar?: ", min_val=1, max_val=20, requerido=True)
		
		# booleano
		cantidad_valida = BicicletaControlador().validar_cantidad_solicitada(nro_solicitado)

		if not cantidad_valida:
			print("No existen suficientes bicicletas disponibles.")
			util.presiona_continuar()
			alquilar_bici()

		tiempo_alquiler = opcion = util.leer_entero("Tiempo de alquiler, en horas: ", min_val=1, max_val=8, requerido=True)

		monto_alquiler = BicicletaControlador().alquilar(cedula, nro_solicitado, tiempo_alquiler)
		print("El monto a abonar es: Gs " + str(monto_alquiler))

	util.presiona_continuar()

def devolver_bici():
	cedula = util.leer_cadena("Ingrese el nro. de cédula de quien devuelve: ", requerido=True)
	BicicletaControlador().devolver(cedula)
	util.presiona_continuar()

def menu_bicicleta():
	menu_bici = {}
	titulo = "titulo"
	funcion = "funcion"

	menu_bici[1] = {titulo: "Alquilar", funcion: alquilar_bici}
	menu_bici[2] = {titulo: "Devolver", funcion: devolver_bici}
	menu_bici[3] = {titulo: "Volver al menú principal", funcion: menu_principal}

	while True:
		# util.limpiar_pantalla()
		print("-------------------MENU BICICLETA-------------------------")
		for key in menu_bici.keys():
			print("{}- {}".format(key, menu_bici[key][titulo]))
		print("-----------------------------------------------------------")
		max_val = len(menu_bici)
		opcion = util.leer_entero("Ingrese una opción: ", min_val=1, max_val=max_val, requerido=True)
		# ejecutamos la opcion asociada al menú
		menu_bici[opcion][funcion]()

def menu_principal():
	menu_principal = {}
	titulo = "titulo"
	funcion = "funcion"

	menu_principal[1] = {titulo: "Buscar persona por cédula", funcion: buscar_cedula}
	menu_principal[2] = {titulo: "Registrar entrada", funcion: registrar_entrada}
	menu_principal[3] = {titulo: "Registrar salida", funcion: registrar_salida}
	menu_principal[4] = {titulo: "Registrar persona", funcion: registrar_persona}
	menu_principal[5] = {titulo: "Listar ", funcion: salir}	 # TODO esto no está implementado todavía!! Ni hace falta :D
	menu_principal[6] = {titulo: "Ir a menú de BICICLETAS", funcion: menu_bicicleta}
	menu_principal[7] = {titulo: "Salir", funcion: salir}

	while True:
		
		print("-------------------MENU PRINCIPAL -------------------------")
		for key in menu_principal.keys():
			print("{}- {}".format(key, menu_principal[key][titulo]))
		print("-----------------------------------------------------------")
		max_val = len(menu_principal)
		opcion = util.leer_entero("Ingrese una opción: ", min_val=1, max_val=max_val, requerido=True)
		# ejecutamos la opcion asociada al menú
		menu_principal[opcion][funcion]()



menu_principal() 
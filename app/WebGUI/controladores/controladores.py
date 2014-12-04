# -*- encoding: utf-8 -*-
import shelve
from abc import ABCMeta, abstractmethod
from modelos.modelos import Persona, Visita, VisitaMenor, Bicicleta, BicicletaConfig
from datetime import datetime, date

from util import util

persona_db = "persona.db"
visita_db = "visitante.db"
bici_db = "bicicleta.db"
config_db = "config.db"
template_base = "base.html"

class NoTieneVisita(Exception):
    pass
class NoExistePersona(Exception):	# deprecar esto. Causaba excepcion al intentar capturar esta Exception
	pass

class PersonaControlador():

	def crear(self, **kwargs):
		"""Método para crear un registro de persona en la base de datos"""

		r = Respuesta()

		try:
			self.validar_atributos(**kwargs)
		except Exception as e:
			r.mensaje = "No se registraron los datos. " + str(e)
			r.exito = False
			r.template = "formulario_persona.html"
			return r

		p = Persona(cedula=kwargs['cedula'],
					nombre=kwargs['nombre'],
					apellido=kwargs['apellido'],
					sexo=kwargs['sexo'],
					edad=kwargs['edad']
		)

		s = shelve.open(persona_db)
		
		# preguntar si ya existe antes de guardar
		if self.existe(p.get_cedula()):
			# ya existe
			r.mensaje = "Ya existe persona con esta cedula"
			r.exito = False
			r.template = template_base

		else:
			# no existe. Entonces, registrar
			s[p.get_cedula()] = p
			r.mensaje = "Se registraron los datos exitosamente"
			r.exito = True
			r.template = "persona_tabla.html"

		# parsea la instancia de Persona a un dict
		r.objeto = util.objeto_a_diccionario(p)

		s.close()
		return r

	def validar_atributos(self, **kwargs):
		print("Validando attributos...")
		print("Se reciben:")
		print(kwargs)
		"""Método que verifica la existencia de los atributos requeridos para la creación de una persona"""
		atr_requerido = ["cedula", "nombre", "apellido", "sexo", "edad"]

		for atr in atr_requerido:
			print(atr)
			if atr not in kwargs or kwargs[atr] is None or kwargs[atr].strip() == '':
				raise Exception("Parámetro requerido '{0}' ausente".format(atr))

		# TODO validar contenido de los parámetros. Prioridad baja

	def destruir(self, id_obj):		# plato de oro ?
		"""Método para borrar el registro de una persona"""
		s = shelve.open(persona_db)

		if id_obj in s.keys():
			del s[id_obj]
			s.close()
		else:
			raise Exception("No existe persona con cédula %s en los registros." % (id_obj))
			s.close()
			
	def get_id(self, objeto):
		# para una instancia de Persona() ya guardada, su id es su atributo 'cedula' 
		return objeto.get_cedula()

	def existe(self, cedula):
		"""Función que verifica la existencia de una persona en la base de datos"""
		s = shelve.open(persona_db)

		if cedula in s.keys():
			existe = True
		else:
			existe = False
		
		s.close()

		return existe

	def recuperar(self, cedula):
		"""Función que retorna el objeto Persona, si existe en la base datos"""
		s = shelve.open(persona_db)
		if cedula not in s.keys():
			# Correcion de bug en examen: Intentaba hacer un raise de excepcion NoExistePersona y causaba otra excepcion.
			raise Exception("No existen registros para esta cédula.")
		tmp = s[cedula]
		s.close()
		
		return tmp

	def buscar(self, cedula):

		# Instanciamos el objeto Respuesta
		r = Respuesta()

		if self.existe(cedula):
			p = self.recuperar(cedula)

			r.objeto = util.objeto_a_diccionario(p)
			r.exito = True

			# renderizar la tabla de datos de la persona
			r.template = 'persona_tabla.html'
			r.mensaje = "Se encontraron los siguientes datos"

		else:
			r.mensaje = "No se encontró a ninguna persona con cédula {0} entre los registros. Puede registrarla completando el formulario.".format(cedula)
	
			# renderizar el formulario de registro de persona
			r.template = 'formulario_persona.html'

		return r

class VisitaControlador():

	def validar_entrada(self, cedula):
		"""	
			validar_entrada(cedula) -> None
			Método para validar entrada de una persona. No pasa la verificación si en la última visita no 
			se marcó salida. 
			Provoca excepción si no se supera validación
		"""

		ultima_visita = self.ultima_visita(cedula)
		id_visita = ultima_visita.get_id_visita()
		s = shelve.open(visita_db)
		tmp_visita = s[id_visita]
		s.close()

		if tmp_visita.get_hora_salida() is None:
			raise Exception("No se podrá marcar entrada. Esta persona ya se encuentra dentro del parque.")

	def validar_salida(self, cedula):
		"""	
			validar_salida(cedula) -> str id de ultima visita
			Método para validar salida de una persona. Supera la verificación si en la última visita no 
			se marcó salida. 
			Provoca excepción si no se supera validación
		"""
		ultima_visita = self.ultima_visita(cedula)
		id_visita = ultima_visita.get_id_visita()
		s = shelve.open(visita_db)
		tmp_visita = s[id_visita]
		s.close()

		if tmp_visita.get_hora_salida() is not None:
			raise Exception("No se podrá marcar salida. La ultima visita para esta cédula ya tiene marcada una hora de salida.")
		else:
			return id_visita

	def esta_adentro(self, cedula):
		""" esta_adentro(str) -> Booleano
			Método para verificar si la visita se encuentra en curso.
		"""
		ultima_visita = self.ultima_visita(cedula)
		id_visita = ultima_visita.get_id_visita()
		s = shelve.open(visita_db)
		tmp_visita = s[id_visita]
		s.close()
		if tmp_visita.get_hora_salida() is not None:
			return False	# Ya marcó salida en última visita. Terminó la visita
		else:
			return True		# Ultima visita no tiene marcada hora de salida. Se encuentra en curso la visita.

	def marcar_entrada(self, cedula):
		"""Método para registrar la entrada de una persona al parque"""
		id_visitante = cedula

		existe_persona = PersonaControlador().existe(cedula)

		if existe_persona:
			try:
				self.validar_entrada(cedula)
			except NoTieneVisita:
				pass	# No existe ninguna visita para esta cédula. La validación de entrada no fue necesaria.

			s = shelve.open(visita_db)

			total_registros = len(s)
			id_visita = str(total_registros + 1)

			fecha_visita = util.fecha_actual()
			hora_entrada = util.hora_actual()

			v = Visita(id_visita, id_visitante, fecha_visita, hora_entrada)

			s[id_visita] = v
			return v

		else:
			v = None
			raise Exception("No existe una persona con la cédula indicada.")

	def marcar_salida(self, cedula):
		"""Método para registrar la salida de una persona del parque"""
		id_visita = self.validar_salida(cedula)

		s = shelve.open(visita_db)

		tmp_visita = s[id_visita]
		if tmp_visita.get_hora_salida() is None:
			hora_salida = util.hora_actual()
			tmp_visita.set_hora_salida(hora_salida)
		else:
			s.close()
			raise Exception("No se podrá marcar salida. La ultima visita para esta cédula ya tiene marcada una hora de salida.")

		s[id_visita] = tmp_visita
		s.close()
		return tmp_visita

	def ultima_visita(self, cedula):
		"""
			ultima_visita(str) -> Visita()
			Método para obtener la visita más reciente asociada a una persona, según su nro de cédula
		"""
		
		visitas = shelve.open(visita_db)

		visita_lista = [int(v.get_id_visita()) for v in visitas.values() if v.get_id_visitante() == cedula]

		if visita_lista:
			ultima_visita_id = sorted(visita_lista)[-1]
		else:
			raise NoTieneVisita("No existen registros de visitas para la cédula indicada")

		ultima_visita = visitas[str(ultima_visita_id)]
		visitas.close()

		return ultima_visita

	def marcar_visita(self, cedula, **kwargs):
		accion = kwargs["accion"]

		r = Respuesta()

		try:
			if accion.lower() == "marcar entrada":
				visita = self.marcar_entrada(cedula)
				r.mensaje = "Se registró la entrada correctamente"

			elif accion.lower() == "marcar salida":
				visita = self.marcar_salida(cedula)
				r.mensaje = "Se registró la salida correctamente"

			r.objeto = util.objeto_a_diccionario(visita)
		
		except Exception as e:
			r.mensaje = str(e)

		r.template = "campos_visita.html"

		return r

class VisitaMenorControlador(VisitaControlador):
	"""Clase para implementar la visita de un menor de edad al parque"""

	def marcar_entrada(self, cedula, cedula_adulto):
		"""Método para registrar la entrada de una persona al parque"""
		id_visitante = cedula

		existe_persona = PersonaControlador().existe(cedula)

		if existe_persona:
			try:
				self.validar_entrada(cedula)
			except NoTieneVisita:
				pass	# No existe ninguna visita para esta cédula. La validación de entrada no fue necesaria.

			s = shelve.open(visita_db)

			total_registros = len(s)
			id_visita = str(total_registros + 1)

			fecha_visita = util.fecha_actual()
			hora_entrada = util.hora_actual()

			v = VisitaMenor(cedula_adulto=cedula_adulto, id_visita=id_visita, 
						id_visitante=id_visitante, fecha_visita=fecha_visita, 
						hora_entrada=hora_entrada)

			s[id_visita] = v
			return v

		else:
			v = None
			raise Exception("No existe una persona con la cédula indicada.")
		
class AlquilableControlador(metaclass=ABCMeta):

	@abstractmethod
	def alquilar(self):
		pass

	@abstractmethod
	def devolver(self):
		pass

class BicicletaControlador(AlquilableControlador):
	def crear(self, **kwargs):

		s = shelve.open(bici_db)
		total_registros = len(s)

		id_num = total_registros + 1

		b = Bicicleta(id_num=id_num, marca=kwargs['marca'],
					estado="DISPONIBLE")

		s[str(id_num)] = b

		s.close()
	
	def alquilar(self, cedula, nro_solicitado, tiempo_alquiler):

		r = Respuesta()
		fallo_str = ''

		# valida al solicitante. Debe estar presente en el parque.
		if not self.validar_solicitante(cedula):
			r.mensaje = "La cédula {0} no corresponde a alguien presente en el parque. No se podrá realizar el alquiler.".format(cedula)
			r.template = "bici_info.html"
			return r

		# valida disponibilidad de la cantidad solicitada
		nro_solicitado = int(nro_solicitado)
		nro_disponible = self.cantidad_disponible()

		if nro_solicitado > nro_disponible:
			r.mensaje = "Sólo existe(n) {0} bicicletas disponibles. No se podrá realizar el alquiler.".format(nro_disponible)
			r.template = "bici_info.html"
			return r

		# se registra el alquiler.
		lista = self.lista_disponible()[:nro_solicitado]

		s = shelve.open(bici_db)

		for id_bici in lista:
			# sobreescribe el estado de cada bicicleta a ser alquilada
			tmp = s[id_bici]
			tmp.set_estado("NO DISPONIBLE")
			tmp.set_cedula_solicitante(cedula)
			tmp.set_tiempo_alquiler(tiempo_alquiler)

			s[id_bici] = tmp
		s.close()

		# monto_total = int(nro_solicitado) * int(tiempo_alquiler) * 10000	# calculo original. Se remplazo por calcular_monto()

		pre_monto_total = self.calcular_monto_total(nro_solicitado, int(tiempo_alquiler))

		descuento = self.calcular_descuento(nro_solicitado)

		monto_final = pre_monto_total - descuento

		if nro_solicitado > 1:
			r.mensaje = "Se alquilaron {0} bicicletas exitosamente. El monto a abonar es de G. {1}- Tiene G. {2} de descuento.".format(nro_solicitado, monto_final, descuento)

		else:
			r.mensaje = "Se alquilaron {0} bicicletas exitosamente. El monto a abonar es de G. {1}".format(nro_solicitado, monto_final)
		
		r.template = "bici_info.html"

		return r
		
	def devolver(self, cedula):
		r = Respuesta()
		r.template = "bici_info.html"

		# valida al solicitante. Debe estar presente en el parque.
		if not self.validar_solicitante(cedula):
			r.mensaje = "La cédula {0} no corresponde a alguien presente en el parque. No se podrá realizar la devolución.".format(cedula)
			r.template = "bici_info.html"
			return r		
		
		s = shelve.open(bici_db)

		lista_devolver = self.listar_por_cedula(cedula)
		cantidad_devolver = len(lista_devolver)

		if cantidad_devolver == 0:
			r.mensaje = "No existen bicicletas alquiladas para este número de cédula."
			return r

		# genera una lista con el ID de cada bici para volverlas al estado DISPONIBLE
		lista_id = [bici.get_id_num() for bici in lista_devolver]
		self.marcar_disponible(lista_id)
		
		s.close()

		r.objeto = lista_devolver
		r.mensaje = "Se devuelven {0} bicicleta(s)".format(cantidad_devolver)
	
		return r
		

	def validar_solicitante(self, cedula):
		"""	validar_solicitante(str) -> Booleano
			Determina si el solicitante se encuentra o no dentro dentro del parque; condición 
			necesaria para alquilar o devolver bicicleta.
		"""
		# la persona existe en BD y actualmente de visita?
		if PersonaControlador().existe(cedula) and VisitaControlador().esta_adentro(cedula):
			return True
		else:
			return False

	def validar_cantidad_solicitada(self, nro_solicitado):
		nro_disponible = self.cantidad_disponible()

		if int(nro_solicitado) > nro_disponible:
			return False
		else:
			return True

	def lista_disponible(self):
		s = shelve.open(bici_db)
		lista_disponible = [b.get_id_num() for b in s.values() if b.get_estado() == "DISPONIBLE"]
		s.close()
		return lista_disponible

	def lista_no_disponible(self):
		s = shelve.open(bici_db)
		lista_no_disponible = [b.get_id_num() for b in s.values() if b.get_estado() != "DISPONIBLE"]
		s.close()
		return lista_no_disponible

	def cantidad_disponible(self):
		return len(self.lista_disponible())

	def marcar_no_disponible(self, lista_id):
		s = shelve.open(bici_db)

		for id_bici in lista_id:
			tmp = s[id_bici]
			tmp.set_estado("NO DISPONIBLE")
			s[id_bici] = tmp

		s.close()

	def marcar_disponible(self, lista_id):
		s = shelve.open(bici_db)
		for id_bici in lista_id:
			tmp = s[id_bici]
			tmp.set_estado("DISPONIBLE")
			tmp.set_cedula_solicitante(None)
			tmp.set_tiempo_alquiler(None)
			s[id_bici] = tmp

		s.close()

	def listar_por_cedula(self, cedula):
		s = shelve.open(bici_db)

		lista_no_disponible = [b.get_id_num() for b in s.values() if b.get_estado() != "DISPONIBLE"]

		# genera una lista de objetos Bicicleta
		lista_bici = [b for b in s.values() if b.get_cedula_solicitante() == cedula]

		return lista_bici

	def calcular_descuento(self, cantidad):
		"""Función para calcular un descuento sobre el monto total."""
		
		s = shelve.open(config_db)
		config = s['bicicleta']


		monto_hora = config.get_monto()

		if cantidad > 1:
			porcentaje_desc = config.get_porcentaje_desc()		# num entero: 10 --> 10% descuento
			monto_descuento = cantidad * monto_hora * porcentaje_desc / 100
		else:
			monto_descuento = 0

		s.close()

		return monto_descuento


	def calcular_monto_total(self, cantidad, horas):
		"""Funcion que calcula el monto total. No considera descuentos, si hubiesen"""
		s = shelve.open(config_db)
		config = s['bicicleta']

		porcentaje_desc = config.get_porcentaje_desc()		# num entero: 10 --> 10% descuento
		monto_hora = config.get_monto()

		s.close()

		monto_total = monto_hora * cantidad * horas
		
		return monto_total

class Respuesta():
	"""Clase para unificar la respuesta del controlador a la vista.
	   Todo objeto Respuesta tendrá los sgtes. atributos:
	   - 'objeto': Persona o Bicicleta y otros a ser implementados.
	   - 'template': str con el nombre del archivo .html a renderizar. "base.html" por defecto.
	   - 'exito': booleano que indica si la petición fracasó o no. False por defecto.
	   - 'mensaje': str con información para el usuario. Cadena vacía por defecto.
	"""
	def __init__(self, objeto={}, template='base.html', exito=False, mensaje=''):
		# Al no tener atributos privados no se necesitan ni setters ni getters.
		self.objeto = objeto
		self.template = template
		self.exito = exito
		self.mensaje = mensaje


class BicicletaConfigControlador():

	def set_monto_hora(self, nuevo_monto):
		conf = BicicletaConfig()
		conf.set_monto(int(nuevo_monto))

		s = shelve.open(config_db)
		s['bicicleta'] = conf

		s.close()


		r = Respuesta()
		r.mensaje = "El nuevo monto por hora es de: G. {0}".format(nuevo_monto)
		r.template = "bici_info.html"

		return r

	def get_monto_hora(self):
		s = shelve.open(config_db)

		conf = s['bicicleta']
		monto_hora = conf.get_monto()
		return monto_hora




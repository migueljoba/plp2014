import shelve
from abc import ABCMeta, abstractmethod
from modelos import Persona, Visita, VisitaMenor, Bicicleta
from datetime import datetime, date

import util

persona_db = "persona.db"
visita_db = "visitante.db"
bici_db = "bicicleta.db"

class NoTieneVisita(Exception):
    pass
class NoExistePersona(Exception):	# deprecar esto. Causaba excepcion al intentar capturar esta exception
	pass

class PersonaControlador():

	def crear(self, **kwargs):
		"""Función para crear un registro para una persona en la base de datos"""
		p = Persona(cedula=kwargs['cedula'],
					nombre=kwargs['nombre'],
					apellido=kwargs['apellido'],
					sexo=kwargs['sexo'],
					edad=kwargs['edad']
		)

		print(p)

		s = shelve.open(persona_db)
		# preguntar si ya existe antes de guardar
		
		if self.existe(p.get_cedula()):
			print("Ya existe persona con esta cedula")
			# cedula = p.get_cedula()
			print(s[p.get_cedula()])
			exito = False

		else:
			s[p.get_cedula()] = p
			exito = True
		
		# s[p.get_cedula()] = p
		s.close()
		return exito

	def validar_atributos(self, **kwargs):
		"""Método que verifica la existencia de los atributos requeridos para la creación de una persona"""
		attr_requerido = ["cedula", "nombre", "apellido", "sexo", "edad"]

		for atr in attr_requerido:
			if atr not in kwargs:
				raise Exception("Parámetro requerido '%s' ausente: " % (atr))

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
			return False	# Ya mercó salida en última visita. Terminó la visita
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
		# pedimos la lista de los IDs de las bicis disponibles
		lista = self.lista_disponible()[:nro_solicitado]

		s = shelve.open(bici_db)

		for id_bici in lista:
			tmp = s[id_bici]
			tmp.set_estado("NO DISPONIBLE")
			tmp.set_cedula_solicitante(cedula)
			tmp.set_tiempo_alquiler(tiempo_alquiler)

			s[id_bici] = tmp

		s.close()

		return nro_solicitado * tiempo_alquiler * 10000
		
	def devolver(self, cedula):
		lista = self.lista_no_disponible()
		
		s = shelve.open(bici_db)

		for id_bici in lista:
			if s[id_bici].get_cedula_solicitante() == cedula:
				tmp = s[id_bici]
				tmp.set_estado("DISPONIBLE")
				tmp.set_cedula_solicitante(None)
				tmp.set_tiempo_alquiler(None)
				s[id_bici] = tmp
		s.close()


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
			s[id_bici] = tmp

		s.close()

	def listar_por_cedula(self, cedula):
		s = shelve.open(bici_db)

		lista_no_disponible = [b.get_id_num() for b in s.values() if b.get_estado() != "DISPONIBLE"]

		# genera una lista de objetos Bicicleta
		lista_bici = [b for b in s.values() if b.get_cedula_solicitante() == cedula]

		return lista_bici
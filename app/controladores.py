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
class NoExistePersona(Exception):
	pass

class ControladorMaster():	# deprecar
	
	def crear(objeto):
		print("Llama a metodo crear()")
		id_obj = objeto.get_cedula()

		if s.has_key(id_obj):	 #deprecar
			print("Ya existe esta persona")
		s[id_obj] = objeto
	
	def listar_todo():
		pass

	def listar_por_estado():
		pass

	def valida_creacion(self, objeto):

		id_obj = objeto.get_cedula()

		if s.has_key(id_obj): # ya existe 
			pass

	@abstractmethod
	def get_id_objeto(self, objeto):
		pass
	
	@abstractmethod
	def destruir(self, objeto):
		pass

class PersonaControlador(ControladorMaster):

	def crear(self, **kwargs):
		
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
		attr_requerido = ["cedula", "nombre", "apellido", "sexo", "edad"]

		for atr in attr_requerido:
			if atr not in kwargs:
				raise Exception("Parámetro requerido '%s' ausente: " % (atr))

		# TODO validar contenido de los parámetros. Prioridad baja

	def destruir(self, id_obj):		# plato de oro ?

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
			raise NoExistePersona("No existen registros para esta cédula.")
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
			raise Exception("No se podrá marcar entrada. Esta persona ya se encuentra dentro parque.")

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

	def marcar_entrada(self, cedula):
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
	def marcar_entrada(self, cedula, cedula_adulto):
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
		
class AlquilableControlador():

	def alquilar(self):
		pass
	
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
	
	def alquilar(self):
		pass

	def devolver(self):
		pass
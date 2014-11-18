import shelve
from abc import ABCMeta, abstractmethod
from modelos import Persona, Visita
from datetime import datetime, date

import util

persona_db = "persona.db"
visita_db = "visitante.db"

class YaExiste(Exception):
    pass




class ControladorMaster():
	
	def crear(objeto):
		print("Llama a metodo crear()")
		id_obj = objeto.get_cedula()

		if s.has_key(id_obj):
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

	def destruir(self, id_obj):

		s = shelve.open(persona_db)

		if id_obj in s.keys():
			del s[id_obj]
			s.close()
		else:
			raise Exception("No existe persona con cédula %s en los registros." % (id_obj))
			s.close()
			
	def get_id(self, objeto):
		# print("llama a get_id()")
		# para una instancia de Persona() ya guardada, su id es su atributo 'cedula' 
		return objeto.get_cedula()

	def existe(self, cedula):
		# print("llama a existe()")
		s = shelve.open(persona_db)

		if cedula in s.keys():
			existe = True
		else:
			existe = False
		
		s.close()

		return existe

	def recuperar(self, id_obj):
		
		s = shelve.open(persona_db)
		tmp = s[id_obj]
		s.close()
		
		return tmp


class VisitaControlador():

	def crear(self, cedula):
		id_visitante = cedula

		existe_persona = PersonaControlador().existe(cedula)

		if existe_persona:
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
		ultima_visita = self.ultima_visita(cedula)
		id_visita = ultima_visita.get_id_visita()

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

	def ultima_visita(self, cedula):
		"""Método para obtener la visita más reciente asociada a una persona, según su nro de cédula"""
		
		visitas = shelve.open(visita_db)

		visita_lista = [int(v.get_id_visita()) for v in visitas.values() if v.get_id_visitante() == cedula]

		if visita_lista:
			ultima_visita_id = sorted(visita_lista)[-1]
		else:
			raise Exception("No existen registros de visitas para la cédula indicada")

		ultima_visita = visitas[str(ultima_visita_id)]
		visitas.close()

		return ultima_visita
		
# class VisitaControlador(ControladorMaster):
	""" introducir CI. Si no existe CI, pedir datos de la persona. Luego de cargar datos, o luego de comprobar existencia, permiter a 
		usuario hacer click sobre algo que diga "marcar entrada". Esto debe crear un nuevo registro en la tabla de visitas que se autoincrementara, 
		tendra la CI de persona, hora entrada y hora salida.
		Hora salida se podrá marcar luego.
	"""

#	pass
	


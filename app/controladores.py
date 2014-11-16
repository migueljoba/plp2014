import shelve
from abc import ABCMeta, abstractmethod
from modelos import Persona
persona_db = "persona.db"
visitante_db = "visitante.db"

class YaExiste(Exception):
    pass




class ControladorMaster():

	def crear(objeto):
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

		else:
			s[p.get_cedula()] = p
		
		# s[p.get_cedula()] = p
		s.close()

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
		print("llama a get_id()")
		# para una instancia de Persona() ya guardada, su id es su atributo 'cedula' 
		return objeto.get_cedula()

	def existe(self, cedula):
		print("llama a existe()")
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




class VisitanteControlador(ControladorMaster):

	def crear(self, objeto):
		pass
		


class VisitaControlador(ControladorMaster):
	""" introducir CI. Si no existe CI, pedir datos de la persona. Luego de cargar datos, o luego de comprobar existencia, permiter a 
		usuario hacer click sobre algo que diga "marcar entrada". Esto debe crear un nuevo registro en la tabla de visitas que se autoincrementara, 
		tendra la CI de persona, hora entrada y hora salida.
		Hora salida se podrá marcar luego.
	"""

	pass
	



class Persona():
	
	def __init__(self, cedula=None, nombre=None, apellido=None, edad=None, sexo=None, **kwargs):
		self.__cedula = cedula
		self.__nombre = nombre
		self.__apellido = apellido
		self.__edad = edad
		self.__sexo = sexo

	def get_cedula(self):
		return self.__cedula

	def set_cedula(self, cedula):
		self.__cedula = cedula

	def get_nombre(self):
		return self.__nombre

	def set_nombre(self, nombre):
		self.__nombre = nombre
                        
	def get_apellido(self):
		return self.__apellido

	def set_apellido(self, apellido):
		self.__apellido = apellido

	def get_edad(self):
		return self.__edad

	def set_edad(self, edad):
		self.__edad = edad

	def get_sexo(self):
		return self.__sexo

	def set_sexo(self, sexo):
		self.__sexo = sexo


class Visitante(Persona):
	
	def __init__(self, fecha_visita=None, hora_entrada=None, hora_salida=None, **kwargs):
		super().__init__(**kwargs)
		self.__fecha_visita = fecha_visita
		self.__hora_entrada = hora_entrada
		self.__hora_salida = hora_salida

	def get_fecha_visita(self):
		return self.__fecha_visita

	def set_fecha_visita(self, fecha_visita):
		self.__fecha_visita = fecha_visita

	def get_hora_entrada(self):
		return self.__hora_entrada

	def set_hora_entrada(self, hora_entrada):
		self.__hora_entrada = hora_entrada

	def get_hora_salida(self):
		return self.__hora_salida

	def set_hora_salida(self, hora_salida):
		self.__hora_salida = hora_salida


class VisitanteMenor(Visitante):

	def __init__(self, cedula_adulto=None, **kwargs):
		super().__init__(**kwargs)
		self.__cedula_adulto = cedula_adulto

	def get_cedula_adulto(self):
		return self.__cedula_adulto

	def set_cedula_adulto(self, cedula_adulto):
		self.__cedula_adulto = cedula_adulto


class Alquilable():
	def __init__(self, cedula_solicitante=None, hora_inicio=None, hora_fin=None, precio=None):
		self.__cedula_solicitante = cedula_solicitante
		self.__hora_inicio = hora_inicio
		self.__hora_fin = hora_fin
		self.__precio = precio


	def get_cedula_solicitante(self):
		return self.__cedula_solicitante

	def set_cedula_solicitante(self, cedula_solicitante):
		self.__cedula_solicitante = cedula_solicitante

	def get_hora_inicio(self):
		return self.__hora_inicio

	def set_hora_inicio(self, hora_inicio):
		self.__hora_inicio = hora_inicio

	def get_hora_fin(self):
		return self.__hora_fin

	def set_hora_fin(self, hora_fin):
		self.__hora_fin = hora_fin

	def get_precio(self):
		return self.__precio

	def set_precio(self, precio):
		self.__precio = precio


class Bicicleta(Alquilable):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

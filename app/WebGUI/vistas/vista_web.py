# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

from controladores.controladores import PersonaControlador, VisitaMenorControlador, VisitaControlador, BicicletaControlador, BicicletaConfigControlador, Respuesta
import util

# def rutas_web():

app = Flask(__name__)
app.static_folder = '../static'
app.template_folder = '../templates'

"""
@app.errorhandler(404)
def page_not_found(e):
    return "Especificó una URL inexistente para esta aplicación. Si Ud. mismo la escribió, por favor verifíquela :(", 404

@app.errorhandler(405)
def method_not_allowed(e):
    return "Este método no está permitido", 405

@app.errorhandler(500)
def method_not_allowed(e):
    return "Parece que ocurrió un error... vuelva a intentarlo más tarde", 500
"""

@app.route("/")
def home():
	# retorna a la vista principal de la aplicación
	return render_template("base.html")

@app.route("/buscar", methods=['GET'])
def buscar_persona():
	data = request.args
	cedula = data.get('cedula')

	p = PersonaControlador()
	resultado = p.buscar(cedula)

	t = resultado.template

	return render_template(t, contexto=resultado, cedula=cedula)

@app.route("/marca_visita", methods=['POST'])
def marca_visita():
	data = request.form
	
	cedula = data.get('cedula')
	accion = data.get("accion_visita")

	v = VisitaControlador()
	resultado = v.marcar_visita(cedula, accion=accion)

	t = resultado.template

	return render_template(t, contexto=resultado)

@app.route("/registrar_persona", methods=['POST'])
def registrar_persona():
	data = request.form

	cedula = data.get("cedula")
	nombre = data.get("nombre")
	apellido = data.get("apellido")
	edad = data.get("edad")
	sexo = data.get("sexo")
	
	p = PersonaControlador()

	resultado = p.crear(cedula=cedula, nombre=nombre, apellido=apellido,
			sexo=sexo, edad=edad)

	t = resultado.template

	return render_template(t, contexto=resultado)

@app.route("/bici", methods=['GET'])
def bici_home():
	return render_template("bici_base.html")


@app.route("/bici/alquilar", methods=['POST'])
def alquilar_bici_post():
	data = request.form

	cedula = data.get('cedula')
	nro_solicitado = data.get('cantidad')
	tiempo_alquiler = data.get('tiempo')

	b = BicicletaControlador()
	resultado = b.alquilar(cedula, nro_solicitado, tiempo_alquiler)

	t = resultado.template

	return render_template(t, contexto=resultado)


@app.route("/bici/alquilar", methods=['GET'])
def alquilar_bici():
	b = BicicletaControlador()
	disponible = b.cantidad_disponible()
	c = {'cantidad': range(1, disponible + 1), 'nro':disponible}
	return render_template("form_alquilar.html", contexto=c)


@app.route("/bici/devolver", methods=['POST'])
def devolver_bici_post():
	data = request.form

	cedula = data.get('cedula')

	b = BicicletaControlador()
	resultado = b.devolver(cedula)

	t = resultado.template
	print(t)

	return render_template(t, contexto=resultado)


@app.route("/bici/devolver", methods=['GET'])
def devolver_bici():
		return render_template("form_devolver.html", contexto={})


@app.route("/bici/config", methods=['GET'])
def config_bici():
		return render_template("form_config_bici.html", contexto={})

@app.route("/bici/config", methods=['POST'])
def config_bici_post():
	data = request.form

	monto_new = data.get('monto_new')
	
	print(monto_new)

	bici_config = BicicletaConfigControlador()
	
	resultado = bici_config.set_monto_hora(monto_new)

	t = resultado.template

	return render_template(t, contexto=resultado)



def iniciar_app():
	app.run(debug=True, host="0.0.0.0")


# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

from controladores import PersonaControlador, VisitaMenorControlador, VisitaControlador, BicicletaControlador, Respuesta
import util

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("base.html")


@app.route("/buscar", methods=['GET'])
def buscar_persona():
	data = request.args
	cedula = data.get('cedula')

	p = PersonaControlador()
	resultado = p.buscar(cedula)

	t = resultado.template

	return render_template(t, contexto=resultado, cedula=cedula)

@app.route("/marca_entrada", methods=['POST'])
def marca_visita():
	data = request.form

	if 'entrada' in data:
		print("Quiero ENTRADA")

	elif 'salida' in data:
		print("Quiero SALIDA")

	return render_template("base.html")

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

if __name__ == "__main__":
    app.run(debug=True)



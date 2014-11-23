# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
	
	c = {'var1': 'soy var1',
	'var2': 'soy var2',
	'var3': 'soy var3',
	'var4': 'soy var4',
	}

	return render_template("base.html")


@app.route("/buscar", methods=['GET'])
def buscar_persona():
	data = request.args
	print data

	cedula = data.get('cedula')

	if 'buscar' in data:
		print "Se solicita búsqueda"
	
	print cedula

	contexto = {
				'cedula': cedula,
	}

	return render_template("persona_tabla.html", contexto=contexto)

@app.route("/marca_entrada", methods=['POST'])
def marca_visita():
	data = request.form

	if 'entrada' in data:
		print "Quiero ENTRADA"

	elif 'salida' in data:
		print "Quiero SALIDA"

	return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)
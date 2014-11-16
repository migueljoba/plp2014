from tkinter import *

from modelos import Persona, Visitante
import shelve

from controladores import PersonaControlador

from datetime import datetime, date

# Info sobre cursores 		http://www.tcl.tk/man/tcl8.4/TkCmd/cursors.htm
# Documentacion basica 		http://effbot.org/tkinterbook/
# Estilo					http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-style-layer.html
# 	... mas Estilo ttk		https://docs.python.org/3/library/tkinter.ttk.html
# validaciones en vista 	https://www.packtpub.com/books/content/miscellaneous-tips

persona_db = "persona.db"
visitante_db = "visitante.db"

def abrir_db():
	s = shelve.open(persona_db)
	return s

def registrar_entrada():
	ahora = datetime.now()
	fecha_hoy = ahora.date()
	hora_actual = ahora.time()

	v = Visitante(fecha_visita=fecha_hoy,
				hora_entrada=hora_actual)

	# s = shelve.open(visitante_db)




def registrar_persona():
	
	cedula = entry_cedula.get()
	nombre = entry_nombre.get()
	apellido = entry_apellido.get()
	sexo = sexo_var.get()
	edad = entry_edad.get()
	extra = entry_extra.get()

	PersonaControlador().crear(cedula=cedula, nombre=nombre, 
				apellido=apellido, sexo=sexo,
				edad=edad)

def buscar_persona():

	cedula = entry_cedula.get()
	existe = PersonaControlador().existe(cedula)

	if existe:
		print(PersonaControlador().recuperar(cedula))
	else:
		print("Ahora implementar carga de nueva persona")





def borrar_persona():
	s = abrir_db()
	cedula = entry_borrar_cedula.get()

	if cedula in s.keys():
		print("Borrando cedula: " + cedula)
		del s[cedula]
	else:
		# aca pedir datos de la persona, porque no existe en la BD todavía
		print("No existe esa cedula.")

	s.close()

top = Tk()

label_cedula = Label(top, text="Cedula")
label_cedula.pack()
entry_cedula = Entry(top, bd=0)
entry_cedula.pack()

boton_buscar = Button(top, text="Buscar", width=10, command=buscar_persona)
boton_buscar.pack()



label_nombre = Label(top, text="Nombre")
label_nombre.pack()
entry_nombre = Entry(top, bd=0)
entry_nombre.pack()

label_apellido = Label(top, text="Apellido")
label_apellido.pack()
entry_apellido = Entry(top, bd=0)
entry_apellido.pack()

edad_var = IntVar()

label_edad = Label(top, text="Edad")
label_edad.pack()
entry_edad = Entry(top, textvariable=edad_var, bd=0)
entry_edad.pack()


label_extra = Label(top, text="extra")
label_extra.pack()
entry_extra = Entry(top, bd=0)
entry_extra.pack()




sexo_var = StringVar()

label_sexo = Label(top, text="Sexo")
label_sexo.pack()

fem_radio = Radiobutton(top, text="femenino", variable=sexo_var, value="F", bd=0, indicatoron=0, cursor="hand2", bg="red")
fem_radio.pack()

masc_radio = Radiobutton(top, text="masculino", variable=sexo_var, value="M",bd=0, indicatoron=0, cursor="hand2", bg="blue")
masc_radio.pack()

# label_vacio = Label(top, text="")
# label_vacio.pack()

boton_guardar = Button(top, text="Guardar", width=10, command=registrar_persona)
boton_guardar.pack()


label_buscar_cedula = Label(top, text="Buscar por cedula")
label_buscar_cedula.pack()
entry_buscar_cedula = Entry(top, bd=0)
entry_buscar_cedula.pack()

boton_buscar = Button(top, text="Buscar", width=10, command=buscar_persona)
boton_buscar.pack()


label_borrar_cedula = Label(top, text="Borrar por cedula")
label_borrar_cedula.pack()
entry_borrar_cedula = Entry(top, bd=0)
entry_borrar_cedula.pack()

boton_borrar = Button(top, text="Borrar", width=10, command=borrar_persona)
boton_borrar.pack()

top.mainloop()


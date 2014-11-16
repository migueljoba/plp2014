# http://stackoverflow.com/questions/4399180/python-tkinter-possible-to-set-the-min-max-height-or-width-of-a-tkinter-or-ttk
from tkinter import *
from tkinter.messagebox import *

persona_bd = {"4212111": {"nombre": "Miguel", "apellido": "Baez", "cedula": 4212111, "edad": 25},
}

# azul "#3998D6"
# rosado "#D06F83"

def mostrar_informacion(p):
	print(str(p))
	persona_frame.pack(side=LEFT)

def buscar_cedula():
	persona_form.pack_forget()
	persona_frame.pack_forget()

	cedula = entry_cedula.get()
	if cedula in persona_bd:
		print("HAY PERSONA")
		p = persona_bd[cedula]
		print(p)
		persona_form.pack_forget()

		mostrar_informacion(p)

	else:
		titulo = "No se encontraron registros"
		mensaje =  "No existen registros para la C.I. nro. {0}, ¿Desea cargar los datos ahora?".format(cedula)
		if askyesno(titulo, mensaje):
			print("Entra en askyesno TRUE")
			persona_form.pack(side=LEFT)

		
		persona_frame.pack_forget()
		

root = Tk()

##########################################################
# Frame principal: entrada de cédula y botón de búsqueda #
##########################################################
frame = Frame(root, width=5000, height=1000, background="#3998D6")

label_cedula = Label(frame, text="Ingrese Cédula", fg="white", bg="#3998D6", font=("Helvetica", 16))
label_cedula.place(relx=0.5, rely=0.2, anchor="s")

entry_cedula = Entry(frame, bd=0, justify=CENTER,  width=24)
entry_cedula.place(relx=0.5, rely=0.5, anchor="c")

boton_buscar_cedula = Button(frame, command=buscar_cedula, text ="Buscar", relief=FLAT, bd=0, bg="#0074C7", fg="white", width=20, height=2, activebackground="#00518B", activeforeground="white")
boton_buscar_cedula.pack(side=BOTTOM, pady=5)

frame.place(relx=.5, rely=.2, anchor="n", width=3000, height=150)


frame_dinamico = Frame(root, width=3000, height=500, background="white")


##########################################################
# Frame con botones de marcar entrada o salida           #
##########################################################
persona_frame = Frame(frame_dinamico, width=800, height=800)
label_datos = Label(persona_frame, text=str(persona_bd))
label_datos.pack()

boton_marcar_entrada = Button(persona_frame, text ="Marcar Entrada", relief=FLAT, bd=0, bg="#0074C7", fg="white", width=20, height=2, activebackground="#00518B", activeforeground="white")
boton_marcar_entrada.pack(side=LEFT, pady=5)
boton_marcar_salida = Button(persona_frame, text ="Marcar Salida", relief=FLAT, bd=0, bg="#0074C7", fg="white", width=20, height=2, activebackground="#00518B", activeforeground="white")
boton_marcar_salida.pack(side=RIGHT, pady=5)

##########################################################
# Frame que contiene a los campos para el registro de    #
# una nueva persona                                      #
##########################################################

persona_form = Frame(frame_dinamico, width=800, height=1000)

label_nombre = Label(persona_form, text="Nombre", height=3)
label_nombre.pack()
entry_nombre = Entry(persona_form, bd=0)
entry_nombre.pack(pady=5)

label_apellido = Label(persona_form, text="Apellido")
label_apellido.pack()
entry_apellido = Entry(persona_form, bd=0)
entry_apellido.pack(pady=5)

edad_var = IntVar()

label_edad = Label(persona_form, text="Edad")
label_edad.pack()
entry_edad = Entry(persona_form, textvariable=edad_var, bd=0)
entry_edad.pack()


sexo_var = StringVar()
label_sexo = Label(persona_form, text="Sexo")
label_sexo.pack()
fem_radio = Radiobutton(persona_form, text="femenino", variable=sexo_var, value="F", bd=0, indicatoron=0, cursor="hand2", bg="#D06F83")
fem_radio.pack()
masc_radio = Radiobutton(persona_form, text="masculino", variable=sexo_var, value="M",bd=0, indicatoron=0, cursor="hand2", bg="blue")
masc_radio.pack()


# persona_form.place(relx=0.5, rely=0.5, anchor="c")
# persona_form.pack(side=LEFT)

frame_dinamico.place(relx=0.5, rely=0.5, anchor="n")	# esta configuracion funciona bien


root.minsize(500,500)
root.geometry("1000x800")
root.configure(background='#FFFFFF')
root.mainloop()
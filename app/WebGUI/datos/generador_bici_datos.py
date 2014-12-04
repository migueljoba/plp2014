# Script para generar los datos para la BD de bicis
import shelve
import random
from modelos.modelos import Bicicleta

bici_db = "bicicleta.db"

s = shelve.open(bici_db)

marcas = ["Giant", "Fuji", "Scott", "Kona", "Trek"]

for i in range(1,21):

	bici = Bicicleta(id_num=str(i), marca=random.choice(marcas),
			estado="DISPONIBLE", precio_hora=10000)

	s[str(i)] = bici

s.close()







from time import sleep
from pdb import set_trace
from random import randint
import os
from threading import Thread
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
mixer.init()

mixer.music.load("sounds/init.ogg")
MISSILE= mixer.Sound("sounds/missile.ogg")
BLUM= mixer.Sound("sounds/blum.ogg")
WATER= mixer.Sound("sounds/water.ogg")
FX1= mixer.Sound("sounds/fx1.ogg")
REGISTER= mixer.Sound("sounds/register.ogg")
ERROR= mixer.Sound("sounds/error.ogg")
WHISTLE= mixer.Sound("sounds/whistle.ogg")
REGISTER.set_volume(0.7)
WINNER= mixer.Sound("sounds/winner.ogg")
NO= mixer.Sound("sounds/no.ogg")
YES= mixer.Sound("sounds/yes.ogg")
YES.set_volume(0.7)
INPUT= mixer.Sound("sounds/input.ogg")
INPUT.set_volume(0.7)

def verificar(coordenada):
	coordenada= list(coordenada)
	letra= coordenada.pop(0)
	try:
		num= int("".join(coordenada))
	except:
		return None, None
	return letra, num

class Configuraciones():
	def __init__(self):
		self.casilleros= None
		self.barcos= None
		self.letras= 2
		self.tema= None
		self.main()

	def main(self):
		canciones= {"1": ["Waka Waka", "sounds/waka-waka.ogg"], "2": ["Among us", "sounds/among-us.ogg"], "3": ["Miráculus", "sounds/miraculous.ogg"]}
		casilleros= {"1": "abcdef", "2": "abcdefgh", "3": "abcdefghij"}
		barcos= {"1": 3, "2": 4, "3": 5}
		os.system("color 2")
		print('Hola. En primer lugar configuremos un poco esto.')
		while True:
			cancion= input('¿Qué canción querés de fondo?: 1; waca waca. 2; among us. 3; miraculous')
			if not self.verify(cancion): continue
			print(f"perfecto. Seleccionaste {canciones[cancion][0]} como música de fondo.")
			self.tema= canciones[cancion][1]
			REGISTER.play()
			print("Ahora vamos con los casilleros:")
			break
		while True:
			casilleros_usuario= input("1, 6 casilleros. 2, 8 casilleros. 3, 10 casilleros")
			if not self.verify(casilleros_usuario): continue
			self.casilleros= casilleros[casilleros_usuario]
			REGISTER.play()
			print(f"Seleccionaste {len(casilleros[casilleros_usuario])} casilleros. Y por último, la cantidad de barcos por jugador")
			break
		while True:
			barcos_usuario= input("1, 3 barcos. 2, 4 barcos. 3, 5 barcos")
			if not self.verify(barcos_usuario): continue
			self.barcos= barcos[barcos_usuario]
			REGISTER.play()
			print(f"Seleccionaste que sean {barcos[barcos_usuario]} barcos por jugador. ¡Ahora sí!, a jugar...")
			input()
			break

	def verify(self, valor):
		if valor in ["1", "2", "3"]:
			return True
		else:
			print(f"{valor}, es un valor incorrecto. Solo puedes escribir los números; 1, 2, o 3. Vamos otra vez")
			return False

class Jugador():
	def __init__(self):
		self.nombre= None
		self.barcos= []
		self.restantes= []
		self.start()

	def start(self):
		INPUT.play()
		while True:
			nombre= input("Ingresá tu nombre y pulsá intro")
			if nombre =="":
				continue
			else:
				self.nombre= nombre
				break
		print(f"Hola {self.nombre}. Ahora vamos a seleccionar las casillas donde esconder tus preciados barcos...")
		input("Pulsá intro para comenzar la selección")
		self.seleccionar_barcos()
		print("¡Listo! Ya están seleccionados tus barcos.")
		for l in configuraciones.casilleros:
			for n in range(len(configuraciones.casilleros)):
				self.restantes.append("".join([l,str(n+1)]))
		pregunta= input("Querés que te diga cuales son las casillas seleccionadas? escribí la letra s y pulsá intro. Sino solo intro")
		if pregunta == "s":
			print("\n".join(self.barcos))
			input("intro para continuar")

	def seleccionar_barcos(self):
		x= 1
		print(f"Ingresá una letra desde la a, hasta la {configuraciones.casilleros[-1]}. Luego un número del 1 al {len(configuraciones.casilleros)}, e intro para finalizar:")
		FX1.play()
		while True:
			if len(self.barcos) == configuraciones.barcos: break
			coordenada= input(f'Barco {x}')
			letra, num= verificar(coordenada)
			if not letra: continue
			if letra in configuraciones.casilleros and num <= len(configuraciones.casilleros):
				if not coordenada in self.barcos:
					self.barcos.append(coordenada)
					print(coordenada)
					FX1.play()
					x+=1
				else:
					print("Esa casilla está ocupada!, probá con otra....")
					ERROR.play()
					continue
			else:
				print("Datos incorrectos. Volvé a intentarlo")
				ERROR.play()
				continue

mixer.music.load("sounds/init.ogg")
mixer.music.play(-1)

print("Battalla naval")
sleep(2)
configuraciones= Configuraciones()

jugador_1= Jugador()
REGISTER.play()
input(f'Listo {jugador_1.nombre}. ✌. Que pase el que sigue')
jugador_2= Jugador()
mixer.music.stop()
WHISTLE.play()
print(f'Listo {jugador_2.nombre}. ✌.¡A prepararse para la batalla!')
input("intro para continuar")

jugadores= [jugador_1, jugador_2]
print('Y el jugador que va a comenzar es...')
sleep(2)
aleatorio= randint(0,1)
print(f'¡{jugadores[aleatorio].nombre}!')
sleep(1)
j1,j2=jugadores.pop(aleatorio),jugadores.pop()

mixer.music.load(configuraciones.tema)
mixer.music.set_volume(0.4)
mixer.music.play(-1)

input('¡Que comience el juego! Pulsá intro para iniciar la partida')

def winner():
	while True:
		sleep(5)
		print(f"¡{j1.nombre}! victoria! ¡victoria! ¡victoria!")
		sleep(5)
		print(f"¡Felicitaciones {j1.nombre}!")

def finish():
	mixer.music.stop()
	YES.play()
	sleep(3)
	WINNER.play()
	Thread(target=winner, daemon= True).start()
	sleep(WINNER.get_length())
	exit()

def disparar(coordenada):
	MISSILE.play()
	sleep(MISSILE.get_length()-1)
	if coordenada in j2.barcos:
		j2.barcos.remove(coordenada)
		j2.restantes.remove(coordenada)
		if len(j2.barcos) > 0:
			BLUM.play()
			if len(j2.barcos) == 1:
				NO.play()
				sleep(BLUM.get_length()-5)
				print(f"¡Jaque mate! {j2.nombre} tiene solo un barco en su flota...")
			else:
				YES.play()
				sleep(BLUM.get_length()-5)
			return True
		else:
			finish()
	else:
		WATER.play()
		j2.restantes.remove(coordenada)
		sleep(WATER.get_length()-2)
		return False

def estadoActual(op):
	mixer.music.pause()
	if op == 1:
		print(f'{j1.nombre} tiene {len(j1.barcos)} en su flota.')
		print(f'{j2.nombre} tiene {len(j2.barcos)} en su flota')
	else:
		print(f"{j2.nombre} tiene disponibles las siguientes casillas; {'. '.join(j2.restantes)}")
	input("pulsá intro para continuar el juego")
	mixer.music.unpause()

while True:
	coordenada= input(f'{j1.nombre}; escribe las cordenadas y pulsa intro para disparar tu misil')
	if coordenada == "": continue
	if coordenada == "p":
		estadoActual(1)
		continue
	elif coordenada == "r":
		estadoActual(2)
		continue
	letra, num= verificar(coordenada)
	if not letra: continue
	if letra in configuraciones.casilleros and num <= len(configuraciones.casilleros):
		if not coordenada in j2.restantes:
			ERROR.play()
			print(f'La coordenada {coordenada} ya fué disparada. Probá con una diferente...')
			continue
		else:
			disparar(coordenada)
	else:
		print(f'La coordenada; {coordenada}, no es válida.')
		continue
	j1,j2=j2,j1


#Módulo de fecha
import datetime

print(datetime.date.today())

fecha_complete = datetime.datetime.now()
print(fecha_complete)
print(fecha_complete.year)
print(fecha_complete.month)
print(fecha_complete.day)

fecha_personalizada = fecha_complete.strftime("%d/%m/%Y")
print(fecha_personalizada)
print(datetime.datetime.now().timestamp())

#Módulo matemáticas
import math

print(f"Raíz cuadrada de 10: {math.sqrt(10)}") 
print(f"Número pi: {math.pi}")
print(f"Redondear {math.ceil(6.565656)}") #Redondear arriba
print(f"Redondear {math.floor(6.565656)}") #Redondear abajo

#Módulo random
import random
print(f"Número aleatorio entre 1 y 10: {random.randint(1,10)}")

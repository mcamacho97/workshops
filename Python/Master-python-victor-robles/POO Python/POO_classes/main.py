# Programación orientada a objetos (PO0)
# RECORDAR:
# Clase es un molde para crear objetos.
# Un objeto es una instancia de una clase.
# Un atributo o propiedad es una variable dentro de una clase.
# Un método es una función dentro de una clase.


# Definición de la clase vehículo
class Coche:

    # Atributos o propiedades de la clase
    color = "Rojo"
    marca = "Ferrari"
    modelo = "Aventador"
    velocidad = 300
    caballaje = 500
    plazas = 2

    # Métodos (función) de la clase
    def setColor(self, color):
        self.color = color
    
    def getColor(self):
        return self.color

    def setModelo(self, modelo):
        self.modelo = modelo
    
    def getModelo(self):
        return self.modelo

    def acelerar(self):
        self.velocidad += 1
    
    def frenar(self):
        self.velocidad -= 1

    def getVelocidad(self):
        return self.velocidad
    

# Instanciando la clase Coche
miCoche = Coche()

miCoche.setColor("Azul")
miCoche.setModelo("Murciélago")
print("COCHE 1")

print(miCoche.marca, miCoche.getColor(), miCoche.getModelo())
# print("Velocidad actual", miCoche.getVelocidad())
# miCoche.acelerar()
# miCoche.acelerar()
# miCoche.acelerar()
# miCoche.acelerar()
# miCoche.frenar()
# print("Velocidad nueva", miCoche.getVelocidad())

print("------------------------------------------------------")
print("COCHE 2")
# Crear más objetos
coche2 = Coche()
coche2.setColor("verde")
coche2.setModelo("Gallardo")

print(coche2.marca, coche2.getColor(), coche2.getModelo())
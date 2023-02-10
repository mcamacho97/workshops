# Programación orientada a objetos (PO0)
# RECORDAR:
# Clase es un molde para crear objetos.
# Un objeto es una instancia de una clase.
# Un atributo o propiedad es una variable dentro de una clase.
# Un método es una función dentro de una clase.


# Definición de la clase vehículo
class Coche:
    
    soy_publico = "Hola, soy un atributo público"
    __soy_privado = "Hola, soy un atributo privado" # Atributo privado por el guión bajo

    # Constructor
    def __init__(self, color, marca, modelo, velocidad, caballaje, plazas):
        self.color = color
        self.marca = marca
        self.modelo = modelo
        self.velocidad = velocidad
        self.caballaje = caballaje
        self.plazas = plazas

    # Métodos (función) de la clase
    def getPrivado(self):
        return self.__soy_privado

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
    
    def getMarca(self):
        return self.marca

    def setMarca(self, marca):
        self.marca = marca
    
    def getInfo(self):
        info = "Color: " + self.color + "\n"
        info += "Marca: " + self.marca + "\n"
        info += "Modelo: " + self.modelo + "\n"
        info += "Velocidad: " + str(self.velocidad) + "\n"
        info += "Caballaje: " + str(self.caballaje) + "\n"
        info += "Plazas: " + str(self.plazas) + "\n"
        return info
        
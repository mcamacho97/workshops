# Herencia, posibilidad de compartir atributos entre clases padre-hijo
# y compartir metodos entre clases padre-hijo

class Persona:
    def get_nombre(self):
        return self.nombre
    
    def get_apellidos(self):
        return self.apellidos
    
    def get_altura(self):
        return self.altura
    
    def get_edad(self):
        return self.edad

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_apellidos(self, apellidos):
        self.apellidos = apellidos
    
    def set_altura(self, altura):
        self.altura = altura
    
    def set_edad (self, edad):
        self.edad = edad

    def hablar(self):
        return "Estoy hablando"

    def caminar(self):
        return "Estoy caminando"

    def dormir(self):
        return "Estoy durmiendo"

class Informatico(Persona):
    def __init__(self):
        self.lenguajes = "Python"
        self.experiencia = 5
        self.habilidades = "programacion orientada a objetos"
    
    def get_lenguajes(self):
        return self.lenguajes
    
    def aprender(self, lenguajes):
        self.lenguajes = lenguajes
        return self.lenguajes

    def programar(self):
        return "Estoy programando"

    def reparar_PC(self):
        return "Estoy reparando PC"	

class TecnicoRedes(Informatico):
    def __init__(self):
        super().__init__() # invocamos al constructor de la clase padre
        self.auditar_redes = "Experto"
        self.experienciaRedes = 15
    
    def auditoria(self):
        return "Estoy auditando redes"
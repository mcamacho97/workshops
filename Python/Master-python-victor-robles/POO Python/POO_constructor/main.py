from coche import Coche

carro = Coche("Amarillo", "Honda", "Civic", 150, 200, 4)

print(carro.getInfo())


# Detectar tipado
if type(carro) == Coche:
    print("Es un objeto de la clase Coche")
else:
    print("No es un objeto de la clase Coche")

# Visibilidad
print(carro.soy_publico)
print(carro.getPrivado())
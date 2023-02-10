cantantes = ["2pac", "Drake", "Bad Bunny", "Julio Iglesias"]
numeros = [1, 2, 3, 6, 9, 10, 3]

# Ordenar
print(numeros)
numeros.sort()
print(numeros)

# Añadir elementos
cantantes.append("Gustavo Cerati") # Agrega un elemento al final de la lista
cantantes.insert(1, "Axl Rose") # Inserta un elemento en una posición específica
print(cantantes)

# Eliminar elementos
cantantes.pop(1) #Elimina el elemento en la posición 1
cantantes.remove("Bad Bunny") #Elimina el elemento "Bad Bunny"
print(cantantes)

# Lista reversa
print(numeros)
numeros.reverse()
print(numeros)

# Buscar dentro de una lista
print('Drake' in cantantes)

# Contar elementos
print(len(cantantes))

# Cuantas veces aparece un elemento
numeros.append(1)
print(numeros.count(1))

# Conseguir índice de un elemento
print(cantantes.index("Drake"))

# Unir listas
cantantes.extend(numeros)
print(cantantes)
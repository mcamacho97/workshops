numbers = [1, 3, 2, 4, 6, 5, 7, 8]
numbers_lenght = len(numbers)
numbers_ordered = sorted(numbers)

def show_list(list_to_show):
    result = ""
    for element in list_to_show:
        result += "Elemento "+ str(element)
        result += "\n"
    return result

# Reocrrer y mostrar
print("######## Recorrer y mostrar ########")
print(show_list(numbers))

# Ordenar y mostrar
print("######## Ordenar y mostrar ########")
numbers_ordered = sorted(numbers)
print(show_list(numbers_ordered))

# Mostrar su longitud
print("######## Mostrar Longitud ########")
print("La longitud de la lista es: " + str(numbers_lenght))

# Búsqueda en la lista
print("######## Búsqueda en la lista ########")
search_input = int(input("Introduce un número en la lista: "))

validation = isinstance(search_input, int)

while not validation or search_input <= 0:
    search_input = int(input("Introduce un número en la lista: "))
else:
    print(f"Has introducido el número {search_input}")
    numbers.append(search_input)

print(f"#### Buscar en la lista el número {search_input} #####")
search = numbers.index(search_input)
print(f"El número {search_input} se encuentra en la posición {search} de la lista")
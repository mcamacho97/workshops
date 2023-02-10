pelicula = "Batman"

# Definir lista
peliculas = ["Batman", "Superman", "Spiderman"]
cantantes = list(('Juan', 'Pedro', 'Ana'))
years = list(range(1980, 2020))
variada = ["Mauricio", 30, 4.4, True]

# Indices
print(peliculas[1])
print(peliculas[-1])
print(cantantes[0:2])
print(peliculas[1:])

# Añadir elementos a la lista
cantantes.append("Cerati")
print(cantantes)

# # Recorrer lista
# print("*********  Lista de Películas ***********")

# nueva_pelicula = ""
# while nueva_pelicula != "stop":
#     nueva_pelicula = input("Introduce una película: ")

#     if nueva_pelicula != "stop":
#         peliculas.append(nueva_pelicula)

# for pelicula in peliculas:
#     print(f"{peliculas.index(pelicula)+1}. {pelicula}")

# Lista multidimensionales
print("\n*********  Lista de contactos ***********")
contactos = [
    [
        "Juan",
        "juan@juan.com",
    ],
    [
        "Pedro",
        "pedro@pedro.com",
    ],
    [
        "Luis",
        "luis@luis.com",
    ],
    [
        "Mauricio",
        "mcm@mcm.com",
    ],
]

# Recorrer lista de contactos
for contacto in contactos:
    for elemento in contacto:
        if contacto.index(elemento) == 0:
            print("Nombre: " + elemento)
        else:
            print("Correo: " + elemento)
    print("\n")
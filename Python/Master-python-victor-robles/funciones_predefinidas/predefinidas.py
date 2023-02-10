nombre = "Mauricio"

# funciones generales
print(type(nombre))

# Detectar el tipado
comprobar = isinstance(nombre, str)
if comprobar:
    print("Es una cadena")
else:
    print("No es una cadena")

# Limpiar espacios
frase = "      mi contenido      "
print(frase)
print(frase.strip())

# Eliminar variables
year = 2022
print(year)
del year
# print(year)

# Comprobar variable vacia
texto  = " ff "

if len(texto) <= 0:
    print("La variable esta vacia")
else:
    print(f"La variable no esta vacia, tiene {len(texto)} caracteres")

# Encontrar caracteres
frase = "La vida es bella"
print(frase.find("vida"))

# Reemplazar caracteres
nueva_frase = frase.replace("vida", "moto")
print(nueva_frase)

# Mayúsculas y minúsculas
print(nombre)
print(nombre.lower())
print(nombre.upper())
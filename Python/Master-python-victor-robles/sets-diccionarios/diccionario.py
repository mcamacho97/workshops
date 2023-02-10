"""
Diccionario es un tipo de datos que almacena un conjunto de datos
Formato key:value
"""

persona = {
    "nombre": "Juan",
    "apellido": "Perez",
    "edad": 25,
}

print(persona['edad'])

# Lista con diccionarios
contactos = [
    {"nombre": "Juan", "telefono": 123456789},
    {"nombre": "Mauricio", "telefono": 23232323},
    {"nombre": "Francys", "telefono": 121212},
    {"nombre": "Claudia", "telefono": 232323},
]
contactos[0]['nombre'] = 'Toño'
print(contactos[0]['nombre'])

print("\n Lista con contactos: ")
print("----------------------------------")

for contacto in contactos:
    print(f"Nombre del contacto: {contacto['nombre']}")
    print(f"Nombre del contacto: {contacto['telefono']}")
    print("----------------------------------")
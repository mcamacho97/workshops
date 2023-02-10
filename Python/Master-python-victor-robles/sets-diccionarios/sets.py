"""
SET es un tipo de datos para tener una colección de valores,
pero no tiene ni indice ni orden
"""

personas = {
    "Mauricio",
    "Claudia",
    "Francys"
}

personas.add("Antonio")
personas.remove("Mauricio")

print(personas)
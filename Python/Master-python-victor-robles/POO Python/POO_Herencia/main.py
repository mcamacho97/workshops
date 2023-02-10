import clases

persona = clases.Persona()
persona.set_nombre("Mauricio")
persona.set_apellidos("Camacho")
persona.set_altura("172cm")
persona.set_edad("25 años")

print(f"La persona es: {persona.get_nombre()} {persona.get_apellidos()}")
print(f"Su altura es: {persona.get_altura()}")
print(persona.hablar())

informatico = clases.Informatico()
informatico.set_nombre("Juan")
informatico.set_apellidos("Garcia")

print(f"El informatico es: {informatico.get_nombre()} {informatico.get_apellidos()}")
print(informatico.get_lenguajes())
print(informatico.caminar())

tecnico = clases.TecnicoRedes()
tecnico.set_nombre("Manuel")
print(tecnico.auditar_redes, tecnico.get_nombre(), tecnico.get_lenguajes())
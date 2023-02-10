from io import open
import pathlib
import shutil

# Abrir archivo

#__file__ is the path to the current file
path = str(pathlib.Path(__file__).parent.absolute()) + "/fichero_copiado.txt"
print(path)
file_object= open(path, "a+") # a+ es para leer y escribir

# Escribir en el archivo
file_object.write("Soy un texto de prueba\n")

# Cerrar archivo
file_object.close()

# Abrir archivo
path = str(pathlib.Path(__file__).parent.absolute()) + "/archivo_texto.txt"
file_object= open(path, "r") # r es para leer

# Leer archivo
content = file_object.read()
print(content)

# Leer contenido y guardar en lista
content_lines = file_object.readlines()
file_object.close()
print(content_lines)

for element in content_lines:
    print(f"- {element.capitalize()}")

# Copiar archivo
original_path = str(pathlib.Path(__file__).parent.absolute()) + "/archivo_texto.txt"
new_path = str(pathlib.Path(__file__).parent.absolute()) + "/archivo_texto_copiado.txt"
shutil.copy(original_path, new_path)

# Mover archivo / Renombrar
original_path = str(pathlib.Path().parent.absolute()) + "/fichero_copiado.txt"
new_path = str(pathlib.Path().parent.absolute()) + "/fichero_texto.txt"

shutil.move(original_path, new_path)

# Eliminar archivo
import os
original_path = str(pathlib.Path(__file__).parent.absolute()) + "/archivo_texto.txt"
os.remove(original_path)

# Comprobar si existe un archivo
import os.path

print(os.path.abspath(__file__)) #abspath() devuelve la ruta absoluta del archivo
print(os.path.exists("fichero_copiado.txt")) #exists() devuelve True o False si existe o no el archivo
print(os.path.isfile("fichero_copiado.txt")) #isfile() devuelve True o False si es un archivo o no))
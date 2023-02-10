import os
import shutil

# Crear carpeta
if not os.path.isdir("./mi_carpeta"):
    os.mkdir("./mi_carpeta")
else:
    print("Ya existe la carpeta")

# Eliminar carpeta
os.rmdir("./mi_carpeta")

# Copiar una carpeta
original_path = './mi_carpeta'
new_path = './mi_carpeta_copia'

shutil.copy(original_path, new_path)

# Ver contenido de carpeta
print("Contenido de mi carpeta")
folder_content = os.listdir("./mi_carpeta")

for file_object in folder_content:
    print(f"Fichero: {file_object}")

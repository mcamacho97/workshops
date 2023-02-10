# Importar módulo
import sqlite3

# Conexión a la base de datos
conexion = sqlite3.connect('pruebas.db')

# Crear un cursor
cursor = conexion.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(100),
    descripcion TEXT,
    precio INT(255)
    )
""")

# Guardar cambios
conexion.commit()

# Insertar datos
# cursor.execute("""
#     INSERT INTO productos VALUES(NULL, 'Primer Producto', 'Pantalón azul', 15000)
# """
# )
# conexion.commit()

# Borrar registros
# cursor.execute("""
#     DELETE FROM productos
# """)
# conexion.commit()


# Insertar muchos productos
productos = [
    ("Ordenador", "Laptop", 800),
    ("Ordenador", "Laptop", 600),
    ("Ordenador", "Laptop", 1000),
    ("Ordenador", "Laptop", 200),
]
cursor.executemany("INSERT INTO productos VALUES(NULL,?,?,?)", productos)
conexion.commit()

# Update
cursor.execute("""
    UPDATE productos WHERE precio = 80
""")


# Listar datos
cursor.execute("SELECT * FROM productos")
productos = cursor.fetchall()

for producto in productos:
    print(producto[1])
    print(producto[2])

producto = cursor.fetchone()

# Cerrar conexión
conexion.close()

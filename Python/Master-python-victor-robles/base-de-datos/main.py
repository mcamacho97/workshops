import mysql.connector

#Connecting to the database
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",	
    database="master_python",
)
# Creating a cursor object using the cursor() method
cursor = database.cursor()

# # Creating a new database
# cursor.execute("CREATE DATABASE IF NOT EXISTS master_python")

# cursor.execute("SHOW DATABASES")

# for bd in cursor:
#   print(bd)

# Creating a new table
cursor.execute("""
CREATE TABLE IF NOT EXISTS vehiculos(
    id int(10) auto_increment not null,
    marca varchar(50) not null,
    modelo varchar(50) not null,
    precio float(10,2) not null,
    CONSTRAINT pk_vehiculo PRIMARY KEY (id)
)
""")
cursor.execute("SHOW TABLES")

for table in cursor:
  print(table)

# Inserting a new record
cursor.execute("INSERT INTO vehiculos VALUES(null, 'Opel', 'Astra', '18500')")
# Duplas de coches
coches = [
    ('Seat', 'Ibiza', 5000),
    ('Renault', 'Clio', 15000),
    ('Citroen', 'Saxo', 2000),
    ('Mercedes', 'Clase C', 35000)
]

# Inserting multiple records using executemany() method
cursor.executemany("INSERT INTO vehiculos VALUES (null, %s, %s, %s)", coches)
database.commit()

# Showing the data
cursor.execute("SELECT * FROM vehiculos WHERE precio <= 5000 AND marca = ''")
result = cursor.fetchall()

print("-------------TODOS MIS COCHES-------------")
for coche in result:
    print(coche[1], coche[3])

# Deleting a record
cursor.execute("DELETE FROM vehiculos WHERE marca = 'Opel'")
database.commit()
print(cursor.rowcount, "borrados!")

# Updating a record
cursor.execute("UPDATE vehiculos SET modelo = 'León' WHERE marca = 'Seat'")
database.commit()
print(cursor.rowcount, "actualizados!")
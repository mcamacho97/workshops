# Capturar excepciones y manejar errores de código
# susceptible a fallos/errores

# Manejar una excepción de manera genérica
try:
    nombre = input("Ingrese su nombre: ")

    if len(nombre) > 1:
        nombre_usuario = "El nombre es " + nombre

    print(nombre_usuario)
except:
    print("Error en el nombre")
else:
    print("Ejecutado correctamente")
finally:
    print("Fin del programa")

# Manejar múltiples excepciones de manera genérica
try:
    numero = int(input("Ingrese un número para elevarlo al cuadrado: "))
    print("El cuadrado es: ", str(numero * numero))
except TypeError:
    print("Debes de convertir tus cadenas a enteros")
except ValueError:
    print("Debes ingresar números enteros")
except Exception as e:
    print(f"Ha ocurrido un error: {type(e)}")
    print(f"Ha ocurrido un error: {e}")
    print("Ha ocurrido un error: ", type(e).__name__) #__name__ es el nombre del módulo

# Excepciones personalizadas
try:
    nombre = input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad: "))

    if edad < 5 or edad > 110:
        raise ValueError("La edad no es válida")
    elif len(nombre) <= 1:
        raise ValueError("El nombre no es válido")
    else:
        print("Ejecutado correctamente")
except ValueError:
    print("Error en la edad o el nombre")
except Exception as e:
    print("Ha ocurrido un error: ", e)
def holamundo(nombre):
    return f"Hola {nombre}"

def calculadora(number_1, number_2, basic = False):
    suma = number_1 + number_2
    rest = number_1 - number_2
    mul = number_1 * number_2
    division = number_1 / number_1

    string = ""

    if basic != False:
        string += f"Suma: {number_1} + {number_2} = {suma}\n"
        string += f"Resta: {number_1} - {number_2} = {rest}\n"
    else:
        string += f"Multiplicación: {number_1} * {number_2} = {mul}\n"
        string += f"División: {number_1} / {number_2} = {division}\n"
    
    return string
    
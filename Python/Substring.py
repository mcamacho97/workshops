"""users = users.withColumn("UserFirstName",substring_index(users.UserFullName," ",1)) \
                    .withColumn("UserLastName",when(isnull(col("UserLastName")) , substring_index(users.UserFullName," ",-2)) \
                    .otherwise(substring_index(users.UserFullName," ",-2)))"""

CLI_NombreCompleto_First = "\x04\x04\x04\x04\Test"
if len(CLI_NombreCompleto_First) >= 10 :
    print("ERROR NUMERO DE CARACTERES")
    splitString = CLI_NombreCompleto_First.split(" ")
    print(splitString)
    CLI_NombreCompleto_First = splitString[0]
    print(CLI_NombreCompleto_First)

else:
    print("PASO")

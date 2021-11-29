def unir_nombre(primer_nombre, apellido):
    return primer_nombre + apellido


unir_nombre("juanito", "perez")  # 'juanito perez'
unir_nombre(1, 2)  # 3


def unir_nombre_2(primer_nombre: str, apellido: str):
    return primer_nombre + apellido


unir_nombre_2("juanito", "perez")
unir_nombre_2(1, 2)


def unir_nombre_3(primer_nombre: str, apellido: str, edad):
    return primer_nombre + apellido + edad


unir_nombre_3("juanito", "perez", 3)


def unir_nombre_4(primer_nombre: str, apellido: str, edad: int) -> str:
    return primer_nombre + apellido + str(edad)


a = unir_nombre_4("juanito", "perez", 3)

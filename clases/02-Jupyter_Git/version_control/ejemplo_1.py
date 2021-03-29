# Ejemplo 1: Control de versiones
# TODO: agregar descripción eval

D = {'atributo_1':'negro','atributo_2':'1312'}
with open("dict.txt", "w") as outfile:
    outfile.write(str(D))

with open("dict.txt", "r") as infile:
    dict_items = infile.read()

a = 'primer ejemplo de control de versiones' 
print(a)

D_final = eval(dict_items)
print(D_final)

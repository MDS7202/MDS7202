# Se define la clase base Zord
class DinoZord:
    '''Clase base ejemplo.
    '''
    def __init__(self, nombre, color, habilidad, largo, ancho, velocidad):
        self.nombre = nombre
        self.color = color
        self.habilidad = habilidad
        self.largo = largo
        self.ancho = ancho
        self.velocidad = velocidad

    # Método de ataque
    def attack(self):
        print(f'⚔️ {self.nombre.title()} ataca usando {self.habilidad} !! ⚔️')

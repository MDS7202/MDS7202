from src.zords.dinozord import DinoZord


class Pterodactyl(DinoZord):
    '''Clase derivada - Herencia simple'''

    def __init__(self):
        super().__init__(nombre='Pterodactyl Dinozord',
                         color='pink',
                         habilidad='twin lasers',
                         largo=21,
                         ancho=84,
                         velocidad='match 2.5')

    # Método protegido de ensamblaje
    def _modo(self):
        if self.pilot:
            print(self.pilot + ' dice: ensamblando pecho')

    def boost_defense(self):
        print('Zord con defensa mejorada')

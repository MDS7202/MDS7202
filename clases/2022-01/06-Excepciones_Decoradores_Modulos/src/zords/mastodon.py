from src.zords.dinozord import DinoZord


class Mastodon(DinoZord):
    '''Clase derivada - Herencia simple'''

    def __init__(self):
        super().__init__(nombre='Mastodon Dinozord',
                         color='black',
                         habilidad='frigid blasts of cold air',
                         largo=24.7,
                         ancho=108,
                         velocidad=120)

    # Método protegido de ensamblaje
    def _modo(self):
        if self.pilot:
            print(self.pilot + ' dice: ensamblando espalda y brazos')

    def boost_strength(self):
        print('Zord con fuerza mejorada')

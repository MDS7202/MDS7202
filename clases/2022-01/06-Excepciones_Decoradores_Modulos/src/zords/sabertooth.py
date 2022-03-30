from src.zords.dinozord import DinoZord


class Sabertooth(DinoZord):
    '''Clase derivada - Herencia simple'''

    def __init__(self):
        super().__init__(nombre='Sabertooth Tiger Dinozord',
                         color='yellow',
                         habilidad='large yellow laser',
                         largo=37.3,
                         ancho=141,
                         velocidad=140)

    # Método protegido de ensamblaje
    def _modo(self):
        if self.pilot:
            print(self.pilot + ' dice: ensamblando pierna derecha')

    def boost_agility(self):
        print('Zord con agilidad mejorada')

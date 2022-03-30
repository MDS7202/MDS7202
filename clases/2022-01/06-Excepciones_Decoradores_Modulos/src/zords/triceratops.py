from src.zords.dinozord import DinoZord


class Triceratops(DinoZord):
    '''Clase derivada - Herencia simple'''

    def __init__(self):
        super().__init__(nombre='Triceratops Dinozord',
                         color='blue',
                         habilidad='laser shots',
                         largo=37.3,
                         ancho=141,
                         velocidad=140)

    # Método protegido de ensamblaje
    def _modo(self):
        if self.pilot:
            print(self.pilot + ' dice: ensamblando pierna izquierda')

    def boost_endurance(self):
        print('Zord con resistencia mejorada')

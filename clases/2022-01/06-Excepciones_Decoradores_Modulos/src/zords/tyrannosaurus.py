from src.zords.dinozord import DinoZord


class Tyrannosaurus(DinoZord):
    '''Clase derivada - Herencia simple'''

    # Se utililiza el método constructor directamente desde la clase base
    def __init__(self):
        super().__init__(nombre='Tyrannosaurus Dinozord',
                         color='red',
                         habilidad='fire energy blasts',
                         largo=45,
                         ancho=96,
                         velocidad=120)

    # Método protegido de ensamblaje
    def _modo(self):
        if self.pilot:
            print(self.pilot + ' dice: ensamblando torso y cabeza')

    def boost_dexterity(self):
        print('Zord con destreza mejorada')

from src.zords.dinozord import DinoZord
from src.zords.mastodon import Mastodon
from src.zords.pterodactyl import Pterodactyl
from src.zords.sabertooth import Sabertooth
from src.zords.triceratops import Triceratops
from src.zords.tyrannosaurus import Tyrannosaurus


class MegaZord(Tyrannosaurus, Mastodon, Triceratops, Sabertooth, Pterodactyl):
    '''Clase derivada - Ejemplo herencia multiple'''

    # Constructor

    def __init__(self, tyrannosaurus, mastodon, triceratops, sabertooth,
                 pterodactyl):

        # Secuencia de ensamblaje
        tyrannosaurus._modo()
        mastodon._modo()
        triceratops._modo()
        sabertooth._modo()
        pterodactyl._modo()
        '''
        Constructor de caracteristicas base usando la clase base DinoZord, 
        observe que no se declaro explicitamente como clase base al definir
        MegaZord, sin embargo sus atributos se heredan.
        
        '''

        DinoZord.__init__(self, nombre='Mega Zord',
                          color='Multicolor',
                          habilidad='Power Sword',
                          largo=67,
                          ancho=570,
                          velocidad=140)

        # variables de la clase
        self._components = (tyrannosaurus, mastodon, triceratops, sabertooth,
                            pterodactyl)
        self._mode = 'tank_mode'

        # asignación de piloto
        self.pilot = [zord.pilot for zord in self._components]

        # Fin secuencia de construcción
        print()
        print(f'⚔️ Megazord activado en {self._mode}! ⚔️')

    ''' Metodos: overriding y metodos nuevos.'''

    # method overriding
    def _modo(self):
        return self._mode

    # Nueva funcionalidad: wrapper de métodos heredados por herencia multiple
    def boost(self):
        self.boost_dexterity()
        self.boost_defense()
        self.boost_agility()
        self.boost_endurance()
        self.boost_strength()

    # Nueva funcionalidad: cambio de modo
    def change_mode(self):
        if self._mode == 'battle_mode':
            print('Cambiando a Tank Mode')
            self._mode = 'tank_mode'

        else:
            print('Cambiando a Battle Mode')
            self._mode = 'battle_mode'

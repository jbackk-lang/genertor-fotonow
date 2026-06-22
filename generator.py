from pole import Pole
from foton import Foton

def generuj_foton(pole):
    energia = pole.energia_pola()
    return Foton(energia)

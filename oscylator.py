from pole_dualne import PolaDualne
from generator_dualny import generuj_foton_z_pola

class Oscylator:
    def __init__(self, skretA, skretB):
        self.pola = PolaDualne(skretA, skretB)
        self.stan = 0  # 0 = A aktywne, 1 = B aktywne

    def tik(self):
        # przełączanie stanu
        self.stan = 1 - self.stan

        if self.stan == 0:
            aktywne = self.pola.pole_A
        else:
            aktywne = self.pola.pole_B

        return generuj_foton_z_pola(aktywne)

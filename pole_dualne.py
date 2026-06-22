class Pole:
    def __init__(self, skret=0.0):
        self.skret = skret

    def energia(self):
        return abs(self.skret) * 0.001


class PolaDualne:
    def __init__(self, skret1, skret2):
        self.pole_A = Pole(skret1)
        self.pole_B = Pole(skret2)

    def aktywne_pole(self):
        if self.pole_A.skret > 0 and self.pole_B.skret <= 0:
            return self.pole_A
        if self.pole_B.skret > 0 and self.pole_A.skret <= 0:
            return self.pole_B
        return None

class Pole:
    def __init__(self, skret=0.0):
        self.skret = skret

    def zmien_skret(self, delta):
        self.skret += delta

    def energia_pola(self):
        return abs(self.skret) * 0.001

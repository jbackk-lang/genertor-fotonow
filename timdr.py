class TIMDR:
    def figura(self, x):
        return x

    def widmo(self, x):
        return x[1] - x[0] if isinstance(x, tuple) else x

    def liczba(self, x):
        return x

    def dynamika(self, x):
        return x

    def filtr(self, x):
        f = self.figura(x)
        w = self.widmo(f)
        l = self.liczba(w)
        d = self.dynamika(l)
        return d

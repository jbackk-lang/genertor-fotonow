from foton import Foton

def generuj_foton_z_pola(pole):
    if pole is None:
        return None

    energia = pole.energia()
    if energia <= 0:
        return None

    return Foton(energia)

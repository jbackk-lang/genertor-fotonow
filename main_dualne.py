from pole_dualne import PolaDualne
from generator_dualny import generuj_foton_z_pola

def main():
    pola = PolaDualne(skret1=12.0, skret2=-8.0)

    aktywne = pola.aktywne_pole()
    foton = generuj_foton_z_pola(aktywne)

    print("=== DWA POLA O PRZECIWNYCH SKRĘTACH ===")
    print("Pole A:", pola.pole_A.skret)
    print("Pole B:", pola.pole_B.skret)

    if foton:
        print("Foton wygenerowany!")
        print("Energia:", foton.energia)
        print("Częstotliwość:", foton.czestotliwosc)
    else:
        print("Brak emisji — aktywne pole nie spełnia warunków.")

if __name__ == "__main__":
    main()

from oscylator import Oscylator

def main():
    osc = Oscylator(skretA=12.0, skretB=-12.0)

    print("=== OSCYLATOR DWÓCH PÓL ===")

    for i in range(10):
        foton = osc.tik()
        if foton:
            print(f"Krok {i}: FOTON → energia {foton.energia}")
        else:
            print(f"Krok {i}: brak emisji")

if __name__ == "__main__":
    main()

# Generator Fotonów (Photon Generator)

Urządzenie polowe, w którym **skręt pola elektromagnetycznego** wymusza emisję fotonów.  
Bez wybijania elektronów.  
Bez półprzewodników.  
Bez klasycznej optyki.

To **nie jest laser**.  
To **nie jest LED**.  
To **jest topologiczny generator światła**, w którym geometria i dynamika pola EM decydują o emisji.

---

## 🔥 Idea fizyczna

Model opiera się na założeniu, że:

- pole EM posiada **skręt (torsion)**, który może być dodatni lub ujemny  
- tylko **skręt dodatni** prowadzi do emisji fotonu  
- skręt ujemny jest stanem „ciemnym”  
- dwa pola o przeciwnych skrętach tworzą **oscylator**  
- oscylator generuje rytm emisji (światło impulsowe lub ciągłe)  
- TIMDR pełni rolę filtra interpretacyjnego (FIGURA → WIDMO → LICZBA → DYNAMIKA)

---

## 📁 Struktura projektu
genertor-fotonow
pole.py
foton.py
generator.py
pole_dualne.py
generator_dualny.py
oscylator.py
timdr.py
main.py
main_dualne.py
main_oscylator.py
README.md
LICENSE
design
theory


---

---

## ⚙️ Jak to działa

### 1. Pole EM
Pole ma tylko jedną cechę: **skręt**.     Pole(skret=12.0)

Energia pola jest proporcjonalna do wartości skrętu.

---

### 2. Emisja fotonu
Foton powstaje tylko wtedy, gdy:

- skręt > 0  
- energia pola > 0  

Wtedy:energia → częstotliwość → foton


---

### 3. Dwa pola o przeciwnych skrętach

A → B → A → B → ...


W każdym kroku:

- jeśli aktywne pole ma skręt dodatni → generuje foton  
- jeśli ujemny → brak emisji  

To daje **rytm światła**.

---

## ▶️ Uruchamianie

### Podstawowy generator:
python main.py

### Dwa pola:
python main_dualne.py


### Oscylator:
python main_oscylator.py


---

## 🧠 TIMDR — filtr interpretacyjny

TIMDR przetwarza dane w czterech krokach:

1. **FIGURA** – struktura wejścia  
2. **WIDMO** – różnica, przejście, skok  
3. **LICZBA** – stabilizacja  
4. **DYNAMIKA** – wynik ruchu  

Może być użyty do:

- analizy skrętu  
- modulacji emisji  
- kontroli oscylatora  
- interpretacji sygnału wyjściowego  

---

## 🚀 Co można dodać dalej

### 1. Rezonator polowy  
Model z folderu *design* — odbicia, sprzężenia, modulacja.

### 2. Operator J  
Synchronizacja skrętów, przejścia między polami, „punkt skrętu”.

### 3. Wizualizacja ASCII  
Rysowanie skrętu, energii, rytmu oscylatora.

### 4. Emisja wielopolowa  
Sieć pól → interferencje → wzory światła.

### 5. Integracja z TIMDR  
TIMDR jako warstwa sterująca oscylatorem.

### 6. Tryb ciągły  
Oscylator z samowzbudzeniem → światło ciągłe.

### 7. Tryb impulsowy  
Oscylator z modulacją → światło impulsowe.

---

## 📌 Status projektu

To jest **prototyp fizyczno‑topologiczny**.  
Celem jest zbudowanie modelu, który:

- nie używa elektronów  
- nie wymaga półprzewodników  
- generuje światło czysto polowo  
- opiera się na skręcie i topologii EM  

Projekt jest otwarty na rozwój.

---

## 📜 Licencja

MIT — możesz używać, modyfikować i rozwijać.


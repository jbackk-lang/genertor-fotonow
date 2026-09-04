# Analiza wymiarowa: skręt, krzywizna, czas — próba realnej interpretacji fizycznej

> **Status: próba fizycznej interpretacji, WYBRANA ŚWIADOMIE** (nie
> "czysta grawitacja informacyjna"). To oznacza inny standard niż
> reszta repo do tej pory: każda wielkość musi mieć realną jednostkę
> SI i realne uzasadnienie, a nie tylko nazwę. Werdykt na końcu tego
> dokumentu (§6) jest zamierzenie nieprzyjemny w jednym miejscu — to
> konsekwencja wybranej ścieżki, nie efekt uboczny, którego unikam.

## 0. Inwentarz — co obecnie istnieje w kodzie i jakie ma (nie ma) jednostki

| Wielkość | Gdzie | Obecna wartość | Jednostka SI |
|---|---|---|---|
| `skręt` | `pole.py` | dowolny float (np. 12.0, -8.0) | **brak** |
| `energia_pola()` | `pole.py` | `abs(skręt)*0.001` | zakładana jako J, ale nieuzasadniona |
| `Foton.czestotliwosc` | `foton.py` | `energia/6.626e-34` | Hz — formuła E=hf jest poprawna, WEJŚCIE nie jest |
| krok oscylatora (`tik()`) | `oscylator.py` | licznik całkowity, brak Δt | **brak** |
| `omega_input`/`omega_pivot` | `resonance_validator.py` | dowolny float | **brak** (nazwa sugeruje rad/s, kod tego nie wymusza) |
| geometria rogu | `design/photon_horn_v1.md` | długość gardzieli 0,2–0,5·λ, kąt 10–20° | m, ° — **to jedyne miejsce, gdzie już są prawdziwe jednostki** |

Wniosek z samego inwentarza, zanim jeszcze przejdziemy do fizyki:
tylko geometria (rozdział `design/`) miała od początku realne
jednostki. Wszystko, co dotyczy "skrętu" i energii, było czystymi
liczbami.

## 1. Skręt — próba identyfikacji z realną wielkością fizyczną

Realne pole EM ma dokładnie jedną znaną, zmierzoną, skwantowaną
wielkość pasującą do opisu "skręt dodatni/ujemny, topologiczny": **orbitalny
moment pędu (OAM) wiązki wirowej** (Allen, Beijersbergen, Spreeuw,
Woerdman, *Phys. Rev. A* 45, 8185 (1992) — realny, wielokrotnie
zmierzony efekt, używany m.in. w pęsetach optycznych i komunikacji
kwantowej).

- Wiązka o **ładunku topologicznym ℓ** (liczba całkowita, dodatnia,
  ujemna lub zero) ma fazę zmieniającą się jako `exp(iℓφ)` wokół osi
  propagacji — to jest dosłownie "skręt" frontu falowego, ze znakiem.
- Każdy foton w takiej wiązce niesie moment pędu wzdłuż osi
  `L_z = ℓħ`, gdzie `ħ = 1.054571817×10⁻³⁴ J·s`.
- **To jest najlepiej pasująca realna wielkość** — ma znak, jest
  topologiczna (liczba całkowita, nie dowolna ciągła), i jest
  zmierzona eksperymentalnie.

**Od razu jedno ograniczenie, którego kod dziś nie respektuje:** `ℓ`
musi być liczbą CAŁKOWITĄ. `skret=12.0` pasuje (ℓ=12), ale każda
niecałkowita wartość skrętu w tym modelu nie odpowiada niczemu
fizycznemu pod tą interpretacją.

### 1a. Krytyczne odkrycie tej analizy: energia i skręt są NIEZALEŻNE

W realnej fizyce energia fotonu zależy WYŁĄCZNIE od częstotliwości:
`E = hf = ħω`. **Nie zależy od ℓ.** Foton o ℓ=1000 i foton o ℓ=0 mogą
mieć dokładnie tę samą energię — to są dwa niezależne stopnie
swobody (energia ↔ częstotliwość; OAM ↔ struktura przestrzenna fazy).

To oznacza, że centralne założenie kodu —
`energia_pola() = abs(skręt)*0.001`, czyli "energia proporcjonalna do
skrętu" — **jest fizycznie błędne**, nie tylko źle skalibrowane. Pod
identyfikacją skręt=ℓ nie ma żadnej stałej skalującej, która by to
naprawiła, bo w prawdziwej elektrodynamice/QED energia i moment
pędu orbitalny są rachunkowo niezależne. To nie jest problem doboru
stałej — to problem struktury równania.

## 2. Energia pola — realna formuła (niezależna od skrętu)

Żeby mieć fizycznie sensowną energię, trzeba ją liczyć z amplitudy
pola, nie ze skrętu:

```
u = (ε₀E² + B²/μ₀) / 2        [J/m³]   — gęstość energii pola EM
E_całkowita = u · V_wnęki      [J]      — V z realnej geometrii rezonatora
f = c / λ                       [Hz]     — z geometrii wnęki (dokładny mod
                                           zależy od kształtu — cylindryczny/
                                           sferyczny, patrz resonator-notes.md)
```

gdzie `ε₀ = 8.8541878128×10⁻¹² F/m`, `μ₀ ≈ 1.25663706×10⁻⁶ H/m`,
`c = 2.99792458×10⁸ m/s` (dokładna, definicja SI).

**Przykład liczbowy, zakotwiczony w już istniejących parametrach z
`design/photon_horn_v1.md`** (wejście mikrofalowe, jak zapisano w
`resonator-notes.md`): dla f=10 GHz, `λ=c/f≈0,030 m` (3 cm) — długość
gardzieli 0,2–0,5·λ daje **0,6–1,5 cm**, co jest realnym, sensownym
wymiarem mechanicznym. To pokazuje, że CZĘŚĆ modelu (geometria) była
od początku dimensionally poprawna — problem jest wyłącznie w
warstwie "skręt → energia → foton".

## 3. Krzywizna — realna wielkość z geometrii rogu

`design/photon_horn_v1.md` opisuje róg jako stożek lub "róg
wykładniczy". Dla rogu wykładniczego, profil promienia:

```
r(z) = r_gardziel · exp(z / z_c)      [m]
```

Krzywizna tej krzywej (standardowa definicja różniczkowo-geometryczna,
ten sam typ obiektu co `κ` w Aksjomacie G10 z `GIA-TIMDR` — krzywizna
KRZYWEJ, nie powierzchni):

```
κ(z) = r''(z) / (1 + r'(z)²)^(3/2)      [1/m]
```

To jest realna, mierzalna wielkość inżynierska — wpływa na
dopasowanie impedancji i kierunkowość anteny (dobrze znany temat w
inżynierii mikrofalowej: zysk/VSWR rogu zależy od profilu flary).
**Ale — to trzeba powiedzieć wprost — krzywizna rogu wpływa na
DOPASOWANIE I KIERUNKOWOŚĆ już istniejącej fali, nie na to, czy
foton w ogóle powstaje.** To jest realny efekt inżynierski
opakowany w tym repo w język "generowania fotonów", którym nie jest.

*(Uwaga na marginesie: gdyby ktoś chciał policzyć κ(z) numerycznie dla
konkretnego profilu, można by w zasadzie użyć tej samej rodziny narzędzi
co `TIMDR-Geometry-Formalism/timdr_geometry/envelope.py` — ale to
osobna krzywa (róg wykładniczy, nie zaokrąglony trójkąt), więc
wymagałby nowego, osobnego modułu, nie bezpośredniego użycia G10.)*

## 4. Czas — brakująca skala, i realny konflikt dwóch skal

`Oscylator.tik()` dziś nie ma żadnego Δt — to goły licznik kroków.
Żeby to fizycznie zakotwiczyć, trzeba rozróżnić DWIE różne skale
czasowe, które model obecnie miesza w jedno:

1. **Okres fali nośnej** `T_nośna = 1/f_wnęki`. Dla f=10 GHz:
   `T_nośna = 100 ps = 1×10⁻¹⁰ s`. To jest realny okres oscylacji
   samego pola EM we wnęce.
2. **Okres widocznego rytmu światła** — README mówi o "rytmie
   emisji (światło impulsowe lub ciągłe)" w sensie DOSTRZEGALNYM.
   Ludzkie oko rejestruje migotanie do ~50-90 Hz — żeby rytm A→B→A→B
   był widoczny, trzeba `T_widoczny` rzędu **10⁻²–10⁻¹ s**, czyli
   **~10⁹ razy dłuższy** niż okres nośnej.

To są dwie fizycznie różne warstwy: nośna (carrier, GHz) i obwiednia/
modulacja (envelope, Hz) — pomylenie ich to ten sam typ błędu
kategorii, przed którym `GIA-TIMDR/TIMDR_Branch_Specification.md`
ostrzega w zupełnie innym kontekście (różne obiekty pod tą samą
nazwą). `oscylator.py` musi jawnie wybrać, którą skalę reprezentuje
`tik()` — dziś nie robi żadnej z nich.

**Podejście uzupełniające (prostsze, ogólniejsze):** zamiast
identyfikować `skręt` z konkretną wielkością fizyczną (OAM, §1), można
po prostu wprowadzić stałą skalującą `α_T` [s/krok] i pisać
`t_fiz = α_T · tik()` — bez żadnego twierdzenia o TYM, czym fizycznie
jest krok. To dokładnie framework `α_T/α_L/α_E`, opisany teraz w
`GIA-TIMDR/docs/theory/TIMDR_Gravity_Speculative.md` §4a ("Jednostki i
skalowanie"), i on wprost tłumaczy skąd biorą się częstotliwości rzędu
10³¹ Hz w tym repo: liczone jako `f~1/tik()` z krokiem modelowym
nieprzeskalowanym (efektywnie `α_T=1 krok`, nie sekundy) — to wybór
skali, nie błąd arytmetyczny. Ten sam mechanizm dotyczy
`energia_pola()=abs(skręt)*0.001` — dopóki nie wprowadzi się `α_E`
[J·m] i nie napisze `E_fiz=α_E·|skręt|`, wynik `abs(skręt)*0.001` nie
ma wymiaru [J] (niezależnie od problemu strukturalnego z §1a, który
dotyczy czegoś innego — że energia i skręt są fizycznie niezależnymi
stopniami swobody, więc żadne `α_E` tego nie naprawi). Te dwa
podejścia (OAM-identyfikacja tutaj, α-skalowanie w GIA-TIMDR) nie są
sprzeczne — α-skalowanie samo w sobie nie mówi CZYM fizycznie jest
skręt, tylko czyni liczby wymiarowo spójne; OAM-identyfikacja próbuje
odpowiedzieć na pytanie "czym jest", i to ono, nie brak skalowania,
jest miejscem gdzie ta analiza w §1a/§6 poniżej napotyka granicę
znanej fizyki.

## 5. Nowa stała: κ_twist — jawnie oznaczona jako niepotwierdzona

Skoro (§1a) energia i skręt są w realnej fizyce niezależne, a model
chce jednak twierdzić, że skręt WYWOŁUJE emisję, jedyny uczciwy sposób
to wprost postulować NOWĄ stałą sprzężenia — dokładnie tej samej
rangi epistemicznej co np. postulowana stała sprzężenia aksionu w
fizyce poza Modelem Standardowym: legalna hipoteza, zerowe
potwierdzenie eksperymentalne.

```
Γ_emisji = κ_twist · |ℓ|^n · u        [1/s]   (hipotetyczna szybkość emisji)
```

gdzie `u` to gęstość energii pola (§2, J/m³), `n` nieokreślony
wykładnik (najprostszy wybór n=1), a `κ_twist` ma wymagane wymiary
`[κ_twist] = m³/(J·s)` (żeby całość wyszła w 1/s). **Wartość
`κ_twist` jest NIEZNANA — nie istnieje w żadnej literaturze, nie
została zmierzona, nie wynika z żadnego znanego lagranżjanu QED.**
Wpisanie tu jakiejkolwiek liczby (np. "κ_twist=1" w jednostkach
naturalnych) byłoby dokładnie tym samym błędem co pierwsza wersja
`foton.py` — liczbą bez uzasadnienia, tylko ubraną w nowy symbol.

**Test falsyfikowalności, gdyby ktoś chciał to naprawdę zbadać** (w
duchu protokołu numerologii z `GIA-TIMDR/SKILL_timdr-signal-framework.md`
§2): zasilić realną wnękę rezonansową wiązką o kontrolowanym ℓ
(realizowalne — spiralna płytka fazowa albo hologram widlasty na
wejściu mikrofalowym), trzymać moc wejściową stałą, mierzyć emisję
kalibrowanym fotodetektorem przy ℓ=0 (kontrola negatywna) i przy kilku
wartościach ℓ≠0 obu znaków, sprawdzić czy sygnał koreluje ze
znakiem/wartością ℓ ponad szum RF/cieplny. Bez takiego pomiaru
`κ_twist` pozostaje czysto formalnym symbolem.

## 6. Werdykt — świadoma decyzja o interpretacji fizycznej

Wybrałeś ścieżkę "próba realnej interpretacji fizycznej". Wynik tej
próby, uczciwie:

- **Geometria (róg, wnęka, czas nośnej)** — daje się w pełni osadzić w
  realnych jednostkach SI, z realnymi wzorami inżynierii mikrofalowej.
  To NIE jest problem.
- **Skręt jako OAM (ℓ)** — daje się osadzić realnie, ze znaną stałą
  (ħ), ale jako wielkość niosąca moment pędu, NIE energię.
- **"Skręt powoduje emisję fotonu bez elektronów"** — nie daje się
  osadzić w znanej fizyce przy użyciu istniejących stałych (c, h, ħ,
  ε₀, μ₀). Wymaga POSTULOWANIA nowej stałej sprzężenia (κ_twist) o
  nieznanej wartości — co jest formalnie dopuszczalne jako hipoteza
  poza Modelem Standardowym, ale wtedy trzeba to tak właśnie nazywać:
  **hipoteza niepotwierdzona, nie zasada inżynierska gotowa do
  budowy**.

To nie jest wynik "model jest zły, więc odrzucam". To jest dokładnie
to, o co prosiłeś: analiza wymiarowa doprowadzona do końca, z
uczciwym zaznaczeniem, gdzie kończy się znana fizyka, a zaczyna
otwarta, jawnie oznaczona hipoteza — ten sam wzorzec co
`TIMDR_Gravity_Speculative.md` w GIA-TIMDR, tylko zastosowany tu, do
tego repo.

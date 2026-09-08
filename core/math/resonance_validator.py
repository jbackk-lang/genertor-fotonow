import numpy as np
from math import gcd

class FieldResonanceValidator:
    """
    Sprawdza topologiczną homogeniczność granic pól w skalach makro, atomowej
    oraz kwantowej (Photon Engine) przy użyciu bezwymiarowej analizy stosunków fourierowskich.
    
    Weryfikuje zachowanie energii w punktach zwrotnych oraz wyznacza dynamiczne
    wektory dążenia (gradienty pędu) dla struktur niedomkniętych.
    """
    
    def __init__(self, max_harmonic=8, default_tolerance=1e-3):
        self.max_harmonic = max_harmonic
        self.default_tolerance = default_tolerance

    def validate_boundary_state(self, omega_input, omega_pivot, tolerance=None):
        """
        Główna metoda walidacyjna analizująca stan sprzężenia pól.
        
        Parametry:
        ----------
        omega_input : float - Częstotliwość wzbudzenia / napływu energii układu.
        omega_pivot : float - Naturalna częstotliwość rezonatora (punktu zwrotnego).
        tolerance   : float - Opcjonalna czułość detekcji idealnego domknięcia.
        
        Zwraca:
        -------
        dict - Kompletny zestaw metryk topologicznych i wektorów ewolucji pola.
        """
        if tolerance is None:
            tolerance = self.default_tolerance

        # Zapobieganie dzieleniu przez zero przy skrajnych stanach brzegowych
        if omega_pivot == 0:
            raise ValueError("Częstotliwość punktu zwrotnego (omega_pivot) nie może wynosić 0.")

        # 1. Wyznaczenie surowego stosunku częstotliwości (bezwymiarowa geometria)
        raw_ratio = float(omega_input) / float(omega_pivot)
        
        best_m = 1
        best_n = 1
        min_delta = float('inf')
        
        # 2. Identyfikacja najbliższego teoretycznego węzła topologicznego (m:n)
        for n in range(1, self.max_harmonic + 1):
            m = round(raw_ratio * n)
            if m == 0 or m > self.max_harmonic * 2:
                continue
                
            delta = abs(raw_ratio - (m / n))
            if delta < min_delta:
                min_delta = delta
                best_m = m
                best_n = n

        # Sprowadzenie ułamka m/n do formy nieskracalnej (węzeł podstawowy)
        common_divisor = gcd(best_m, best_n)
        m_prime = best_m // common_divisor
        n_prime = best_n // common_divisor

        # 3. Wyznaczenie Indeksu Spójności Geometrycznej (GRI)
        # Określa gęstość symetrii w docelowym punkcie domknięcia układu
        geometric_resonance_index = 1.0 / (m_prime * n_prime)
        
        # 4. Ocena domknięcia struktury (Warunek brzegowy jako wyznacznik stabilności)
        is_structure_closed = min_delta <= tolerance
        target_ratio = best_m / best_n

        # 5. Wyznaczenie Wektora Ewolucji Pola (kierunek dążenia topologicznego)
        if is_structure_closed:
            evolution_direction = "stable"
        else:
            # Określenie, czy układ dąży do kontrakcji fazowej, czy ekspansji
            evolution_direction = "contraction" if raw_ratio < target_ratio else "expansion"

        # 6. Kalkulacja asymetrycznej siły gradientowej (Asymmetric Driving Force)
        # Dla układów niedomkniętych generuje potencjał uogólniony (np. anizotropię pędu)
        if is_structure_closed:
            asymmetric_gradient_force = 0.0
        else:
            asymmetric_gradient_force = min_delta * geometric_resonance_index

        # Zwrócenie kompletnego profilu walidacyjnego struktury pola
        return {
            "topological_node": f"{m_prime}:{n_prime}",
            "raw_ratio": round(raw_ratio, 6),
            "field_tension_delta": round(min_delta, 6),
            "is_structure_closed": is_structure_closed,
            "predicted_closure_point": round(target_ratio, 6),
            "field_evolution_vector": evolution_direction,
            "asymmetric_gradient_force": round(asymmetric_gradient_force, 6),
            "geometric_resonance_index": round(geometric_resonance_index, 4)
        }


# =====================================================================
# WALIDACJA WZGLĘDEM DANYCH RZECZYWISTYCH / KALIBRACJA
# =====================================================================
#
# Wszystkie wywołania walidatora powyżej (i w BLOKU TESTOWYM niżej)
# porównują predykcję wyłącznie z syntetycznymi, ręcznie dobranymi
# parami częstotliwości (400/200, 301.8/200, 800/500) — to sprawdza
# jedynie WEWNĘTRZNĄ spójność algorytmu, nigdy zgodność z czymkolwiek
# rzeczywistym. Poniższy blok domyka pętlę: predykcja -> porównanie
# z danymi rzeczywistymi/referencyjnymi -> kalibracja (jeśli uzasadniona).
#
# UCZCIWA UWAGA O ŹRÓDLE DANYCH (przeczytano całe repo w poszukiwaniu
# realnych danych, patrz design/*.md, theory/*.md, uwaga.md):
# W repozytorium NIE ma ŻADNYCH faktycznie zmierzonych w laboratorium
# częstotliwości rezonansowych. Jest tylko: (a) zakresy projektowe bez
# konkretnych liczb pomiarowych (np. "gardziel: 0.2-0.5 λ", kąt 10-20°
# w design/photon_horn_v1.md) oraz (b) jeden zakotwiczony PRZYKŁAD
# liczbowy w theory/dimensional-analysis.md: f=10 GHz jako przykładowe
# wejście mikrofalowe komory rezonansowej, z którego wynika λ≈3 cm.
# To nie jest pomiar laboratoryjny — to przykład ilustracyjny w dokumencie
# analizy wymiarowej. Żadna para (omega_input, omega_pivot) z realnym
# pomiarem nigdzie w repo nie istnieje.
#
# Dlatego jako dane referencyjne poniżej użyto NIE danych zmierzonych,
# lecz ścisłych, ugruntowanych w literaturze wzorów teorii cylindrycznej
# wnęki rezonansowej (mikrofalowej) — dokładnie tego typu rezonatora,
# który resonator-notes.md i photon_horn_v1.md opisują jako komorę Λ
# ("Rezonator cylindryczny... łatwy do wykonania, przewidywalne mody").
# Częstotliwości modów własnych TM0n0 cylindrycznej wnęki wynikają
# WPROST z warunków brzegowych Maxwella:
#
#     f_TM0n0 = c * j(0,n) / (2*pi*a)
#
# gdzie j(0,n) to n-te miejsce zerowe funkcji Bessela J0, a `a` to
# promień wnęki. Miejsca zerowe J0 i pochodnej J1 (mod TE111) to stałe
# matematyczne tabelowane od dziesięcioleci (Abramowitz & Stegun,
# "Handbook of Mathematical Functions", tabl. 9.5) i używane wprost przy
# projektowaniu realnych wnęk mikrofalowych (np. Pozar, "Microwave
# Engineering", 4th ed., tabl. 6.1). To są realne stałe fizyczne/
# matematyczne (konsekwencja równań Maxwella + geometria), NIE dane
# zmierzone przez autora tego repo w laboratorium. To rozróżnienie
# ("literatura/teoria" vs "pomiar") jest tu celowo utrzymane jawnie.
#
# Promień wnęki `a` dobrano tak, by TM010 wypadło dokładnie na 10 GHz —
# to ten sam punkt liczbowy, którego repo już używa jako przykład w
# theory/dimensional-analysis.md (nie nowa, znikąd wzięta liczba).

# Miejsca zerowe funkcji Bessela (Abramowitz & Stegun, tabl. 9.5)
BESSEL_J0_ZERO_1 = 2.4048255577       # j(0,1) -> mod TM010 (podstawowy)
BESSEL_J0_ZERO_2 = 5.5200781103       # j(0,2) -> mod TM020
BESSEL_J0_ZERO_3 = 8.6537279129       # j(0,3) -> mod TM030
BESSEL_J1PRIME_ZERO_1 = 1.8411837813  # j'(1,1) -> mod TE111

_TM010_ANCHOR_GHZ = 10.0  # przykład liczbowy zakotwiczony w theory/dimensional-analysis.md

REAL_CAVITY_REFERENCE_DATA = [
    {
        "label": "TM020 vs TM010 (ta sama cylindryczna wnęka mikrofalowa)",
        "omega_pivot": _TM010_ANCHOR_GHZ,
        "omega_input": _TM010_ANCHOR_GHZ * (BESSEL_J0_ZERO_2 / BESSEL_J0_ZERO_1),
        "source": ("j(0,2)/j(0,1); Abramowitz & Stegun, Handbook of Mathematical "
                   "Functions, tabl. 9.5. Wzor f_TM0n0=c*j(0,n)/(2*pi*a): Pozar, "
                   "Microwave Engineering, 4th ed., tabl. 6.1."),
    },
    {
        "label": "TM030 vs TM010 (ta sama cylindryczna wnęka mikrofalowa)",
        "omega_pivot": _TM010_ANCHOR_GHZ,
        "omega_input": _TM010_ANCHOR_GHZ * (BESSEL_J0_ZERO_3 / BESSEL_J0_ZERO_1),
        "source": "j(0,3)/j(0,1); Abramowitz & Stegun, tabl. 9.5.",
    },
    {
        "label": "TE111 vs TM010 (ta sama cylindryczna wnęka mikrofalowa)",
        "omega_pivot": _TM010_ANCHOR_GHZ,
        "omega_input": _TM010_ANCHOR_GHZ * (BESSEL_J1PRIME_ZERO_1 / BESSEL_J0_ZERO_1),
        "source": "j'(1,1)/j(0,1); Abramowitz & Stegun, tabl. 9.5.",
    },
]


def evaluate_against_reference(validator, reference_cases):
    """
    Uruchamia walidator na parach częstotliwości pochodzących z realnych,
    ugruntowanych w literaturze wzorów teorii wnęk rezonansowych (nie
    syntetycznych par z BLOKU TESTOWEGO), i zwraca listę wyników z
    policzonym odchyleniem predykcji (`predicted_closure_point`) od
    rzeczywistego stosunku częstotliwości (`raw_ratio`, policzony wprost
    z podanych realnych częstotliwości wejściowych).

    Parametry:
    ----------
    validator : FieldResonanceValidator
    reference_cases : list[dict] - każdy z kluczami
        "omega_input", "omega_pivot", "label", opcjonalnie "source".

    Zwraca:
    -------
    list[dict] - jeden wpis na przypadek referencyjny.
    """
    results = []
    for case in reference_cases:
        prediction = validator.validate_boundary_state(
            case["omega_input"], case["omega_pivot"]
        )
        real_ratio = prediction["raw_ratio"]
        predicted = prediction["predicted_closure_point"]

        signed_relative_deviation = (real_ratio - predicted) / predicted
        results.append({
            "label": case.get("label", "?"),
            "source": case.get("source", ""),
            "real_reference_ratio": real_ratio,
            "predicted_closure_point": predicted,
            "field_tension_delta": prediction["field_tension_delta"],
            "signed_relative_deviation": round(signed_relative_deviation, 6),
            "absolute_relative_deviation": round(abs(signed_relative_deviation), 6),
            "is_structure_closed": prediction["is_structure_closed"],
        })
    return results


def detect_systematic_bias(evaluation_results, max_relative_spread=0.5):
    """
    Sprawdza, czy odchylenia predykcji względem danych referencyjnych
    mają SPÓJNY kierunek i skalę (systematyczne obciążenie, możliwe do
    skorygowania jedną stałą), czy są niespójne co do znaku/rozrzutu
    (nieodłączny błąd przybliżenia wymiernego m/n o ograniczonym
    mianowniku, którego NIE należy sztucznie "korygować").

    `max_relative_spread` to próg (rozstęp odchyleń / |średnia
    odchyleń|) poniżej którego uznajemy obciążenie za wystarczająco
    spójne, by mówić o systematyczności, a nie o przypadkowym rozrzucie.
    """
    if not evaluation_results:
        raise ValueError("Brak wyników do analizy obciążenia systematycznego.")

    deviations = [r["signed_relative_deviation"] for r in evaluation_results]
    mean_deviation = sum(deviations) / len(deviations)
    signs = {1 if d > 0 else (-1 if d < 0 else 0) for d in deviations}
    consistent_sign = len(signs) == 1 and 0 not in signs

    if mean_deviation != 0:
        relative_spread = (max(deviations) - min(deviations)) / abs(mean_deviation)
    else:
        relative_spread = float("inf")

    systematic = bool(consistent_sign and relative_spread <= max_relative_spread)

    return {
        "n_cases": len(evaluation_results),
        "mean_signed_relative_deviation": round(mean_deviation, 6),
        "consistent_sign": consistent_sign,
        "relative_spread": round(relative_spread, 3) if relative_spread != float("inf") else None,
        "systematic_bias_detected": systematic,
    }


def build_calibration(evaluation_results, max_relative_spread=0.5):
    """
    Na podstawie wyników `evaluate_against_reference` decyduje, czy
    wprowadzić stałą korekcyjną (`correction_factor`) dla przyszłych
    predykcji, czy pozostawić walidator bez zmian i jawnie udokumentować
    dlaczego korekta nie jest uzasadniona.

    Zwraca:
    -------
    dict z "correction_factor" (1.0 = brak korekty), "bias_analysis"
    (wynik `detect_systematic_bias`) i "reason" (uzasadnienie tekstowe).
    """
    bias = detect_systematic_bias(evaluation_results, max_relative_spread)

    if bias["systematic_bias_detected"]:
        correction_factor = 1.0 / (1.0 + bias["mean_signed_relative_deviation"])
        reason = (
            f"Wykryto spójne obciążenie ({bias['mean_signed_relative_deviation'] * 100:.3f}% "
            f"w {bias['n_cases']} przypadkach, ten sam znak, rozrzut "
            f"{bias['relative_spread']} <= {max_relative_spread}). Zastosowano stałą "
            "korekcyjną mnożącą przyszłe omega_input."
        )
    else:
        correction_factor = 1.0
        reason = (
            "Brak spójnego obciążenia systematycznego (niespójny znak i/lub rozrzut "
            f"powyżej progu {max_relative_spread}; szczegóły: {bias}). Zaobserwowane "
            "odchylenia są zgodne z nieodłącznym błędem przybliżenia wymiernego "
            "(dopasowanie niewymiernych stosunków rzeczywistych modów wnęki "
            "ułamkiem m/n o mianowniku <= max_harmonic), a NIE z błędem "
            "kalibracji samego wzoru. Nie wprowadzono sztucznej korekty."
        )

    return {
        "correction_factor": round(correction_factor, 6),
        "bias_analysis": bias,
        "reason": reason,
    }


class CalibratedFieldResonanceValidator(FieldResonanceValidator):
    """
    FieldResonanceValidator z opcjonalną stałą korekcyjną wyznaczoną
    przez `build_calibration` na podstawie danych referencyjnych.

    Korekta mnoży `omega_input` PRZED wykonaniem standardowej walidacji
    - kompensuje wykryte, spójne, systematyczne obciążenie predykcji
    względem danych rzeczywistych/referencyjnych. Gdy
    `correction_factor == 1.0` (brak wykrytego obciążenia), zachowuje
    się identycznie jak klasa bazowa.
    """

    def __init__(self, correction_factor=1.0, max_harmonic=8, default_tolerance=1e-3):
        super().__init__(max_harmonic=max_harmonic, default_tolerance=default_tolerance)
        self.correction_factor = correction_factor
        self.calibration_report = None
        self.calibration_evaluation = None

    @classmethod
    def from_reference_data(cls, reference_cases, base_validator=None, **kwargs):
        """Buduje skalibrowany walidator, ucząc się na `reference_cases`."""
        base_validator = base_validator or FieldResonanceValidator(**kwargs)
        results = evaluate_against_reference(base_validator, reference_cases)
        calibration = build_calibration(results)
        instance = cls(
            correction_factor=calibration["correction_factor"],
            max_harmonic=base_validator.max_harmonic,
            default_tolerance=base_validator.default_tolerance,
        )
        instance.calibration_report = calibration
        instance.calibration_evaluation = results
        return instance

    def validate_boundary_state(self, omega_input, omega_pivot, tolerance=None):
        corrected_input = omega_input * self.correction_factor
        return super().validate_boundary_state(corrected_input, omega_pivot, tolerance)


# =====================================================================
# BLOK TESTOWY pipeline'u walidacji dla trzech skal geometrycznych
# =====================================================================
if __name__ == "__main__":
    validator = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)
    
    print("=" * 60)
    print("PROFIL WALIDACYJNY: JEDNOLITA GEOMETRIA POLA")
    print("=" * 60)

    # 1. Skala Atomowa: Stabilność nuklearna wokół punktu żelaza (Struktura domknięta)
    print("\n[SKALA ATOMOWA] - Test stabilności izotopowej (Helium/Fe):")
    atom_data = validator.validate_boundary_state(omega_input=400.0, omega_pivot=200.0)
    for k, v in atom_data.items():
        print(f"  {k}: {v}")

    # 2. Skala Makro: Dysk akrecyjny Sgr A* (Niedomknięcie przejściowe -> Emisja ROSAT)
    print("\n[SKALA MAKRO] - Dynamika transferu energii 2MASS -> ROSAT:")
    macro_data = validator.validate_boundary_state(omega_input=301.8, omega_pivot=200.0)
    for k, v in macro_data.items():
        print(f"  {k}: {v}")

    # 3. Skala Kwantowa: Photon Engine (Trwałe niedomknięcie -> Asymetryczny Pęd)
    # Celowo bardzo niska tolerancja, by uchwycić stały gradient siły napędowej
    print("\n[SKALA KWANTOWA] - Sztuczna koniunkcja pól (Photon Engine):")
    quantum_data = validator.validate_boundary_state(omega_input=800.0, omega_pivot=500.0, tolerance=1e-6)
    for k, v in quantum_data.items():
        print(f"  {k}: {v}")
    print("=" * 60)

    # 4. Walidacja względem danych RZECZYWISTYCH/referencyjnych (nie syntetycznych)
    #    + kalibracja, jeśli odchylenie okaże się systematyczne.
    print("\n" + "=" * 60)
    print("KROK 4: WALIDACJA WZGLĘDEM DANYCH REFERENCYJNYCH + KALIBRACJA")
    print("(cylindryczna wnęka mikrofalowa, mody TM/TE z zer Bessela -")
    print(" ugruntowana literatura, NIE pomiar laboratoryjny z tego repo)")
    print("=" * 60)

    reference_results = evaluate_against_reference(validator, REAL_CAVITY_REFERENCE_DATA)
    for r in reference_results:
        print(f"\n[{r['label']}]")
        print(f"  źródło: {r['source']}")
        print(f"  rzeczywisty stosunek częstotliwości: {r['real_reference_ratio']}")
        print(f"  predykcja walidatora (predicted_closure_point): {r['predicted_closure_point']}")
        print(f"  odchylenie względne (ze znakiem): {r['signed_relative_deviation']*100:.4f}%")
        print(f"  domknięte w domyślnej tolerancji: {r['is_structure_closed']}")

    calibration = build_calibration(reference_results)
    print("\n[WYNIK KALIBRACJI]")
    print(f"  correction_factor: {calibration['correction_factor']}")
    print(f"  analiza obciążenia: {calibration['bias_analysis']}")
    print(f"  uzasadnienie: {calibration['reason']}")
    print("=" * 60)

"""
Testy dla core/math/resonance_validator.py.

Nie istniał wcześniej żaden katalog `tests/` w tym repo (sprawdzono
strukturę repozytorium) - ten plik jest pierwszym zestawem testów
automatycznych. Uruchamianie:

    python -m unittest tests/test_resonance_validator.py -v

lub, z katalogu głównego repo:

    python -m pytest tests/test_resonance_validator.py -v
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core", "math"))

from resonance_validator import (  # noqa: E402
    BESSEL_J0_ZERO_1,
    BESSEL_J0_ZERO_2,
    BESSEL_J0_ZERO_3,
    BESSEL_J1PRIME_ZERO_1,
    REAL_CAVITY_REFERENCE_DATA,
    CalibratedFieldResonanceValidator,
    FieldResonanceValidator,
    build_calibration,
    detect_systematic_bias,
    evaluate_against_reference,
)


class TestFieldResonanceValidatorBaseline(unittest.TestCase):
    """Testy podstawowego zachowania walidatora (istniejąca logika)."""

    def setUp(self):
        self.validator = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)

    def test_perfect_octave_closure(self):
        result = self.validator.validate_boundary_state(400.0, 200.0)
        self.assertEqual(result["topological_node"], "2:1")
        self.assertTrue(result["is_structure_closed"])
        self.assertEqual(result["predicted_closure_point"], 2.0)

    def test_zero_pivot_raises(self):
        with self.assertRaises(ValueError):
            self.validator.validate_boundary_state(400.0, 0.0)

    def test_open_structure_reports_gradient(self):
        result = self.validator.validate_boundary_state(301.8, 200.0)
        self.assertFalse(result["is_structure_closed"])
        self.assertGreater(result["asymmetric_gradient_force"], 0.0)


class TestEvaluateAgainstReference(unittest.TestCase):
    """
    Testy funkcji walidacji względem danych rzeczywistych/referencyjnych
    (mody cylindrycznej wnęki mikrofalowej, wyznaczone zerami funkcji
    Bessela - patrz komentarze źródłowe w resonance_validator.py).
    """

    def setUp(self):
        self.validator = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)

    def test_reference_ratios_match_bessel_zero_formula(self):
        # Sanity check niezależny od implementacji: stosunek częstotliwości
        # podanych jako dane referencyjne musi odpowiadać dokładnie
        # stosunkowi odpowiednich zer Bessela (to jest definicja tych
        # danych, nie coś co walidator "odkrywa").
        tm020_case = REAL_CAVITY_REFERENCE_DATA[0]
        expected_ratio = BESSEL_J0_ZERO_2 / BESSEL_J0_ZERO_1
        actual_ratio = tm020_case["omega_input"] / tm020_case["omega_pivot"]
        self.assertAlmostEqual(actual_ratio, expected_ratio, places=9)

    def test_evaluate_returns_one_result_per_case(self):
        results = evaluate_against_reference(self.validator, REAL_CAVITY_REFERENCE_DATA)
        self.assertEqual(len(results), len(REAL_CAVITY_REFERENCE_DATA))
        for case, result in zip(REAL_CAVITY_REFERENCE_DATA, results):
            self.assertEqual(result["label"], case["label"])

    def test_deviation_is_internally_consistent(self):
        # Re-derywacja odchylenia niezależnie od build_calibration/detect_*,
        # żeby wyłapać regresję w samym evaluate_against_reference.
        results = evaluate_against_reference(self.validator, REAL_CAVITY_REFERENCE_DATA)
        for r in results:
            expected = (r["real_reference_ratio"] - r["predicted_closure_point"]) / r["predicted_closure_point"]
            self.assertAlmostEqual(r["signed_relative_deviation"], round(expected, 6), places=6)

    def test_real_cavity_modes_are_not_perfectly_closed(self):
        # TM020/TM030/TE111 są rządzone niewymiernymi (Bessel-zero) stosunkami
        # - w ogólności NIE oczekujemy domknięcia w domyślnej tolerancji 1e-3,
        # w przeciwieństwie do syntetycznych par w BLOKU TESTOWYM (400/200 itd).
        results = evaluate_against_reference(self.validator, REAL_CAVITY_REFERENCE_DATA)
        closed_flags = [r["is_structure_closed"] for r in results]
        # Przynajmniej jedna z trzech par realnych modów powinna wypaść poza
        # tolerancję - inaczej model "przypadkiem" pasowałby do fizyki wnęki
        # lepiej niż uzasadnia to teoria (co byłoby zaskoczeniem wartym
        # zbadania, nie oznaką poprawności).
        self.assertTrue(any(not c for c in closed_flags))

    def test_deviation_magnitude_is_plausible_and_bounded(self):
        # Odchylenia względne powinny być małe (rzędu <=5%) - to sprawdza,
        # że dane wejściowe i formuła nie mają rażącego błędu jednostek/
        # rzędu wielkości, bez zakładania konkretnej wartości co do cyfry.
        results = evaluate_against_reference(self.validator, REAL_CAVITY_REFERENCE_DATA)
        for r in results:
            self.assertLess(r["absolute_relative_deviation"], 0.05)
            self.assertGreater(r["absolute_relative_deviation"], 0.0)


class TestDetectSystematicBias(unittest.TestCase):

    def test_empty_results_raises(self):
        with self.assertRaises(ValueError):
            detect_systematic_bias([])

    def test_consistent_positive_bias_is_detected(self):
        synthetic_results = [
            {"signed_relative_deviation": 0.010},
            {"signed_relative_deviation": 0.011},
            {"signed_relative_deviation": 0.0095},
        ]
        bias = detect_systematic_bias(synthetic_results)
        self.assertTrue(bias["consistent_sign"])
        self.assertTrue(bias["systematic_bias_detected"])
        self.assertAlmostEqual(bias["mean_signed_relative_deviation"], 0.010167, places=5)

    def test_mixed_sign_is_not_systematic(self):
        synthetic_results = [
            {"signed_relative_deviation": 0.02},
            {"signed_relative_deviation": -0.01},
            {"signed_relative_deviation": 0.015},
        ]
        bias = detect_systematic_bias(synthetic_results)
        self.assertFalse(bias["consistent_sign"])
        self.assertFalse(bias["systematic_bias_detected"])

    def test_real_reference_data_is_not_a_consistent_systematic_bias(self):
        # Kluczowe uczciwe stwierdzenie tego zadania: trzy realne pary modów
        # wnęki (TM020, TM030, TE111 vs TM010) dają odchylenia o RÓŻNYCH
        # znakach/skali (sprawdzone ręcznie: ok. +0.42%, +2.08%, -0.04%),
        # bo są rządzone różnymi, niepowiązanymi liniowo stosunkami zer
        # Bessela. To NIE jest systematyczne obciążenie samego wzoru
        # walidatora - i test to potwierdza zamiast zakładać.
        validator = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)
        results = evaluate_against_reference(validator, REAL_CAVITY_REFERENCE_DATA)
        bias = detect_systematic_bias(results)
        self.assertFalse(bias["systematic_bias_detected"])


class TestBuildCalibrationAndCalibratedValidator(unittest.TestCase):

    def test_no_correction_when_no_systematic_bias(self):
        validator = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)
        results = evaluate_against_reference(validator, REAL_CAVITY_REFERENCE_DATA)
        calibration = build_calibration(results)
        self.assertEqual(calibration["correction_factor"], 1.0)
        self.assertIn("Nie wprowadzono sztucznej korekty", calibration["reason"])

    def test_correction_applied_and_cancels_synthetic_bias(self):
        # Konstruujemy trzy syntetyczne przypadki ze SPÓJNYM +1% obciążeniem
        # względem trzech różnych węzłów wymiernych (3:2, 5:3, 7:4), z
        # marginesem bezpieczeństwa od sąsiednich węzłów sprawdzonym ręcznie,
        # żeby dopasowanie m:n było jednoznaczne.
        omega_pivot = 100.0
        targets = [1.5, 5.0 / 3.0, 1.75]
        offset = 1.01
        synthetic_cases = [
            {
                "label": f"synthetic-{i}",
                "omega_pivot": omega_pivot,
                "omega_input": omega_pivot * target * offset,
                "source": "syntetyczny przypadek testowy (nie dane referencyjne)",
            }
            for i, target in enumerate(targets)
        ]

        base_validator = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)
        uncalibrated = evaluate_against_reference(base_validator, synthetic_cases)
        bias = detect_systematic_bias(uncalibrated)
        self.assertTrue(bias["systematic_bias_detected"])
        self.assertAlmostEqual(bias["mean_signed_relative_deviation"], 0.01, places=2)

        calibrated_validator = CalibratedFieldResonanceValidator.from_reference_data(
            synthetic_cases, base_validator=base_validator
        )
        self.assertAlmostEqual(calibrated_validator.correction_factor, 1.0 / offset, places=4)

        calibrated_results = evaluate_against_reference(calibrated_validator, synthetic_cases)
        for before, after in zip(uncalibrated, calibrated_results):
            self.assertLess(
                after["absolute_relative_deviation"],
                before["absolute_relative_deviation"],
            )
            # Po korekcie odchylenie powinno być bliskie zeru (do zaokrągleń).
            self.assertLess(after["absolute_relative_deviation"], 1e-3)

    def test_calibrated_validator_defaults_to_identity_behavior(self):
        # correction_factor=1.0 => zachowanie identyczne z klasą bazową.
        base = FieldResonanceValidator(max_harmonic=8, default_tolerance=1e-3)
        calibrated = CalibratedFieldResonanceValidator(correction_factor=1.0)
        self.assertEqual(
            base.validate_boundary_state(400.0, 200.0),
            calibrated.validate_boundary_state(400.0, 200.0),
        )


if __name__ == "__main__":
    unittest.main()



import unittest

from logic_synthesis import analyze_logic
from minimizer import minimize_logic


class TestLogicSynthesis(unittest.TestCase):

    def test_example_circuit(self):
        circuit = {
            "inputs": ["A", "B", "C"],
            "gates": [
                {
                    "id": "g1",
                    "type": "AND",
                    "inputs": ["A", "B"]
                },
                {
                    "id": "g2",
                    "type": "OR",
                    "inputs": ["g1", "C"]
                }
            ],
            "output": "g2"
        }

        result = analyze_logic(circuit)

        self.assertEqual(
            result["on_set"], [1, 3, 5, 6, 7]
        )
        self.assertEqual(
            result["off_set"], [0, 2, 4]
        )

        minimized = minimize_logic(
            result["variables"],
            result["on_set"],
            result["off_set"]
        )

        self.assertEqual(
            minimized["sop_literals_saved"], 12
        )
        self.assertEqual(
            minimized["pos_literals_saved"], 5
        )
        self.assertEqual(
            minimized["prime_implicant_count"], 2
        )
        self.assertEqual(
            minimized["essential_prime_implicant_count"], 2
        )

    def test_constant_zero(self):
        result = minimize_logic(
            ["A", "B"], [], [0, 1, 2, 3]
        )

        self.assertEqual(result["minimized_sop"], "0")
        self.assertEqual(result["minimized_pos"], "0")

    def test_constant_one(self):
        result = minimize_logic(
            ["A", "B"], [0, 1, 2, 3], []
        )

        self.assertEqual(result["minimized_sop"], "1")
        self.assertEqual(result["minimized_pos"], "1")


if __name__ == "__main__":
    unittest.main()

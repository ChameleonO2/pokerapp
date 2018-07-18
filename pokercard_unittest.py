import unittest
from enum import Enum
from handdicison import PokerCard

class TestPokerCard(unittest.TestCase):
    """
    test class of handdicison.py
    """
    Marks = Enum('Marks', 'Spade Club Heart Dia')
    def test_disern_card(self):
        val = 0
        expected = 1
        expected2  = self.Marks(1)
        actual,actual2 = PokerCard().disern_card(val)
        self.assertEqual(expected,actual)

    def test_disern_card2(self):
        val = 0
        expected = 1
        expected2  = self.Marks(1)
        actual,actual2 = PokerCard().disern_card(val)
        self.assertEqual(expected,actual)

if __name__ == "__main__":
    unittest.main()

import unittest
from handdicison import PokerCard

class TestPokerCard(unittest.TestCase):
    """
    test class of handdicison.py
    """

    def test_disern_card(self):
        val = 0
        expected = 1
        expected2  = 'Spade'
        actual,actual2 = PokerCard().disern_card(val)
        self.assertEqual(expected,actual)

    def test_disern_card2(self):
        val = 0
        expected = 1
        expected2  = 'Spade'
        actual,actual2 = PokerCard().disern_card(val)
        self.assertEqual(expected,actual)

if __name__ == "__main__":
    unittest.main()

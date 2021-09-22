from unittest import TestCase
from unittest.mock import patch
from combat import dice, dice_str, d100

@patch('combat.randint', return_value=2)
class TestDice(TestCase):
    
    def test_dice(self, mocked_randint):
        roll1 = dice(3)
        roll2 = dice(3, 2)
        roll3 = dice(3, 2, 1)

        self.assertEqual(roll1, 2)
        self.assertEqual(roll2, 4)
        self.assertEqual(roll3, 5)
    
    def test_dice_str(self, mocked_randint):
        roll1 = dice_str("1d3")
        roll2 = dice_str("2d3")
        roll3 = dice_str("2d3+1")
        roll4 = dice_str("2d3-1")
        roll5 = dice_str("2d3-1+imp")
        roll6 = dice_str("2d3-1+strmod")
        roll7 = dice_str("2d3-1+sklmod")
        roll8 = dice_str("2d3+sklmod")
        
        self.assertEqual(roll1, 2)
        self.assertEqual(roll2, 4)
        self.assertEqual(roll3, 5)
        self.assertEqual(roll4, 3)
        self.assertEqual(roll5, 3)
        self.assertEqual(roll6, 3)
        self.assertEqual(roll7, 3)
        self.assertEqual(roll8, 4)



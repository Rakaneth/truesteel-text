from charfactory import build_char
from equipfactory import make_armor, make_implement, make_weapon
from equip import ImplementStats, WeaponStats, ArmorStats
from unittest import TestCase

class CharacterTest(TestCase):

    def setUp(self) -> None:
        self.warrior = build_char("human", "warrior")
        self.magician = build_char("elf", "magician")
        self.warlock = build_char("dwarf", "warlock")
        self.player = build_char("korashi", "warrior", "Ogluk")

    def test_warbase(self):
        #basics
        self.assertEqual(self.warrior.strength, 25)
        self.assertEqual(self.warrior.stamina, 25)
        self.assertEqual(self.warrior.speed, 20)
        self.assertEqual(self.warrior.skill, 20)
        self.assertEqual(self.warrior.sagacity, 20)
        self.assertEqual(self.warrior.smarts, 15)
        self.assertEqual(self.warrior.melee, 20)
        self.assertEqual(self.warrior.magic, 0)
        self.assertTrue(self.warrior.alive)
    
    def test_warderived(self):
        #derived
        self.assertEqual(self.warrior.atp, 40)
        self.assertEqual(self.warrior.dfp, 90)
        self.assertEqual(self.warrior.tou, 75)
        self.assertEqual(self.warrior.wil, 70)
        self.assertEqual(self.warrior.pwr, 17)
        self.assertEqual(self.warrior.damage, "1+strmod")
        self.assertEqual(self.warrior.body, 14)
        self.assertEqual(self.warrior.mind, 12)
        self.assertEqual(self.warrior.soul, 33)

    
    def test_equipped(self):
        #equipped
        brass_rod = make_implement("brass rod")
        dagger = make_weapon("dagger")
        half_plate = make_armor("halfplate")

        #skilled in fighting
        self.warrior.stats.melee = 20
        self.warrior.stats.magic = 10

        self.warrior.armor = half_plate
        self.warrior.weapon = dagger
        self.warrior.implement = brass_rod

        self.assertEqual(self.warrior.atp, 50)
        self.assertEqual(self.warrior.dfp, 90)
        self.assertEqual(self.warrior.pwr, 37)
        self.assertEqual(self.warrior.defense, 4)
        self.assertEqual(self.warrior.damage, "1d4+sklmod")


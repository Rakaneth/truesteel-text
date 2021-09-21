from character import Character, BaseStats
from equip import ImplementStats, WeaponStats, ArmorStats
from unittest import TestCase

class CharacterTest(TestCase):

    def setUp(self) -> None:
        self.test_dude = Character(
            name="Test Dude",
            stats=BaseStats()
        )

    def test_charbase(self):
        #basics
        self.assertEqual(self.test_dude.name, "Test Dude")
        self.assertEqual(self.test_dude.stats.strength, 20)
        self.assertEqual(self.test_dude.stats.stamina, 20)
        self.assertEqual(self.test_dude.stats.skill, 20)
        self.assertEqual(self.test_dude.stats.speed, 20)
        self.assertEqual(self.test_dude.stats.sagacity, 20)
        self.assertEqual(self.test_dude.stats.smarts, 20)
        self.assertEqual(self.test_dude.stats.magic, 0)
        self.assertEqual(self.test_dude.stats.melee, 0)

    def test_derived(self):
        #derived
        self.assertEqual(self.test_dude.atp, 20)
        self.assertEqual(self.test_dude.dfp, 20)
        self.assertEqual(self.test_dude.tou, 70)
        self.assertEqual(self.test_dude.wil, 70)
        self.assertEqual(self.test_dude.pwr, 20)
        self.assertEqual(self.test_dude.defense, 0)
        self.assertEqual(self.test_dude.damage, (1, 1))
    
    def test_equipped(self):
        #equipped
        brass_rod = ImplementStats(
            name="Brass Rod",
            durability=50,
            max_dur=50,
            pwr=10,
            damage=(1, 3)
        )
        dagger = WeaponStats(
            name="Dagger",
            durability=50,
            max_dur=50,
            damage=(1, 4)
        )
        half_plate = ArmorStats(
            name="Half Plate",
            durability=100,
            defense=4,
            max_dur=100
        )
        #skilled in fighting
        self.test_dude.stats.melee = 20
        self.test_dude.stats.magic = 10

        self.test_dude.armor = half_plate
        self.test_dude.weapon = dagger
        self.test_dude.implement = brass_rod

        self.assertEqual(self.test_dude.atp, 40)
        self.assertEqual(self.test_dude.dfp, 40)
        self.assertEqual(self.test_dude.pwr, 40)
        self.assertEqual(self.test_dude.defense, 4)
        self.assertEqual(self.test_dude.damage, (1, 4))


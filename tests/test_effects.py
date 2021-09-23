import effects as ef
import combat as cbt

from unittest import TestCase
from unittest.mock import patch
from charfactory import build_char
from character import DamageType


class TestEffects(TestCase):
    def setUp(self):
        self.victim = build_char("human", "warrior", "Dan")
    
    def test_dmg(self):
        with patch('combat.randint', return_value=3):
            dmg = ef.Damage("1d6+2", DamageType.BODY)
            self.assertEqual(dmg.name, ef.EffectNames.DAMAGE.value)
            cbt.apply_effect(self.victim, dmg)
        
        cbt.tick_effects(self.victim)
        self.assertEqual(self.victim.body, 9)
        self.assertIsNone(self.victim.find_effect(ef.EffectNames.DAMAGE.value))
    
    def test_burn(self):
        burn = ef.Burn(2)
        cbt.apply_effect(self.victim, burn)
        for _ in range(2):
            self.assertIsNotNone(self.victim.find_effect(ef.EffectNames.BURN.value))
            cbt.tick_effects(self.victim)
            
        self.assertIsNone(self.victim.find_effect(ef.EffectNames.BURN.value))
        self.assertEqual(self.victim.body, 8)

    def test_shield(self):
        burn = ef.Burn(1)
        shield = ef.Shield(5, 100)
        
        with patch('combat.randint', return_value=2):
            shield_dmg = ef.Damage("1d2", DamageType.BODY)
            no_shield_dmg = ef.Damage("1d2", DamageType.MIND, False, False)
            for eff in (burn, shield, shield_dmg, no_shield_dmg):
                cbt.apply_effect(self.victim, eff)
        
        self.assertEqual(self.victim.body, 14)
        self.assertEqual(shield.potency, 98)
        cbt.tick_effects(self.victim)
        self.assertEqual(self.victim.mind, 10)
        self.assertEqual(shield.potency, 95)

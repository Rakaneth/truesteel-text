from unittest import TestCase
from charfactory import build_char
from equipfactory import make_armor, make_implement, make_weapon
from critscript import compile, CritScriptSyntaxError

class TestCritScript(TestCase):
    def setUp(self):
        self.emberspark_ary = [
            "atk(pwr vs dfp)",
            "Damage Body 1d3+IMP",
            "Damage Soul 1d2+IMP",
            "Effect Soulburn 1",
            "crit",
            "Effect Soulburn 5",
            "endcrit",
            "endatk"
        ]
        self.emberspark_expected = [
            "atk(pwr vs dfp)",
            "damage body 1d3+imp",
            "damage soul 1d2+imp",
            "effect soulburn 1",
            "crit",
            "effect soulburn 5",
            "endcrit",
            "endatk"   
        ]
        self.savagery_ary = [
            "do 2 times",
            "atk(atp vs dfp)",
            "Damage Body WEAPON",
            "Effect Bleed 1",
            "endatk",
            "done"
        ]
        self.savagery_expected = [
            "do 2 times",
            "atk(atp vs dfp)",
            "damage body weapon",
            "effect bleed 1",
            "endatk",
            "done"  
        ]
        self.emberspark_str = """
#This spell hits one target.
#Caster makes a PWR roll against target's DFP.
#If successful, target takes 1d3 + caster's implement in Body damage and 1d2 + caster's implement 
#in Soul damage as well as the Soulburn debuff for 1 turn. 
#On crit, this deals an additional 5 turns of Soulburn.

atk(pwr vs dfp) 
    Damage Body 1d3+IMP 
    Damage Soul 1d2+IMP
    Effect Soulburn 1
    crit 
        Effect Soulburn 5
    endcrit
endatk"""
        self.savagery_str = """
#This attack hits 1 target twice and inflicts Bleed.
do 2 times
    atk(atp vs dfp)
        Damage Body WEAPON
        Effect Bleed 1
    endatk
done"""
        
    def test_oneliners(self):
        bleed1 = compile("Effect Bleed 1")
        shield = compile("Effect Shield 10 100")
        body_imp = compile("Damage Body 1d4+IMP")
        soul_weap = compile("Damage Soul WEAPON")

        self.assertListEqual(bleed1, ["effect bleed 1"])
        self.assertListEqual(shield, ["effect shield 10 100"])
        self.assertListEqual(body_imp, ["damage body 1d4+imp"])
        self.assertListEqual(soul_weap, ["damage soul weapon"])
        self.assertRaises(CritScriptSyntaxError, compile, "Unknown")
    
    def test_arrays(self):
        em_compiled = compile(self.emberspark_ary)
        sv_compiled = compile(self.savagery_ary)
        self.assertListEqual(em_compiled, self.emberspark_expected)
        self.assertListEqual(sv_compiled, self.savagery_expected)

    def test_string(self):
        em_compiled = compile(self.emberspark_str)
        sv_compiled = compile(self.savagery_str)
        self.assertListEqual(em_compiled, self.emberspark_expected)
        self.assertListEqual(sv_compiled, self.savagery_expected)
    
    def test_do_failures(self):
        do_before_done = """
        done
        atk(atp vs tou)
            Effect Bleed 1
        endatk
        do 2 times
        """
        no_done = """
        do 2 times
            atk(atp vs dfp)
                Damage Body WEAPON
            endatk
        """
        no_do = """
        atk(pwr vs dfp)
            Effect Burn 5
        endatk
        done
        """
        odd_do = """
        do 2 times
            Effect Shield 10 100
        done
        do
            Effect Bleed 10
        """
        nested_do = """
        do 2 times
            atk(atp vs dfp)
                do 4 times
                    Damage Body 1
                done
            endatk
        done
        """
        self.assertRaises(CritScriptSyntaxError, compile, do_before_done)
        self.assertRaises(CritScriptSyntaxError, compile, no_done)
        self.assertRaises(CritScriptSyntaxError, compile, no_do)
        self.assertRaises(CritScriptSyntaxError, compile, odd_do)
        self.assertRaises(CritScriptSyntaxError, compile, nested_do)

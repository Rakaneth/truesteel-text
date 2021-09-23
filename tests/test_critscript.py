import critscript as cr
import combat as cbt

from unittest import TestCase
from charfactory import build_char
from equipfactory import make_armor, make_implement, make_weapon



class TestCritScript(TestCase):
    def setUp(self):
        self.emberspark_ary = [
            "atk(pwr vs dfp)",
            "hit",
            "Damage Body 1d3+IMP",
            "Damage Soul 1d2+IMP",
            "Effect Soulburn 1",
            "endhit",
            "crit",
            "Effect Soulburn 5",
            "endcrit",
            "endatk"
        ]
        self.emberspark_expected = [
            "atk(pwr vs dfp)",
            "hit",
            "damage body 1d3+imp",
            "damage soul 1d2+imp",
            "effect soulburn 1",
            "endhit",
            "crit",
            "effect soulburn 5",
            "endcrit",
            "endatk"   
        ]
        self.savagery_ary = [
            "do 2 times",
            "atk(atp vs dfp)",
            "hit",
            "Damage Body WEAPON",
            "Effect Bleed 1",
            "endhit",
            "endatk",
            "done"
        ]
        self.savagery_expected = [
            "do 2 times",
            "atk(atp vs dfp)",
            "hit",
            "damage body weapon",
            "effect bleed 1",
            "endhit",
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
    hit
        Damage Body 1d3+IMP 
        Damage Soul 1d2+IMP
        Effect Soulburn 1
    endhit
    crit 
        Effect Soulburn 5
    endcrit
endatk"""
        self.savagery_str = """
#This attack hits 1 target twice and inflicts Bleed.
do 2 times
    atk(atp vs dfp)
        hit
            Damage Body WEAPON
            Effect Bleed 1
        endhit
    endatk
done"""
        
    def test_oneliners(self):
        bleed1 = cr.crit_compile("Effect Bleed 1")
        shield = cr.crit_compile("Effect Shield 10 100")
        body_imp = cr.crit_compile("Damage Body 1d4+IMP")
        soul_weap = cr.crit_compile("Damage Soul WEAPON")

        self.assertListEqual(bleed1, ["effect bleed 1"])
        self.assertListEqual(shield, ["effect shield 10 100"])
        self.assertListEqual(body_imp, ["damage body 1d4+imp"])
        self.assertListEqual(soul_weap, ["damage soul weapon"])
        self.assertRaises(cr.UnknownCritSyntaxError, cr.crit_compile, "Unknown")
        self.assertRaises(cr.BadEffectError, cr.crit_compile, "Effect Bad 12")
    
    def test_arrays(self):
        em_compiled = cr.crit_compile(self.emberspark_ary)
        sv_compiled = cr.crit_compile(self.savagery_ary)
        self.assertListEqual(em_compiled, self.emberspark_expected)
        self.assertListEqual(sv_compiled, self.savagery_expected)

    def test_string(self):
        em_compiled = cr.crit_compile(self.emberspark_str)
        sv_compiled = cr.crit_compile(self.savagery_str)
        self.assertListEqual(em_compiled, self.emberspark_expected)
        self.assertListEqual(sv_compiled, self.savagery_expected)
    
    def test_do_failures(self):
        done_before_do = """
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
        do 18 times
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
        self.assertRaises(cr.EarlyDoneError, cr.crit_compile, done_before_do)
        self.assertRaises(cr.NoDoneError, cr.crit_compile, no_done)
        self.assertRaises(cr.EarlyDoneError, cr.crit_compile, no_do)
        self.assertRaises(cr.NoDoneError, cr.crit_compile, odd_do)
        self.assertRaises(cr.NestedDoBlockError, cr.crit_compile, nested_do)
    
    def test_crit_failures(self):
        crit_outside = """
        crit
            Damage Body 10d10
        endcrit
        """
        endcrit_before_crit = """
        endcrit
            Damage Body 10d10
        crit
        """
        no_crit = """
        Damage Body 10d10
        endcrit
        """
        no_endcrit = """
        atk(atp vs dfp)
            crit
                Damage Body 10d10
        endatk

        """
        odd_crit = """
        atk(atp vs dfp)
            crit
                Damage Body 10d10
            endcrit
        endatk
        atk(pwr vs tou)
            crit
        endatk
        """
        nested_crit = """
        atk(atp vs dfp)
            Damage Body 1d10
            crit
                Damage Body 10d10
                crit
                    Damage Soul 10d10
                endcrit
            endcrit
        end
        """

        self.assertRaises(cr.CritWithoutAtkError, cr.crit_compile, crit_outside)
        self.assertRaises(cr.EarlyEndCritError, cr.crit_compile, endcrit_before_crit)
        self.assertRaises(cr.EarlyEndCritError, cr.crit_compile, no_crit)
        self.assertRaises(cr.NoEndCritError, cr.crit_compile, no_endcrit)
        self.assertRaises(cr.NoEndCritError, cr.crit_compile, odd_crit)
        self.assertRaises(cr.NestedCritBlockError, cr.crit_compile, nested_crit)

    def test_dice_string_base(self):
        waryar = build_char("human", "warrior", "Fred")
        test_string = "1d3+imp+weapon+strmod+sklmod"
        test1 = cbt.dice_script_parse(waryar, test_string)
        self.assertEqual(test1, "1d3+0+1+2+2+2")
        
    def test_dice_string_equipped(self):
        waryar = build_char("human", "warrior", "Fred")
        wpn = make_weapon("mace")
        test_string = "1d3+imp+weapon+strmod+sklmod"
        waryar.weapon = wpn
        test2 = cbt.dice_script_parse(waryar, test_string)
        self.assertEqual(test2, "1d3+0+1d4+2+2+2")
    
    def test_dice_string_with_implement(self):
        waryar = build_char("human", "warrior", "Fred")
        wpn = make_weapon("mace")
        imp = make_implement("oak staff")
        test_string = "1d3+imp+weapon+strmod+sklmod"
        waryar.weapon = wpn
        waryar.implement = imp
        test3 = cbt.dice_script_parse(waryar, test_string)
        self.assertEqual(test3, "1d3+1d6+1d4+2+2+2")




# CritScript #
A tiny domain language for describing skills and on-crit effects for System 12.

## Purpose ##
CritScript makes an attempt to define certain game functions as data, so they can be stored in data files..

## Samples ##

### Weapons ###
In System 12, weapons usually have some kind of effect on crit instead of the usual extra damage. These are one-liners, usually, but could theoretically be scripts unto themselves.

* Shortswords: `Bleed 1`
* Daggers: `Body 2d4+SKLMOD`

### Skills ###

Skills and magic are longer pieces of code, separated by newlines.
* The Emberspark spell:
```
#This spell hits one target.
#Caster makes a PWR roll against target's DFP.
#If successful, target takes 1d3 + caster's implement in Body damage and 1d2 + caster's implement in Soul damage as well as the Soulburn debuff for 1 turn. On crit, this deals an additional 5 turns of Soulburn.

atk(pwr vs dfp) 
    Damage Body 1d3+IMP 
    Damage Soul 1d2+IMP
    Effect Soulburn 1
    crit 
        Effect Soulburn 5
    endcrit
endatk
```

* The Savagery attack:
```
#This attack hits 1 target twice and inflicts Bleed.
do 2 times
    atk(atp vs dfp)
        Damage Body WEAPON
        Effect Bleed 1
    endatk
done
```

## Implementation ##

CritScript is run against a target or targets. CritScript code is rendered into a list and interpreted against a target:

`run_script(user: Character, targets: Iterable[Character], script: List[str])`

## Usage ##

Below is a sample JSON file that holds the above skills. This example pre-renders the lines of code into an array format, but another tool could do this from text files containing CritScript.

```json
{
    "emberspark": {
        "targets": 1,
        "code": [
            "atk(pwr vs dfp)",
            "Damage Body 1d3+IMP",
            "Damage Soul 1d2+IMP",
            "Effect Soulburn 1",
            "crit",
            "Effect Soulburn 5",
            "endcrit",
            "endatk"
        ]
    },
    "savagery": {
        "targets": 1,
        "code": [
            "do 2 times",
            "atk(atp vs dfp)",
            "Damage Body WEAPON",
            "Effect Bleed 1",
            "endatk",
            "done"
        ]
    }
}
```






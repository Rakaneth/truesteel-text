# CritScript #
A tiny domain language for describing skills and on-crit effects for System 12.

## Purpose ##
CritScript makes an attempt to define certain game functions as data, so they can be stored in data files..

## Samples ##

### Weapons ###
In System 12, weapons usually have some kind of effect on crit in addition to or instead of the usual extra damage. These are one-liners, usually, but could theoretically be scripts unto themselves.

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
    hit
        Damage Body 1d3+IMP 
        Damage Soul 1d2+IMP
        Effect Soulburn 1
    endhit
    crit 
        Effect Soulburn 5
    endcrit
endatk
```

* The Fireball spell:
```
#This spell hits all targets and applies the Burning effect.
Damage Body 1d6+IMP
Effect Burn 1
```

* The Savagery attack:
```
#This attack hits 1 target twice and inflicts Bleed.
do 2 times
    atk(atp vs dfp)
        hit
            Damage Body WEAPON
            Effect Bleed 1
        endhit
    endatk
done
```

## Implementation ##

Raw CritScript is compiled by `crit_compile` in the `critscript` module. CritScript's limited domain prevents it from having runtime errors, and so all errors are detected at compile time. The compiled CritScript becomes a compressed list of instructions, which is run against a target or targets by `run_script`.

`crit_compile(code: Union[List[str], str]) -> List[str]`

`run_script(user: Character, targets: Iterable[Character], script: List[str])`

## Usage ##

### JSON File ###

Below is a sample JSON file that holds the above skills. This example pre-renders the lines of code into an array format, which would be the best way to store CritScript in JSON or YAML files. **It is vitally important that the targeting scheme (currently just "1","all", or "self") be conveyed in the JSON file.**

```json
{
    "emberspark": {
        "targets": "1",
        "code": [
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
    },
    "fireball": {
        "targets": "all",
        "code": [
            "Damage Body 2d6+IMP",
            "Effect Burn 1",
        ]
    },
    "savagery": {
        "targets": "1",
        "code": [
            "do 2 times",
            "atk(atp vs dfp)",
            "hit",
            "Damage Body WEAPON",
            "Effect Bleed 1",
            "endhit",
            "endatk",
            "done"
        ]
    }
}
```
### CritData Files ###

CritScript also has its own data format with the extension `.critdata`. The function `read_critdata` returns a `dict` mapping skill names to compiled, ready-to-use CritScript.

`read_critdata(filename: str) -> dict`

A CritData file looks like this:
```
[Soulspark:Target 1]
    atk(pwr vs dfp)
        hit
            Damage Body 1d3+IMP
            Damage Soul 1d2+IMP
            Effect Soulburn 1
        endhit
    endatk
[/Soulspark]

[Fireball:Target All]
    Damage Body 1d6+IMP
[/Fireball]

[Savagery:Target 1]
    Target 1
    do 2 times
        atk(atp vs dfp)
            hit
                Damage Body WEAPON
                Effect Bleed 1
            endhit
        endatk
    done
[/Savagery]
```

Each skill begins with an opening tag that combines the skill's name and targeting specification. 

* `Target 1` means that the skill targets one enemy.
* `Target All` means that the skill targets all enemies.
* `Target Self` means that the skill targets the user.

The CritScript code defining what the skill does follows the opening tag. Finally, the closing tag repeats the name of the skill with a backslash, much in the style of BBCode.

## Reference ##

CritScript is written from the point of view of the user of the skill. It is assumed that the code is being run against a selected target or group of enemies. 

### Comments ###

Lines beginning with `#` are ignored, and so can be used for comments. **Inline comments are not currently supported.**

### Casing ###

Casing does not matter. `EFFECT BURN 1`, `Effect Burn 1`, `effect burn 1`, and `EfFeCt BuRn 1` are all valid.

### Whitespace ###

Lines are separated by the newline (`\n`) character. Dice notation cannot have spaces inside the string. Trailing and leading whitespace on lines is ignored (allowing for indentation, as in the examples)

### Effects ###

A line in the form of `Effect [name of effect] [duration of effect]([potency of effect]` applies the effect to all targets with the given duration and potency. The name given must be a valid effect.
* TODO: List of valid effect names

#### Effect Samples ####
* `Effect Bleed 1` applies the Bleed effect for 1 turn.
* `Effect Shield 10 100` applies the Shield effect for 10 turns at 100 potency.

### Damage ###

A line in the form of `Damage [Body|Mind|Soul] [dice-notation|WEAPON]` applies the listed damage type in the amount specified by the dice notation. `WEAPON` replaces the dice notation and inserts the damage of the user's weapon (including crit effects). One of `IMP`, `SKLMOD`, or `STRMOD` can be added to the dice notation to include the user's implement damage, skill-based modifier, or strength-based modifier respectively.

#### Damage Examples ####
Our user for the following samples has this loadout:

```
Str 25 (+2 strength mod)
Skl 15 (+1 skill mod)

Weapon: Dagger (1d4+sklmod, crit: Damage Body 2d4)
Implement: Brass Rod(1d3)
```

* `Damage Body 1d3` deals 1d3 Body damage
* `Damage Body 1d3+1` deals 1d3+1 Body damage
* `Damage Body 1d3+STRMOD` deals 1d3+2 Body damage.
* `Damage Body 1d3+SKLMOD` deals 1d3+1 Body damage.
* `Damage Body WEAPON` deals 1d4+1 Body damage.
* `Damage Soul 1d6+2+IMP` deals 1d3+1d6+2 Soul damage.

### Blocks ###

There are six block constructs in CritScript: `do`, `atk`, `crit`, `miss`, `hit` and `self`. 

#### Self (NOT IMPLEMENTED YET) ####

Self-blocks begin with `self` and end with `endself`. Code run in a self-block is always applied to the user. This allows for things like risky powers that damage oneself to use or self-buffs.

```
#Shield spell
self
    Effect Shield 10 100
endself

#Soul Sacrifice spell
self
    Damage Soul 1d3
endself
Damage Body 2d10+IMP
```

#### Do ####

Do-blocks begin with `do (n) times` and end with `done`. Code run in do-blocks is repeated `n` times.

```
#Savagery
do 2 times
    atk(atp vs dfp)
        hit
            Damage Body WEAPON
            Effect Bleed 1
        endhit
    endatk
done
```

#### Atk ####

Atk-blocks begin with `atk([stat] vs [stat])` and end with `endatk`. Code in atk-blocks is run if a successful attack is rolled with the given stats. The first stat can be one of `atp` or `pwr`, while the second stat can be one of `dfp`, `wil`,  or `tou`.**Any other values given will raise an error.** Code in atk-blocks will be run separately for each attacker in the case of an `all` target; this means that each defender gets a separate chance to resist the attack. Together, atk-blocks, hit-blocks, crit-blocks, and miss-blocks can combine in a manner similar to `if`, `then`, `else if`, and `else` in mainstream programming languages.

* If the attack specified in `atk` succeeds:
    * Run any encountered `hit` blocks.
    * If the attack was a critical hit, run any encountered `crit` blocks. Otherwise, skip them.
    * Skip any encountered `miss` blocks.
* If the attack misses:
    * Run any encountered `miss` blocks.
    * Skip any encountered `hit` blocks.
    * Skip any encountered `crit` blocks.

##### Hit (NOT IMPLEMENTED YET) #####
Hit-blocks begin with `hit` and end with `endhit`. Code in hit-blocks is run if the attack roll generated by the enclosing atk-block is successful.

* **It is an error to use a hit-block outside of an atk-block.**

##### Crit #####

Crit-blocks begin with `crit` and end with `endcrit`. Code in crit-blocks is run if the attack roll generated by a previous atk-block scored a critical hit. While it is not techncially an error to use multiple crit-blocks within one atk-block, it is generally unnecessary to do so.
* **It is an error to use a crit-block outside of an atk-block.** 

```
#Heartseeker
atk(atp vs dfp)
    hit
        Damage Body WEAPON
    endhit
    crit
        Damage Body 3d8+SKLMOD
    endcrit
endatk
```

##### Miss (NOT IMPLEMENTED YET) #####

Miss-blocks begin with `miss` and end with `endmiss`. Code in miss-blocks is run if the attack roll generated by a previous atk-block missed. While it is not technically an error to use multiple miss-blocks within one atk-block, it is generally unnecessary to do so.
* **It is an error to use a miss-block outside of an atk-block.** 

```
#Mind Sear
atk(pwr vs wil)
    hit
        Damage Mind 2d6+IMP
    endhit
    miss
        Damage Mind 1d6+IMP
    endmiss
endatk 
```










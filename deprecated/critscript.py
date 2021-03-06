import re

from typing import Iterable, List, Union
from character import Character
from combat import apply_effect, remove_effect, hit, damage, RollResult
from effects import EffectNames

DO_PATTERN = re.compile(r"do (?P<times>\d+) times")
ATK_PATTERN = re.compile(r"atk\((?P<atk_stat>atp|pwr) vs (?P<defense_stat>\d+|tou|wil|dfp)\)")
COMMENT_PATTERN = re.compile(r"#.*")
DMG_PATTERN = re.compile(r"damage (?P<dtype>body|soul|mind) (?P<dmg>(?:(?:[+-]?\d+d\d+)|(?:[+-]?(?:imp|sklmod|strmod|weapon))|(?:[+-]?\d+))+)")
EFF_PATTERN = re.compile(r"effect (?P<eff>[a-z]+)\s+(?P<duration>\d+)(?:$|\s+(?P<potency>\d+))")
EFF_NAMES = [name.value.lower() for name in EffectNames]

class CritScriptSyntaxError(Exception):
    """Custom exception raised when CritScript errors occur."""
    def __init__(self, line_no: int, line: str, err_string: str):
        msg = f"Error in script line {line_no+1}: {line}\n{err_string}"
        self.line = line
        self.line_no = line_no
        self.msg = msg
        super().__init__(msg)

class EarlyEndCritError(CritScriptSyntaxError):
    """Raised when `endcrit` precedes `crit`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "endcrit before crit")

class EarlyDoneError(CritScriptSyntaxError):
    """Raised when `done` precedes `do`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "done before do")

class EarlyEndAtkError(CritScriptSyntaxError):
    """Raised when `endatk` precedes `atk`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "endatk before atk")

class EarlyEndSelfError(CritScriptSyntaxError):
    """Raised when `endself` precedes `self`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "endself before self")

class EarlyEndHitError(CritScriptSyntaxError):
    """Raised when `endhit` precedes `hit`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "endhit before hit")

class EarlyEndMissError(CritScriptSyntaxError):
    """Raised when `endmiss` precedes `miss`."""
    def __init__(self, line_no, int, line: str):
        super().__init__(line_no, line, "endmiss before miss")

class NestedCritBlockError(CritScriptSyntaxError):
    """Raised when a `crit` block is inside another."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "nested crit block")

class NestedDoBlockError(CritScriptSyntaxError):
    """Raised when a `do` block is inside another."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "nested do block")

class NestedAtkBlockError(CritScriptSyntaxError):
    """Raised when an `atk` block is inside another."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "nested atk block")

class NestedHitBlockError(CritScriptSyntaxError):
    """Raised when a `hit` block is inside another."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "nested hit block")

class NestedMissBlockError(CritScriptSyntaxError):
    """Raised when a `miss` block is inside another."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "nested miss block")

class NestedSelfBlockError(CritScriptSyntaxError):
    """Raised when a `self` block is inside another."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "nested self block")

class NoEndCritError(CritScriptSyntaxError):
    """Raised when `endcrit` is omitted from a `crit` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "crit without endcrit")

class NoEndAtkError(CritScriptSyntaxError):
    """Raised when `endatk` is omitted from an `atk` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "atk wtihout endatk")

class NoDoneError(CritScriptSyntaxError):
    """Raised when `done` is omitted from a `do` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "do without done")

class NoEndHitError(CritScriptSyntaxError):
    """Raised when `endhit` is omitted from a `hit` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "hit without endhit")

class NoEndMissError(CritScriptSyntaxError):
    """Raised when `endmiss` is omitted from a `miss` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "miss without endmiss")

class NoEndSelfError(CritScriptSyntaxError):
    """Raised when `endself` is omitted from a `self` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "self without endself")

class UnknownCritSyntaxError(CritScriptSyntaxError):
    """Raised when incorrect CritScript syntax is encountered."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "unrecognized syntax")

class BadEffectError(CritScriptSyntaxError):
    """Raised when an invalid effect is given."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "unrecognized effect")

class CritWithoutAtkError(CritScriptSyntaxError):
    """Raised when `crit` is used outside of an `atk` block."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "crit outside of atk block")

class HitWithoutAtkError(CritScriptSyntaxError):
    """Raised when `hit` is used outside of an `atk` block,"""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "hit outside of atk block")

class MissWithoutAtkError(CritScriptSyntaxError):
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "miss outside of atk block")





def crit_compile(code: Union[List[str], str]) -> List[str]:
    """
    Compiles CritScript `code` (as a list or raw string) into an array of
    instructions that can be fed to `Combat.run_script`. See 
    `critscript.md` for further documentation on CritScript.
    """
    if isinstance(code, str):
        raw_code = [ln for ln in code.split("\n") if len(ln) > 0]
    else:
        raw_code = code
    
    do_open = False
    atk_open = False
    crit_open = False
    self_open = False
    hit_open = False
    miss_open = False
    last_crit_idx = -1
    last_atk_idx = -1
    last_do_idx = -1
    last_hit_idx = -1
    last_self_idx = -1
    last_miss_idx = -1
    last_do_line = ""
    last_atk_line = ""

    stripped_code = [
        ln.strip().lower() 
        for ln in raw_code 
        if not ln.strip().startswith('#')
        if len(ln.strip()) > 0]
    
    for line_no, line in enumerate(stripped_code):
        eff = EFF_PATTERN.match(line)
        if line == "endcrit":
            if not crit_open:
                raise EarlyEndCritError(line_no, line)
            else:
                crit_open = False
        elif line == "endatk":
            if not atk_open:
                raise EarlyEndAtkError(line_no, line)
            else:
                atk_open = False
        elif line == "done":
            if not do_open:
                raise EarlyDoneError(line_no, line)
            else:
                do_open = False
        elif line == "endmiss":
            if not miss_open:
                raise EarlyEndMissError(line_no, line)
            else:
                miss_open = False
        elif line == "endself":
            if not self_open:
                raise EarlyEndSelfError(line_no, line)
            else:
                self_open = False
        elif line == "endhit":
            if not hit_open:
                raise EarlyEndHitError(line_no, line)
            else:
                hit_open = False
        elif line == "crit": 
            if crit_open:
                raise NestedCritBlockError(line_no, line)
            elif not atk_open:
                raise CritWithoutAtkError(line_no, line)
            else:
                crit_open = True
                last_crit_idx = line_no
        elif line == "hit":
            if hit_open:
                raise NestedHitBlockError(line_no, line)
            elif not atk_open:
                raise HitWithoutAtkError(line_no, line)
            else:
                hit_open = True
                last_hit_idx = line_no
        elif line == "miss":
            if miss_open:
                raise NestedHitBlockError(line_no, line)
            elif not atk_open:
                raise MissWithoutAtkError(line_no, line)
            else:
                miss_open = True
                last_miss_idx = line_no
        elif line == "self":
            if self_open:
                raise NestedSelfBlockError(line_no, line)
            else:
                self_open = True
                last_self_idx = line_no
        elif DO_PATTERN.match(line):
            if do_open:
                raise NestedDoBlockError(line_no, line)
            else:
                do_open = True
                last_do_idx = line_no
                last_do_line = line
        elif ATK_PATTERN.match(line):
            if atk_open:
                raise NestedAtkBlockError(line_no, line)
            else:
                atk_open = True
                last_atk_idx = line_no
                last_atk_line = line
        elif eff:
            if eff.group("eff") not in EFF_NAMES:
                raise BadEffectError(line_no, line)
        elif DMG_PATTERN.match(line):
            pass
        elif line == "weaponcrit":
            pass
        else:
            raise UnknownCritSyntaxError(line_no, line)
    
    if crit_open:
        raise NoEndCritError(last_crit_idx, "crit")
    
    if do_open:
        raise NoDoneError(last_do_idx, last_do_line)
    
    if atk_open:
        raise NoEndAtkError(last_atk_idx, last_atk_line)
    
    if miss_open:
        raise NoEndMissError(last_miss_idx, "miss")
    
    if self_open:
        raise NoEndSelfError(last_self_idx, "self")
    
    if hit_open:
        raise NoEndHitError(last_hit_idx, "hit")
        
    return stripped_code

def run_atk_block(
    user: Character, 
    cur_target: Character, 
    roll_result: RollResult, 
    subscript: List[str]
):
    subinst_counter = 0
    while subinst_counter < len(subscript):
        cur_cmd = subscript[subinst_counter]
        #if 




def run_script(
    user: Character, 
    targets: Iterable[Character],
    script: List[str]
):
    inst_counter = 0

    cur_cmd = script[inst_counter]
    do_match = DO_PATTERN.match(cur_cmd)
    atk_match = ATK_PATTERN.match(cur_cmd)

    if inst_counter >= len(script):
        return
    elif do_match:
        num_times = int(do_match.group("times"))
        done_idx = script.index("done", inst_counter)
        for _ in range(num_times):
            run_script(user, targets, script[inst_counter+1:done_idx])
        inst_counter = done_idx
    elif cur_cmd == "self":
        endself_idx = script.index("endself", inst_counter)
        run_script(user, (user,), script[inst_counter+1:endself_idx])
        inst_counter = endself_idx
    elif atk_match:
        endatk_idx = script.index("endatk", inst_counter)
        for target in targets:
            atk_result = hit(user, target, atk_match.group("atk_stat"), atk_match.group("def_stat"))
            run_atk_block(user, target, atk_result, script[inst_counter+1:endatk_idx])



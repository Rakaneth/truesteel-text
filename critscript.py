import re

from typing import Iterable, List, Union
from character import Character
from combat import apply_effect, remove_effect, hit, damage
from effects import EffectNames

DO_PATTERN = re.compile(r"do (?P<times>\d+) times")
ATK_PATTERN = re.compile(r"atk\((?P<atk_stat>atp|pwr) vs (?P<defense_stat>\d+|tou|wil|dfp)\)")
COMMENT_PATTERN = re.compile(r"#.*")
DMG_PATTERN = re.compile(r"damage (?P<dtype>body|soul|mind) (?P<dmg>weapon|\d+d\d+(?:\+.+)*)")
EFF_PATTERN = re.compile(r"effect (?P<eff>[a-z]+)\s+(?P<duration>\d+)(?:$|\s+(?P<potency>\d+))")
EFF_NAMES = [name.value.lower() for name in EffectNames]

class CritScriptSyntaxError(Exception):
    """Custom exception raised when CritScript errors occur."""

    def __init__(self, line_no: int, line: str, err_string: str):
        msg = f"Error in script line {line_no+1}: {line}\n{err_string}"
        super().__init__(msg)

class EarlyEndCritError(CritScriptSyntaxError):
    """Raised when `endcrit` comes before `crit`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "endcrit before crit")

class EarlyDoneError(CritScriptSyntaxError):
    """Raised when `done` comes before `do`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "done before do")

class EarlyEndAtkError(CritScriptSyntaxError):
    """Raised when `endatk` comes before `atk`."""
    def __init__(self, line_no: int, line: str):
        super().__init__(line_no, line, "endatk before atk")

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

def crit_compile(code: Union[List[str], str]) -> List[str]:
    """
    Compiles CritScript `code` (as a list or raw string) into an array of
    instructions that can be fed to `run_scripts`. See 
    `critscript.md` for further documentation on CritScript.
    """
    if isinstance(code, str):
        raw_code = [ln for ln in code.split("\n") if len(ln) > 0]
    else:
        raw_code = code
    
    do_open = False
    atk_open = False
    crit_open = False
    last_crit_idx = -1
    last_atk_idx = -1
    last_do_idx = -1
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
        elif line == "crit": 
            if crit_open:
                raise NestedCritBlockError(line_no, line)
            elif not atk_open:
                raise CritWithoutAtkError(line_no, line)
            else:
                crit_open = True
                last_crit_idx = line_no
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
        else:
            raise UnknownCritSyntaxError(line_no, line)
    
    if crit_open:
        raise NoEndCritError(last_crit_idx, "crit")
    
    if do_open:
        raise NoDoneError(last_do_idx, last_do_line)
    
    if atk_open:
        raise NoEndAtkError(last_atk_idx, last_atk_line)
        
    return stripped_code



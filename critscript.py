import re

from typing import Coroutine, Iterable, List, Union
from character import Character
from combat import apply_effect, remove_effect, hit, damage

do_pattern = re.compile(r"do (?P<times>\d+) times")
atk_pattern = re.compile(r"atk\((?P<atk_stat>atp|pwr) vs (?P<defense_stat>\d+|tou|wil|dfp)\)")
comment_pattern = re.compile(r"#.*")
dmg_pattern = re.compile(r"damage (?P<dtype>body|soul|mind) (?P<dmg>weapon|\d+d\d+(?:\+.+)*)")
eff_pattern = re.compile(r"effect (?P<eff>[a-z]+)\s+(?P<duration>\d+)(?:$|\s+(?P<potency>\d+))")
dice_pattern = re.compile(r"(?P<num>\d+)d(?P<sides>\d+)(?P<mods>(?:\+(?:\d+|IMP|STRMOD|SKLMOD))*)")

class CritScriptSyntaxError(Exception):
    """Custom exception raised when CritScript errors occur."""

    def __init__(self, line_no: int, line: str, err_string: str):
        msg = f"Error in script line {line_no+1}: {line}\n{err_string}"
        super().__init__(msg)

def compile(code: Union[List[str], str]) -> List[str]:
    if isinstance(code, str):
        raw_code = [ln for ln in code.split("\n") if len(ln) > 0]
    else:
        raw_code = code
    
    do_open = False
    atk_open = False
    crit_open = False

    stripped_code = [
        ln.strip().lower() 
        for ln in raw_code 
        if not ln.strip().startswith('#')
        if len(ln.strip()) > 0]
    
    for line_number, line in enumerate(stripped_code):
        if line == "endcrit":
            if not crit_open:
                raise CritScriptSyntaxError(line_number, line, "endcrit before crit")
            else:
                crit_open = False
        elif line == "endatk":
            if not atk_open:
                raise CritScriptSyntaxError(line_number, line, "endatk before atk")
            else:
                atk_open = False
        elif line == "done":
            if not do_open:
                raise CritScriptSyntaxError(line_number, line, "done before do")
            else:
                do_open = False
        elif line == "crit": 
            if crit_open:
                raise CritScriptSyntaxError(line_number, line, "nested crit blocks")
            crit_open = True
        elif do_pattern.match(line):
            if do_open:
                raise CritScriptSyntaxError(line_number, line, "nested do blocks")
            do_open = True
        elif atk_pattern.match(line):
            if atk_open:
                raise CritScriptSyntaxError(line_number, line, "nested atk blocks")
            atk_open = True
        elif eff_pattern.match(line):
            pass
        elif dmg_pattern.match(line):
            pass
        else:
            raise CritScriptSyntaxError(line_number, line, "unrecognized syntax")
    
    if crit_open:
        raise CritScriptSyntaxError(line_number, line, "crit without endcrit")
    
    if do_open:
        raise CritScriptSyntaxError(line_number, line, "do without done")
    
    if atk_open:
        raise CritScriptSyntaxError(line_number, line, "atk without endatk")
        
    return stripped_code
        
    
def run_script(user: Character, targets: Iterable[Character], code: List[str]):
    compiled = compile(code)




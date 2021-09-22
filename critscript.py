import re

from typing import Iterable, List, Union
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
    
    raw_endcrit = True
    raw_done = True
    raw_endatk = True

    stripped_code = [
        ln.strip().lower() 
        for ln in raw_code 
        if not ln.strip().startswith('#')
        if len(ln.strip()) > 0]
    
    for line_number, line in enumerate(stripped_code):
        if line == "endcrit":
            if raw_endcrit:
                raise CritScriptSyntaxError(line_number, line, "endcrit before crit")
            else:
                raw_endcrit = True
        elif line == "endatk":
            if raw_endatk:
                raise CritScriptSyntaxError(line_number, line, "endatk before atk")
            else:
                raw_endatk = True
        elif line == "done":
            if raw_done:
                raise CritScriptSyntaxError(line_number, line, "done before do")
            else:
                raw_done = True
        elif line == "crit": 
            if not "endcrit" in stripped_code[line_number:]:
                raise CritScriptSyntaxError(line_number, line, "crit without endcrit")
            raw_endcrit = False
        elif do_pattern.match(line):
            if not "done" in stripped_code[line_number:]:
                raise CritScriptSyntaxError(line_number, line, "do without done")
            raw_done = False
        elif atk_pattern.match(line):
            if not "endatk" in stripped_code[line_number:]:
                raise CritScriptSyntaxError(line_number, line, "atk without endatk")
            raw_endatk = False
        elif eff_pattern.match(line):
            pass
        elif dmg_pattern.match(line):
            pass
        else:
            raise CritScriptSyntaxError(line_number, line, "unrecognized syntax")
        
    return stripped_code
        
    
def run_script(user: Character, targets: Iterable[Character], code: List[str]):
    compiled = compile(code)




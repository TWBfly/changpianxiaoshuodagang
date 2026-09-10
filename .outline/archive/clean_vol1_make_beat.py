# -*- coding: utf-8 -*-
"""Ensure all make_beat calls across vol1_specs.py have exactly 10 arguments"""

import ast
from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def clean_vol1():
    vol1_path = OUTLINE_DIR / "vol1_specs.py"
    lines = vol1_path.read_text(encoding="utf-8").splitlines()
    
    new_lines = []
    for line in lines:
        if "make_beat(" in line and line.strip().startswith("make_beat("):
            # Parse line with ast
            try:
                tree = ast.parse(line.strip())
                call = tree.body[0].value
                if isinstance(call, ast.Call):
                    if len(call.args) == 9:
                        # Find where delta dict is (usually 7th or 8th arg)
                        # We need 10 args: (role, cause, actor, b_goal, action, counterforce, info_choice, delta_dict, a_goal, pressure)
                        # Let's inspect the args
                        arg_strs = [ast.unparse(a) for a in call.args]
                        # If len is 9, insert an empty/default dramatic reason before delta (or after info_choice)
                        # Let's check which arg is dict
                        dict_idx = -1
                        for idx, a in enumerate(call.args):
                            if isinstance(a, ast.Dict):
                                dict_idx = idx
                                break
                        if dict_idx == 6:
                            # missing info_choice before delta
                            arg_strs.insert(6, '"展现核心戏剧推动力"')
                        elif dict_idx == 7:
                            # has 7 args before delta, 1 after -> missing pressure at the end
                            arg_strs.append('"推进核心因果闭环"')
                        
                        indent = " " * (len(line) - len(line.lstrip()))
                        new_line = indent + f"make_beat({', '.join(arg_strs)}),"
                        new_lines.append(new_line)
                        continue
                    elif len(call.args) == 11:
                        # remove extra arg
                        arg_strs = [ast.unparse(a) for a in call.args[:10]]
                        indent = " " * (len(line) - len(line.lstrip()))
                        new_line = indent + f"make_beat({', '.join(arg_strs)}),"
                        new_lines.append(new_line)
                        continue
            except Exception as e:
                pass
        new_lines.append(line)
        
    vol1_path.write_text("\n".join(new_lines), encoding="utf-8")
    print("Fixed vol1_specs.py make_beat arg counts!")

if __name__ == "__main__":
    clean_vol1()

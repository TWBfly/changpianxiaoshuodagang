# -*- coding: utf-8 -*-
"""Fix Volume IDs and typos across vol4, vol5, vol6"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def fix_all():
    # 1. vol4_specs.py: replace CHAR.xiao_xiao with CHAR.xiao_minghuang
    f4 = OUTLINE_DIR / "vol4_specs.py"
    t4 = f4.read_text(encoding="utf-8")
    t4_fixed = t4.replace('"CHAR.xiao_xiao"', '"CHAR.xiao_minghuang"')
    f4.write_text(t4_fixed, encoding="utf-8")
    print("Fixed vol4_specs.py")

    # 2. vol5_specs.py: replace VOLUME.v5_slaying_immortals with VOLUME.v5_taiji_battle
    f5 = OUTLINE_DIR / "vol5_specs.py"
    t5 = f5.read_text(encoding="utf-8")
    t5_fixed = t5.replace('"VOLUME.v5_slaying_immortals"', '"VOLUME.v5_taiji_battle"')
    f5.write_text(t5_fixed, encoding="utf-8")
    print("Fixed vol5_specs.py")

    # 3. vol6_specs.py: replace VOLUME.v6_grand_era with VOLUME.v6_world_renewal
    f6 = OUTLINE_DIR / "vol6_specs.py"
    t6 = f6.read_text(encoding="utf-8")
    t6_fixed = t6.replace('"VOLUME.v6_grand_era"', '"VOLUME.v6_world_renewal"')
    f6.write_text(t6_fixed, encoding="utf-8")
    print("Fixed vol6_specs.py")

if __name__ == "__main__":
    fix_all()

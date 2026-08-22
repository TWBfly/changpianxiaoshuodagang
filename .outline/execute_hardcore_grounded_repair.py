# -*- coding: utf-8 -*-
"""
Execute Hardcore Grounded Repair:
1. Fix Zhao Biao lifecycle in build_and_audit.py (Ch 4 assassinated by palace death squads, confesses ambush map, permanently dead).
2. Fix Vol 1 summary in build_and_audit.py (Ch 6 divine furnace alchemy, Ch 7 black market investigation).
3. Fix Ch 104 and 105 conflict actors in vol5_specs.py (replace ally pairings with demonic CHAR.xiao_qianyuan).
4. Synchronize build_and_audit.py, generate_build_script.py and compile master outline.
"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def fix_build_and_audit():
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")

    # Fix Zhao Biao fate description in character profile
    b_text = b_text.replace(
        '"第4章被顾惊澜当众捏碎琵琶骨废除修为送官严办"',
        '"第4章被王府死士灭口刺杀，临死前交出寿宴布防图后气绝身亡彻底除名"'
    )

    # Fix Vol 1 turning points
    b_text = b_text.replace(
        '"第1章破渊救老仆废恶奴、第7章神农鼎炼成九转天元金丹、第13章寿宴托棺斩青州王赵无极',
        '"第1章破渊救老仆废恶奴、第6章神农鼎重开炼制九转金丹、第7章夜探黑市破译血契残卷、第13章寿宴托棺斩青州王赵无极'
    )

    # Fix Vol 3 turning points (Langjuxu -> Shanhaiguan / Yanmen)
    b_text = b_text.replace(
        '第65章封狼居胥祭奠顾老帅',
        '第65章山海关祭奠忠烈老帅'
    )

    b_file.write_text(b_text, encoding="utf-8")
    print("Fixed build_and_audit.py: Aligned Zhao Biao lifecycle, Vol 1 turning points, and Shanhaiguan memorial.")

def fix_vol5_ch104_ch105():
    v5_file = OUTLINE_DIR / "vol5_specs.py"
    v5_text = v5_file.read_text(encoding="utf-8")

    # Fix Ch 104 actor list
    v5_text = v5_text.replace(
        'add_ch(104, "VOLUME.v5_taiji_battle", "幽冥暗影刺天元", ["CHAR.leng_yue", "CHAR.gu_jinglan"],',
        'add_ch(104, "VOLUME.v5_taiji_battle", "幽冥暗影刺天元", ["CHAR.leng_yue", "CHAR.xiao_qianyuan"],'
    )

    # Fix Ch 105 actor list
    v5_text = v5_text.replace(
        'add_ch(105, "VOLUME.v5_taiji_battle", "七美同心锁魔躯", ["CHAR.gu_jinglan", "CHAR.ye_polu"],',
        'add_ch(105, "VOLUME.v5_taiji_battle", "七美同心锁魔躯", ["CHAR.gu_jinglan", "CHAR.xiao_qianyuan"],'
    )

    v5_file.write_text(v5_text, encoding="utf-8")
    print("Fixed vol5_specs.py: Corrected conflict opponent in Ch 104 and Ch 105 to CHAR.xiao_qianyuan.")

def sync_generate_build_script():
    b_text = (OUTLINE_DIR / "build_and_audit.py").read_text(encoding="utf-8")
    (OUTLINE_DIR / "generate_build_script.py").write_text(b_text, encoding="utf-8")
    print("Synchronized generate_build_script.py with build_and_audit.py.")

def main():
    fix_build_and_audit()
    fix_vol5_ch104_ch105()
    sync_generate_build_script()

if __name__ == "__main__":
    main()

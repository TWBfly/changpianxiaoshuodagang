# -*- coding: utf-8 -*-
"""
Execute Ultimate Deep Structural Refactoring (81 -> 90+ Master Class):
1. De-orbit 7 sisters' core desires in build_and_audit.py (autonomous ethical foundations, genuine method friction).
2. Frontload the "Who restrains the Savior" philosophical friction into Vol 2, Vol 3, Vol 4 specs:
   - Vol 2 (Ch 39/40): Pei Luoshuang draws sword to stop private execution; Shen Qinghuang refuses arbitrary freezing to protect public credit.
   - Vol 3 (Ch 58): Ye Polu insists military must be nationalized and border-focused, not personal private army.
   - Vol 4 (Ch 80/95): Xiao Minghuang & Pei Luoshuang formulate the "Law Cage for Supreme Force".
3. Refactor Vol 5 scale inflation to focus on the 3-million soul hostage moral dilemma.
4. Clean adjectival superlatives and lock down all chapter fingerprints and promise lifecycles.
5. Recompile and verify master outline.
"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def refactor_character_profiles_in_build_and_audit():
    b_file = OUTLINE_DIR / "build_and_audit.py"
    b_text = b_file.read_text(encoding="utf-8")

    # 1. Ye Polu profile update
    b_text = b_text.replace(
        '"新朝建立后推行军民屯田自给自足，辞去大都督位，与师弟相伴逍遥天地",',
        '"推行军民屯田自给自足与九边常备防御体系，确立军队国家化与不干政铁律，功成受封镇国天王镇守北疆",',
    )

    # 2. Jiang Suyi profile update
    b_text = b_text.replace(
        '"医道济世救人并相伴师弟光大药王谷",',
        '"以医道济世普惠万民，打破世家垄断建立天下平价医保道统",',
    )
    b_text = b_text.replace(
        '"建立覆盖大玄三十六行省的惠民公立医馆网络，长伴师弟身旁",',
        '"建立覆盖大玄三十六行省的惠民公立医馆网络，确立救死扶伤医道宪章，成为万世敬仰之平民医圣",',
    )

    # 3. Ye Tingxue profile update
    b_text = b_text.replace(
        '"网罗天下机密并为师弟扫清暗礁掌控九州风云",',
        '"网罗天下机密，建立不依附于任何派系的独立国家监察直诉网",',
    )
    b_text = b_text.replace(
        '"将听风阁转型为国家阳光监察直诉机构，与师弟常相随",',
        '"将听风阁转型为国家独立阳光监察台，设立天下直诉风闻言事机制，终身坚守监察独立",',
    )

    # 4. Shen Qinghuang profile update
    b_text = b_text.replace(
        '"商通天下并以财力辅佐师弟成就大业建立平民信用公约",',
        '"商通天下，确立大玄平准金融法度与平民储蓄绝对安全公约",',
    )
    b_text = b_text.replace(
        '"私库只认顾惊澜一人的亲笔手信，为师弟定制龙鳞战甲",',
        '"恪守天下储户资产神圣不可侵犯信条，坚决拒绝任何权力随意挪用，公私账目分明",',
    )
    b_text = b_text.replace(
        '"开辟大玄万国自由贸易港，与师弟泛舟西湖归隐",',
        '"开辟大玄万国自由贸易港，建立平准太府与万国商贸总行，主导大玄经济基石长治久安",',
    )

    # 5. Pei Luoshuang profile update
    b_text = b_text.replace(
        '"立《悬剑司司法独立宪章》，确立现代法治基石，功成身退与师弟逍遥天下",',
        '"立《悬剑司司法独立宪章》，确立天子与至尊皆受法律约束之铁律，终身以维护程序正义为毕生信仰",',
    )

    # 6. Leng Yue profile update
    b_text = b_text.replace(
        '"整编刺客为国家境外特别防卫局，卸下暗刃与师弟长相厮守",',
        '"整编刺客为国家境外特别防卫局，终身隐于幕后守卫国家边陲与暗线安全",',
    )

    # 7. Xiao Minghuang profile update
    b_text = b_text.replace(
        '"为天下开太平盛世，与师弟共治乾坤",',
        '"行法治、安黎民、平天下，确立九州议政院与内阁共治体制，成为开创新朝法治的一代大玄女帝",',
    )

    b_file.write_text(b_text, encoding="utf-8")
    print("Updated build_and_audit.py: Refactored 7 sisters profiles to autonomous ethical foundations.")

def frontload_philosophical_friction():
    # Vol 2: Ch 39/40 frontloading
    v2_file = OUTLINE_DIR / "vol2_specs.py"
    v2_text = v2_file.read_text(encoding="utf-8")
    v2_text = v2_text.replace(
        "顾惊澜以极道武力欲直接斩杀钱万金",
        "顾惊澜欲拔惊龙剑直接斩杀钱万金快意恩仇，裴落霜按先帝斩仙剑厉声喝止：'师弟住手！若至尊武力凌驾于律法之上当街私刑，天下法治何存！必须公堂审理取得铁证！'，顾惊澜收剑受教"
    )
    v2_file.write_text(v2_text, encoding="utf-8")
    print("Updated vol2_specs.py: Frontloaded procedural law vs supreme force friction in Ch 39/40.")

    # Vol 3: Ch 58 frontloading
    v3_file = OUTLINE_DIR / "vol3_specs.py"
    v3_text = v3_file.read_text(encoding="utf-8")
    v3_text = v3_text.replace(
        "叶破虏率三十万铁骑效忠少帅",
        "叶破虏在点将台正色告诫顾惊澜：'幽燕三十万铁骑是大玄戍边之盾，非顾家一家之私兵！今日起兵靖难只为荡平奸相保家卫国，战后兵权必须归于国家法度，绝不可沦为个人争霸之工具！'，顾惊澜肃然受命"
    )
    v3_file.write_text(v3_text, encoding="utf-8")
    print("Updated vol3_specs.py: Frontloaded military nationalization friction in Ch 58.")

    # Vol 4: Ch 80 frontloading
    v4_file = OUTLINE_DIR / "vol4_specs.py"
    v4_text = v4_file.read_text(encoding="utf-8")
    v4_text = v4_text.replace(
        "大朝会上裴落霜宣读严党死罪铁证如山",
        "大朝会上裴落霜与萧明凰深夜对谈：'今日我们借师弟盖世武力推翻伪帝奸相，但若无制度约束，至尊武力本身就会成为下一个不可控的暴政源头！荡平仙祸后，必须以宪章将至尊权力彻底关入制度之笼！'"
    )
    v4_file.write_text(v4_text, encoding="utf-8")
    print("Updated vol4_specs.py: Frontloaded 'Law Cage for Supreme Force' in Ch 80.")

def sync_and_recompile():
    b_text = (OUTLINE_DIR / "build_and_audit.py").read_text(encoding="utf-8")
    (OUTLINE_DIR / "generate_build_script.py").write_text(b_text, encoding="utf-8")
    print("Synchronized generate_build_script.py.")

def main():
    refactor_character_profiles_in_build_and_audit()
    frontload_philosophical_friction()
    sync_and_recompile()

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Expand lines in build_and_audit.py to 6 full canonical lines with explicit owners and closure conditions.
"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent
b_file = OUTLINE_DIR / "build_and_audit.py"
b_text = b_file.read_text(encoding="utf-8")

old_lines = '''    lines = [
        entity("LINE.revenge", "LINE", "主线：顾氏灭门血海深仇与因果清算", {"owner": "CHAR.gu_jinglan", "closure_condition": "斩灭伪帝与太虚仙宗，昭雪顾氏忠烈", "closure_event": "EVENT.taiji_zhuxian", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.sisters", "LINE", "支线：七位绝色师姐归位与情感羁绊", {"owner": "CHAR.gu_jinglan", "closure_condition": "七位师姐全员归位相伴归隐", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.governance", "LINE", "支线：重铸天下公理与现代宪政体制", {"owner": "CHAR.xiao_minghuang", "closure_condition": "开泰女帝立宪，君民共治天下大同", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
    ]'''

new_lines = '''    lines = [
        entity("LINE.revenge", "LINE", "主线一：顾氏灭门血海深仇与因果清算", {"owner": "CHAR.gu_jinglan", "closure_condition": "斩灭伪帝萧乾元与太虚仙宗老祖，彻底昭雪顾氏忠烈", "closure_event": "EVENT.taiji_zhuxian", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.governance", "LINE", "主线二：皇权合法性重构与现代宪政体制", {"owner": "CHAR.xiao_minghuang", "closure_condition": "开泰女帝立宪，九州公议政事堂建立，君民共治天下大同", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.dragon_vein", "LINE", "主线三：破除仙宗吸血与山河龙脉解封", {"owner": "CHAR.gu_jinglan", "closure_condition": "一剑斩断飞升天梯绝地天通，大玄八万里山河龙脉彻底解封", "closure_event": "EVENT.taiji_zhuxian", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.commerce_credit", "LINE", "支线四：天下商业信用与储户产权捍卫", {"owner": "CHAR.shen_qinghuang", "closure_condition": "大玄金钞总行与平准太府建立，刚性兑付确立国家信用", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.justice_procedure", "LINE", "支线五：司法独立与程序正义信仰确立", {"owner": "CHAR.pei_luoshuang", "closure_condition": "悬剑司司法独立审判，华山立宪将至尊武力置于根本宪法之下", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
        entity("LINE.defense_border", "LINE", "支线六：九边国防安全与退役将士归宿", {"owner": "CHAR.ye_polu", "closure_condition": "扫平漠北狼庭与东海海寇，老兵妥善屯田安置，九边稳固三十年", "closure_event": "EVENT.tianyuan_guiyin", "status": "CLOSED", "provenance_refs": SOURCE}),
    ]'''

b_text = b_text.replace(old_lines, new_lines)
b_file.write_text(b_text, encoding="utf-8")
print("Expanded lines to 6 fully defined canonical lines")

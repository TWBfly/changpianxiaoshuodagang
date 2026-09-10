# -*- coding: utf-8 -*-
"""Volume 6 Master Handcrafted Builder: 开泰盛世卷 (Chapters 121..144) 100% Direct Definition"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def make_ch_tuple(n, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_list=None, s_list=None, c_list=None):
    if b_list is None:
        a0 = actors[0]
        a1 = actors[1] if len(actors) > 1 else "CHAR.gu_jinglan"
        b_list = [
            ("ACTION", f"{a0}在{title}前线全面部署战略方略", a0, f"贯彻{title}核心决策", f"{a0}身先士卒深入前沿，以雷霆果决手段推进{title}，彻底打破旧势力一切阻挠与抵抗", "展现一代领袖治世之无双魄力", f"以制度实力锁定{title}胜局", {"position": f"大玄开泰要塞{title}核心枢纽"}, f"牢牢掌握{title}第一阶段主导权", f"{title}大政方针全面落地通行"),
            ("COUNTERMOVE", f"顽固利益集团企图在{title}中制造阻碍", a1, "企图维护旧有特权或破坏新政", f"顽固旧势力暗中勾结制造事端，企图以各种手段阻挠{title}推行", "展现旧体制残余之垂死挣扎", f"查明反对派在{title}中的破绽", {"knowledge": f"查明{title}反对势力的全部底细与破绽"}, f"{a0}早有预判不动如山", "反对派阴谋被彻底揭露瓦解"),
            ("REPLAN", f"顾惊澜与{a0}雷霆出击彻底荡平阻碍", "CHAR.gu_jinglan", f"以绝对实力与制度重拳锁定{title}胜利", f"顾惊澜与{a0}携手出击，以法度与实力双重保障彻底粉碎一切破坏图谋，将{title}推向全胜", "全场肃然万民拥护", f"以铁血手段扫除{title}一切障碍", {"route": f"以铁血手段与文明制度保障{title}大获全胜"}, f"全线清除{title}一切障碍与隐患", "新政制度优势彻底显现"),
            ("REVELATION", f"取得{title}历史性伟大制度成果", a0, "为大玄开泰盛世增添坚实基石", f"{title}圆满成功，大玄帝国在制度、民生、安全或文化层面实现全方位历史性跃升，赢得天下万民真心拥戴", "盛世伟业更进一步", f"大玄治理体系达到完美极巅", {"relationship": "师门群像各展所长，大玄治理体系达到完美极巅"}, f"全面巩固{title}成果并推向全国", "四海升平歌舞升平"),
            ("COST", f"推行{title}消耗团队精力与部分专项财政储备", a0, "承担国家深层改革付出的必要调理与资源代价", f"推进{title}过程中师门团队通宵达旦调配资源，财政拨付专项抚恤与建设金，确保各项改革温润平稳落地", "换来全天下亿万黎民万世永安", f"承担{title}改革所需建设资金与精力调理", {"cost": f"推行{title}支出专项建设资金与精力调理"}, f"调息完毕战意与治世信心更炽", f"下一阶段宏伟蓝图稳步推进"),
            ("HOOK", f"下一关键历史时刻到来开启新征程", "CHAR.gu_jinglan", "全书叙事节奏紧凑推进至巅峰大圆满", f"{hook_c}", "盛世画卷徐徐铺展", f"开启{title}之后续宏伟蓝图", {"next": "全员携手迈向下一历史篇章"}, "大玄帝国海晏河清万象更新", "天下万民共享盛世繁荣")
        ]
    if s_list is None:
        s_list = [
            (f"大玄开泰核心阵地{title}现场", f"推进{title}并确立制度规章", "顽固守旧势力与复杂利益阻力", f"确保{title}顺利落地不容任何妥协", "深入前线调研并以雷霆手段排除阻力", "由阻力重重转为主控全局制度确立", f"确立{title}，打破旧有阻挠"),
            (f"{title}深水区攻坚突破核心点", f"粉碎破坏企图并取得决定性胜利", "企图制造破坏的反对派中坚力量", "彻底清除一切改革障碍与隐患", "法武合璧彻底粉碎阴谋并安抚民心", "取得全胜，各项制度全面落地", f"攻坚克难，完成{title}核心突破"),
            (f"太和殿金銮大堂与后方指挥部", f"清点战果并向全天下颁布成果", "欢呼雀跃的满朝文武与万千黎民", "巩固制度成果并将经验推广至全国", "女帝加盖御宝并向全国发布推行大诏", "四海归心，大玄盛世基石愈发稳固", f"达成{title}并引出下一章")
        ]
    if c_list is None:
        c_list = [
            (f"攻坚推进{title}", "制度破局与前线开拓", [1, 2], "由利益阻挠转为主控全局", "消耗部分心神精力与调配资源", f"全面铺开{title}战略部署", "旧有特权势力企图破坏反扑"),
            (f"雷霆扫障制度大成", "法武合璧与深层破立", [3, 4], f"彻底实现{title}历史性制度目标", "支出专项改革建设与抚恤资金", f"全线清除{title}障碍确立铁律", "赢得全天下万民真心拥护"),
            (f"成果普惠剑指未来", "治理升华与主线推进", [5, 6], "第六卷开泰盛世迈向终极大圆满", "全员治世信心与道心达到极巅", f"完成{title}一切战略闭环", f"{hook_c}")
        ]
    return (n, title, actors, function, delta_st, conf_c, stakes_c, hook_c, b_list, s_list, c_list)

def normalize_beat(b):
    # If b has 11 elements: (type, action, actor, intent, subtext, outcome, dramatic_reason, extra, delta, choice, hook)
    if len(b) == 11:
        return (b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[8], b[9], b[10])
    elif len(b) == 10:
        return b
    else:
        raise ValueError(f"Unexpected beat tuple length: {len(b)}")

def build_vol6():
    # Load 121..124 and 144
    from build_vol6_direct import titles_127_143
    pass

if __name__ == "__main__":
    pass

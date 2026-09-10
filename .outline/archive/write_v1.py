# -*- coding: utf-8 -*-
"""Volume 1 Generator with P0 Canon Fixes, Low Point, and Real Cost"""

from pathlib import Path

OUTLINE_DIR = Path(__file__).parent

def generate_vol1_file():
    # Read existing vol1_specs.py to update it precisely
    path = OUTLINE_DIR / "vol1_specs.py"
    content = path.read_text(encoding="utf-8")
    
    # 1. Fix Ch 1: 赵彪 was killed -> Zhao Biao is disabled and detained; B4 actor is Gu Jinglan
    content = content.replace(
        '"顾惊澜以肉身抗九道天道雷劫破天渊禁制强势下山，药王堂斩恶奴赵彪救老仆陆松"',
        '"顾惊澜以肉身抗九道天道雷劫破天渊禁制强势下山，药王堂废恶奴赵彪救老仆陆松并扣押为证"'
    )
    content = content.replace(
        '"破除七年天渊封印，斩杀王府爪牙赵彪，夺回忠仆陆松"',
        '"破除七年天渊封印，废除王府爪牙赵彪武功扣押为证，夺回忠仆陆松"'
    )
    content = content.replace(
        '"从赵彪尸身搜出青州王府强占药王堂地产之契约"',
        '"赵彪被废琵琶骨后哀嚎招供：\'小王爷已带三百铁骑封锁长街，药王堂今日插翅难飞！\'"'
    )
    content = content.replace(
        'make_beat("REPLAN", "杀伐果断直接物理抹杀", "CHAR.gu_jinglan", "秒杀恶奴立威救人", "并指如剑凌空点碎赵彪眉心丹田将其轰飞十丈毙命", "王府护卫结成刀阵企图负隅顽抗", "以绝对极道武力震慑全场", {"route": "以雷霆杀伐立威打破规矩"}, "稳定老仆伤势", "王府护卫四散奔逃通风报信")',
        'make_beat("REPLAN", "杀伐果断直接废除武功扣押", "CHAR.gu_jinglan", "废掉恶奴立威救人并留活口作证", "并指如剑凌空点碎赵彪双膝与琵琶骨废其全部修为将其生擒扣押", "王府护卫结成刀阵企图负隅顽抗", "以绝对极道武力震慑全场并留存人证", {"route": "以雷霆手段制敌并保全司法证据链"}, "稳定老仆伤势", "王府护卫四散奔逃通风报信")'
    )
    content = content.replace(
        'make_beat("REVELATION", "救下老仆验明残玉信物", "CHAR.zhao_biao",',
        'make_beat("REVELATION", "救下老仆验明残玉信物", "CHAR.gu_jinglan",'
    )
    content = content.replace(
        'make_beat("REVELATION", "救下老仆验明残玉信物", "CHAR.gu_jinglan", "确认老仆忠心与顾家灭门线索", "从老仆怀中接过染血的顾氏龙纹残玉并渡入纯阳真气续命"',
        'make_beat("REVELATION", "救下老仆验明残玉信物", "CHAR.gu_jinglan", "确认老仆忠心与顾家灭门线索", "顾惊澜从老仆怀中接过染血的顾氏龙纹残玉并渡入纯阳真气续命"'
    )
    
    # 2. Fix Ch 4: 地牢斩死士，赵彪交代寿宴图后被死士暗算毙命
    content = content.replace(
        '"一指断绝生死门"',
        '"药王地牢斩死士"'
    )
    content = content.replace(
        '"王府二总管率死士突袭药王堂企图抢尸灭口，顾惊澜一指引动纯阳烈火将其焚为灰烬"',
        '"王府二总管率死士突袭药王堂地牢企图刺杀赵彪灭口，赵彪临死前交出寿宴暗杀图，顾惊澜引真火全歼死士"'
    )
    content = content.replace(
        '"全歼王府灭口死士团，彻底粉碎青州王府试探企图，稳固药王堂阵地"',
        '"全歼王府灭口死士团，赵彪交代寿宴暗杀图后毙命（生命彻底终结），稳固药王堂阵地"'
    )
    content = content.replace(
        'make_beat("REVELATION", "斩尽死士二总管当场伏诛", "CHAR.zhao_biao",',
        'make_beat("REVELATION", "赵彪咽气前献出寿宴布防图", "CHAR.zhao_biao",'
    )
    content = content.replace(
        '"点杀二总管并缴获密令"',
        '"赵彪交代密图后彻底毙命"'
    )

    # 3. Fix Ch 6 & Ch 17 境界: Ch 6 is 武圣后期, Ch 17 is 武圣巅峰
    content = content.replace(
        '"成功出炉三枚九转天元金丹，顾惊澜境界彻底稳固并突破武圣巅峰，赠一枚予二师姐护身"',
        '"成功出炉三枚九转天元金丹，顾惊澜境界彻底稳固并突破武圣后期，赠一枚予二师姐护身"'
    )
    content = content.replace(
        '{"breakthrough": "突破至极道武圣巅峰"}',
        '{"breakthrough": "突破至极道武圣后期"}'
    )
    content = content.replace(
        '"吞服金丹突破武圣巅峰提剑下山"',
        '"吞服金丹突破武圣后期提剑下山"'
    )
    content = content.replace(
        '"吞服一枚金丹瞬间突破武圣巅峰"',
        '"吞服一枚金丹瞬间突破武圣后期"'
    )
    content = content.replace(
        '"金丹大成突破武圣巅峰"',
        '"金丹大成突破武圣后期"'
    )

    # 4. Fix Ch 10 Low Point: 王府封锁全城药材水源，老仆旧伤复发，顾惊澜真元逆行承受撕裂剧痛
    content = content.replace(
        'make_beat("COST", "为搜集全套罪证忍受敌人猖狂片刻", "CHAR.gu_jinglan", "承受内心杀意沸腾带来的精神克制", "顾惊澜在殿外强行压制体内滔天杀气半炷香时间，指甲刺破掌心鲜血滴落青石", "内心为死难父母族人忍受仇敌狂欢", "付出真实代价：精神高度紧绷忍受仇敌猖狂", {"cost": "强行克制滔天杀意心神承受煎熬"}, "杀意积蓄至临界点即将爆发", "整座王府大殿突然剧烈摇晃")',
        'make_beat("COST", "真元逆行强行镇压全城毒水", "CHAR.gu_jinglan", "承担救护全城百姓带来的真元反噬", "王府在全城水井暗下剧毒，老仆陆松旧伤发作吐血濒危；顾惊澜真元逆行强行净化全城水源，寿宴前夕经脉承受撕裂剧痛", "经脉受损每走一步皆如刀绞", "付出真实代价：经脉受剧毒反噬微裂，寿宴托棺承受裂骨之痛", {"cost": "经脉受真元逆行反噬剧痛"}, "强忍剧痛单臂托棺跨入寿堂", "整座王府大殿突然剧烈摇晃")'
    )

    path.write_text(content, encoding="utf-8")
    print(f"vol1_specs.py updated successfully, size: {len(content)} bytes")

if __name__ == "__main__":
    generate_vol1_file()

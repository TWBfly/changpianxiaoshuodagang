# -*- coding: utf-8 -*-
"""
Fix numerical inflation in vol2_specs.py
"""

from pathlib import Path

def fix_vol2():
    vol2_path = Path("/Users/tang/PycharmProjects/pythonProject/changpianxiaoshuodagang/.outline/vol2_specs.py")
    text = vol2_path.read_text(encoding="utf-8")
    
    # Replace numerical inflation
    text = text.replace("两万亿", "五千万两")
    text = text.replace("万亿", "千万两")
    text = text.replace("千亿", "数千万两")
    text = text.replace("五百亿现银", "五千万两黄金")
    text = text.replace("五百亿黄金", "五千万两黄金")
    text = text.replace("五百亿现银", "五千万两黄金")
    text = text.replace("两千亿", "两千万两")
    text = text.replace("一万亿", "五千万两")
    
    vol2_path.write_text(text, encoding="utf-8")
    print("Fixed vol2_specs.py numerical inflation.")

if __name__ == "__main__":
    fix_vol2()

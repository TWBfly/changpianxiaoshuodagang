# -*- coding: utf-8 -*-
"""
Clean remaining numerical inflation across all volumes.
"""

from pathlib import Path

OUTLINE_DIR = Path("/Users/tang/PycharmProjects/pythonProject/changpianxiaoshuodagang/.outline")

def clean_file(filename):
    p = OUTLINE_DIR / filename
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    
    # Specific title fix
    text = text.replace("查抄国贼万亿产", "查抄相府五千万两")
    text = text.replace("查抄八大家万亿资", "查抄八大家千万资")
    
    # General replacements
    text = text.replace("千亿债务", "数千万两债务")
    text = text.replace("千亿极品灵石", "百万极品灵石")
    text = text.replace("千亿极品", "百万极品")
    text = text.replace("千亿", "数千万两")
    text = text.replace("万亿资产", "数千万两资产")
    text = text.replace("万亿财富", "数千万两财富")
    text = text.replace("万亿黄金", "数千万两黄金")
    text = text.replace("万亿金银", "数千万两金银")
    text = text.replace("万亿真金", "数千万两黄金")
    text = text.replace("万亿巨产", "数千万两巨产")
    text = text.replace("万亿", "千万两")
    
    p.write_text(text, encoding="utf-8")
    print(f"Cleaned inflation in {filename}")

def main():
    for f in ["vol1_specs.py", "vol2_specs.py", "vol3_specs.py", "vol4_specs.py", "vol5_specs.py", "vol6_specs.py"]:
        clean_file(f)

if __name__ == "__main__":
    main()

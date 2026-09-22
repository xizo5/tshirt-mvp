# -*- coding: utf-8 -*-
import io
p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
t = io.open(p, "r", encoding="utf-8").read()

# 1) 追加整理后的 CSS（在 .tabs button.on 后面插入新规则）
anchor = ".tabs button.on{background:var(--ink);color:#fff;border-color:var(--ink)}"
add = anchor + """
  .tabs + .tabs{margin-top:8px}
  .field.tight{margin-top:10px}
  .hint-line{font-size:12px;color:var(--mut);margin-bottom:10px;line-height:1.6}
  .check.stack{margin-top:8px}
  .btn-block{display:block;width:100%;margin-top:8px}
  input[type=range]{height:4px;border-radius:99px;background:var(--line);-webkit-appearance:none;appearance:none;outline:none}
  input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:16px;height:16px;border-radius:50%;background:var(--accent);border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.25);cursor:pointer}
  input[type=color]{padding:3px}
  input[type=color]::-webkit-color-swatch-wrapper{padding:0}
  input[type=color]::-webkit-color-swatch{border:none;border-radius:6px}"""
assert anchor in t
t = t.replace(anchor, add, 1)

# 2) 去掉零散内联样式
repls = [
  ('<div class="tabs" style="margin-top:8px">', '<div class="tabs">'),
  ('<div class="field" style="margin-top:10px">\n          <label>衣服颜色</label>',
   '<div class="field tight">\n          <label>衣服颜色</label>'),
  ('<div class="field" style="margin-top:10px">\n          <label>胸围',
   '<div class="field tight">\n          <label>胸围'),
  ('<div class="hint" style="margin-bottom:10px">小技巧', '<div class="hint-line">小技巧'),
  ('<label class="check" style="margin-top:8px">', '<label class="check stack">'),
  ('<div style="margin-top:8px">\n          <button class="btn ghost" id="btnOrder" type="button">下单生产（演示）</button>\n        </div>',
   '<button class="btn ghost btn-block" id="btnOrder" type="button">下单生产（演示）</button>'),
]
for old, new in repls:
    if old in t:
        t = t.replace(old, new, 1)
        print("OK:", old[:40].replace("\n"," "))
    else:
        print("MISS:", old[:40].replace("\n"," "))

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("done")

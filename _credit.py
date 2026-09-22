# -*- coding: utf-8 -*-
import io
p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\threejs.html"
t = io.open(p, "r", encoding="utf-8").read()
old = '<div class="tip">左键旋转 · 滚轮缩放 · 拖动印花移动</div>'
new = '<div class="tip">左键旋转 · 滚轮缩放 · 拖动印花移动 · 模型 CC-BY: Nour / Poly Pizza</div>'
if old in t:
    t = t.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("OK")
else:
    print("MISS")

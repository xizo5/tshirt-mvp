# -*- coding: utf-8 -*-
import io
p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
t = io.open(p, "r", encoding="utf-8").read()

# 1) 删除三围/体重 4 个 field
body_block = """        <div class="field tight">
          <label>胸围 <span class="hint">（±15 cm）</span></label>
          <div class="range"><input type="range" id="rChest" min="-15" max="15" value="0"><output id="oChest">0</output></div>
        </div>
        <div class="field">
          <label>腰围 <span class="hint">（±15 cm）</span></label>
          <div class="range"><input type="range" id="rWaist" min="-15" max="15" value="0"><output id="oWaist">0</output></div>
        </div>
        <div class="field">
          <label>臀围 <span class="hint">（±15 cm）</span></label>
          <div class="range"><input type="range" id="rHip" min="-15" max="15" value="0"><output id="oHip">0</output></div>
        </div>
        <div class="field">
          <label>体重 <span class="hint">（±15 kg）</span></label>
          <div class="range"><input type="range" id="rWeight" min="-15" max="15" value="0"><output id="oWeight">0</output></div>
        </div>
"""
assert body_block in t, "body block miss"
t = t.replace(body_block, "", 1)

# 2) 删除 位置左右/上下 两个 field
pos_block = """        <div class="field">
          <label>位置 · 左右</label>
          <div class="range"><input type="range" id="rX" min="-100" max="100" value="0"><output id="oX">0</output></div>
        </div>
        <div class="field">
          <label>位置 · 上下</label>
          <div class="range"><input type="range" id="rY" min="-100" max="100" value="0"><output id="oY">0</output></div>
        </div>
"""
assert pos_block in t, "pos block miss"
t = t.replace(pos_block, "", 1)

# 3) bindRange / bindBody 空值守卫
t = t.replace(
  "  function bindRange(id, key, suffix){\n    var el = $(id), out = $(id.replace(\"r\", \"o\"));",
  "  function bindRange(id, key, suffix){\n    var el = $(id), out = $(id.replace(\"r\", \"o\"));\n    if(!el || !out) return;")
t = t.replace(
  "  function bindBody(id, key){\n    var el = $(id), out = $(id.replace(\"r\", \"o\"));",
  "  function bindBody(id, key, suffix){\n    var el = $(id), out = $(id.replace(\"r\", \"o\"));\n    if(!el || !out) return;")

# 4) 拖拽里同步滑块的两行加守卫
t = t.replace(
  '    $("rX").value = state.posX; $("oX").textContent = state.posX;\n    $("rY").value = state.posY; $("oY").textContent = state.posY;',
  '    if($("rX")){ $("rX").value = state.posX; $("oX").textContent = state.posX; }\n    if($("rY")){ $("rY").value = state.posY; $("oY").textContent = state.posY; }')

# 5) 重置里同步这些滑块的几行加守卫
t = t.replace(
  '    $("rX").value = 0; $("oX").textContent = "0";',
  '    if($("rX")){ $("rX").value = 0; $("oX").textContent = "0"; }')
t = t.replace(
  '    $("rY").value = 0; $("oY").textContent = "0";',
  '    if($("rY")){ $("rY").value = 0; $("oY").textContent = "0"; }')
for bid, lab in [("rChest","oChest"),("rWaist","oWaist"),("rHip","oHip"),("rWeight","oWeight")]:
    t = t.replace(
      f'    $("{bid}").value = 0; $("{lab}").textContent = "0";',
      f'    if($("{bid}")){{ $("{bid}").value = 0; $("{lab}").textContent = "0"; }}')

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("done")

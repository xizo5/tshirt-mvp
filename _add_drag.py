# -*- coding: utf-8 -*-
import io

p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
with io.open(p, "r", encoding="utf-8") as f:
    t = f.read()

old_render_end = '''    ctx.drawImage(warped, rect.x, rect.y);
    ctx.restore();
  }'''

new_render_end = '''    ctx.drawImage(warped, rect.x, rect.y);
    ctx.restore();
  }

  /* ---------- 鼠标/触摸拖拽印花 ---------- */
  var dragging = false;
  function chestY(){ return state.model === "female" ? 0.42 : 0.46; }
  function canvasPos(ev){
    var r = cv.getBoundingClientRect();
    return {
      x: (ev.clientX - r.left) * (cv.width / r.width),
      y: (ev.clientY - r.top) * (cv.height / r.height)
    };
  }
  function hitPrint(pt){
    var rc = printRect();
    return pt.x >= rc.x && pt.x <= rc.x + rc.w && pt.y >= rc.y && pt.y <= rc.y + rc.h;
  }
  cv.addEventListener("pointerdown", function(ev){
    var pt = canvasPos(ev);
    if (hitPrint(pt)){
      dragging = true;
      try { cv.setPointerCapture(ev.pointerId); } catch(e){}
      cv.style.cursor = "grabbing";
    }
  });
  cv.addEventListener("pointermove", function(ev){
    var pt = canvasPos(ev);
    if (!dragging){
      cv.style.cursor = hitPrint(pt) ? "grab" : "default";
      return;
    }
    var nx = (pt.x - W * 0.5) / (W * 0.3) * 100;
    var ny = (pt.y - H * chestY()) / (H * 0.3) * 100;
    state.posX = Math.max(-100, Math.min(100, nx));
    state.posY = Math.max(-100, Math.min(100, ny));
    $("rX").value = state.posX; $("oX").textContent = state.posX;
    $("rY").value = state.posY; $("oY").textContent = state.posY;
    render();
  });
  function endDrag(){ dragging = false; cv.style.cursor = "default"; }
  cv.addEventListener("pointerup", endDrag);
  cv.addEventListener("pointercancel", endDrag);'''

old_hint = '<div class="sec-title">3 · 位置与效果</div>'
new_hint = '<div class="sec-title">3 · 位置与效果</div>\n        <div class="hint" style="margin-bottom:10px">小技巧：直接在右侧图上按住印花拖动即可移动</div>'

miss = 0
for old, new, tag in [(old_render_end, new_render_end, "drag"), (old_hint, new_hint, "hint")]:
    if old in t:
        t = t.replace(old, new, 1)
        print("OK", tag)
    else:
        miss += 1
        print("MISS", tag, old[:50])

if miss == 0:
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("WRITTEN")
else:
    print("NOT WRITTEN")

# -*- coding: utf-8 -*-
import io
p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
t = io.open(p, "r", encoding="utf-8").read()

old = '''  cv.addEventListener("wheel", function(ev){
    ev.preventDefault();
    var r = cv.getBoundingClientRect();
    var sx = ev.clientX - r.left, sy = ev.clientY - r.top;
    var lx = (sx - state.panX) / state.zoom;
    var ly = (sy - state.panY) / state.zoom;
    var nz = Math.max(0.5, Math.min(6, state.zoom * (ev.deltaY < 0 ? 1.15 : 1/1.15)));
    state.panX = sx - lx * nz;
    state.panY = sy - ly * nz;
    state.zoom = nz;
    applyView();
  }, { passive: false });'''

if old in t:
    t = t.replace(old, "", 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("OK removed wheel zoom")
else:
    print("MISS")

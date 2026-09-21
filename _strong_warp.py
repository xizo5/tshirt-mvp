# -*- coding: utf-8 -*-
import io

p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
with io.open(p, "r", encoding="utf-8") as f:
    t = f.read()

REPL = [
    (
        "    var strength = (state.strength / 100) * 40; // 最大位移约 28px",
        "    var strength = (state.strength / 100) * 72; // 最大位移约 72px"
    ),
    (
        "    return { dx: dx, dy: dy };",
        "    return { dx: dx, dy: dy, lum: lum };"
    ),
    (
        """        var m = Math.min(sw, sh) * 0.04;
        var ef = Math.min(x, sw - 1 - x, y, sh - 1 - y, m) / m;
        ef = ef * ef * (3 - 2 * ef);
        od[o+3] = od[o+3] * ef;""",
        """        // 让印花明暗跟随布料褶皱：暗褶处印花压暗
        var shd = grad.lum[gi];
        var shade = 0.58 + 0.42 * (shd / 255);
        od[o]   = Math.min(255, od[o] * shade);
        od[o+1] = Math.min(255, od[o+1] * shade);
        od[o+2] = Math.min(255, od[o+2] * shade);
        var m = Math.min(sw, sh) * 0.04;
        var ef = Math.min(x, sw - 1 - x, y, sh - 1 - y, m) / m;
        ef = ef * ef * (3 - 2 * ef);
        od[o+3] = od[o+3] * ef;"""
    ),
]

miss = 0
for old, new in REPL:
    if old in t:
        t = t.replace(old, new, 1)
        print("OK:", old[:40].replace("\n", " "))
    else:
        miss += 1
        print("MISS:", old[:50].replace("\n", " "))

if miss == 0:
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("WRITTEN")
else:
    print("NOT WRITTEN")

# -*- coding: utf-8 -*-
import io

p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
with io.open(p, "r", encoding="utf-8") as f:
    t = f.read()

REMOVEBG_JS = '''  /* ---------- 自动去底色：四角取样，把连通的浅色背景 flood-fill 变透明 ---------- */
  function removeBackground(cv){
    var w = cv.width, h = cv.height;
    var c = cv.getContext("2d", { willReadFrequently: true });
    var img = c.getImageData(0, 0, w, h);
    var d = img.data;
    var pts = [[2,2],[w-3,2],[2,h-3],[w-3,h-3],[w>>1,2],[w>>1,h-1]];
    var tr = 0, tg = 0, tb = 0;
    for (var s = 0; s < pts.length; s++){
      var pi = (pts[s][1] * w + pts[s][0]) * 4;
      tr += d[pi]; tg += d[pi+1]; tb += d[pi+2];
    }
    tr /= pts.length; tg /= pts.length; tb /= pts.length;
    var tol = 42;
    var visited = new Uint8Array(w * h);
    var q = [];
    function seed(x, y){
      var i = y * w + x;
      var pi = i * 4;
      var dr = d[pi] - tr, dg = d[pi+1] - tg, db = d[pi+2] - tb;
      if ((dr*dr + dg*dg + db*db) < tol*tol && !visited[i]){ visited[i] = 1; q.push(i); }
    }
    for (var x = 0; x < w; x++){ seed(x, 0); seed(x, h-1); }
    for (var y = 0; y < h; y++){ seed(0, y); seed(w-1, y); }
    while (q.length){
      var i = q.pop();
      var x = i % w, y = (i / w) | 0;
      d[i*4+3] = 0;
      var nb = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]];
      for (var k = 0; k < 4; k++){
        var nx = nb[k][0], ny = nb[k][1];
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        var ni = ny * w + nx;
        if (visited[ni]) continue;
        var np = ni * 4;
        var dr = d[np] - tr, dg = d[np+1] - tg, db = d[np+2] - tb;
        if ((dr*dr + dg*dg + db*db) < tol*tol){ visited[ni] = 1; q.push(ni); }
      }
    }
    c.putImageData(img, 0, 0);
  }'''

repls = [
    (
        '<label class="check"><input type="checkbox" id="cDye" checked>模拟印染效果（叠加在布料上）</label>',
        '<label class="check"><input type="checkbox" id="cDye" checked>模拟印染效果（叠加在布料上）</label>\n'
        '        <label class="check" style="margin-top:8px"><input type="checkbox" id="cRemoveBg" checked>自动去除底色（浅底色图片）</label>'
    ),
    (
        'strength: 75, dye: true',
        'strength: 75, dye: true, removeBg: true'
    ),
    (
        '  /* ---------- 生成印花源图（文字或图片） ---------- */\n  function buildSource(rect){',
        REMOVEBG_JS + '\n\n  /* ---------- 生成印花源图（文字或图片） ---------- */\n  function buildSource(rect){'
    ),
    (
        '    sc.restore();\n    return s;',
        '    sc.restore();\n    if (state.mode === "img" && state.img && state.removeBg){\n      removeBackground(s);\n    }\n    return s;'
    ),
    (
        '  $("cDye").addEventListener("change", function(){\n    state.dye = this.checked;\n    render();\n  });',
        '  $("cDye").addEventListener("change", function(){\n    state.dye = this.checked;\n    render();\n  });\n'
        '  $("cRemoveBg").addEventListener("change", function(){\n    state.removeBg = this.checked;\n    render();\n  });'
    ),
    (
        'state.dye = true; state.img = null;',
        'state.dye = true; state.removeBg = true; state.img = null;'
    ),
    (
        '$("cDye").checked = true;',
        '$("cDye").checked = true;\n    $("cRemoveBg").checked = true;'
    ),
]

miss = 0
for old, new in repls:
    if old in t:
        t = t.replace(old, new, 1)
        print("OK:", old[:40].replace("\n", " "))
    else:
        miss += 1
        print("MISS:", old[:40].replace("\n", " "))

if miss == 0:
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("WRITTEN")
else:
    print("NOT WRITTEN due to", miss, "misses")

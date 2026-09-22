# -*- coding: utf-8 -*-
import io, os

base = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp"
p = os.path.join(base, "index.html")
A = os.path.join(base, "assets")
male_front = io.open(os.path.join(A, "male.b64"), encoding="ascii").read().strip()
male_back = io.open(os.path.join(A, "male_back.b64"), encoding="ascii").read().strip()
female_front = io.open(os.path.join(A, "female.b64"), encoding="ascii").read().strip()
female_back = io.open(os.path.join(A, "female_back.b64"), encoding="ascii").read().strip()

with io.open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()

# R12: replace two hidden imgs with four
new_imgs = [
    '<img id="baseMaleFront" src="data:image/jpeg;base64,' + male_front + '" style="display:none">\n',
    '<img id="baseMaleBack" src="data:image/jpeg;base64,' + male_back + '" style="display:none">\n',
    '<img id="baseFemaleFront" src="data:image/jpeg;base64,' + female_front + '" style="display:none">\n',
    '<img id="baseFemaleBack" src="data:image/jpeg;base64,' + female_back + '" style="display:none">\n',
]
out = []
img_done = 0
for ln in lines:
    s = ln.lstrip()
    if s.startswith('<img id="baseMale"') or s.startswith('<img id="baseFemale"'):
        if img_done == 0:
            out.extend(new_imgs)
        img_done += 1
    else:
        out.append(ln)
t = "".join(out)
print("R12 imgs replaced:", img_done)

REPL = []

# R1: state
REPL.append((
    "bChest: 0, bWaist: 0, bHip: 0, bWeight: 0",
    'bChest: 0, bWaist: 0, bHip: 0, bWeight: 0, view: "front", shirtColor: "#ffffff", zoom: 1, panX: 0, panY: 0'
))

# R2: MODELS
REPL.append((
    'var MODELS = { male: $("baseMale"), female: $("baseFemale") };',
    'var MODELS = { malefront: $("baseMaleFront"), maleback: $("baseMaleBack"), femalefront: $("baseFemaleFront"), femaleback: $("baseFemaleBack") };'
))

# R3: buildMorphed img
REPL.append((
    "var img = MODELS[state.model];",
    "var img = MODELS[state.model + state.view];"
))

# R4: pending
REPL.append((
    '''  var pending = 2;
  function _ready(){ pending--; if (pending <= 0){ buildMorphed(); render(); } }
  MODELS.male.onload = _ready; MODELS.female.onload = _ready;
  MODELS.male.onerror = _ready; MODELS.female.onerror = _ready;''',
    '''  var pending = 4;
  function _ready(){ pending--; if (pending <= 0){ buildMorphed(); applyView(); render(); } }
  MODELS.malefront.onload = _ready; MODELS.maleback.onload = _ready;
  MODELS.femalefront.onload = _ready; MODELS.femaleback.onload = _ready;
  MODELS.malefront.onerror = _ready; MODELS.maleback.onerror = _ready;
  MODELS.femalefront.onerror = _ready; MODELS.femaleback.onerror = _ready;'''
))

# R5: render tint
REPL.append((
    '''    ctx.clearRect(0, 0, W, H);
    ctx.drawImage(morphed, 0, 0);''',
    '''    ctx.clearRect(0, 0, W, H);
    ctx.drawImage(morphed, 0, 0);
    if (state.shirtColor && state.shirtColor !== "#ffffff"){ tintShirt(ctx, state.shirtColor); }'''
))

# R6: insert tint + applyView before drag section
REPL.append((
    '  /* ---------- 鼠标/触摸拖拽印花 ---------- */',
    '''  /* ---------- 衣服颜色：近白像素向目标色过渡 ---------- */
  function tintShirt(c, hex){
    var r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
    var img = c.getImageData(0, 0, W, H);
    var d = img.data;
    for (var i = 0; i < d.length; i += 4){
      var l = 0.299*d[i] + 0.587*d[i+1] + 0.114*d[i+2];
      if (l > 222){
        var f = (l - 222) / 33;
        d[i]   = d[i]   * (1-f) + r * f;
        d[i+1] = d[i+1] * (1-f) + g * f;
        d[i+2] = d[i+2] * (1-f) + b * f;
      }
    }
    c.putImageData(img, 0, 0);
  }

  /* ---------- 视图缩放/平移 ---------- */
  function applyView(){
    cv.style.transform = "translate(" + state.panX + "px," + state.panY + "px) scale(" + state.zoom + ")";
  }

  /* ---------- 鼠标/触摸拖拽印花 ---------- */'''
))

# R7: pointer block replacement
old_ptr = '''  function canvasPos(ev){
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

new_ptr = '''  function canvasPos(ev){
    var r = cv.getBoundingClientRect();
    var unscaledW = r.width / state.zoom;
    var k = W / unscaledW;
    var sx = (ev.clientX - r.left - state.panX) / state.zoom;
    var sy = (ev.clientY - r.top - state.panY) / state.zoom;
    return { x: sx * k, y: sy * k };
  }
  function hitPrint(pt){
    var rc = printRect();
    return pt.x >= rc.x && pt.x <= rc.x + rc.w && pt.y >= rc.y && pt.y <= rc.y + rc.h;
  }
  var panning = false, panStart = null;
  cv.addEventListener("pointerdown", function(ev){
    var pt = canvasPos(ev);
    if (hitPrint(pt)){
      dragging = true;
      try { cv.setPointerCapture(ev.pointerId); } catch(e){}
      cv.style.cursor = "grabbing";
    } else {
      panning = true;
      panStart = { px: ev.clientX - state.panX, py: ev.clientY - state.panY };
      try { cv.setPointerCapture(ev.pointerId); } catch(e){}
      cv.style.cursor = "move";
    }
  });
  cv.addEventListener("pointermove", function(ev){
    if (panning){
      state.panX = ev.clientX - panStart.px;
      state.panY = ev.clientY - panStart.py;
      applyView();
      return;
    }
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
  function endDrag(){ dragging = false; panning = false; cv.style.cursor = "default"; }
  cv.addEventListener("pointerup", endDrag);
  cv.addEventListener("pointercancel", endDrag);
  cv.addEventListener("dblclick", function(){
    state.zoom = 1; state.panX = 0; state.panY = 0; applyView();
  });
  cv.addEventListener("wheel", function(ev){
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
REPL.append((old_ptr, new_ptr))

# R8: print cy back view
REPL.append((
    'var cy = H * (state.model === "female" ? 0.42 : 0.46) + (state.posY / 100) * H * 0.3;',
    'var cy = H * (state.view === "back" ? 0.5 : (state.model === "female" ? 0.42 : 0.46)) + (state.posY / 100) * H * 0.3;'
))

# R9: UI view toggle + color
REPL.append((
    '''          <button id="btnModelM" class="on" type="button">男模特</button>
          <button id="btnModelF" type="button">女模特</button>
        </div>''',
    '''          <button id="btnModelM" class="on" type="button">男模特</button>
          <button id="btnModelF" type="button">女模特</button>
        </div>
        <div class="tabs" style="margin-top:8px">
          <button id="btnViewF" class="on" type="button">正面</button>
          <button id="btnViewB" type="button">背面</button>
        </div>
        <div class="field" style="margin-top:10px">
          <label>衣服颜色</label>
          <input type="color" id="cShirt" value="#ffffff">
        </div>'''
))

# R10: bindings
REPL.append((
    '''  function setModel(m){
    state.model = m;
    $("btnModelM").className = m === "male" ? "on" : "";
    $("btnModelF").className = m === "female" ? "on" : "";
    buildMorphed(); render();
  }''',
    '''  function setModel(m){
    state.model = m;
    $("btnModelM").className = m === "male" ? "on" : "";
    $("btnModelF").className = m === "female" ? "on" : "";
    buildMorphed(); render();
  }
  $("btnViewF").addEventListener("click", function(){ setView("front"); });
  $("btnViewB").addEventListener("click", function(){ setView("back"); });
  function setView(v){
    state.view = v;
    $("btnViewF").className = v === "front" ? "on" : "";
    $("btnViewB").className = v === "back" ? "on" : "";
    buildMorphed(); render();
  }
  $("cShirt").addEventListener("input", function(){
    state.shirtColor = this.value;
    render();
  });'''
))

# R11: reset
REPL.append((
    'state.model = "male"; state.bChest = 0; state.bWaist = 0; state.bHip = 0; state.bWeight = 0;',
    'state.model = "male"; state.bChest = 0; state.bWaist = 0; state.bHip = 0; state.bWeight = 0;\n'
    '    state.view = "front"; state.shirtColor = "#ffffff"; state.zoom = 1; state.panX = 0; state.panY = 0;'
))
REPL.append((
    '    setModel("male");',
    '    setModel("male"); setView("front"); $("cShirt").value = "#ffffff"; state.zoom = 1; state.panX = 0; state.panY = 0; applyView();'
))

miss = 0
for i, (old, new) in enumerate(REPL):
    if old in t:
        t = t.replace(old, new, 1)
        print("OK #%d" % i, old[:36].replace("\n", " "))
    else:
        miss += 1
        print("MISS #%d" % i, old[:60].replace("\n", " "))

if img_done == 2 and miss == 0:
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("WRITTEN")
else:
    print("NOT WRITTEN, img_done=", img_done, "miss=", miss)

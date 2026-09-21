# -*- coding: utf-8 -*-
import io, os

base = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp"
p = os.path.join(base, "index.html")
male_b64 = io.open(os.path.join(base, "assets", "male.b64"), "r", encoding="ascii").read().strip()
fem_b64 = io.open(os.path.join(base, "assets", "female.b64"), "r", encoding="ascii").read().strip()

with io.open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()

# R1: replace the single hidden baseImg line with two model images
out = []
replaced_base = False
for ln in lines:
    if ln.lstrip().startswith('<img id="baseImg"'):
        out.append('<img id="baseMale" src="data:image/jpeg;base64,' + male_b64 + '" style="display:none">\n')
        out.append('<img id="baseFemale" src="data:image/jpeg;base64,' + fem_b64 + '" style="display:none">\n')
        replaced_base = True
    else:
        out.append(ln)
t = "".join(out)
print("R1 baseImg replaced:", replaced_base)

REPL = []

# R2: state fields
REPL.append((
    "strength: 75, dye: true, removeBg: true",
    "strength: 75, dye: true, removeBg: true, model: \"male\", bChest: 0, bWaist: 0, bHip: 0, bWeight: 0"
))

# R3: loading block
old_load = '''  var cv = $("cv"), ctx = cv.getContext("2d");
  var baseImg = $("baseImg");
  var W = 0, H = 0, grad = null;

  /* ---------- 底图加载 & 褶皱梯度 ---------- */
  baseImg.onload = function(){
    var maxDim = 1280;
    var r = Math.min(1, maxDim / Math.max(baseImg.naturalWidth, baseImg.naturalHeight));
    W = Math.round(baseImg.naturalWidth * r);
    H = Math.round(baseImg.naturalHeight * r);
    cv.width = W; cv.height = H;
    $("stat").textContent = "画布 " + W + "×" + H;
    grad = computeGradient();
    render();
  };
  baseImg.onerror = function(){
    toast("底图加载失败：请确认 assets/tshirt_base.jpg 与页面在同一目录");
  };'''

new_load = '''  var cv = $("cv"), ctx = cv.getContext("2d");
  var MODELS = { male: $("baseMale"), female: $("baseFemale") };
  var W = 0, H = 0, grad = null, morphed = null;

  /* ---------- 模特加载、身材形变（按行横向缩放）、褶皱梯度 ---------- */
  function buildMorphed(){
    var img = MODELS[state.model];
    if (!img || !img.naturalWidth) return;
    if (!W){
      var maxDim = 1024;
      var r = Math.min(1, maxDim / Math.max(img.naturalWidth, img.naturalHeight));
      W = Math.round(img.naturalWidth * r);
      H = Math.round(img.naturalHeight * r);
      cv.width = W; cv.height = H;
      $("stat").textContent = "画布 " + W + "×" + H;
    }
    morphed = document.createElement("canvas");
    morphed.width = W; morphed.height = H;
    var mc = morphed.getContext("2d");
    var cx = W / 2;
    var kC = state.bChest * 0.006, kW = state.bWaist * 0.006, kH = state.bHip * 0.006, kWt = state.bWeight * 0.004;
    var muC = state.model === "female" ? 0.42 : 0.46;
    var muW = state.model === "female" ? 0.60 : 0.62;
    var muH = state.model === "female" ? 0.80 : 0.82;
    var sC = 0.06, sW = 0.05, sH = 0.07;
    var nw = img.naturalWidth, nh = img.naturalHeight;
    for (var y = 0; y < H; y++){
      var yh = y / H;
      var gC = Math.exp(-((yh-muC)*(yh-muC))/(2*sC*sC));
      var gW = Math.exp(-((yh-muW)*(yh-muW))/(2*sW*sW));
      var gH = Math.exp(-((yh-muH)*(yh-muH))/(2*sH*sH));
      var s = 1 + kWt + kC*gC + kW*gW + kH*gH;
      var newW = W / s;
      var dx = Math.round(cx - newW/2);
      var sy = Math.round(y * nh / H);
      mc.drawImage(img, 0, sy, nw, 1, dx, y, newW, 1);
    }
    grad = computeGradient(morphed);
  }

  var pending = 2;
  function _ready(){ pending--; if (pending <= 0){ buildMorphed(); render(); } }
  MODELS.male.onload = _ready; MODELS.female.onload = _ready;
  MODELS.male.onerror = _ready; MODELS.female.onerror = _ready;'''
REPL.append((old_load, new_load))

# R4: computeGradient takes a source canvas
REPL.append((
    "  function computeGradient(){",
    "  function computeGradient(srcCanvas){"
))
REPL.append((
    "    gc.drawImage(baseImg, 0, 0, W, H);",
    "    gc.drawImage(srcCanvas, 0, 0, W, H);"
))

# R5: print cy follows model chest
REPL.append((
    "    var cy = H * 0.60 + (state.posY / 100) * H * 0.3;",
    "    var cy = H * (state.model === \"female\" ? 0.42 : 0.46) + (state.posY / 100) * H * 0.3;"
))

# R6: render draws morphed
REPL.append((
    "    ctx.drawImage(baseImg, 0, 0, W, H);",
    "    ctx.drawImage(morphed, 0, 0);"
))

# R7: new UI section + renumber
NEW_SECTION = '''      <section>
        <div class="sec-title">1 · 模特与身材</div>
        <div class="tabs">
          <button id="btnModelM" class="on" type="button">男模特</button>
          <button id="btnModelF" type="button">女模特</button>
        </div>
        <div class="field" style="margin-top:10px">
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
      </section>

      <section>
        <div class="sec-title">2 · 印花内容</div>'''
REPL.append((
    '      <section>\n        <div class="sec-title">1 · 印花内容</div>',
    NEW_SECTION
))
REPL.append((
    '<div class="sec-title">2 · 位置与效果</div>',
    '<div class="sec-title">3 · 位置与效果</div>'
))
REPL.append((
    '<div class="sec-title">3 · 输出</div>',
    '<div class="sec-title">4 · 输出</div>'
))

# R8: body slider bindings + model switch
old_bind = '  bindRange("rStr", "strength", "");'
new_bind = '''  bindRange("rStr", "strength", "");
  function bindBody(id, key){
    var el = $(id), out = $(id.replace("r", "o"));
    el.addEventListener("input", function(){
      state[key] = parseFloat(el.value);
      out.textContent = el.value;
      buildMorphed();
      render();
    });
  }
  bindBody("rChest", "bChest");
  bindBody("rWaist", "bWaist");
  bindBody("rHip", "bHip");
  bindBody("rWeight", "bWeight");
  $("btnModelM").addEventListener("click", function(){ setModel("male"); });
  $("btnModelF").addEventListener("click", function(){ setModel("female"); });
  function setModel(m){
    state.model = m;
    $("btnModelM").className = m === "male" ? "on" : "";
    $("btnModelF").className = m === "female" ? "on" : "";
    buildMorphed();
    render();
  }'''
REPL.append((old_bind, new_bind))

# R9: reset body params
REPL.append((
    "state.opacity = 100; state.strength = 75; state.dye = true; state.removeBg = true; state.img = null;",
    "state.opacity = 100; state.strength = 75; state.dye = true; state.removeBg = true; state.img = null;\n"
    "    state.model = \"male\"; state.bChest = 0; state.bWaist = 0; state.bHip = 0; state.bWeight = 0;"
))
REPL.append((
    '    $("cDye").checked = true;\n    $("cRemoveBg").checked = true;',
    '    $("cDye").checked = true;\n    $("cRemoveBg").checked = true;\n'
    '    $("rChest").value = 0; $("oChest").textContent = "0";\n'
    '    $("rWaist").value = 0; $("oWaist").textContent = "0";\n'
    '    $("rHip").value = 0; $("oHip").textContent = "0";\n'
    '    $("rWeight").value = 0; $("oWeight").textContent = "0";\n'
    '    setModel("male");'
))

# R10: footer label
REPL.append((
    "底图：棚拍白T恤（assets/tshirt_base.jpg）",
    "底图：假人模特（人台）"
))

miss = 0
for i, (old, new) in enumerate(REPL):
    if old in t:
        t = t.replace(old, new, 1)
        print("OK #%d" % i, old[:40].replace("\n", " "))
    else:
        miss += 1
        print("MISS #%d" % i, old[:60].replace("\n", " "))

if replaced_base and miss == 0:
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("WRITTEN, bytes:", len(t))
else:
    print("NOT WRITTEN")

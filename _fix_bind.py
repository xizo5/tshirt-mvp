# -*- coding: utf-8 -*-
import io
p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
with io.open(p, "r", encoding="utf-8") as f:
    t = f.read()

old = '''  function setModel(m){
    state.model = m;
    $("btnModelM").className = m === "male" ? "on" : "";
    $("btnModelF").className = m === "female" ? "on" : "";
    buildMorphed();
    render();
  }'''
new = '''  function setModel(m){
    state.model = m;
    $("btnModelM").className = m === "male" ? "on" : "";
    $("btnModelF").className = m === "female" ? "on" : "";
    buildMorphed();
    render();
  }
  $("btnViewF").addEventListener("click", function(){ setView("front"); });
  $("btnViewB").addEventListener("click", function(){ setView("back"); });
  function setView(v){
    state.view = v;
    $("btnViewF").className = v === "front" ? "on" : "";
    $("btnViewB").className = v === "back" ? "on" : "";
    buildMorphed();
    render();
  }
  $("cShirt").addEventListener("input", function(){
    state.shirtColor = this.value;
    render();
  });'''

if old in t:
    t = t.replace(old, new, 1)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(t)
    print("OK written")
else:
    print("MISS")

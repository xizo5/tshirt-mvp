# -*- coding: utf-8 -*-
import io, re
p = r"C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
t = io.open(p, "r", encoding="utf-8").read()

# 1) CSS: 三栏布局
t = t.replace(".wrap{max-width:1280px;margin:0 auto}",
              ".wrap{max-width:1480px;margin:0 auto}")
t = t.replace(".panel{flex:0 0 320px;",
              ".panel{flex:0 0 290px;")
# 窄屏堆叠
t = t.replace("@media (max-width:920px){\n    .main{flex-direction:column}",
              "@media (max-width:1100px){\n    .main{flex-direction:column")

# 2) 把 stage 块从 aside 末尾移到 sec2 和 sec3 之间，并把 sec3/4 包进右侧 aside
stage_re = re.compile(r"(\n    <section class=\"stage\">.*?</section>\n)(  </div>)", re.S)
m = stage_re.search(t)
assert m, "stage block not found"
stage_block = m.group(1)
# 从原位置删除
t = t[:m.start()] + "\n" + m.group(2) + t[m.end():]

# 在 sec2 结束后插入 </aside> + stage + <aside class="panel right">
boundary = "      </section>\n\n      <section>\n        <div class=\"sec-title\">3 · 位置与效果</div>"
assert boundary in t, "boundary not found"
new_boundary = ("      </section>\n"
                "    </aside>\n"
                + stage_block +
                "    <aside class=\"panel\">\n"
                "      <section>\n"
                "        <div class=\"sec-title\">3 · 位置与效果</div>")
t = t.replace(boundary, new_boundary, 1)

# 现有末尾的 </aside> 正好作为右栏闭合，无需改

io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("restructured ok")

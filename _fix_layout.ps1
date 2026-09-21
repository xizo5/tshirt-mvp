$html = "C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp\index.html"
$t = [IO.File]::ReadAllText($html)
$pairs = @(
  @('var size = base * 0.34 * (state.scale / 100);', 'var size = base * 0.30 * (state.scale / 100);'),
  @('var cy = H * 0.42 + (state.posY / 100) * H * 0.3;', 'var cy = H * 0.60 + (state.posY / 100) * H * 0.3;'),
  @('strength: 60, dye: true', 'strength: 75, dye: true'),
  @('(state.strength / 100) * 28', '(state.strength / 100) * 40'),
  @('max="100" value="60"><output id="oStr">60', 'max="100" value="75"><output id="oStr">75'),
  @('state.strength = 60; state.dye = true', 'state.strength = 75; state.dye = true'),
  @('$("rStr").value = 60; $("oStr").textContent = "60";', '$("rStr").value = 75; $("oStr").textContent = "75";'),
  @("od[o+c] = top * (1-fy) + bot * fy;`n        }", "od[o+c] = top * (1-fy) + bot * fy;`n        }`n        var m = Math.min(sw, sh) * 0.04;`n        var ef = Math.min(x, sw - 1 - x, y, sh - 1 - y, m) / m;`n        ef = ef * ef * (3 - 2 * ef);`n        od[o+3] = od[o+3] * ef;")
)
foreach ($p in $pairs) {
  if ($t.Contains($p[0])) { $t = $t.Replace($p[0], $p[1]); "OK: " + $p[0].Substring(0, [Math]::Min(40, $p[0].Length)) }
  else { "MISS: " + $p[0].Substring(0, [Math]::Min(40, $p[0].Length)) }
}
[IO.File]::WriteAllText($html, $t, (New-Object Text.UTF8Encoding($false)))

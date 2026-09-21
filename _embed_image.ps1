Add-Type -AssemblyName System.Drawing
$base = "C:\Users\AI\DoubaoWork\chats\2026-09-21\new-chat-1\tshirt-mvp"
$src = "$base\assets\tshirt_base.jpg"
$tmp = "$base\assets\_resized.jpg"
$html = "$base\index.html"

$img = [System.Drawing.Image]::FromFile($src)
$w = 960; $h = 1280
$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.DrawImage($img, 0, 0, $w, $h)
$g.Dispose()

$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$eps = New-Object System.Drawing.Imaging.EncoderParameters(1)
$eps.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]85)
$bmp.Save($tmp, $enc, $eps)
$bmp.Dispose(); $img.Dispose()

$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($tmp))
$text = [IO.File]::ReadAllText($html)
if ($text.Contains('__TEE_BASE64__')) {
    $text = $text.Replace('__TEE_BASE64__', $b64)
    [IO.File]::WriteAllText($html, $text, (New-Object Text.UTF8Encoding($false)))
    "OK replaced, base64 length: $($b64.Length)"
} else {
    "MARKER NOT FOUND"
}
Remove-Item $tmp -ErrorAction SilentlyContinue

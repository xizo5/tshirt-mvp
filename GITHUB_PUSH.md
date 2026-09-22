# 本地项目上传 GitHub 完整流程

以本项目（`tshirt-mvp`，纯前端单文件 HTML）为例，记录从零把本地目录推到 GitHub 私有仓库的全过程，包括踩过的坑。

---

## 0. 前置条件

- 已安装 Git（`git --version` 能出版本号即可）
- 已有 GitHub 账号
- 本地项目目录准备好，知道哪些文件该进仓库、哪些不该（截图、临时脚本、密钥等）

---

## 1. 配置提交身份（只需一次）

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

> 不加 `--global` 就只对当前仓库生效。本项目里我们用的是局部配置：
> `git config user.name "zuohb"` / `git config user.email "1410128330@qq.com"`。

---

## 2. 准备 GitHub Token（关键，容易踩坑）

去 GitHub → Settings → Developer settings → Personal access tokens 生成一个 token。

### 强烈建议用 **Classic** token，勾选 `repo` 权限

```bash
# 创建仓库用 API：POST https://api.github.com/user/repos
```

### ⚠️ 踩坑：Fine-grained token 不能创建仓库

我们第一次用 fine-grained token 调创建仓库接口，直接 403：

```
403 Resource not accessible by personal access token
```

**原因**：fine-grained token 即使勾选了仓库权限，也不允许通过 API 创建"全新"的仓库；只有 classic token 勾 `repo` scope 才行。

**两条路任选**：
- 用 classic token 自动建库（推荐，本文流程）；
- 或手动在网页 https://github.com/new 新建空仓库，token 只用来推送。

---

## 3. 创建远程仓库

### 方式 A：API 自动创建（需要 classic token）

```powershell
$token = "ghp_xxxxxxxx"
$h = @{ Authorization = "token $token"; "User-Agent" = "tshirt-push" }
$body = @{
  name        = "仓库名"
  description = "描述"
  private     = $true        # 私有；公开改 $false
  auto_init   = $false       # 必须空仓库，不要自动 README
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
  -Method Post -Headers $h -Body $body -ContentType "application/json"
```

返回 JSON 里 `full_name`（如 `xizo5/tshirt-mvp`）和 `clone_url` 就是仓库地址。

### 方式 B：网页手动创建

打开 https://github.com/new → 填仓库名 → 选 Private → **不要勾选** Add README / .gitignore / license → Create。

> 一旦仓库里有了 README 等文件，首次 push 前要先 `git pull --rebase origin main` 合并，否则会报 non-fast-forward。空仓库最省事。

---

## 4. 本地初始化与提交

在项目根目录：

```bash
git init -b main
```

写 `.gitignore`，把不需要的东西挡在外面：

```gitignore
# 本项目实际用到的忽略项
_shots/          # 自检截图
*.b64            # base64 临时文件
*.log
.DS_Store
Thumbs.db
```

> 原则：截图、临时产物、密钥、本地缓存不进仓库。素材图（`assets/*.jpg`）这种交付要用的才进。

提交：

```bash
git add -A
git status --short        # 先看一眼暂存清单对不对
git commit -m "MVP: 项目初始化"
```

Windows 上 Git 提示 `LF will be replaced by CRLF` 是正常警告，不用管。

---

## 5. 推送（token 嵌入 URL，推完立刻清掉）

```bash
cd 项目目录

# 用 token 做一次性 remote
git remote add origin "https://用户名:你的token@github.com/用户名/仓库名.git"

git push -u origin main

# ★ 关键：把 remote 里的 token 删掉，本地不保留密钥
git remote set-url origin "https://github.com/用户名/仓库名.git"

# 验证
git remote -v
```

> 为什么必须清掉？token 会明文写进 `.git/config`，任何人拿到这个文件就拿到了你的 GitHub 权限。
> 推完执行 `set-url` 换成不含 token 的干净地址即可。后续 push 时 Git 会走系统凭据管理器（首次弹窗登录一次即可）。

---

## 6. 验证

打开 `https://github.com/用户名/仓库名`，应该能看到：

- `main` 分支
- 刚才 commit 的文件清单
- 提交记录里有你刚那条 commit

---

## 7. 日常后续工作流

```bash
git add -A
git commit -m "改了什么"
git push
```

拉别人/自己别处的更新：

```bash
git pull
```

查看状态：

```bash
git status
git log --oneline
```

---

## 踩坑清单（本次实际遇到）

| 现象 | 原因 | 解法 |
|---|---|---|
| 创建仓库 API 返回 403 | fine-grained token 无建库权限 | 换 classic token 勾 `repo`，或网页手动建 |
| push 报 non-fast-forward | 远程仓库已有 README 等文件 | `git pull --rebase origin main` 后再 push |
| push 时 PowerShell 报 NativeCommandError | git 把进度写到 stderr，PowerShell 当错 | 看输出里有没有 `[new branch]` /分支信息，有才是真成功 |
| 不想把 token 留本地 | `.git/config` 里 remote 含明文 token | push 后立刻 `git remote set-url origin 干净地址` |
| `LF will be replaced by CRLF` | Windows 换行符自动转换 | 正常警告，可忽略 |

---

## 安全提醒

- 任何 token 发出来之后都算泄露。本次用过的 token，记得去 GitHub → Settings → Developer settings 里 **Revoke**，需要时重新生成。
- 永远不要把 token 写进 `README`、`.env`、脚本并提交到远程仓库；`.gitignore` 里要兜住这类文件。

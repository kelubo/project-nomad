# Project N.O.M.A.D. 中文定制版

本目录及其配套的分支策略，让你的 fork 在**持续跟踪上游**的同时，拥有**完整中文界面**和**中国离线地图**。

---

## 一、为什么要这样组织（先读这段）

上游原作者仓库是 `Crosstalk-Solutions/project-nomad`，你的 fork 是 `kelubo/project-nomad`。如果直接在代码里改中文，上游每次更新都会和你改过的文件冲突，"跟踪上游"就变成"无休止解冲突"。

所以采用**分支隔离 + 定制资产集中**的策略：

```
上游 Crosstalk-Solutions/main
        │ fetch + merge
        ▼
   main 分支           ← 纯净镜像，永远跟随上游，不含任何中文
        │ merge
        ▼
   zh-cn 分支          ← 你的定制版：界面汉化 + 中国地图 + 本文档
        │ push
        ▼
   origin (你的 fork) 的 zh-cn 分支
```

**所有中文定制资产都放在 `zh-cn/` 目录**，与上游源码物理隔离——上游几乎不会碰这个目录，因此同步时几乎零冲突。少数必须改动上游源码的地方（如 i18n 注入点），改动量也控制到最小。

---

## 二、当前状态

| 项目 | 状态 |
|---|---|
| 上游远程 `upstream` | 已配置，指向 Crosstalk-Solutions 官方仓库 |
| `main` 分支 | 已同步到上游最新（v1.35.1 之后） |
| `zh-cn` 分支 | 已创建，承载所有定制 |
| 同步脚本 | `zh-cn/sync-upstream.sh`（已测试） |
| 界面汉化 | 见下方「汉化进度」 |
| 中国地图 | 见 `zh-cn/maps/` |

---

## 三、日常同步上游（核心操作）

### 一键同步

在项目根目录执行：

```bash
bash zh-cn/sync-upstream.sh
```

它会自动完成：
1. `git fetch upstream` 拉取上游最新代码和标签
2. 把更新合并进纯净的 `main` 分支
3. 切换到 `zh-cn` 分支并合并 `main`（**你的汉化和地图改动会保留**）
4. 把 `main` 和 `zh-cn` 都推送到你的 fork（origin）

### 其他用法

```bash
bash zh-cn/sync-upstream.sh --check     # 只检查落后多少，不改任何东西
bash zh-cn/sync-upstream.sh --no-push   # 只同步到本地，不推送
```

### 发生合并冲突时

如果脚本报冲突，通常是"你改过的某个文件，上游也改了"。处理步骤：

```bash
git status                      # 查看哪些文件冲突
# 逐个编辑冲突文件，保留你的中文改动，同时接纳上游的新功能
git add <冲突文件>
git commit
bash zh-cn/sync-upstream.sh     # 重新跑，完成推送
```

**降低冲突的关键**：汉化文本集中在 `zh-cn/` 的语言包文件里，组件文件只做一次性的 `t()` 改造。上游若改了某组件的文案，你只需在语言包里补一个 key，不必再碰组件结构。

---

## 四、Windows 下 GitHub SSH 通道（本机环境）

本机命令行 OpenSSH 直连 GitHub 会被拒（无 `~/.ssh` 密钥），但 pageant 里已加载 GitHub 密钥。脚本会自动使用 plink wrapper：

- wrapper 位置：`C:\Users\Administrator\bin\plink-wrapper.sh`
- 内容：`exec "/c/Program Files/TortoiseGit/bin/TortoiseGitPlink.exe" -batch "$@"`
- 前提：使用 GitHub 前确保 **pageant 正在运行**并已加载密钥

如果换机器/换用户，需要重新建 wrapper 并确认 pageant 密钥，否则 `git fetch/push` 会失败。

---

## 五、界面汉化

（汉化实现与进度在 `zh-cn/i18n-progress.md` 中维护）

技术路线：轻量自建 i18n（避免引入大依赖），中文文本集中在语言包，组件通过 `t('key')` 引用。

> 上游新增的 `install/nomad-translate/` 是给 ZIM 阅读内容做机器翻译的代理（翻译百科正文），**不是管理界面 i18n**，因此管理界面仍需本方案的汉化。

---

## 六、中国离线地图

详见 `zh-cn/maps/README.md`。要点：

- 地图格式为 `.pmtiles`，系统原生支持从公开 URL 下载、也支持自定义 URL 导入
- 上游地图清单 `maps.json` 是**从上游 GitHub URL 远程拉取**的，本定制通过本地覆盖方式加入中国地图清单
- 中国地图数据从 Protomaps 官方每日构建**远程裁切**得到，无需下载 120GB 全球数据
- 全国 bbox：`73.0,3.0,136.0,54.0`；`-14` 级缩放约 5–8GB；可用更紧的 bbox 减小体积

---

## 七、注意事项

- **不要**直接在 `main` 分支写任何中文改动，main 必须保持纯净
- 每次同步前建议先 `git status` 确认工作区干净
- 汉化时保留品牌名 `N.O.M.A.D.`、技术名词、URL 链接不翻译
- 上游大版本更新（major）后，建议先在 `--no-push` 模式下同步并检查 `npm run build` 是否通过，再推送

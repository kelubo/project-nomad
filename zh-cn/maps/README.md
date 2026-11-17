# 中国离线地图（zh-cn 定制）

让 N.O.M.A.D. 的「离线地图」支持中国全国及各省地图，基于 Protomaps / OpenStreetMap 数据。

---

## 一、工作原理

N.O.M.A.D. 的地图能力：
- 地图文件格式为 **`.pmtiles`**（单文件矢量瓦片 archive）
- 地图清单从 GitHub 拉取（原版只有美国各州，见 `collections/maps.json`）
- 系统内置 `pmtiles extract` 能力，可从 Protomaps 全球数据**按边界裁切**出区域文件，无需下载 120GB 全球数据

中文定制做了三件事：
1. **`maps.zh-cn.json`** — 中文增强版清单（原版美国各州 + 新增「中国」分区），由 `gen_manifest.py` 生成
2. **本地清单加载补丁** — `collection_manifest_service.ts` 里约 12 行改动：优先读本地中文清单，缺失则回退上游远程清单
3. **`build-china-maps.sh`** — 从 Protomaps 每日构建远程裁切中国地图的脚本

---

## 二、生成中国地图文件

### 1. 安装裁切工具

```bash
bash zh-cn/maps/build-china-maps.sh --install-pmtiles
```

脚本会自动下载 go-pmtiles CLI 到 `zh-cn/maps/bin/`。Windows 会提示手动下载 `pmtiles.exe`。

### 2. 裁切地图

```bash
# 生成全部（全国 + 9 个省市）
bash zh-cn/maps/build-china-maps.sh

# 只生成全国
bash zh-cn/maps/build-china-maps.sh nationwide

# 只生成指定省份
bash zh-cn/maps/build-china-maps.sh beijing guangdong
```

输出在 `zh-cn/maps/output/`，文件名如 `china_nationwide_2026-11_z14.pmtiles`。

**参数说明：**
- 数据源：`https://maps.protomaps.com/builds/latest.pmtiles`（官方每日构建，可用 `SOURCE_URL` 环境变量改）
- 缩放级别：默认 z14（`MAXZOOM=14`），覆盖中国全境约 5–8GB；改小可减小体积
- bbox 定义：`zh-cn/maps/bboxes.json`，全国用 `73.0,3.0,136.0,54.0`（含南海诸岛）
- 裁切会从远程读取几十 GB 数据块，**耗时取决于网速**，不是实时进度

> 提示：更紧凑的全国 bbox `73.5,18.0,135.0,53.5`（大陆+港澳台，不含南海诸岛）可显著减小文件，按需在 `bboxes.json` 里替换。

---

## 三、托管地图文件

裁切出的 `.pmtiles` 需要一个**公开可访问的 URL**（系统只从 URL 下载）。推荐用 GitHub Release：

1. 在你的 fork 上创建 tag `china-maps`
2. 把 `output/` 里的所有 `.pmtiles` 作为附件上传到该 Release
3. 得到形如 `https://github.com/kelubo/project-nomad/releases/download/china-maps/xxx.pmtiles` 的 URL

> GitHub Release 单文件上限 2GB（免费版），全国 5–8GB 的文件需拆分或用其他存储（如 Cloudflare R2、自建对象存储）。可按省份分别托管，全国文件可选生成或省略。

---

## 四、让软件加载中文清单

清单文件 `maps.zh-cn.json` 里的 `url` 必须与上一步的托管地址一致。

### 生成/更新清单

```bash
# 用默认 fork Release 地址生成
python3 zh-cn/maps/gen_manifest.py

# 指定你自己的 Release / 存储前缀
python3 zh-cn/maps/gen_manifest.py --repo https://github.com/<你>/project-nomad/releases/download/china-maps
```

### 部署本地清单文件

后端服务通过以下路径（按顺序）查找本地清单：
1. 环境变量 `MAPS_SPEC_LOCAL_PATH` 指定的路径
2. 默认：`{程序工作目录}/zh-cn/maps/maps.zh-cn.json`

Docker 部署时，需把该文件挂载/复制进容器的对应路径，例如 docker-compose 加：

```yaml
volumes:
  - ./zh-cn/maps/maps.zh-cn.json:/app/zh-cn/maps/maps.zh-cn.json:ro
```

若本地清单不存在，系统会自动回退到上游远程清单（行为与官方版一致，只是没有中国分区）。

---

## 五、使用

1. 部署好中文清单后，重启 Command Center
2. 进入 **Maps → Settings / Download by region**，会看到新增的「中国地图」分区
3. 选择全国或某省下载（需联网下载一次，之后离线可用）
4. 下载后在地图界面即可离线查看

也可以在设置页用「自定义 URL 导入」直接粘贴某个 `.pmtiles` 的公开 URL 单独加载，无需改清单。

---

## 六、上游更新后

上游更新 `collections/maps.json`（比如新增美国州）后，重新生成本地清单即可同步：

```bash
git fetch upstream && git checkout main && git merge upstream/main
git checkout zh-cn && git merge main
python3 zh-cn/maps/gen_manifest.py --repo <你的URL前缀>
git add zh-cn/maps/maps.zh-cn.json && git commit -m "更新中文地图清单"
```

或者直接跑一键同步脚本 `zh-cn/sync-upstream.sh`，再重新生成清单。

---

## 七、数据署名与合规

- 地图数据来自 OpenStreetMap 贡献者（ODbL 许可）与 Protomaps，请保留署名（系统界面已自动显示 © OpenStreetMap © Protomaps）
- 请遵守当地地图数据相关法律法规
- 全国地图 bbox 含南海诸岛；如需符合特定地图审核要求，请自行核对并使用合规数据源

#!/usr/bin/env bash
# ============================================================
# 从 Protomaps 官方每日构建远程裁切中国地图 (.pmtiles)
# ------------------------------------------------------------
# 无需下载 120GB 全球数据：pmtiles CLI 通过 HTTP Range 请求
# 按需从远程全球文件提取指定 bbox，生成本地小文件。
#
# 用法：
#   bash zh-cn/maps/build-china-maps.sh              # 生成全部（全国+省份）
#   bash zh-cn/maps/build-china-maps.sh nationwide   # 只生成全国
#   bash zh-cn/maps/build-china-maps.sh beijing guangdong  # 指定省份
#   bash zh-cn/maps/build-china-maps.sh --install-pmtiles  # 仅安装工具
#
# 环境要求：
#   - Linux/macOS/Windows(WSL或Git Bash)，有 curl/tar
#   - 磁盘空间：全国 z14 约 5-8GB，省份每个几百 MB
#   - 网络：需能访问 maps.protomaps.com（提取时会取几十 GB 数据块）
#
# 注意：地图数据版权归 OpenStreetMap 贡献者，使用时请保留署名
#       （系统界面已显示 © OpenStreetMap © Protomaps）。
# ============================================================
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
info(){ echo -e "${BLUE}[信息]${NC} $*"; }
ok(){   echo -e "${GREEN}[成功]${NC} $*"; }
warn(){ echo -e "${YELLOW}[注意]${NC} $*"; }
err(){  echo -e "${RED}[错误]${NC} $*"; }

HERE="$(cd "$(dirname "$0")" && pwd)"
OUT_DIR="${HERE}/output"
PMTILES_BIN="${PMTILES_BIN:-${HERE}/bin/pmtiles}"
SOURCE_URL="${SOURCE_URL:-https://maps.protomaps.com/builds/latest.pmtiles}"
MAXZOOM="${MAXZOOM:-14}"
VERSION="2026-11"

# 安装 go-pmtiles
install_pmtiles(){
  info "安装 go-pmtiles CLI..."
  mkdir -p "${HERE}/bin"
  local ver="1.30.2"
  local os="Linux"; command -v uname >/dev/null && case "$(uname -s)" in
    Darwin) os="Darwin" ;; MINGW*|MSYS*|CYGWIN*) os="Windows" ;;
  esac
  local arch="x86_64"; case "$(uname -m)" in aarch64|arm64) arch="arm64" ;; esac
  local pkg="go-pmtiles_${ver}_${os}_${arch}.tar.gz"
  local url="https://github.com/protomaps/go-pmtiles/releases/download/v${ver}/${pkg}"
  if [ "$os" = "Windows" ]; then
    pkg="go-pmtiles_${ver}_Windows_x86_64.zip"
    url="https://github.com/protomaps/go-pmtiles/releases/download/v${ver}/${pkg}"
    warn "Windows 请手动从 $url 下载 pmtiles.exe 放到 ${HERE}/bin/，然后重跑"
    return 0
  fi
  curl -fL "$url" -o "${HERE}/bin/${pkg}"
  tar -xzf "${HERE}/bin/${pkg}" -C "${HERE}/bin" pmtiles
  chmod +x "${HERE}/bin/pmtiles"
  ok "pmtiles 已安装: ${PMTILES_BIN}"
}

if [ "${1:-}" = "--install-pmtiles" ]; then install_pmtiles; exit 0; fi

if [ ! -x "$PMTILES_BIN" ]; then
  warn "未找到 pmtiles CLI，尝试自动安装..."
  install_pmtiles
fi
[ -x "$PMTILES_BIN" ] || { err "pmtiles CLI 不可用，请手动安装后重试"; exit 1; }

mkdir -p "$OUT_DIR"

# 读取 bbox 定义（用 python 解析 json，避免 bash 处理 json 的坑）
get_bbox(){
  python3 - "$1" <<'PY'
import json,sys
d=json.load(open('zh-cn/maps/bboxes.json',encoding='utf-8'))
k=sys.argv[1]
if k=='nationwide': print(d['全国'])
elif k=='nationwide_compact': print(d['全国_紧凑'])
else: print(d['省份'].get(k,''))
PY
}

extract(){
  local id="$1" bbox="$2"
  [ -z "$bbox" ] && { err "未找到 $id 的 bbox"; return 1; }
  local out="${OUT_DIR}/${id}_${VERSION}_z${MAXZOOM}.pmtiles"
  if [ -f "$out" ]; then warn "$id 已存在，跳过（删除 $out 可重新生成）"; return 0; fi
  info "裁切 $id  bbox=$bbox  maxzoom=$MAXZOOM -> $(basename "$out")"
  warn "这一步会从远程取数据块，耗时取决于网速，请耐心等待..."
  "$PMTILES_BIN" extract "$SOURCE_URL" "$out" --bbox="$bbox" --maxzoom="$MAXZOOM"
  local sz; sz=$(du -h "$out" | cut -f1)
  ok "完成 $id : $sz"
}

TARGETS=("$@")
if [ ${#TARGETS[@]} -eq 0 ]; then
  TARGETS=(nationwide beijing shanghai guangdong zhejiang jiangsu sichuan shandong henan hubei)
fi

for t in "${TARGETS[@]}"; do
  extract "$t" "$(get_bbox "$t")"
done

echo
ok "全部完成！输出目录: $OUT_DIR"
warn "下一步：把 output/ 里的 .pmtiles 上传到 GitHub Release（tag=china-maps）"
warn "        或你自己的公开存储，并确保 zh-cn/maps/maps.zh-cn.json 里的 URL 与之对应。"

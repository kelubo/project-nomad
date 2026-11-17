#!/usr/bin/env bash
# ============================================================
# N.O.M.A.D. 上游同步脚本（fork 持续跟踪）
# ------------------------------------------------------------
# 作用：从上游原作者仓库拉取最新代码 -> 更新纯净的 main 分支
#       -> 合并进 zh-cn 定制分支（汉化 + 中国地图）-> 推送到你的 fork
#
# 分支模型：
#   upstream/main  ──fetch──>  main (纯净镜像，跟随上游)
#                                 │
#                                 └──merge──> zh-cn (你的定制)
#                                                 │
#                                            push origin zh-cn
#
# 用法：
#   bash zh-cn/sync-upstream.sh            # 完整同步 + 推送
#   bash zh-cn/sync-upstream.sh --no-push   # 只同步到本地，不推送
#   bash zh-cn/sync-upstream.sh --check     # 只检查落后多少，不做改动
#
# 前提：已配置 upstream 远程、已装 pageant 密钥（Windows 下经
#       plink wrapper 走 SSH，见 zh-cn/README-zh.md）
# ============================================================
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
info(){ echo -e "${BLUE}[信息]${NC} $*"; }
ok(){   echo -e "${GREEN}[成功]${NC} $*"; }
warn(){ echo -e "${YELLOW}[注意]${NC} $*"; }
err(){  echo -e "${RED}[错误]${NC} $*"; }

NO_PUSH=0; CHECK_ONLY=0
for a in "$@"; do
  case "$a" in
    --no-push) NO_PUSH=1 ;;
    --check)   CHECK_ONLY=1 ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
  esac
done

# 确保在项目根目录运行
if [ ! -d .git ]; then err "请在仓库根目录运行此脚本（当前目录没有 .git）"; exit 1; fi

# SSH wrapper：Windows + pageant 场景，若存在则自动使用
if [ -x "$HOME/bin/plink-wrapper.sh" ]; then
  export GIT_SSH_COMMAND="$HOME/bin/plink-wrapper.sh"
  info "使用 SSH wrapper: $GIT_SSH_COMMAND"
fi

# 确认远程存在
if ! git remote get-url upstream >/dev/null 2>&1; then
  err "未配置 upstream 远程。请先执行："
  err '  git remote add upstream git@github.com:Crosstalk-Solutions/project-nomad.git'
  exit 1
fi

info "拉取上游最新代码..."
git fetch upstream --tags

AHEAD=$(git rev-list --count upstream/main..main)
BEHIND=$(git rev-list --count main..upstream/main)
info "main 相对上游：领先 $AHEAD / 落后 $BEHIND"

if [ "$CHECK_ONLY" -eq 1 ]; then
  [ "$BEHIND" -eq 0 ] && ok "main 已是最新" || warn "main 落后上游 $BEHIND 个提交，建议运行同步"
  exit 0
fi

if [ "$BEHIND" -eq 0 ] && [ "$AHEAD" -eq 0 ]; then
  ok "main 已是最新，无需更新"
else
  info "更新 main 分支..."
  CUR=$(git branch --show-current)
  git checkout main
  # 优先快进；若因本地合并提交无法快进则用普通合并（历史已证明无冲突）
  if ! git merge --ff-only upstream/main >/dev/null 2>&1; then
    info "无法快进，使用合并提交方式..."
    if ! git merge --no-edit upstream/main; then
      err "main 合并冲突！请手动解决冲突后执行 git commit，再重跑本脚本。"
      git merge --abort 2>/dev/null || true
      git checkout "$CUR" 2>/dev/null || true
      exit 1
    fi
  fi
  ok "main 已更新到上游最新"
fi

info "合并到 zh-cn 定制分支..."
if ! git checkout zh-cn 2>/dev/null; then
  warn "zh-cn 分支不存在，正在从 main 创建..."
  git checkout -b zh-cn main
fi
if ! git merge --no-edit main; then
  err "============================================================"
  err "zh-cn 合并出现冲突（多半是你改过的文件上游也改了）。"
  err "处理方式："
  err "  1) git status 查看冲突文件"
  err "  2) 逐个编辑解决冲突（保留你的汉化/中文地图改动）"
  err "  3) git add <冲突文件> && git commit"
  err "  4) 重新运行本脚本完成推送"
  err "============================================================"
  exit 1
fi
ok "zh-cn 已合并上游最新代码，你的汉化与中文地图改动已保留"

if [ "$NO_PUSH" -eq 1 ]; then
  warn "按 --no-push 要求，跳过推送"
  exit 0
fi

info "推送到你的 fork (origin)..."
git push origin main
git push origin zh-cn
ok "同步完成：main 与 zh-cn 均已推送到 origin"

echo
ok "全流程结束。现在 main 是纯净上游镜像，zh-cn 是你的中文定制版。"

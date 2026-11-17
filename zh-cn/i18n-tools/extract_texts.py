#!/usr/bin/env python3
# ============================================================
# 从所有 TSX 组件提取待翻译的英文文案 -> zh-cn/i18n-tools/pending.json
# ------------------------------------------------------------
# 提取三类候选：
#   1) JSX 文本节点  >Some English text<
#   2) JSX 属性值    title="..." placeholder="..." 等
#   3) JS 字符串字面量（交给人工判断，不自动替换）
#
# 用法：python3 zh-cn/i18n-tools/extract_texts.py
# ============================================================
import os, re, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INERTIA = os.path.join(ROOT, 'admin', 'inertia')

# 只提取"看起来是英文句子/词组"的文案
RE_JSX_TEXT = re.compile(r'>\s*([A-Za-z][A-Za-z0-9 ,.\'!?()/\-:+&%]{2,120}?)\s*<')
RE_JSX_ATTR = re.compile(
    r'\b(title|placeholder|label|description|alt|aria-label|value)="([A-Za-z][A-Za-z0-9 ,.\'!?()/\-:+&%]{2,120}?)"'
)
# 跳过明显不是文案的：CSS 类、URL、变量名等
def is_text(s: str) -> bool:
    s = s.strip()
    if not s or len(s) < 2:
        return False
    if 'http' in s or '://' in s or s.startswith(('/', '#', 'w-', 'h-', 'text-', 'bg-')):
        return False
    if not re.search(r'[a-zA-Z]{2}', s):
        return False
    # 至少有一个空格或是常见单词（过滤纯驼峰标识符）
    if ' ' not in s and not s[0].isupper():
        return False
    return True

def main():
    found = {}
    for dirpath, _, filenames in os.walk(INERTIA):
        for fn in filenames:
            if not fn.endswith('.tsx'):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT).replace('\\', '/')
            src = open(path, encoding='utf-8').read()
            items = set()
            for m in RE_JSX_TEXT.findall(src):
                if is_text(m):
                    items.add(m.strip())
            for _, m in RE_JSX_ATTR.findall(src):
                if is_text(m):
                    items.add(m.strip())
            for t in items:
                found.setdefault(t, []).append(rel)

    out = os.path.join(os.path.dirname(__file__), 'pending.json')
    data = {k: {'files': sorted(set(v)), 'zh': ''} for k, v in sorted(found.items())}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'提取 {len(data)} 条候选文案 -> {out}')

if __name__ == '__main__':
    main()

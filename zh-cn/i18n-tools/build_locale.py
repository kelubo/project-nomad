#!/usr/bin/env python3
# ============================================================
# 根据译文表生成中文语言包 admin/inertia/locales/zh-CN.ts
# 译文维护在 translations.json（英文原文 -> 中文）
# 用法：python3 zh-cn/i18n-tools/build_locale.py
# ============================================================
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

trans = json.load(open(os.path.join(HERE, 'translations.json'), encoding='utf-8'))
# 去掉空译文（未翻译的保持英文原文）
trans = {k: v for k, v in trans.items() if v and v.strip()}

def ts_str(s: str) -> str:
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n') + "'"

lines = [
    '// [zh-cn] 中文语言包 —— 由 zh-cn/i18n-tools/build_locale.py 生成，请勿手工编辑',
    '// 译文源文件：zh-cn/i18n-tools/translations.json',
    'export const zhCN: Record<string, string> = {',
]
for k, v in sorted(trans.items()):
    lines.append(f'  {ts_str(k)}: {ts_str(v)},')
lines.append('}')
lines.append('')

out = os.path.join(ROOT, 'admin', 'inertia', 'locales', 'zh-CN.ts')
open(out, 'w', encoding='utf-8').write('\n'.join(lines))
print(f'生成 {out}，共 {len(trans)} 条译文')

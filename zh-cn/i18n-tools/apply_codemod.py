#!/usr/bin/env python3
# ============================================================
# 批量把组件里的英文文案替换为 t('...') 调用
# ------------------------------------------------------------
# 保守策略，只替换能被准确匹配、且语言包里有译文的文案：
#   1) JSX 纯文本节点:  >English text<        ->  >{t('English text')}<
#   2) JSX 属性值:      title="English text"  ->  title={t('English text')}
#   3) 已翻译文件顶部自动加: import { tGlobal as t } from '~/lib/i18n'
#
# 用法：
#   python3 zh-cn/i18n-tools/apply_codemod.py --dry-run          # 预览改动统计
#   python3 zh-cn/i18n-tools/apply_codemod.py                     # 实际应用
#   python3 zh-cn/i18n-tools/apply_codemod.py --file <相对路径>   # 只处理单个文件
# ============================================================
import os, re, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
INERTIA = os.path.join(ROOT, 'admin', 'inertia')
TRANS = json.load(open(os.path.join(HERE, 'translations.json'), encoding='utf-8'))
TRANS = {k: v for k, v in TRANS.items() if v and v.strip()}

IMPORT_LINE = "import { tGlobal as t } from '~/lib/i18n'\n"

# JSX 文本节点：> 纯英文文案 <（排除含 {} 表达式、换行、JSX 标签）
RE_JSX_TEXT = re.compile(r'(>)([A-Za-z][A-Za-z0-9 ,.\'!?()/\-:+&%]{1,120}?)(<)')
# JSX 字符串属性（注意：开引号属于前缀，闭引号要吞掉，替换为 {} 表达式时不保留引号）
RE_JSX_ATTR = re.compile(r'(\b(?:title|placeholder|label|description|alt|aria-label)=")([A-Za-z][A-Za-z0-9 ,.\'!?()/\-:+&%]{1,120}?)"')

def ts_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"

def convert(src: str):
    count = 0

    def repl_text(m):
        nonlocal count
        txt = m.group(2)
        if txt not in TRANS:
            return m.group(0)
        count += 1
        return f"{m.group(1)}{{t({ts_str(txt)})}}{m.group(3)}"

    def repl_attr(m):
        nonlocal count
        txt = m.group(2)
        if txt not in TRANS:
            return m.group(0)
        count += 1
        # group(1) 形如 title=" ，需去掉末尾的 =" 再改用 {} 表达式
        prefix = m.group(1)[:-2]
        return f"{prefix}={{t({ts_str(txt)})}}"

    out = RE_JSX_TEXT.sub(repl_text, src)
    out = RE_JSX_ATTR.sub(repl_attr, out)
    if count > 0 and "from '~/lib/i18n'" not in out:
        # 插到第一条真正的 import 语句之前；若没有 import 则插到文件最顶部
        m = re.search(r'^import\s', out, re.MULTILINE)
        idx = m.start() if m else 0
        out = out[:idx] + IMPORT_LINE + out[idx:]
    return out, count

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--file', help='相对 admin/inertia 的路径')
    args = ap.parse_args()

    if args.file:
        files = [os.path.join(INERTIA, args.file)]
    else:
        files = []
        for dp, _, fns in os.walk(INERTIA):
            for fn in fns:
                if fn.endswith('.tsx'):
                    files.append(os.path.join(dp, fn))

    total = 0
    changed_files = 0
    for path in sorted(files):
        src = open(path, encoding='utf-8').read()
        out, n = convert(src)
        if n:
            total += n
            changed_files += 1
            rel = os.path.relpath(path, ROOT).replace('\\', '/')
            print(f'{n:3d}  {rel}')
            if not args.dry_run:
                open(path, 'w', encoding='utf-8').write(out)
    print(f'--- 共替换 {total} 处，涉及 {changed_files} 个文件' + ('（DRY RUN，未写入）' if args.dry_run else ''))

if __name__ == '__main__':
    main()

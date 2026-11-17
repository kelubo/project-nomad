#!/usr/bin/env python3
# ============================================================
# 生成中文增强版地图清单 maps.zh-cn.json
# ------------------------------------------------------------
# 在原始 maps.json（美国各州）基础上追加「中国」分区。
# 当上游更新 maps.json 后，重新运行本脚本即可同步上游改动并
# 保留中国分区（前提：中国分区定义不变）。
#
# 用法：
#   python3 zh-cn/maps/gen_manifest.py
#   python3 zh-cn/maps/gen_manifest.py --base /path/to/upstream/maps.json
#   python3 zh-cn/maps/gen_manifest.py --repo https://github.com/<你>/project-nomad
# ============================================================
import json, argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

# 中国地图 pmtiles 的托管地址前缀。默认指向 fork 的 GitHub Releases，
# 请用 --repo 指定你自己的仓库，或生成后手工编辑 json 里的 url。
DEFAULT_RELEASE_BASE = "https://github.com/kelubo/project-nomad/releases/download/china-maps"

CHINA_COLLECTION = {
    "name": "中国地图",
    "slug": "china",
    "description": "中国全国及各省离线地形图（基于 Protomaps/OpenStreetMap 数据裁切）",
    "icon": "IconMap",
    "language": "zh",
    "resources": [
        # 全国
        {"id": "china_nationwide", "version": "2026-11",
         "title": "中国全境",
         "description": "中国大陆及港澳台全境地形图，约 5-8GB",
         "size_mb": 6000,
         "url": "{base}/china_nationwide_2026-11_z14.pmtiles"},
        # 主要省份/直辖市（bbox 见 bboxes.json）
        {"id": "beijing", "version": "2026-11", "title": "北京市",
         "description": "北京市离线地形图", "size_mb": 180,
         "url": "{base}/beijing_2026-11_z14.pmtiles"},
        {"id": "shanghai", "version": "2026-11", "title": "上海市",
         "description": "上海市离线地形图", "size_mb": 180,
         "url": "{base}/shanghai_2026-11_z14.pmtiles"},
        {"id": "guangdong", "version": "2026-11", "title": "广东省",
         "description": "广东省离线地形图", "size_mb": 700,
         "url": "{base}/guangdong_2026-11_z14.pmtiles"},
        {"id": "zhejiang", "version": "2026-11", "title": "浙江省",
         "description": "浙江省离线地形图", "size_mb": 500,
         "url": "{base}/zhejiang_2026-11_z14.pmtiles"},
        {"id": "jiangsu", "version": "2026-11", "title": "江苏省",
         "description": "江苏省离线地形图", "size_mb": 500,
         "url": "{base}/jiangsu_2026-11_z14.pmtiles"},
        {"id": "sichuan", "version": "2026-11", "title": "四川省",
         "description": "四川省离线地形图", "size_mb": 600,
         "url": "{base}/sichuan_2026-11_z14.pmtiles"},
        {"id": "shandong", "version": "2026-11", "title": "山东省",
         "description": "山东省离线地形图", "size_mb": 550,
         "url": "{base}/shandong_2026-11_z14.pmtiles"},
        {"id": "henan", "version": "2026-11", "title": "河南省",
         "description": "河南省离线地形图", "size_mb": 550,
         "url": "{base}/henan_2026-11_z14.pmtiles"},
        {"id": "hubei", "version": "2026-11", "title": "湖北省",
         "description": "湖北省离线地形图", "size_mb": 500,
         "url": "{base}/hubei_2026-11_z14.pmtiles"},
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=os.path.join(ROOT, 'collections', 'maps.json'),
                    help='上游 maps.json 路径')
    ap.add_argument('--repo', default=DEFAULT_RELEASE_BASE,
                    help='中国地图 pmtiles 的 URL 前缀（GitHub Release 目录）')
    ap.add_argument('--out', default=os.path.join(HERE, 'maps.zh-cn.json'))
    args = ap.parse_args()

    with open(args.base, encoding='utf-8') as f:
        spec = json.load(f)

    # 幂等：若已存在中国分区先移除，避免重复
    spec['collections'] = [c for c in spec['collections'] if c.get('slug') != 'china']

    china = json.loads(json.dumps(CHINA_COLLECTION))  # deep copy
    for r in china['resources']:
        r['url'] = r['url'].format(base=args.repo.rstrip('/'))
    spec['collections'].append(china)

    # 提升 spec_version 以触发客户端刷新缓存
    sv = spec.get('spec_version', '')
    spec['spec_version'] = sv + '-zh-cn'

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)

    total = sum(len(c['resources']) for c in spec['collections'])
    print(f"已生成: {args.out}")
    print(f"分区数: {len(spec['collections'])}（含中国）, 资源总数: {total}, spec_version: {spec['spec_version']}")


if __name__ == '__main__':
    main()

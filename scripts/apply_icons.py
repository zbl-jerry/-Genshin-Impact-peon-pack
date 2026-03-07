#!/usr/bin/env python3
"""
apply_icons.py  <pack_name>  <result_file>
读取 Chrome DevTools MCP 保存的 evaluate_script 结果文件，
提取 base64 缩略图，验证后保存到 packs/<name>/icons/，
并将 icon 字段写入 openpeon.json。
"""
import sys, json, base64, os, re

def apply_icons(pack_name: str, result_file: str):
    packs_dir = os.path.join(os.path.dirname(__file__), '..', 'packs')
    pack_dir  = os.path.realpath(os.path.join(packs_dir, pack_name))
    icons_dir = os.path.join(pack_dir, 'icons')
    manifest_path = os.path.join(pack_dir, 'openpeon.json')

    os.makedirs(icons_dir, exist_ok=True)

    # --- 1. 解析 MCP 结果文件 ---
    with open(result_file, 'r') as f:
        outer = json.loads(f.read())
    text = outer[0]['text']

    m = re.search(r'```json\n(\[.*?\])\n```', text, re.DOTALL)
    if not m:
        print(f"[ERROR] 在结果文件中找不到 JSON 数组", file=sys.stderr)
        sys.exit(1)
    urls = json.loads(m.group(1))
    print(f"  找到 {len(urls)} 张缩略图")

    # --- 2. 统计需要多少张 ---
    with open(manifest_path, encoding='utf-8') as f:
        manifest = json.load(f)
    total_sounds = sum(len(v['sounds']) for v in manifest['categories'].values())
    needed = total_sounds
    print(f"  需要 {needed} 张图标")

    # --- 3. 解码、验证、保存 ---
    saved = []
    for i, uri in enumerate(urls[:needed]):
        m2 = re.match(r'^data:image/(\w+);base64,(.+)$', uri, re.DOTALL)
        if not m2:
            print(f"  [SKIP] #{i}: 非法 data URI")
            continue
        try:
            img_bytes = base64.b64decode(m2.group(2))
        except Exception as e:
            print(f"  [SKIP] #{i}: base64 解码失败 - {e}")
            continue

        # 验证 magic bytes
        ext = None
        if img_bytes[:3] == b'\xff\xd8\xff':
            ext = 'jpg'
        elif img_bytes[:8] == b'\x89PNG\r\n\x1a\n':
            ext = 'png'
        elif img_bytes[:4] == b'RIFF' and img_bytes[8:12] == b'WEBP':
            ext = 'webp'
        if ext is None:
            print(f"  [SKIP] #{i}: 未知文件头 ({img_bytes[:4].hex()})")
            continue
        if len(img_bytes) < 1000:
            print(f"  [SKIP] #{i}: 文件太小 ({len(img_bytes)}B)")
            continue

        fname = f"{pack_name}_{i:02d}.{ext}"
        with open(os.path.join(icons_dir, fname), 'wb') as f:
            f.write(img_bytes)
        saved.append(fname)

    print(f"  保存: {len(saved)}/{needed} 张")

    if len(saved) < needed:
        print(f"  [WARN] 图片不足，将循环复用已有图片")

    # --- 4. 写入 openpeon.json ---
    idx = 0
    for cat_data in manifest['categories'].values():
        for sound in cat_data['sounds']:
            img_fname = saved[idx % len(saved)]
            sound['icon'] = f"icons/{img_fname}"
            idx += 1

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"  openpeon.json 已更新，配置了 {idx} 个图标")

    # --- 5. 安装 ---
    install_dir = os.path.expanduser(f"~/.openpeon/packs/{pack_name}")
    os.makedirs(install_dir, exist_ok=True)
    import shutil
    shutil.copytree(pack_dir, install_dir, dirs_exist_ok=True)
    print(f"  已安装到 {install_dir}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <pack_name> <result_file>")
        sys.exit(1)
    apply_icons(sys.argv[1], sys.argv[2])

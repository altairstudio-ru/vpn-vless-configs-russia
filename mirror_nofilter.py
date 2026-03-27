#!/usr/bin/env python3
# Mirror_nofilter.py — после первого, без фильтра по странам

import os
import shutil
import urllib.parse
import re

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_PATH, "githubmirror")
NEW_DIR = os.path.join(BASE_DIR, "new")
CLEAN_NOFILTER_DIR = os.path.join(BASE_DIR, "clean_nofilter")

PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria", "hysteria2", "hy2", "tuic"]
CHUNK_SIZE = 500

def protocol_of(line: str):
    for p in PROTOCOLS:
        if line.startswith(p + "://"):
            return p
    return None

def extract_host_port_scheme(line: str):
    try:
        u = urllib.parse.urlparse(line)
        return u.hostname, u.port or 443, u.scheme
    except:
        return None, None, None

def clean_start():
    if os.path.exists(CLEAN_NOFILTER_DIR):
        shutil.rmtree(CLEAN_NOFILTER_DIR)
    os.makedirs(CLEAN_NOFILTER_DIR, exist_ok=True)

def write_chunks_by_protocol(base_dir: str, protocol: str, items: list, chunk_size: int = 500):
    proto_dir = os.path.join(base_dir, protocol)
    os.makedirs(proto_dir, exist_ok=True)
    for start in range(0, len(items), chunk_size):
        part = items[start:start + chunk_size]
        part_num = start // chunk_size + 1
        path = os.path.join(proto_dir, f"{protocol}_{part_num:03d}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(part))

def main():
    src_file = os.path.join(NEW_DIR, "all_new.txt")
    if not os.path.exists(src_file):
        print("❌ Не найден файл githubmirror/new/all_new.txt — сначала запусти первый скрипт.")
        return

    clean_start()

    with open(src_file, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    # только валидные протоколы
    lines = [l for l in lines if protocol_of(l)]

    # дедуп по IP:PORT:SCHEME (но уже БЕЗ фильтрации тегов/доменов)
    seen = set()
    clean_keys = []
    for line in lines:
        host, port, scheme = extract_host_port_scheme(line)
        if not host:
            continue
        key = (host, port, scheme)
        if key in seen:
            continue
        seen.add(key)
        clean_keys.append(line)

    # общий файл
    with open(os.path.join(CLEAN_NOFILTER_DIR, "all_nofilter.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(clean_keys))

    # по протоколам (один файл на протокол)
    for p in PROTOCOLS:
        items = [k for k in clean_keys if protocol_of(k) == p]
        if not items:
            continue
        with open(os.path.join(CLEAN_NOFILTER_DIR, f"{p}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(items))

    # чанки по протоколам (если нужно, удобно для импорта)
    by_proto_dir = os.path.join(CLEAN_NOFILTER_DIR, "by_protocol")
    os.makedirs(by_proto_dir, exist_ok=True)
    for p in PROTOCOLS:
        items = [k for k in clean_keys if protocol_of(k) == p]
        if items:
            write_chunks_by_protocol(by_proto_dir, p, items, CHUNK_SIZE)

    print("✅ ГОТОВО (no-filter)")
    print(f"   📥 Всего строк на входе: {len(lines)}")
    print(f"   🔗 Уникальных IP:PORT:SCHEME: {len(clean_keys)}")
    print("\n📊 По протоколам:")
    for p in PROTOCOLS:
        count = len([k for k in clean_keys if protocol_of(k) == p])
        if count:
            print(f"   {p}: {count}")

if __name__ == "__main__":
    main()

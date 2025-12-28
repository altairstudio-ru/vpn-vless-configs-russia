#!/usr/bin/env python3
# Mirror.py — SMART FILTER (No Asia, No Africa, No LatAm)
# Оставляет Европу, Россию, США и "чистые" IP.

import os
import shutil
import requests
import urllib.parse
import base64

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_PATH, "githubmirror")
NEW_DIR = os.path.join(BASE_DIR, "new")
CLEAN_DIR = os.path.join(BASE_DIR, "clean")

PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria", "hysteria2", "hy2", "tuic"]

# === ЧЕРНЫЙ СПИСОК (SOFT FILTER) ===
# Удаляем всё, что имеет ЯВНЫЕ признаки Азии, Африки или Южной Америки.
# Ключи без подписи (голые IP) — ОСТАВЛЯЕМ (чекер сам проверит).
BAD_WORDS = [
    # === 1. АЗИЯ (Ближний Восток, ЦА, ЮВА) ===
    "IRAN", "TEHRAN", "MASHHAD", "ISFAHAN", "SHIRAZ", "TABRIZ", # Иран
    "CHINA", "BEIJING", "SHANGHAI", "SHENZHEN", "GUANGZHOU", "HK", "HONGKONG", "TW", "TAIWAN", # Китай
    "INDIA", "MUMBAI", "DELHI", "BANGALORE", "IN_", # Индия
    "PAKISTAN", "KARACHI", "LAHORE", "PK_", # Пакистан
    "TURKEY", "ISTANBUL", "ANKARA", "TR_", # Турция
    "AFGHANISTAN", "KABUL", "IRAQ", "BAGHDAD", "SYRIA",
    "SAUDI", "RIYADH", "UAE", "DUBAI", "QATAR",
    "INDONESIA", "JAKARTA", "VIETNAM", "HANOI", "THAILAND", "BANGKOK",
    "KOREA", "SEOUL", "JAPAN", "TOKYO", "OSAKA", "SINGAPORE", "SG_",
    "ISRAEL", "TELAVIV", "AZERBAIJAN", "BAKU", "KAZAKHSTAN", "ALMATY", # KZ часто оставляют, но если надо убрать - вот
    
    # === 2. ЮЖНАЯ АМЕРИКА ===
    "BRAZIL", "SAOPAULO", "RIO", "BR_", 
    "ARGENTINA", "BUENOSAIRES", "AR_",
    "CHILE", "COLOMBIA", "MEXICO", "PERU", "VENEZUELA",

    # === 3. АФРИКА ===
    "EGYPT", "CAIRO", 
    "NIGERIA", "LAGOS", 
    "SOUTHAFRICA", "JOHANNESBURG", "CAPETOWN", "ZA_",
    "MOROCCO", "ALGERIA", "TUNISIA", "KENYA", "ETHIOPIA",

    # === 4. МУСОРНЫЕ СЛОВА / ПРОВАЙДЕРЫ ===
    "CLOUDFLARE", "CF_CDN", "WORKER", "PAGES_DEV", # Бесплатный CDN мусор
    "MCI", "MTN", "IRANCELL", "RIGHTEL", "ARVAN", "DERAK", "PARSPACK", # Иран телеком
    "V2RAYNG", "VPN_TELL", "SIVAND", "NAJI", "BAX", "HACKER", "FREE_VPN",
    "RELAY", "POOL", "SHOP", "STORE", "VIP", "PREMIUM", # Реклама

    # === 5. ФЛАГИ (Эмодзи стран-изгоев для фильтра) ===
    "🇮🇷", "🇨🇳", "🇮🇳", "🇵🇰", "🇹🇷", "🇦🇫", "🇮🇶", "🇸🇦", "🇦🇪", "🇮🇩", "🇻🇳", "🇹🇭", 
    "🇰🇷", "🇯🇵", "🇹🇼", "🇸🇬", "🇧🇷", "🇦🇷", "🇲🇽", "🇿🇦", "🇪🇬", "🇳🇬", "🇰🇪", "🇮🇱"
]

# ИСТОЧНИКИ
URLS = [
    # Большие миксы (World/Mix)
    "https://github.com/sakha1370/OpenRay/raw/refs/heads/main/output/all_valid_proxies.txt",
    "https://raw.githubusercontent.com/yitong2333/proxy-minging/refs/heads/main/v2ray.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all",
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_list.json",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub",
    "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt",
    "https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt",
    "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt"
]

CHUNK_SIZE = 500
NEW_BY_PROTO_DIR = os.path.join(NEW_DIR, "by_protocol")

def clean_start():
    if os.path.exists(BASE_DIR): shutil.rmtree(BASE_DIR)
    os.makedirs(NEW_DIR, exist_ok=True)
    os.makedirs(CLEAN_DIR, exist_ok=True)

def protocol_of(line: str):
    for p in PROTOCOLS:
        if line.startswith(p + "://"): return p
    return None

def is_garbage_soft(line):
    """
    Мягкая фильтрация:
    Удаляет только явные совпадения с черным списком.
    """
    line_upper = line.upper()
    
    # 1. Проверка на плохие слова
    for bad in BAD_WORDS:
        if bad in line_upper: 
            return False # Мусор

    # 2. Проверка на локальные адреса
    if "127.0.0.1" in line or "LOCALHOST" in line_upper:
        return False

    # 3. Слишком короткие строки
    if len(line) < 15: return False
    
    return True

def write_chunks_by_protocol(base_dir: str, protocol: str, items: list, chunk_size: int = 500):
    proto_dir = os.path.join(base_dir, protocol)
    os.makedirs(proto_dir, exist_ok=True)
    for start in range(0, len(items), chunk_size):
        part = items[start:start + chunk_size]
        part_num = start // chunk_size + 1
        with open(os.path.join(proto_dir, f"{protocol}_{part_num:03d}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(part))

def main():
    clean_start()
    all_keys = []
    
    print("🚀 Start Mirror: Anti-Asia/Africa/LatAm Mode...")
    
    for i, url in enumerate(URLS, 1):
        try:
            print(f"Loading {i}/{len(URLS)}: {url.split('/')[-1]}...")
            r = requests.get(url, timeout=15)
            if r.status_code != 200: continue
            
            content = r.text.strip()
            # Декодируем Base64
            if "://" not in content and len(content) > 10:
                try: 
                    missing_padding = len(content) % 4
                    if missing_padding: content += '=' * (4 - missing_padding)
                    decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                    lines = decoded.splitlines()
                except: lines = content.splitlines()
            else: 
                lines = content.splitlines()

            added_local = 0
            for line in lines:
                line = line.strip()
                if not line or not protocol_of(line): continue
                
                # ФИЛЬТРАЦИЯ
                if is_garbage_soft(line):
                    all_keys.append(line)
                    added_local += 1
            
            print(f"  -> Found {added_local} valid keys")
            
        except Exception as e: 
            print(f"  -> Error: {e}")

    # Убираем дубли
    all_keys = list(set(all_keys))
    
    print(f"\nСохранение {len(all_keys)} ключей...")

    # Сохраняем общий файл
    with open(os.path.join(NEW_DIR, "all_new.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_keys))

    # Сохраняем по протоколам (опция)
    raw_buckets = {p: [] for p in PROTOCOLS}
    for line in all_keys:
        p = protocol_of(line)
        if p: raw_buckets[p].append(line)

    for p, items in raw_buckets.items():
        if items:
            write_chunks_by_protocol(NEW_BY_PROTO_DIR, p, items, CHUNK_SIZE)

    print(f"✅ DONE. Saved to {NEW_DIR}/all_new.txt")

if __name__ == "__main__":
    main()
























































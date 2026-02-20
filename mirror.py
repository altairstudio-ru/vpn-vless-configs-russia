#!/usr/bin/env python3
# Mirror.py — WHITELIST ONLY (Super Clean)

import os
import shutil
import requests
import urllib.parse
import base64
import json
import re

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_PATH, "githubmirror")
NEW_DIR = os.path.join(BASE_DIR, "new")
CLEAN_DIR = os.path.join(BASE_DIR, "clean")
NEW_BY_PROTO_DIR = os.path.join(NEW_DIR, "by_protocol")

PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria", "hysteria2", "hy2", "tuic"]

# ✅ БЕЛЫЙ СПИСОК (без точки в начале)
GOOD_DOMAINS = [
    # СНГ
    "ru", "by", "kz", "su", "rf",
    # Европа
    "de", "nl", "fi", "gb", "uk", "fr", "se", "pl", "cz", "at",
    "ch", "it", "es", "no", "dk", "be", "ie", "lu", "ee", "lv", "lt"
]

GOOD_TAGS = [
    # Россия/СНГ (кириллица тоже работает)
    "🇷🇺", "🇧🇾", "🇰🇿", "RUSSIA", "MOSCOW", "SPB", "PETERSBURG", "KAZAKHSTAN", 
    "BELARUS", "RU_", "RUS", "РФ", "МОСКВА", "СПБ",
    
    # Европа
    "🇩🇪", "🇳🇱", "🇫🇮", "🇬🇧", "🇫🇷", "🇸🇪", "🇵🇱", "🇨🇿", "🇦🇹", "🇨🇭",
    "🇮🇹", "🇪🇸", "🇳🇴", "🇩🇰", "🇧🇪", "🇮🇪", "🇱🇺", "🇪🇪", "🇱🇻", "🇱🇹", "🇪🇺",
    
    "GERMANY", "DEUTSCHLAND", "NETHERLANDS", "HOLLAND", "FINLAND", 
    "UK", "UNITED KINGDOM", "BRITAIN", "FRANCE", "SWEDEN", "POLAND", 
    "CZECH", "AUSTRIA", "SWISS", "SWITZERLAND", "ITALY", "SPAIN", 
    "NORWAY", "DENMARK", "BELGIUM", "IRELAND", "ESTONIA", "LATVIA", "LITHUANIA",
    
    # Города
    "EUROPE", "AMSTERDAM", "FRANKFURT", "LONDON", "PARIS", "FALKENSTEIN", 
    "LIMBURG", "HELSINKI", "STOCKHOLM", "WARSAW", "PRAGUE", "VIENNA", 
    "ZURICH", "OSLO", "COPENHAGEN", "BRUSSELS", "DUBLIN", "TALLINN", "RIGA", "VILNIUS"
]

URLS_BASE = [
    "https://github.com/sakha1370/OpenRay/raw/refs/heads/main/output/all_valid_proxies.txt",
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt",
    "https://raw.githubusercontent.com/yitong2333/proxy-minging/refs/heads/main/v2ray.txt",
    "https://raw.githubusercontent.com/acymz/AutoVPN/refs/heads/main/data/V2.txt",
    "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/config.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/trojan.txt",
    "https://raw.githubusercontent.com/YasserDivaR/pr0xy/refs/heads/main/ShadowSocks2021.txt",
    "https://raw.githubusercontent.com/mohamadfg-dev/telegram-v2ray-configs-collector/refs/heads/main/category/vless.txt",
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/vless",
    "https://raw.githubusercontent.com/youfoundamin/V2rayCollector/main/mixed_iran.txt",
    "https://raw.githubusercontent.com/mheidari98/.proxy/refs/heads/main/all",
    "https://github.com/Kwinshadow/TelegramV2rayCollector/raw/refs/heads/main/sublinks/mix.txt",
    "https://github.com/LalatinaHub/Mineral/raw/refs/heads/master/result/nodes",
    "https://raw.githubusercontent.com/miladtahanian/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub",
    "https://github.com/MhdiTaheri/V2rayCollector_Py/raw/refs/heads/main/sub/Mix/mix.txt",
    "https://github.com/Epodonios/v2ray-configs/raw/main/Splitted-By-Protocol/vmess.txt",
    "https://github.com/MhdiTaheri/V2rayCollector/raw/refs/heads/main/sub/mix",
    "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt",
    "https://raw.githubusercontent.com/shabane/kamaji/master/hub/merged.txt",
    "https://raw.githubusercontent.com/wuqb2i4f/xray-config-toolkit/main/output/base64/mix-uri",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet.txt",
    "https://raw.githubusercontent.com/STR97/STRUGOV/refs/heads/main/STR.BYPASS",
    "https://raw.githubusercontent.com/V2RayRoot/V2RayConfig/refs/heads/main/Config/vless.txt",
    "https://raw.githubusercontent.com/lagzian/SS-Collector/main/mix_clash.yaml",
    "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Vless.txt",
    "https://raw.githubusercontent.com/Argh94/V2RayAutoConfig/refs/heads/main/configs/Hysteria2.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_list.json",
    "https://raw.githubusercontent.com/NiREvil/vless/main/sub/SSTime",
    "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/main/speed.txt",
    "https://raw.githubusercontent.com/Mahdi0024/ProxyCollector/master/sub/proxies.txt",
    "https://raw.githubusercontent.com/Mosifree/-FREE2CONFIG/refs/heads/main/Reality",
    "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Cable.txt",
]

CONFIG_SOURCES_FILE = os.path.join(BASE_PATH, "config_sources.json")
CHUNK_SIZE = 500

def load_all_urls():
    urls = set(URLS_BASE)
    if os.path.exists(CONFIG_SOURCES_FILE):
        try:
            with open(CONFIG_SOURCES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for u in data:
                    if isinstance(u, str) and u.strip():
                        urls.add(u.strip())
        except Exception as e:
            print(f"⚠️ Не удалось прочитать config_sources.json: {e}")
    return sorted(urls)

def clean_start():
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    os.makedirs(NEW_DIR, exist_ok=True)
    os.makedirs(CLEAN_DIR, exist_ok=True)
    os.makedirs(NEW_BY_PROTO_DIR, exist_ok=True)

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

def is_ip_address(s: str) -> bool:
    """Проверка, является ли строка IP-адресом"""
    if not s:
        return False
    # IPv4
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    # IPv6 (упрощённо)
    ipv6_pattern = r'^[0-9a-fA-F:]+$'
    return bool(re.match(ipv4_pattern, s) or re.match(ipv6_pattern, s))

def is_good_key(line):
    """
    ✅ НОВАЯ ЛОГИКА:
    1. Сначала проверяем ТЕГИ (работает для IP и доменов)
    2. Потом проверяем ДОМЕНЫ (только для доменов, не для IP)
    3. Если ничего не найдено — МУСОР
    """
    line_upper = line.upper()
    
    # Извлекаем имя из конфига
    name = ""
    if "#" in line:
        name = urllib.parse.unquote(line.split("#")[-1]).upper()
    
    # ✅ ШАГ 1: Проверка тегов (работает для ЛЮБЫХ хостов)
    for tag in GOOD_TAGS:
        if tag in name or tag in line_upper:
            return True
    
    # ✅ ШАГ 2: Проверка доменов (только для доменных имён)
    host, _, _ = extract_host_port_scheme(line)
    if host and not is_ip_address(host):
        host_lower = host.lower()
        for dom in GOOD_DOMAINS:
            if host_lower.endswith("." + dom) or host_lower == dom:
                return True
    
    # ❌ Если ничего не подошло — это мусор
    return False

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
    all_keys = set()
    trash_count = 0  # ✅ Счётчик мусора

    urls = load_all_urls()
    print(f"🚀 Старт: всего источников (старые + новые): {len(urls)}")

    for i, url in enumerate(urls, 1):
        try:
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                print(f"{i}/{len(urls)} ❌ HTTP {r.status_code}")
                continue

            content = r.text.strip()

            if "://" not in content:
                try:
                    content = base64.b64decode(content + "==").decode('utf-8', errors='ignore')
                except:
                    pass

            lines = content.splitlines()
            added_local = 0
            trash_local = 0

            for line in lines:
                line = line.strip()
                if not protocol_of(line):
                    continue
                
                if is_good_key(line):
                    if line not in all_keys:
                        all_keys.add(line)
                        added_local += 1
                else:
                    trash_local += 1

            trash_count += trash_local
            print(f"{i}/{len(urls)}: ✅ {added_local} взято | 🗑️ {trash_local} мусор")

        except Exception as e:
            print(f"{i}/{len(urls)} ⚠️ Ошибка: {e}")

    all_keys_list = sorted(all_keys)

    with open(os.path.join(NEW_DIR, "all_new.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_keys_list))

    # Группировка по протоколам
    raw_buckets = {p: [] for p in PROTOCOLS}
    for line in all_keys_list:
        p = protocol_of(line)
        if p:
            raw_buckets[p].append(line)

    for p, items in raw_buckets.items():
        if items:
            write_chunks_by_protocol(NEW_BY_PROTO_DIR, p, items, CHUNK_SIZE)

    # Дедупликация по IP:PORT:SCHEME
    seen_ip = set()
    clean_keys = []

    for line in all_keys_list:
        host, port, scheme = extract_host_port_scheme(line)
        if not host:
            continue
        key = (host, port, scheme)
        if key not in seen_ip:
            seen_ip.add(key)
            clean_keys.append(line)

    # Запись чистых файлов
    for p in PROTOCOLS:
        items = [k for k in clean_keys if protocol_of(k) == p]
        if items:
            with open(os.path.join(CLEAN_DIR, f"{p}.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(items))

    # ✅ Статистика
    print(f"\n✅ ГОТОВО!")
    print(f"   📥 Всего ключей после фильтра: {len(all_keys_list)}")
    print(f"   🔗 Уникальных IP:PORT:SCHEME: {len(clean_keys)}")
    print(f"   🗑️ Выброшено мусора: {trash_count}")
    
    # ✅ Распределение по протоколам
    print(f"\n📊 По протоколам:")
    for p in PROTOCOLS:
        count = len([k for k in clean_keys if protocol_of(k) == p])
        if count > 0:
            print(f"   {p}: {count}")

if __name__ == "__main__":
    main()


















































































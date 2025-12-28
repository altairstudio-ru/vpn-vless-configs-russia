#!/usr/bin/env python3
# Mirror.py — POLYGLOT CLEANER
# Понимает китайские иероглифы (俄罗斯, 德国).
# Удаляет цепочки (->), США (美国) и Китай (中国).
# Декодирует SS:// для глубокой проверки.

import os
import shutil
import requests
import urllib.parse
import base64
import re

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_PATH, "githubmirror")
NEW_DIR = os.path.join(BASE_DIR, "new")
CLEAN_DIR = os.path.join(BASE_DIR, "clean")

PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria", "hysteria2", "hy2", "tuic"]

# 1. БЕЛЫЙ СПИСОК (Добавил китайские названия стран)
GOOD_DOMAINS = [
    ".ru", ".by", ".kz", ".su", ".rf", 
    ".de", ".nl", ".fi", ".gb", ".uk", ".fr", ".se", ".pl", ".cz", ".at",
    ".ch", ".it", ".es", ".no", ".dk", ".be", ".ie", ".lu", ".ee", ".lv", ".lt"
]

GOOD_TAGS = [
    # RU / CIS
    "🇷🇺", "🇧🇾", "🇰🇿", "RUSSIA", "MOSCOW", "SPB", "KAZAKHSTAN", "BELARUS", "RU_", "RUS",
    "俄罗斯", "莫斯科", "哈萨克斯坦", "白俄罗斯", # Китайские названия
    # EUROPE
    "🇩🇪", "🇳🇱", "🇫🇮", "🇬🇧", "🇫🇷", "🇸🇪", "🇵🇱", "🇨🇿", "🇦🇹", "🇨🇭",
    "🇮🇹", "🇪🇸", "🇳🇴", "🇩🇰", "🇧🇪", "🇮🇪", "🇱🇺", "🇪🇪", "🇱🇻", "🇱🇹", "🇪🇺",
    "GERMANY", "DEUTSCHLAND", "NETHERLANDS", "FINLAND", "UK", "UNITED KINGDOM",
    "FRANCE", "SWEDEN", "POLAND", "CZECH", "AUSTRIA", "SWISS", "ITALY",
    "SPAIN", "NORWAY", "DENMARK", "BELGIUM", "IRELAND", "ESTONIA", "LATVIA",
    "LITHUANIA", "EUROPE", "AMSTERDAM", "FRANKFURT", "LONDON", "PARIS",
    "FALKENSTEIN", "LIMBURG", "HELSINKI",
    "德国", "荷兰", "芬兰", "英国", "法国", "瑞典", "波兰", "捷克", "奥地利", # Китайские EU
    "瑞士", "意大利", "西班牙", "挪威", "丹麦", "比利时", "爱尔兰", "欧洲"
]

# 2. ЧЕРНЫЙ СПИСОК (Добавил иероглифы врагов и стрелочки)
BAD_WORDS = [
    "IRAN", "BAX", "NAJI", "PROXYPRO", "HACKERS855", "V2RAYNG_VPN", 
    "TELEGRAM", "VPN_TELL", "FREE_V2RAY", "CONFIG_V2RAY", "SIVAND_VPN",
    "MR_V2RAY", "V2RAY_IR", "ARVANCLOUD", "DERAK", "PARSPACK",
    "RELAY", "POOL", "SHOP", "STORE", "PAY", "BUY", "SALE", "@",
    # Новое:
    "->", "=>", "TO", "中转", "回国", # Цепочки/Реле
    "🇺🇸", "🇨🇳", "🇰🇷", "🇯🇵", "🇧🇷", # Флаги
    "美国", "中国", "韩国", "日本", "巴西", "印度", "越南", # Иероглифы (США, Китай...)
    "USA", "CHINA", "KOREA", "JAPAN", "BRAZIL"
]

URLS = [
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

def try_decode_ss(line):
    """Пытается декодировать SS ссылку, чтобы найти скрытый IP или мусор"""
    try:
        if not line.startswith("ss://"): return ""
        # Убираем тег и ss://
        clean = line.split("#")[0].replace("ss://", "")
        # Если есть @, значит это не Base64 (старый формат), берем часть до @
        if "@" in clean: return clean 
        
        # Base64 fix padding
        clean += "=" * ((4 - len(clean) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(clean)
        return decoded_bytes.decode('utf-8', errors='ignore')
    except:
        return ""

def extract_host_port_scheme(line: str):
    try:
        u = urllib.parse.urlparse(line)
        return u.hostname, u.port, u.scheme
    except: return None, None, None

def is_fake_or_garbage(line):
    """
    True = Хороший ключ (RU/EU, без Китая, без США, без цепочек)
    False = Мусор
    """
    line_upper = line.upper()
    
    # Декодируем внутренности SS для проверки
    decoded_ss = ""
    if line.startswith("ss://"):
        decoded_ss = try_decode_ss(line).upper()
    
    # Собираем строку для проверки (Ссылка + Декод + Тег)
    full_check_str = line_upper + " " + decoded_ss
    if "#" in line:
        full_check_str += " " + urllib.parse.unquote(line.split("#")[-1]).upper()

    # 1. СНАЧАЛА ИЩЕМ ПЛОХИЕ СЛОВА (Anti-Fake & Anti-Chain)
    for bad in BAD_WORDS:
        if bad in full_check_str: return False 

    # 2. ТЕПЕРЬ ИЩЕМ ХОРОШИЕ ПРИЗНАКИ (Whitelist)
    is_good = False
    
    # По тегам и содержимому
    for tag in GOOD_TAGS:
        if tag in full_check_str:
            is_good = True
            break
            
    # По домену (если тегов не нашлось, но домен хороший)
    if not is_good:
        host, _, _ = extract_host_port_scheme(line)
        if host:
            host = host.lower()
            for dom in GOOD_DOMAINS:
                if host.endswith(dom):
                    is_good = True
                    break
    
    return is_good

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
    
    print("🚀 Старт: Сбор RU/EU. Фильтр: Китай, США, Цепочки (->)...")
    
    for i, url in enumerate(URLS, 1):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200: continue
            
            content = r.text.strip()
            if "://" not in content:
                try: lines = base64.b64decode(content + "==").decode('utf-8', errors='ignore').splitlines()
                except: lines = content.splitlines()
            else: lines = content.splitlines()

            added_local = 0
            for line in lines:
                line = line.strip()
                if not protocol_of(line): continue
                
                # ГЛАВНАЯ ПРОВЕРКА
                if is_fake_or_garbage(line):
                    all_keys.append(line)
                    added_local += 1
                
            print(f"{i}/{len(URLS)}: +{added_local}")
            
        except: print(f"{i}/{len(URLS)} Ошибка")

    with open(os.path.join(NEW_DIR, "all_new.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(all_keys))

    raw_buckets = {p: [] for p in PROTOCOLS}
    for line in all_keys:
        p = protocol_of(line)
        if p: raw_buckets[p].append(line)

    for p, items in raw_buckets.items():
        write_chunks_by_protocol(NEW_BY_PROTO_DIR, p, items, CHUNK_SIZE)

    seen_ip = set()
    clean_keys = []
    for line in all_keys:
        host, port, scheme = extract_host_port_scheme(line)
        if not host or not port: continue
        key = (host, port, scheme)
        if key in seen_ip: continue
        seen_ip.add(key)
        clean_keys.append(line)

    for p in PROTOCOLS:
        items = [k for k in clean_keys if protocol_of(k) == p]
        with open(os.path.join(CLEAN_DIR, f"{p}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(items))
            
    print(f"\n✅ ГОТОВО. Чистых ключей: {len(clean_keys)}")

if __name__ == "__main__":
    main()





























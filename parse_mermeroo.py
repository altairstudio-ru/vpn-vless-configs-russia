import requests

URL_SUB_LINKS = "https://raw.githubusercontent.com/mermeroo/V2RAY-CLASH-BASE64-Subscription.Links/main/SUB%20LINKS"
OUT_FILE = "mermeroo_sources.txt"

def is_potential_source(line: str) -> bool:
    line = line.strip()
    if not line.startswith("http"):
        return False
    # режем явные мусорные/не-нодовые ссылки при желании
    bad_ext = (".md", ".html", ".htm")
    if any(line.endswith(ext) for ext in bad_ext):
        return False
    return True

def main():
    print(f"Загружаю SUB LINKS из {URL_SUB_LINKS}...")
    r = requests.get(URL_SUB_LINKS, timeout=15)
    r.raise_for_status()
    lines = r.text.splitlines()

    urls = set()
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        # SUB LINKS может содержать несколько URL в строке, режем по пробелам/запятым
        parts = [p.strip() for p in raw.replace(",", " ").split() if p.strip()]
        for p in parts:
            if is_potential_source(p):
                urls.add(p)

    urls_list = sorted(urls)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(urls_list))

    print(f"Готово. Найдено {len(urls_list)} уникальных URL.")
    print(f"Сохранено в {OUT_FILE}")

if __name__ == "__main__":
    main()

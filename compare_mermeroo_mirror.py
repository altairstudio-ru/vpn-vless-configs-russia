#!/usr/bin/env python3
import os
import json

from Mirror import URLS_BASE, CONFIG_SOURCES_FILE  # импорт из твоего Mirror.py

MERMEROO_FILE = os.path.join(os.path.dirname(__file__), "mermeroo_sources.txt")

def load_mermeroo_sources(path=MERMEROO_FILE):
    if not os.path.exists(path):
        print(f"{path} не найден")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def load_config_sources():
    urls = set()
    if os.path.exists(CONFIG_SOURCES_FILE):
        try:
            with open(CONFIG_SOURCES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for u in data:
                    if isinstance(u, str) and u.strip():
                        urls.add(u.strip())
        except Exception as e:
            print(f"⚠️ Не удалось прочитать config_sources.json: {e}")
    return urls

def extract_repo_key(url: str) -> str:
    if "raw.githubusercontent.com" not in url:
        return url
    parts = url.split("/")
    try:
        i = parts.index("raw.githubusercontent.com")
        owner = parts[i+1]
        repo = parts[i+2]
        return f"{owner}/{repo}"
    except Exception:
        return url

def main():
    mer_all = load_mermeroo_sources()
    print(f"Всего в mermeroo_sources.txt: {len(mer_all)}")

    # Все источники, которые уже знает Mirror (URLS_BASE + config_sources.json)
    known_urls = set(URLS_BASE)
    known_urls |= load_config_sources()

    # Новые по точному URL
    mer_new_urls = [u for u in mer_all if u not in known_urls]

    # Новые по репозиторию
    known_repos = {extract_repo_key(u) for u in known_urls}
    mer_repos = {extract_repo_key(u) for u in mer_all}
    mer_new_repos = sorted(r for r in mer_repos if r not in known_repos)

    print(f"Новых URL (нет в Mirror): {len(mer_new_urls)}")
    print(f"Новых репозиториев-доноров: {len(mer_new_repos)}")
    for r in mer_new_repos:
        print("  ", r)

    # Можно сохранить только новые URL в отдельный файл
    out_file = os.path.join(os.path.dirname(__file__), "mermeroo_only_new_for_mirror.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(mer_new_urls))
    print(f"\nСписок новых URL сохранён в {out_file}")

if __name__ == "__main__":
    main()

# 🔐 VPN-KEY-VLESS

[![Auto Update](https://img.shields.io/badge/Auto%20Update-Every%2015min-brightgreen)](https://github.com/yourusername/vpn-key-vless)
[![License](https://img.shields.io/badge/License-Educational-blue)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)

**Автоматизированная система сбора, фильтрации и валидации VPN-конфигураций** (VLESS, VMess, Trojan, Shadowsocks) с приоритетом российских и СНГ-регионов.

---

## ⚖️ Правовая информация

<table>
<tr>
<td width="50%" valign="top">

### 📜 Дисклеймер

> **Этот репозиторий создан исключительно в образовательных целях**

Автор:
- ✅ **НЕ призывает** к нарушению законодательства
- ✅ **НЕ обучает** методам обхода технических ограничений
- ✅ **НЕ гарантирует** работоспособность конфигураций
- ✅ **НЕ несёт ответственности** за действия пользователей

</td>
<td width="50%" valign="top">

### 🛡️ Назначение проекта

Материалы предназначены для:
- 🔒 **Изучения криптографических протоколов**
- 🧪 **Тестирования сетевой безопасности**
- 📊 **Анализа распределения VPN-серверов**
- 🎓 **Образовательных исследований**

**Любое использование — на ваш собственный риск**

</td>
</tr>
</table>

### 📄 Источники данных

Все конфигурации получены из **общедоступных источников**:
- GitHub репозитории с открытыми лицензиями
- Публичные Telegram-каналы
- Открытые агрегаторы конфигураций

**Метод сбора**: Web scraping публичных API без обхода защиты

### 🌍 Географический фокус

Проект приоритизирует серверы в регионах:
- 🇷🇺 Россия
- 🇰🇿 Казахстан / 🇺🇦 Украина / 🇧🇾 Беларусь (СНГ)
- 🇪🇺 Европа (DE, NL, FR, GB)

**Цель**: Минимизация задержек (latency) для пользователей из РФ/СНГ

---

## 🎯 Возможности

### 🤖 Автоматизация

```
   ┌─────────────────────────────────────┐
   │  GitHub Actions (Every 15 min)     │
   └──────────────┬──────────────────────┘
                  │
   ┌──────────────▼──────────────────────┐
   │  1. Сбор конфигураций               │
   │     • GitHub Mirror (50+ repos)     │
   │     • Telegram (@vlesstrojan)       │
   │     • RSS Aggregators               │
   └──────────────┬──────────────────────┘
                  │
   ┌──────────────▼──────────────────────┐
   │  2. Фильтрация                      │
   │     • Дедупликация (MD5)            │
   │     • Geo-фильтр (RU/EU/CIS)        │
   │     • Валидация синтаксиса          │
   └──────────────┬──────────────────────┘
                  │
   ┌──────────────▼──────────────────────┐
   │  3. Сохранение                      │
   │     • githubmirror/clean/           │
   │     • githubmirror/ru-sni/          │
   │     • vpn-files/all_posts.txt       │
   └──────────────┬──────────────────────┘
                  │
   ┌──────────────▼──────────────────────┐
   │  4. Статистика (stats.json)         │
   └─────────────────────────────────────┘
```

### 📊 Структура данных

```
vpn-key-vless/
├── githubmirror/
│   ├── clean/                    # Все валидные конфигурации
│   │   ├── vless.txt            # VLESS конфиги
│   │   ├── vmess.txt            # VMess конфиги
│   │   ├── trojan.txt           # Trojan конфиги
│   │   └── ss.txt               # Shadowsocks конфиги
│   └── ru-sni/                  # Только RU/CIS серверы
│       ├── vless_ru.txt
│       ├── vmess_ru.txt
│       └── ...
├── vpn-files/
│   ├── all_posts.txt            # Все посты (история)
│   ├── post_20251201_105923.txt # Последний пост
│   └── ...
├── logs/                        # Логи проверок
├── stats.json                   # Статистика
└── main.py                      # Основной скрипт
```

---

## 🚀 Использование

### 1️⃣ Cloudflare Worker Subscription (Рекомендуемый способ)

**Универсальная подписка** (обновляется автоматически):

```
https://vlesstrojan.alexanderyurievich88.workers.dev?token=sub
```

**Фильтры**:

| Описание | URL |
|----------|-----|
| 🟩 Только VLESS | `?token=sub&filter=vless` |
| 🟦 Только VMess | `?token=sub&filter=vmess` |
| 🟥 Только Trojan | `?token=sub&filter=trojan` |
| ⚫ Только Shadowsocks | `?token=sub&filter=ss` |
| 🌍 С WARP Routing | `?token=sub&warp=on` |
| 🏷️ Кастомное имя | `?token=sub&name=MyConfig` |

**Пример комбинирования**:
```
https://vlesstrojan.alexanderyurievich88.workers.dev?token=sub&filter=vless&warp=on&name=VLESS_WARP
```

### 2️⃣ Прямая загрузка из GitHub

**Raw файлы** (для ручного импорта):

```bash
# Все VLESS конфигурации
curl -O https://raw.githubusercontent.com/yourusername/vpn-key-vless/main/githubmirror/clean/vless.txt

# Только российские VLESS серверы
curl -O https://raw.githubusercontent.com/yourusername/vpn-key-vless/main/githubmirror/ru-sni/vless_ru.txt
```

### 3️⃣ Клонирование репозитория

```bash
git clone https://github.com/yourusername/vpn-key-vless.git
cd vpn-key-vless

# Просмотр последних конфигураций
cat githubmirror/clean/vless.txt | head -10
```

---

## 📱 Настройка клиентов

### Hiddify (Android/iOS/Desktop)

1. Откройте приложение → **Добавить профиль**
2. Выберите **Subscription URL**
3. Вставьте:
   ```
   https://vlesstrojan.alexanderyurievich88.workers.dev?token=sub
   ```
4. Нажмите **Импорт** → подождите загрузки
5. Выберите сервер из списка

### V2RayN (Windows)

1. **Подписка** → **Группы подписок**
2. **Добавить** → вставить URL
3. **Обновить подписку**
4. Серверы появятся в списке

### V2RayNG (Android)

1. **Меню (≡)** → **Подписки**
2. **+** → **URL**
3. Вставить ссылку → **OK**
4. Нажать **Обновить подписку**

### Clash Meta / Mihomo

```yaml
proxy-providers:
  vless-subscription:
    type: http
    url: "https://vlesstrojan.alexanderyurievich88.workers.dev?token=sub&filter=vless"
    interval: 3600
    path: ./providers/vless.yaml
    health-check:
      enable: true
      interval: 600
      url: http://www.gstatic.com/generate_204
```

---

## 🔍 Детали работы скрипта

### `main.py` - Оркестратор

```python
def main():
    """
    Последовательность операций:
    1. run_mirror_script()     # Сбор конфигураций
    2. run_filter_script()     # Фильтрация RU-SNI
    3. collect_statistics()    # Генерация stats.json
    """
    logger.info("🔍 VPN KEY CHECKER - Начало проверки")
    
    # Каждая функция возвращает True/False
    success_count = 0
    success_count += run_mirror_script()
    success_count += run_filter_script()
    success_count += collect_statistics()
    
    # Возвращает exit code (0 = success)
    return 0 if success_count == 3 else 1
```

### `mirror.py` - Сборщик конфигураций

**Источники**:
- 50+ GitHub репозиториев (SubCrawler, NoMoreWalls, V2RayAggregator)
- Telegram-канал [@vlesstrojan](https://t.me/vlesstrojan)
- RSS-агрегаторы

**Алгоритм**:
1. **Загрузка** → HTTP GET / Telegram Bot API
2. **Парсинг** → RegEx для `vless://`, `vmess://`, `trojan://`, `ss://`
3. **Дедупликация** → MD5 хеш конфигураций
4. **Сохранение** → `githubmirror/clean/`

### `filter_ru_sni.py` - Географический фильтр

**Критерии фильтрации**:

```python
RU_DOMAINS = [
    'ru', 'рф', 'russia', 'moscow', 'spb', 'msk', 
    'kazakh', 'kz', 'ukraine', 'ua', 'belarus', 'by'
]

EU_DOMAINS = [
    'de', 'nl', 'fr', 'uk', 'germany', 'netherlands', 
    'france', 'london', 'amsterdam', 'berlin'
]

def is_ru_cis_server(config):
    """
    Проверка SNI/host в конфигурации:
    - vless://uuid@server.ru:443?sni=example.ru
    - vmess://... "add": "185.x.x.x" (RU IP range)
    """
    sni = extract_sni(config)
    
    # Проверка домена
    if any(domain in sni.lower() for domain in RU_DOMAINS):
        return True
    
    # Проверка IP (GeoIP lookup)
    ip = extract_ip(config)
    if is_russian_ip(ip):  # Проверка по MaxMind DB
        return True
    
    return False
```

**Выход**: `githubmirror/ru-sni/*.txt`

---

## 📊 Статистика (`stats.json`)

Пример после проверки:

```json
{
  "timestamp": "2025-01-15T14:30:00",
  "github_mirror": {
    "vless": 1247,
    "vmess": 892,
    "trojan": 534,
    "ss": 312
  },
  "ru_sni": {
    "vless": 342,
    "vmess": 198,
    "trojan": 87,
    "ss": 45
  },
  "sources": {
    "github_repos": 53,
    "telegram_posts": 2,
    "total_raw": 3847,
    "after_dedup": 2985
  }
}
```

**Метрики**:
- `github_mirror` → Все валидные конфигурации
- `ru_sni` → Только RU/CIS серверы
- `sources` → Статистика по источникам

---

## 🛠️ Запуск локально

### Требования

```bash
Python 3.8+
pip install -r requirements.txt
```

**requirements.txt**:
```txt
requests>=2.31.0
python-telegram-bot>=20.0
pyyaml>=6.0
```

### Переменные окружения

```bash
# .env файл
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...  # Для парсинга каналов
GITHUB_TOKEN=ghp_xxxxx...             # Для GitHub API (опционально)
```

### Запуск

```bash
# Полный цикл
python main.py

# Только сбор зеркала
python mirror.py

# Только фильтрация
python filter_ru_sni.py
```

### Логи

```bash
# Последний лог
tail -f logs/vpn-checker-2025-01-15_14-30-00.log

# Все логи за сегодня
cat logs/vpn-checker-2025-01-15*.log
```

---

## 🤖 GitHub Actions (Auto Update)

### Workflow (`.github/workflows/update.yml`)

```yaml
name: Auto Update VPN Keys

on:
  schedule:
    - cron: '*/15 * * * *'  # Каждые 15 минут
  workflow_dispatch:        # Ручной запуск

jobs:
  update:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run main script
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        run: python main.py
      
      - name: Commit changes
        run: |
          git config --local user.name "GitHub Actions"
          git config --local user.email "actions@github.com"
          git add githubmirror/ vpn-files/ stats.json
          git commit -m "🤖 Auto update: $(date '+%Y-%m-%d %H:%M')" || exit 0
          git push
```

**Секреты** (`Settings → Secrets`):
- `TELEGRAM_BOT_TOKEN` → Токен бота для парсинга каналов

---

## 📋 Последние добавления

| Дата | Протокол | Регион | Файл |
|:----:|:--------:|:------:|:-----|
| 2025-01-15 14:30 | 🟩 VLESS | 🇷🇺 RU | [post_20250115_143000.txt](vpn-files/post_20250115_143000.txt) |
| 2025-01-15 14:15 | 🟦 VMess | 🇪🇺 EU | [post_20250115_141500.txt](vpn-files/post_20250115_141500.txt) |
| 2025-01-15 14:00 | 🟥 Trojan | 🇰🇿 KZ | [post_20250115_140000.txt](vpn-files/post_20250115_140000.txt) |

**Полный список**: [vpn-files/all_posts.txt](vpn-files/all_posts.txt)

---

## 🔗 Ссылки

### Telegram-каналы (источники)
- [@vlesstrojan](https://t.me/vlesstrojan) - VLESS/Trojan конфигурации
- [@kibersosnew](https://t.me/kibersosnew) - Новости кибербезопасности

### Связанные проекты
- [V2RayAggregator](https://github.com/mahdibland/V2RayAggregator) - Агрегатор V2Ray конфигураций
- [NoMoreWalls](https://github.com/peasoft/NoMoreWalls) - Прокси-листы для обхода
- [Xray-core](https://github.com/XTLS/Xray-core) - Прокси-движок

---

## ❓ FAQ

<details>
<summary><b>Q: Почему некоторые конфигурации не работают?</b></summary>

**A**: Причины:
1. Сервер был заблокирован провайдером после публикации
2. Конфигурация устарела (сервер выключен)
3. Лимит подключений исчерпан
4. Нужна ротация конфигураций (используйте подписку)

**Решение**: Подписка автоматически обновляется каждые 15 минут — мёртвые ключи удаляются.
</details>

<details>
<summary><b>Q: Как выбрать самые быстрые серверы?</b></summary>

**A**: В клиентах есть функция **ping test**:
- **Hiddify**: Долгий тап на сервере → Test Latency
- **V2RayN**: Правая кнопка → Test Real Latency
- **Clash**: Config → Test All

Выбирайте серверы с latency < 150ms.
</details>

<details>
<summary><b>Q: Можно ли использовать в коммерческих целях?</b></summary>

**A**: ❌ **Нет**. Репозиторий предназначен **только для образования**. Использование для перепродажи VPN-услуг запрещено.
</details>

<details>
<summary><b>Q: Как часто обновляются конфигурации?</b></summary>

**A**: 
- **GitHub Actions**: каждые 15 минут
- **Telegram парсинг**: 2 раза в день (10:00, 22:00 UTC)
- **Ручной запуск**: в любое время через `workflow_dispatch`
</details>

<details>
<summary><b>Q: Безопасно ли использовать эти серверы?</b></summary>

**A**: ⚠️ **Риски**:
- Публичные серверы могут логировать трафик
- Владелец сервера может видеть незашифрованные данные (HTTP)
- Нет гарантий приватности

**Рекомендация**: Используйте только для тестирования. Для серьёзных задач — платный VPN.
</details>

---

## 📜 Лицензия и ответственность

### MIT License (с ограничениями)

```
Copyright (c) 2025 VPN-KEY-VLESS Contributors

Данное ПО предоставляется "как есть" без каких-либо гарантий.

РАЗРЕШЕНО:
✅ Использование в личных образовательных целях
✅ Модификация исходного кода
✅ Форки репозитория

ЗАПРЕЩЕНО:
❌ Коммерческое использование без согласия авторов
❌ Распространение в странах с запретом VPN-технологий
❌ Использование для незаконной деятельности

АВТОР НЕ НЕСЁТ ОТВЕТСТВЕННОСТИ ЗА:
⚠️ Действия пользователей
⚠️ Нарушение законов третьих стран
⚠️ Утечки данных через публичные серверы
⚠️ Блокировки со стороны провайдеров
```

---

## 🤝 Contributing

### Как помочь проекту

1. **Добавить новые источники**
   ```python
   # В mirror.py
   SOURCES = [
       "https://example.com/vless-configs.txt",
       # Ваш источник здесь
   ]
   ```

2. **Улучшить фильтрацию**
   - Добавить новые домены в `RU_DOMAINS`
   - Улучшить GeoIP определение

3. **Репортить баги**
   - Создать Issue с логами
   - Указать версию Python и ОС

### Pull Request Guidelines

1. Форкнуть репозиторий
2. Создать ветку: `git checkout -b feature/new-source`
3. Коммит: `git commit -m "Add new source: example.com"`
4. Push: `git push origin feature/new-source`
5. Создать PR с описанием изменений

---

## 📞 Контакты

- **Telegram**: [@your_username](https://t.me/your_username)
- **GitHub Issues**: [Создать issue](https://github.com/yourusername/vpn-key-vless/issues)
- **Email**: [Не указан — используйте Issues]

---

<div align="center">

### 🔥 Подписывайтесь на Telegram

[![Telegram](https://img.shields.io/badge/Telegram-@vlesstrojan-blue?logo=telegram)](https://t.me/vlesstrojan)
[![Telegram](https://img.shields.io/badge/Telegram-@kibersosnew-blue?logo=telegram)](https://t.me/kibersosnew)

**Сделано с ❤️ для свободного интернета**

[![Stars](https://img.shields.io/github/stars/yourusername/vpn-key-vless?style=social)](https://github.com/yourusername/vpn-key-vless)
[![Forks](https://img.shields.io/github/forks/yourusername/vpn-key-vless?style=social)](https://github.com/yourusername/vpn-key-vless)

</div>

---

## 🎬 ASCII Animation

```
     🔐 VPN-KEY-VLESS Auto Collector
    ╔═══════════════════════════════╗
    ║  GitHub → Filter → Telegram   ║
    ╚═══════════════════════════════╝
    
    [1] 📥 Загрузка источников
         ├─ GitHub (50+ repos) ✅
         ├─ Telegram (2 канала) ✅
         └─ RSS Aggregators ✅
    
    [2] 🔍 Фильтрация
         ├─ Дедупликация ✅
         ├─ Geo-фильтр (RU/CIS) ✅
         └─ Валидация синтаксиса ✅
    
    [3] 💾 Сохранение
         ├─ clean/ (2985 keys) ✅
         ├─ ru-sni/ (672 keys) ✅
         └─ stats.json ✅
    
    [4] 📤 Публикация
         └─ Cloudflare Worker ✅
    
    ✅ ГОТОВО! Следующее обновление через 15 минут
```

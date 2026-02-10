#!/usr/bin/env python3
"""
main.py - Основной скрипт для проверки и обновления VPN конфигураций

Функционал:
- Загрузка конфигураций из множества источников
- Фильтрация по географии (Россия, СНГ, Европа)
- Дедупликация
- Сохранение результатов в структурированном виде
- Логирование всех операций
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
import subprocess

# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

BASE_DIR = Path(__file__).parent.absolute()
LOGS_DIR = BASE_DIR / "logs"
STATS_FILE = BASE_DIR / "stats.json"

# Создание директорий
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================================
# ЛОГИРОВАНИЕ
# ============================================================================

def setup_logging():
    """Настройка логирования с выводом в файл и консоль"""
    log_file = LOGS_DIR / f"vpn-checker-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# ОСНОВНЫЕ ФУНКЦИИ
# ============================================================================

def run_mirror_script():
    """Запуск скрипта загрузки зеркала конфигураций"""
    logger.info("🚀 Запуск mirror.py...")
    try:
        result = subprocess.run(
            [sys.executable, "mirror.py"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 минут
        )
        
        if result.returncode != 0:
            logger.error(f"❌ mirror.py завершился с ошибкой: {result.stderr}")
            return False
        
        logger.info("✅ mirror.py завершён успешно")
        if result.stdout:
            logger.info(f"Вывод: {result.stdout}")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("⏱️  mirror.py превышил timeout (5 мин)")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске mirror.py: {e}")
        return False

def run_filter_script():
    """Запуск скрипта фильтрации RU доменов"""
    logger.info("🚀 Запуск filter_ru_sni.py...")
    try:
        result = subprocess.run(
            [sys.executable, "filter_ru_sni.py"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60  # 1 минута
        )
        
        if result.returncode != 0:
            logger.error(f"❌ filter_ru_sni.py завершился с ошибкой: {result.stderr}")
            return False
        
        logger.info("✅ filter_ru_sni.py завершён успешно")
        if result.stdout:
            logger.info(f"Вывод: {result.stdout}")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("⏱️  filter_ru_sni.py превышил timeout (1 мин)")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске filter_ru_sni.py: {e}")
        return False

def collect_statistics():
    """Сбор статистики о проверенных ключах"""
    logger.info("📊 Сбор статистики...")
    try:
        stats = {
            "timestamp": datetime.now().isoformat(),
            "github_mirror": {},
            "ru_sni": {}
        }
        
        # Статистика по githubmirror/clean
        clean_dir = BASE_DIR / "githubmirror" / "clean"
        if clean_dir.exists():
            for protocol_file in clean_dir.glob("*.txt"):
                try:
                    with open(protocol_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    count = len([l for l in lines if l.strip()])
                    protocol = protocol_file.stem
                    stats["github_mirror"][protocol] = count
                    logger.info(f"  {protocol}: {count} конфигураций")
                except Exception as e:
                    logger.warning(f"  Ошибка чтения {protocol_file}: {e}")
        
        # Статистика по RU SNI
        ru_sni_dir = BASE_DIR / "githubmirror" / "ru-sni"
        if ru_sni_dir.exists():
            for protocol_file in ru_sni_dir.glob("*.txt"):
                try:
                    with open(protocol_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    count = len([l for l in lines if l.strip()])
                    protocol = protocol_file.stem
                    stats["ru_sni"][protocol] = count
                    logger.info(f"  RU-SNI {protocol}: {count} конфигураций")
                except Exception as e:
                    logger.warning(f"  Ошибка чтения {protocol_file}: {e}")
        
        # Сохранение статистики
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Статистика сохранена в stats.json")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при сборе статистики: {e}")
        return False

def main():
    """Основная функция"""
    logger.info("="*70)
    logger.info("🔍 VPN KEY CHECKER - Начало проверки")
    logger.info(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*70)
    
    # Счётчик успешных операций
    success_count = 0
    total_steps = 3  # mirror, filter, stats
    
    # 1. Запуск зеркала
    if run_mirror_script():
        success_count += 1
    else:
        logger.warning("⚠️  mirror.py завершился с ошибкой")
    
    # 2. Запуск фильтра
    if run_filter_script():
        success_count += 1
    else:
        logger.warning("⚠️  filter_ru_sni.py завершился с ошибкой")
    
    # 3. Сбор статистики
    if collect_statistics():
        success_count += 1
    else:
        logger.warning("⚠️  Статистика не собрана")
    
    # Итоговый отчёт
    logger.info("="*70)
    if success_count == total_steps:
        logger.info(f"✅ ВСЕ ОПЕРАЦИИ УСПЕШНЫ ({success_count}/{total_steps})")
        logger.info("="*70)
        return 0  # Успех
    elif success_count > 0:
        logger.warning(f"⚠️  ЧАСТИЧНЫЙ УСПЕХ ({success_count}/{total_steps})")
        logger.info("="*70)
        return 1  # Ошибка
    else:
        logger.error(f"❌ ВСЕ ОПЕРАЦИИ НЕ УДАЛИСЬ (0/{total_steps})")
        logger.info("="*70)
        return 2  # Критическая ошибка

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

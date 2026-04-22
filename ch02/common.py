from pathlib import Path

# Путь к папке ch02
BASE_DIR = Path(__file__).resolve().parent.parent
CH02 = BASE_DIR / "ch02"
API_YAML = CH02 / "orders" / "oas.yaml"

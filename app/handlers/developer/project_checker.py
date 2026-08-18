import io
import zipfile
import re
from typing import Dict, List, Tuple

class ProjectCheckerService:
    # Шаблони для пошуку секретів у файлах коду
    SECRET_PATTERNS = [
        re.compile(r"['\"](1[0-9]{9}:[a-zA-Z0-9_-]{35})['\"]"),  # Telegram BOT_TOKEN
        re.compile(r"(?i)(api[_-]?key|secret[_-]?key|jwt[_-]?secret|system[_-]?token)\s*[:=]\s*['\"].+['\"]"),
        re.compile(r"postgres://[^:]+:[^@]+@"),  # Database URI with password
    ]
    
    # Заборонені файли
    FORBIDDEN_FILES = [".env"]

    @classmethod
    def validate_github_url(cls, url: str) -> bool:
        github_regex = r"^https?://(www\.)?github\.com/[\w-]+/[\w.-]+/?$"
        return bool(re.match(github_regex, url.strip()))

    @classmethod
    def analyze_zip(cls, zip_bytes: bytes) -> Tuple[Dict[str, bool], List[str]]:
        results = {
            "README.md": False,
            "requirements.txt": False,
            ".env.example": False,
            ".gitignore": False,
            "Dockerfile": False,
            "docker-compose.yml": False,
            "alembic": False,
            "app/": False,
            "main_entry": False
        }
        
        security_violations = []

        try:
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                file_list = zf.namelist()
                
                # Нормалізуємо шлях кореневої папки, якщо архів запакований у внутрішню папку
                root_prefix = ""
                if len(file_list) > 0 and "/" in file_list[0]:
                    possible_root = file_list[0].split("/")[0] + "/"
                    if all(f.startswith(possible_root) or f == possible_root for f in file_list if f):
                        root_prefix = possible_root

                for file_path in file_list:
                    relative_path = file_path[len(root_prefix):] if root_prefix and file_path.startswith(root_prefix) else file_path
                    lower_name = relative_path.lower()

                    # Перевірка заборонених файлів
                    if any(lower_name.endswith(f) for f in cls.FORBIDDEN_FILES):
                        security_violations.append(f"Знайдено заборонений файл: {relative_path}")

                    # Перевірка наявності обов'язкових елементів
                    if "readme.md" in lower_name:
                        results["README.md"] = True
                    if "requirements.txt" in lower_name:
                        results["requirements.txt"] = True
                    if ".env.example" in lower_name:
                        results[".env.example"] = True
                    if ".gitignore" in lower_name:
                        results[".gitignore"] = True
                    if "dockerfile" in lower_name:
                        results["Dockerfile"] = True
                    if "docker-compose" in lower_name:
                        results["docker-compose.yml"] = True
                    if "alembic" in lower_name:
                        results["alembic"] = True
                    if "app/" in lower_name or relative_path.startswith("app/"):
                        results["app/"] = True
                    if lower_name in ["main.py", "app/main.py", "run.py", "bot.py"]:
                        results["main_entry"] = True

                    # Читаємо вміст текстових файлів для сканування на секрети
                    if not relative_path.endswith("/") and any(lower_name.endswith(ext) for ext in [".py", ".env", ".json", ".yml", ".yaml", ".txt", ".md", ".ini"]):
                        try:
                            content = zf.read(file_path).decode("utf-8", errors="ignore")
                            for pattern in cls.SECRET_PATTERNS:
                                if pattern.search(content):
                                    security_violations.append(f"Потенційний секрет у файлі: {relative_path}")
                                    break
                        except Exception:
                            pass

        except zipfile.BadZipFile:
            return results, ["Помилка: файл не є валідним ZIP-архівом."]

        return results, security_violations
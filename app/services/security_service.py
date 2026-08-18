# services/security_service.py
import os
from typing import Optional
import hmac

ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/jpg", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"}
MAX_UPLOAD_SIZE_BYTES = 20 * 1024 * 1024


def validate_uploaded_file(filename: str, mime_type: str | None, size_bytes: int) -> bool:
    """Reject unsafe uploads and overly large files."""
    if not filename or not isinstance(filename, str):
        return False
    if size_bytes <= 0 or size_bytes > MAX_UPLOAD_SIZE_BYTES:
        return False
    lowered = filename.lower()
    ext = os.path.splitext(lowered)[1]
    if ext not in ALLOWED_UPLOAD_EXTENSIONS:
        return False
    if mime_type and mime_type.lower() not in ALLOWED_MIME_TYPES:
        return False
    return True


class SecurityService:
    def __init__(self):
        self.admin_ids = {int(os.getenv("OWNER_ID", "0"))}
        self.system_token = os.getenv("SYSTEM_TOKEN", "").strip()

    async def is_admin(self, user_id: int) -> bool:
        """Перевірка, чи є користувач адміністратором."""
        return user_id in self.admin_ids

    async def check_permission(self, user_role: str, required_permission: str) -> bool:
        """
        Перевірка дозволів на основі ролі (RBAC - Role Based Access Control).
        Приклад: чи може 'менеджер' переглядати 'зарплати'?
        """
        permissions = {
            "admin": ["view_salary", "edit_employees", "delete_post"],
            "manager": ["view_orders", "add_post"],
            "client": ["view_orders"],
        }

        user_perms = permissions.get(user_role, [])
        return required_permission in user_perms

    async def validate_session(self, token: str) -> bool:
        """Валідація токена безпеки з використанням змінних середовища."""
        if not self.system_token:
            return False
        return hmac.compare_digest(token, self.system_token)
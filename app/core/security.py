import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.core.config import settings

# Контекст для хешування паролів (якщо знадобиться в адмінці)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    """
    Клас для керування безпекою: JWT, хешування та верифікація.
    """
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
        """
        Створення JWT токена для верифікації сесій або зовнішніх API запитів.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET.get_secret_value(), 
            algorithm="HS256"
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict | None:
        """
        Декодування та перевірка JWT токена.
        """
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET.get_secret_value(), 
                algorithms=["HS256"]
            )
            return payload
        except jwt.PyJWTError:
            return None

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хешування пароля для зберігання в БД."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Перевірка пароля при логіні."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def is_admin(user_role: str) -> bool:
        """Перевірка, чи має користувач права адміністратора/власника."""
        return user_role in ["admin", "owner"]

# Екземпляр для зручного використання в сервісах
security = SecurityManager()
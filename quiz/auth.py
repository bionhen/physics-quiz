import hashlib

# Хеш пароля "teacher_123"
# Создание: hashlib.sha256("новый_пароль".encode()).hexdigest()
TEACHER_PASSWORD_HASH = "d88dd718bd27f5ad22f36937be0aea09bec1acbe48b49c88ba0003b80247050f"

def hash_password(password):
    """Хеширует пароль"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password):
    """Проверяет пароль"""
    return hash_password(password) == TEACHER_PASSWORD_HASH 
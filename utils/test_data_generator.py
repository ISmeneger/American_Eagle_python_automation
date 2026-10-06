import random
import string
import uuid


def generate_first_name() -> str:
    return f"Test{uuid.uuid4().hex[:6]}"


def generate_last_name() -> str:
    return f"User{uuid.uuid4().hex[:6]}"


def generate_email() -> str:
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def generate_password() -> str:
    letters = string.ascii_letters
    digits = string.digits

    random_part = "".join(
        random.choices(
            letters + digits,
            k=10,
        )
    )

    return f"A1{random_part}"
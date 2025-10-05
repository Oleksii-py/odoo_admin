from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@transaction.atomic
def register_user(username: str, email: str, password: str, role: str = "user"):
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    user.save()
    return user

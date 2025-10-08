from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Role

User = get_user_model()


@transaction.atomic
def register_user(username: str, email: str, password: str, role: str = "user"):
    manager_role = Role.objects.get(name=role)
    user = User(username=username, email=email, role_id=manager_role)
    user.set_password(password)
    user.save()
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {
        "refresh": str(refresh),
        "access": str(access),
    }

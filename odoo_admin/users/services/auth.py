from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from odoo_admin.redis_utils import block_token

User = get_user_model()


def login_user(username: str, password: str):
    user = authenticate(username=username, password=password)
    if not user:
        return None

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {
        "refresh": str(refresh),
        "access": str(access),
    }


def refresh_tokens(old_refresh_token: str):
    old_refresh = RefreshToken(old_refresh_token)
    jti = old_refresh.get("jti")
    exp = old_refresh.get("exp")
    if jti and exp:
        block_token(jti, exp)

    user = User.objects.get(id=old_refresh["user_id"])
    new_refresh = RefreshToken.for_user(user)
    new_access = new_refresh.access_token
    return {
        "refresh": str(new_refresh),
        "access": str(new_access),
    }


def logout_tokens(
    refresh_token: str = None, access_token: str = None, current_auth=None
):
    blocked = []

    if refresh_token:
        try:
            rt = RefreshToken(refresh_token)
            block_token(rt["jti"], rt["exp"])
            blocked.append("refresh")
        except Exception:
            pass

    if access_token:
        try:
            at = AccessToken(access_token)
            block_token(at["jti"], at["exp"])
            blocked.append("access")
        except Exception:
            pass

    if current_auth:
        try:
            block_token(current_auth["jti"], current_auth["exp"])
            blocked.append("current")
        except Exception:
            pass

    return blocked

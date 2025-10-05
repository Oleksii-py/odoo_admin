from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from odoo_admin.redis_utils import is_token_blocked


class RedisJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        jti = token.get("jti")
        if jti and is_token_blocked(jti):
            raise exceptions.AuthenticationFailed(
                "Token has been revoked (logout or rotation).", code="token_revoked"
            )
        return token

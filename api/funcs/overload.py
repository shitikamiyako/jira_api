import jwt
from config import settings


def get_object(user, token):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        # もしくはreturn payload["user_id"]
        return user.objects.get(id=payload["user_id"])
    # Token期限切れ
    except jwt.ExpiredSignatureError:
        return "Activations link expired"
    # 不正なToken
    except jwt.exceptions.DecodeError:
        return "Invalid Token"
    # ユーザーが存在しない
    except user.DoesNotExist:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        return payload["user_id"]

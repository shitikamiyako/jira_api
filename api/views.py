import jwt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status, permissions, generics, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework_simplejwt import views as jwt_views

from config import settings
from . import custompermissions
from .authentication import CookieHandlerJWTAuthentication
from .models import Task, Category, Profile
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer

User = get_user_model()


class TokenObtainView(jwt_views.TokenObtainPairView):
    # Token発行
    def post(self, request, *args, **kwargs):
        # 任意のSerializerを引っ張ってくる(今回はTokenObtainPairViewで使われているserializers.TokenObtainPairSerializer)
        serializer = self.get_serializer(data=request.data)
        # 検証
        try:
            serializer.is_valid(raise_exception=True)
        # エラーハンドリング
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=status.HTTP_200_OK)

        try:
            res.delete_cookie("access_token")
        except Exception as e:
            print(e)

        # CookieヘッダーにTokenをセットする
        res.set_cookie(
            "access_token",
            serializer.validated_data["access"],
            max_age=60 * 60 * 24,
            httponly=True,
        )
        res.set_cookie(
            "refresh_token",
            serializer.validated_data["refresh"],
            max_age=60 * 60 * 24 * 30,
            httponly=True,
        )

        return res


# CookieからRefresh_Token取得
def refresh_get(request):
    try:
        refresh_token = request.COOKIES["refresh_token"]
        return JsonResponse({"refresh": refresh_token}, safe=False)
    except Exception as e:
        print(e)
        return None


# HTTPRequestのBodyプロパティから送られてきたtokenを受け取る
class TokenRefresh(jwt_views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raize_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])
        # token更新
        res = Response(serializer.validated_data, status=status.HTTP_200_OK)
        # 既存のAccess_Tokenを削除
        res.delete_cookie("user_token")
        # 更新したTokenをセット
        res.set_cookie(
            "user_token",
            serializer.validated_data["access"],
            max_age=60 * 24 * 24 * 30,
            httponly=True,
        )
        return res


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ログインユーザーの情報を返すView,参考に自分で書いたやつ


class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (CookieHandlerJWTAuthentication,)

    # お手本ではAPIViewを使ってget_object()をオーバーロードしてTokenの検証をしていた
    # しかし、generics以下のViewでは無理なので、代わりにget()をオーバーライドしてこちらの処理過程にTokenの検証を挿入
    def get(self, request, *args, **kwargs):
        # Set-CookieにしているのでCookieからトークンを入手
        jwt_token = request.COOKIES.get("access_token")
        if not jwt_token:
            return Response(
                {"error": "No Token"}, status=status.HTTP_400_BAD_REQUEST
            )
        # Token検証
        try:
            payload = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            # もしくはreturn payload["user_id"]でもありだそうな。
            loginuser = User.objects.get(id=payload["user_id"])
            # オブジェクトで返ってくるのでStringならエラーハンドリング
            if type(loginuser) == str:
                return Response(
                    {"error": " Expecting an Object type, but it returned a String type."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # アクティブチェック
            if loginuser.is_active:
                # 通常、generics.CreateAPIView系統はこの処理をしなくてもいい
                # しかしtry-exceptの処理かつ、オーバーライドしているせいかResponse()で返せとエラーが出るので以下で処理
                response = UserSerializer(self.request.user)
                return Response(response.data, status=status.HTTP_200_OK)
            return Response(
                {"error": "user is not active"}, status=status.HTTP_400_BAD_REQUEST
            )
        # Token期限切れ
        except jwt.ExpiredSignatureError:
            return "Activations link expired"
        # 不正なToken
        except jwt.exceptions.DecodeError:
            return "Invalid Token"
        # ユーザーが存在しない
        except User.DoesNotExist:
            payload = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            return payload["user_id"]

    # PUTメソッドを無効
    def update(self, request, *args, **kwargs):
        response = {"message": "PUT method is not allowed"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

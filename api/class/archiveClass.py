# class LoginUserView(RetrieveUpdateAPIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#
#     def get(self, request, *args, **kwargs):
#         jwt_token = request.COOKIES.get("access_token")
#         if not jwt_token:
#             return Response(
#                 {"error": "No Token"}, status=status.HTTP_400_BAD_REQUEST
#             )
#
#         user = overload.get_object(User, jwt_token)
#         result = UserSerializer(user)
#
#         return Response(user)
#
#     if type(user) == str:
#         return Response(
#             {"error": " Expecting an Object type, but it returned a String type."},
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     if user.is_active:
#         return self.request.user
#     return Response(
#         {"error": "user is not active"}, status=status.HTTP_400_BAD_REQUEST
#     )
#
#     def update(self, request, *args, **kwargs):
#         response = {"message": "PUT method is not allowed"}
#         return Response(response, status=status.HTTP_400_BAD_REQUEST)
#
#
# class LoginUserView(views.APIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#
#     def get_object(self, token):
#         try:
#             payload = jwt.decode(
#                 token, settings.SECRET_KEY, algorithms=["HS256"]
#             )
#             # もしくはreturn payload["user_id"]
#             user_id = payload.get("id")
#             return User.objects.get(id=payload["user_id"])
#         # Token期限切れ
#         except jwt.ExpiredSignatureError:
#             return "Activations link expired"
#         # 不正なToken
#         except jwt.exceptions.DecodeError:
#             return "Invalid Token"
#         # ユーザーが存在しない
#         except User.DoesNotExist:
#             return "user does not exists"
#
#     def get(self, request, format=None):
#         jwt_token = request.COOKIES.get("access_token")
#         if not jwt_token:
#             return Response(
#                 {"error": "No token"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         user = self.get_object(jwt_token)
#
#         # get_user_model()から返ってくるUserはObjectなので、Stringならアウト
#         if type(user) == str:
#             return Response(
#                 {"error": " Expecting an Object type, but it returned a String type."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         if user.is_active:
#             serializer = UserSerializer(user)
#             return Response(serializer.data)
#         return Response(
#             {"error": "user is not active"}, status=status.HTTP_400_BAD_REQUEST
#         )